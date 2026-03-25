# Discord Scribe

A standalone Discord bot that joins voice channels, transcribes conversations in real time, and posts a structured meeting summary when the call ends. Designed as a self-hosted service — later promoted to an Office agent.

---

## Concept

The bot lives in a Discord server as a regular member. When someone invites it to a voice channel, it:

1. Joins the channel and sends a polite text greeting
2. Listens to all audio, transcribing each speaker as it goes
3. Waits for the call to end (everyone leaves)
4. Sends the full transcript to an LLM
5. Posts a formatted summary — topics, priority, and next-meeting agenda — to a designated channel

The bot does not speak. It observes and reports.

---

## Architecture

```
Discord Voice Channel
        │
        │  audio streams (per user, PCM)
        ▼
  Voice Capture Layer
  (discord.py AudioSink)
        │
        │  raw .wav per speaker, chunked
        ▼
  Speech-to-Text Engine
  (Whisper, local or API)
        │
        │  timestamped utterances + speaker labels
        ▼
  Transcript Store
  (in-memory dict, flushed to file on session end)
        │
        │  full transcript text
        ▼
  LLM Summarizer
  (Claude API or local model)
        │
        │  structured JSON response
        ▼
  Formatter + Discord Post
  (target channel, rich embed or markdown block)
```

---

## Components

### 1. Discord Bot

**Library:** `discord.py` with the `[voice]` extra, plus `PyNaCl` for encrypted voice transport.

```
pip install "discord.py[voice]" PyNaCl
```

**Required bot permissions (OAuth2 scopes):**
- `bot` scope
- `CONNECT` — join voice channels
- `SPEAK` — required even if the bot never speaks (voice client needs it)
- `USE_VAD` — voice activity detection
- `SEND_MESSAGES` — post to text channels
- `EMBED_LINKS` — for formatted output embeds
- `VIEW_CHANNEL` — read channel state

**Intents required:**
- `voice_states` — detect when users join/leave
- `guilds` — resolve channel/guild objects
- `members` — identify who is in the call (needed to detect "everyone left")

The bot watches `on_voice_state_update` events. When it's the only remaining member in a channel it's recording, it triggers the end-of-session pipeline and disconnects.

---

### 2. Voice Capture

discord.py exposes per-user audio sinks via `VoiceClient.listen(sink)`. Each user's audio arrives as a separate PCM stream, which is what we want — it gives us speaker-labeled audio without needing diarization.

**Sink implementation:**

```python
from discord.sinks import WaveSink

class TranscribingSink(WaveSink):
    """Buffers per-user WAV audio during a session."""

    def __init__(self):
        super().__init__()
        # After session ends: self.audio_data = {user_id: AudioData}
```

`WaveSink` accumulates `.wav` data per `user_id`. When the session ends, we iterate over `sink.audio_data` and feed each user's buffer to the transcription engine.

**Chunked streaming (optional):** For long calls, instead of buffering everything to memory, write rolling 30-second WAV chunks per user to disk. Transcribe each chunk as it's written. Merge the transcript pieces in order at the end. This reduces memory pressure and gives a partial transcript even if the bot crashes mid-call.

---

### 3. Speech-to-Text

**Engine: OpenAI Whisper (local)**

The obvious choice. Runs on CPU (slow) or GPU/Metal (fast). The `whisper` Python package wraps everything.

```
pip install openai-whisper
```

**Model selection by hardware:**

| Hardware | Recommended model | Notes |
|---|---|---|
| CPU only | `base` or `small` | Slow but works |
| Apple Silicon (MPS) | `medium` or `large-v3` | Good quality, real-time-ish |
| NVIDIA GPU (CUDA) | `large-v3` | Best quality, fast |

**Per-speaker transcription:**

```python
import whisper

model = whisper.load_model("medium")

def transcribe_user(audio_bytes: bytes, user_name: str) -> list[dict]:
    # Write bytes to a temp WAV, transcribe, return segments
    result = model.transcribe(audio_path, language="en", word_timestamps=True)
    return [
        {
            "speaker": user_name,
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip()
        }
        for seg in result["segments"]
    ]
```

