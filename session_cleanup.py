#!/usr/bin/env python3
"""
Manual session cleanup: remove sessions older than retention threshold.
"""

import json
import time
from pathlib import Path

# Retention thresholds (milliseconds)
SUBAgent_RETENTION_MS = 2 * 3600 * 1000  # 2 hours
MAIN_RETENTION_MS = 6 * 3600 * 1000      # 6 hours

AGENT_PATHS = [
    ("main", Path("/home/ubuntu/.openclaw/agents/main/sessions/sessions.json")),
    ("ceo", Path("/home/ubuntu/.openclaw/agents/ceo/sessions/sessions.json")),
    ("cto", Path("/home/ubuntu/.openclaw/agents/cto/sessions/sessions.json"))
]

def cleanup_agent(agent_id, sessions_path):
    """Remove stale sessions from an agent's store."""
    if not sessions_path.exists():
        print(f"Session store not found: {sessions_path}")
        return 0
    
    try:
        with open(sessions_path, 'r') as f:
            sessions = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error reading {sessions_path}: {e}")
        return 0
    
    # sessions.json is a dict mapping sessionKey -> session object
    current_time_ms = time.time() * 1000
    deleted = 0
    
    new_sessions = {}
    for session_key, session in sessions.items():
        updated_at = session.get('updatedAt', 0)
        age_ms = current_time_ms - updated_at
        
        # Determine retention based on session type
        is_subagent = ':subagent:' in session_key
        retention_ms = SUBAgent_RETENTION_MS if is_subagent else MAIN_RETENTION_MS
        
        if age_ms > retention_ms:
            print(f"Deleting stale session: {session_key} (age: {age_ms/3600000:.1f}h)")
            deleted += 1
        else:
            new_sessions[session_key] = session
    
    if deleted > 0:
        # Backup original
        backup_path = sessions_path.with_suffix('.json.backup')
        import shutil
        shutil.copy2(sessions_path, backup_path)
        
        # Write updated
        with open(sessions_path, 'w') as f:
            json.dump(new_sessions, f, indent=2)
        print(f"Deleted {deleted} stale sessions from {agent_id}")
    
    return deleted

def main():
    """Clean up all agent session stores."""
    total = 0
    for agent_id, path in AGENT_PATHS:
        deleted = cleanup_agent(agent_id, path)
        total += deleted
    
    print(f"Total deleted: {total}")
    
    # Also kill any Claude model sessions (manual)
    print("\nChecking for Claude model sessions...")
    for agent_id, path in AGENT_PATHS:
        if not path.exists():
            continue
        with open(path, 'r') as f:
            sessions = json.load(f)
        claude_sessions = [k for k, v in sessions.items() 
                          if v.get('model', '').startswith('claude-')]
        if claude_sessions:
            print(f"  {agent_id}: {len(claude_sessions)} Claude sessions (need manual removal)")

if __name__ == '__main__':
    main()