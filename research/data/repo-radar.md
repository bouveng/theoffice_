# Repo Radar — Monitoring Programmers' Public Repositories

Most trend detection watches what people *say* — RSS feeds, social posts, conference talks. This idea watches what they *build*. Public GitHub activity from a curated list of programmers is a leading indicator: the repo appears before the blog post, the commit happens before the tweet.

A developer known for systems work suddenly pushing Rust. Three independent people you respect all creating repos tagged `mcp` in the same week. A quiet architect who never does side projects opens something new. These are signals you can't get from headlines.

---

## The Idea

Maintain a **watched list** of GitHub usernames — programmers whose judgment and taste are considered worth tracking. Periodically poll their public activity via the GitHub API. Diff the current state against the previous snapshot. Surface anything that changed as a structured signal.

This is not follower metrics or star counts. The signal is behavioral: *what are specific people choosing to spend their time on?*

---

## Signal Types

| Signal | What it means |
|---|---|
| New repository created | The person found a problem worth starting from scratch on |
| Language shift in new repos | Moving toward or away from a technology |
| Cluster: multiple watched devs push same topic/language in short window | Framework or approach gaining traction in the practitioner layer |
| High commit velocity on a new repo | Active exploration, not a throwaway |
| New repo with zero stars but meaningful README | Early-stage real work, not a demo |
| Repo topics / tags added | Explicit self-categorization — reliable signal |
| Fork of an obscure repo | The person found something and decided to use it |

---

## Watched List

The list of usernames lives in a config file, not in the script. It is curated manually — this is a high-trust, low-volume list. The value comes from the quality of the people on it, not the quantity.

```json
{
  "watched": [
    "antirez",
    "gvanrossum",
    "kelseyhightower",
    "mitchellh",
    "tpope"
  ],
  "poll_interval_hours": 6
}
```

Starting small (10–20 people) is correct. A list of 200 produces noise; a list of 15 people you actually follow produces signal.

---

## How It Would Work

**Step 1 — Snapshot**
For each watched user, fetch:
- All public repos (name, language, created_at, pushed_at, topics, description, fork, stargazers_count)
- Only repos updated since the last poll

GitHub's public API supports this without authentication at 60 req/hr. With a personal access token: 5,000 req/hr. For a list of 20 people polled every 6 hours, a token is not strictly required but recommended for headroom.

**Step 2 — Diff**
Compare the current snapshot against the stored previous snapshot:
- New repos → always surfaced
- Language distribution change → flag if a new language appears or an existing one drops out
- Topic tags added to existing repos → flag
- Forks of previously untracked repos → flag

**Step 3 — Cluster detection**
After diffing all users, look for overlap:
- Same language appearing as new in ≥2 watched users in the same polling window
- Same topic tag appearing across ≥2 users
- Any signal that multiple independent people are independently converging on something

**Step 4 — Output**
A structured signal report passed to the [CAO](../../agents/management/cao/cao.md):

```
[repo-radar signal — 2026-03-05 06:00]

NEW REPOS
  antirez       → smalldb (C, 3h ago) — "A minimal key-value store experiment"
  mitchellh     → go-wasmtime (Go, 11h ago) — fork of bytecodealliance/wasmtime

LANGUAGE SHIFTS
  kelseyhightower — 3 of last 4 new repos: Rust (previously: Go dominant)

CLUSTER
  Topic "wasm" appeared in new repos from 2 watched devs this window
  → antirez/smalldb (tagged: storage, c)
  → mitchellh/go-wasmtime (tagged: wasm, go)
```

---

## Integration With the [Office](../../framework/office.md)

This maps naturally onto the existing [Signal Scout](../../agents/workers/signal-scout/signal-scout.md) pipeline:

```
repo-radar (cron or COO-scheduled)
        ↓
  Signal Scout — receives structured repo-radar output as a feed event
        ↓
  CAO — ingests, cross-references with existing ChromaDB research
        ↓
  CMO / CEO — acted on as a market intelligence input
```

In practice, this is either:
- **A variant of the [Signal Scout](../../agents/workers/signal-scout/signal-scout.md)** — the same Worker, given a `repo-radar` source type alongside its RSS sources
- **A standalone skill** (`skills/repo-radar.py`) called on a schedule by the [COO](../../agents/specialists/coo/coo.md), with its output pushed directly into the [Signal Scout](../../agents/workers/signal-scout/signal-scout.md)'s input queue

The second option is cleaner. The skill runs, produces a signal report, writes it as a task for the [Signal Scout](../../agents/workers/signal-scout/signal-scout.md) to evaluate and escalate. The [Signal Scout](../../agents/workers/signal-scout/signal-scout.md) applies the same noise filter it applies to everything else.

---

## Minimal Implementation

A working version needs three things:

**1. `config/repo-radar.json`** — the watched list (shown above)

**2. `skills/repo-radar.py`** — the script:
- Reads the config
- Fetches recent activity per user via `GET /users/{username}/repos?sort=pushed&per_page=30`
- Loads previous snapshot from a local JSON file (`data/repo-radar-snapshot.json`)
- Diffs and detects clusters
- Writes updated snapshot
- Outputs a signal report string

**3. A [COO](../../agents/specialists/coo/coo.md) task entry on a schedule** — spawns the skill every N hours, pipes output to the [Signal Scout](../../agents/workers/signal-scout/signal-scout.md)

Total runtime: seconds. No persistent process. No special infrastructure beyond a GitHub token in the local environment.

---

## What This Is Not

- **Not a popularity tracker** — stars and forks are not the signal; behavior is
- **Not GitHub trending** — that is noise aggregated from millions of anonymous users; this is signal from a small list of trusted practitioners
- **Not surveillance** — all data is public by definition; GitHub exposes it explicitly via API

---

## Open Questions

- **Who curates the watched list?** Probably the [CAO](../../agents/management/cao/cao.md) or the Board directly — this is a judgment call, not an automated decision.
- **How stale is acceptable?** A 6-hour poll is a reasonable default; real-time webhooks are possible but require the repos to be owned by you.
- **How does the [CAO](../../agents/management/cao/cao.md) weight repo-radar signals vs. RSS signals?** Practitioner behavior should probably rank higher than aggregated commentary, but this needs to be explicit in the [CAO](../../agents/management/cao/cao.md)'s routing logic.
- **Should the snapshot be stored in ChromaDB or as a flat file?** ChromaDB is overkill for a diff store; a local JSON snapshot file is sufficient. The *signal report* output gets indexed in ChromaDB as `research` type.
- **Authentication** — a single read-only GitHub token with no scopes is sufficient and low-risk. Where does it live in the local environment?