Run transcriptions for all users in parallel (thread pool), then merge and sort by `start` timestamp to get a chronological interleaved transcript.

**Alternative: faster-whisper**

`faster-whisper` is a CTranslate2 reimplementation — roughly 4x faster than vanilla Whisper with the same accuracy. Recommended for production.

```
pip install faster-whisper
```

**Alternative: Whisper API (OpenAI)**

If running on a server without a GPU, offload to the Whisper API. Costs money but requires no local inference hardware. Max file size is 25 MB per request — for long calls, chunk the audio.

---

### 4. Transcript Store

During the call, maintain a session object:

```python
@dataclass
class Session:
    channel_id: int
    guild_id: int
    started_at: datetime
    participants: set[int]          # user IDs seen during the call
    sink: TranscribingSink
    transcript: list[dict]          # populated at end-of-call
```

At end-of-call, serialize the final merged transcript to a JSON file in a `/transcripts/` directory. This gives a durable audit trail and lets you reprocess old calls without re-recording.

```
transcripts/
  2026-03-20_general_1234567890.json
```

---

### 5. LLM Summarizer

The full transcript is formatted as plain text with speaker labels and timestamps, then sent to the LLM with a structured prompt.

**Input format:**

```
[00:00] Alice: Hey, should we move the deploy to Thursday?
[00:04] Bob: Yeah, Thursday works. We need to finish the migration first.
[00:09] Alice: Right. The migration is blocked on the database credentials issue.
...
```

**Prompt:**

```
You are a professional meeting assistant. Below is the full transcript of a voice call.

Analyze the conversation and respond in JSON with this exact structure:
{
  "summary": "2-4 sentence overview of the conversation",
  "topics": [
    { "title": "short topic title", "detail": "1-2 sentences" }
  ],
  "most_important": "title of the single most critical topic and why",
  "agenda": [
    "Action item or discussion point for next meeting"
  ]
}

Transcript:
---
{transcript}
---
```

**Client:**

```python
import anthropic

client = anthropic.Anthropic()

def analyze_transcript(transcript_text: str) -> dict:
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(message.content[0].text)
```

For a local-only setup (no API calls), swap in Ollama with a capable model (e.g. `llama3.3`, `qwen2.5:72b`). Quality will be lower than Claude but it stays fully offline.

---

### 6. Formatter and Post

Takes the structured JSON from the LLM and builds a Discord message. Discord supports markdown in messages — use it.

**Example output message:**

```
📋 **Meeting Summary** — #general | March 20, 2026

**Overview**
The team discussed the Thursday deployment timeline, blocked on a database credentials issue. Alice and Bob agreed to prioritize the credentials fix before proceeding.

---

**Topics Discussed**
• Deploy timeline — Moving the deploy to Thursday; contingent on migration completion
• Migration blocker — Credentials issue needs resolving before migration can proceed
• Onboarding schedule — New hire start date pushed to next week

---

⭐ **Most Important:** Migration blocker
The deployment and onboarding both depend on resolving the credentials issue. This is the critical path item.

---

**Suggested Agenda for Next Meeting**
• [ ] Update on credentials issue — who owns it, what's blocking
• [ ] Confirm Thursday deploy is still on or reschedule
• [ ] Align on new hire onboarding plan
• [ ] Any other blockers to the migration

---
_Transcribed and summarized by Scribe • 3 participants • 00:14:32_
```

Post this as a plain message or a `discord.Embed` for a cleaner visual. Embed is recommended — it gives a colored sidebar, title, and footer, and stands out in the channel.

**Target channel:** configured via an environment variable (`SCRIBE_SUMMARY_CHANNEL_ID`). Can also be set per-server via a simple `/setup #channel` slash command stored in a local SQLite config.

---

## Session Lifecycle

