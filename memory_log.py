#!/usr/bin/env python3
"""
Memory protocol: log completed work to daily memory files.
Scans recent session transcripts for task completions, extracts summaries,
appends to memory/YYYY‑MM‑DD.md.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"

def ensure_memory_dir():
    """Create memory directory if missing."""
    MEMORY_DIR.mkdir(exist_ok=True)

def get_daily_memory_path():
    """Return path to today's memory file."""
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    return MEMORY_DIR / f"{date_str}.md"

def scan_session_transcripts(agent_ids=('main', 'ceo', 'cto'), lookback_hours=24):
    """Scan transcripts for task completion patterns."""
    tasks = []
    
    for agent_id in agent_ids:
        sessions_path = Path(f"/home/ubuntu/.openclaw/agents/{agent_id}/sessions/sessions.json")
        if not sessions_path.exists():
            continue
        
        try:
            with open(sessions_path, 'r') as f:
                sessions = json.load(f)
        except json.JSONDecodeError:
            continue
        
        # Filter recent sessions (updated within lookback)
        cutoff = datetime.utcnow().timestamp() * 1000 - (lookback_hours * 3600 * 1000)
        recent = [s for s in sessions if s.get('updatedAt', 0) > cutoff]
        
        for session in recent:
            transcript_path = session.get('transcriptPath')
            if not transcript_path:
                continue
            
            tpath = Path(transcript_path)
            if not tpath.exists():
                continue
            
            # Read transcript lines
            try:
                with open(tpath, 'r') as f:
                    lines = f.readlines()
            except IOError:
                continue
            
            # Look for task completion patterns
            for line in lines:
                try:
                    entry = json.loads(line.strip())
                    if entry.get('type') != 'message':
                        continue
                    msg = entry.get('message', {})
                    if msg.get('role') != 'assistant':
                        continue
                    content = msg.get('content', [])
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'text':
                            text = item.get('text', '')
                            # Simple pattern matching
                            if any(phrase in text.lower() for phrase in [
                                'task completed', 'completed successfully', 
                                'deliverable', 'result:', 'finished', 'done'
                            ]):
                                # Extract task summary
                                lines = text.split('\n')
                                title = None
                                for l in lines:
                                    if l.strip().startswith('**') and '**' in l:
                                        title = l.strip()
                                        break
                                if not title:
                                    title = lines[0][:100] + '...' if lines[0] else 'Untitled task'
                                
                                tasks.append({
                                    'agent': agent_id,
                                    'session': session.get('sessionId', 'unknown'),
                                    'timestamp': entry.get('timestamp', 0),
                                    'title': title,
                                    'summary': text[:500]  # Truncate
                                })
                except json.JSONDecodeError:
                    continue
    
    return tasks

def append_to_memory(tasks):
    """Append task summaries to daily memory file."""
    if not tasks:
        return
    
    mem_path = get_daily_memory_path()
    ensure_memory_dir()
    
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    with open(mem_path, 'a') as f:
        f.write(f"\n## Memory Log — {timestamp}\n\n")
        for task in tasks:
            f.write(f"**{task['title']}**  \n")
            f.write(f"*Agent:* {task['agent']}  \n")
            f.write(f"*Summary:* {task['summary']}  \n")
            f.write("\n---\n\n")
    
    print(f"Logged {len(tasks)} tasks to {mem_path}")

def main():
    """Run memory logging."""
    print("Scanning for completed tasks...")
    tasks = scan_session_transcripts()
    if tasks:
        append_to_memory(tasks)
    else:
        print("No recent task completions found.")

if __name__ == '__main__':
    main()