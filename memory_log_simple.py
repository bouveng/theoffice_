#!/usr/bin/env python3
"""
Simple memory logging - appends timestamped entry to daily memory file.
"""

from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"

def log_entry(title="Task completed", summary="No details", agent="system"):
    """Append a log entry to today's memory file."""
    MEMORY_DIR.mkdir(exist_ok=True)
    
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    mem_path = MEMORY_DIR / f"{date_str}.md"
    
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    entry = f"""
## {title} — {timestamp}

**Agent:** {agent}  
**Summary:** {summary}

---
"""
    
    # If file doesn't exist, create with header
    if not mem_path.exists():
        header = f"# Daily Memory — {date_str}\n\n"
        with open(mem_path, 'w') as f:
            f.write(header)
    
    with open(mem_path, 'a') as f:
        f.write(entry)
    
    print(f"Logged to {mem_path}")

def main():
    """Example usage."""
    log_entry(
        title="Context discipline implementation",
        summary="Started session cleanup, created heartbeat compression and memory logging scripts.",
        agent="CTO"
    )

if __name__ == '__main__':
    main()