```
User runs /join or drags bot into channel
          │
          ▼
Bot joins voice channel
Bot sends greeting in the channel's linked text chat:
  "👋 I'm here. I'll listen and post a summary when the call ends."
          │
          ▼
Recording starts (WaveSink active)
          │
  [call in progress — users join and leave freely]
          │
          ▼
Last human leaves (on_voice_state_update detects empty channel)
          │
          ▼
Bot stops recording, disconnects
Bot sends "Processing..." message in text channel
          │
          ▼
Transcription (Whisper, parallel per user)
          │
          ▼
Merge + sort transcript by timestamp
Save raw transcript to file
          │
          ▼
LLM analysis (Claude API or local)
          │
          ▼
Format summary
Post to defined summary channel
Update "Processing..." message: "✅ Summary posted in #meeting-notes"
```

Edge cases to handle:
- **Bot is alone from the start** — if no one else joins within 60 seconds, leave quietly with a message.
- **Call exceeds 3 hours** — flush transcript chunks every 30 min to avoid memory overflow.
- **Transcription fails for a user** — skip their audio, note it in the summary footer.
- **LLM API is down** — post the raw transcript instead, flag that summarization failed.
- **Bot crashes mid-call** — on restart, check `/transcripts/` for incomplete sessions and offer to reprocess.

---

## Deployment

The bot runs as a long-lived Python process on a server. Recommended setup:

### Server requirements

- Any Linux VPS (2 GB RAM minimum for `base` Whisper; 8 GB+ for `large-v3`)
- Python 3.11+
- `ffmpeg` installed (required by discord.py voice)
- Optional: NVIDIA GPU for fast local transcription

### Process management

Run as a `systemd` service for automatic restarts:

```ini
# /etc/systemd/system/discord-scribe.service

[Unit]
Description=Discord Scribe Bot
After=network.target

[Service]
User=scribe
WorkingDirectory=/opt/discord-scribe
EnvironmentFile=/opt/discord-scribe/.env
ExecStart=/opt/discord-scribe/.venv/bin/python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### Environment variables

```
DISCORD_TOKEN=...
ANTHROPIC_API_KEY=...         # omit if using local LLM
SCRIBE_SUMMARY_CHANNEL_ID=... # channel to post summaries
WHISPER_MODEL=medium          # base / small / medium / large-v3
TRANSCRIPT_DIR=/opt/discord-scribe/transcripts
```

### Docker (optional)

If deploying to a managed host or want portability:

```dockerfile
FROM python:3.11-slim
RUN apt-get install -y ffmpeg
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

Mount `/app/transcripts` as a volume so transcripts survive container restarts.

---

## Project Structure

```
discord-scribe/
  bot.py                  # entry point, event loop, bot client
  voice.py                # VoiceSession class, audio sink, session lifecycle
  transcribe.py           # Whisper wrapper, per-user transcription, merge logic
  analyze.py              # LLM prompt, structured output parsing
  format.py               # Discord embed/message builder
  store.py                # transcript file I/O, session persistence
  config.py               # env var loading, defaults
  requirements.txt
  .env.example
  transcripts/            # saved JSON transcripts (gitignored)
```

---

## Dependencies

```
discord.py[voice]>=2.3
PyNaCl>=1.5
faster-whisper>=1.0        # or openai-whisper
anthropic>=0.40            # omit if using local LLM
ollama                     # if using local LLM instead
ffmpeg-python              # audio handling
python-dotenv
```

---

## Path to Office Agent

When this graduates from standalone script to an Office agent, the changes are relatively small:

| Standalone | Office agent |
|---|---|
| Hardcoded summary channel | Agent receives target channel as a task parameter |
| Local `.env` config | Config pulled from Office context / MCP |
| Whisper runs locally on the same machine | Transcription offloaded to a dedicated transcription worker |
| Claude API call inline in `analyze.py` | Task dispatched to the Office LLM tier via the task queue |
| Transcript saved to local files | Transcript stored in the Digital Archivist (ChromaDB) |
| Systemd service | Agent registered in Office worker pool, spawned on demand |

The bot's Discord event handling and voice capture stay the same. Only the backend (storage, inference, dispatch) gets swapped out. The standalone version is a clean proof-of-concept that validates the audio pipeline before plugging it into the larger system.
