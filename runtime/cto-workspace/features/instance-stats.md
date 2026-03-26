# CTO Feature: Instance Stats Display

## Overview
The CTO provides real‑time instance statistics in the #theoffice_ channel using UTF‑8 enhanced formatting.

## Trigger Commands
- `instance`
- `show instance`
- `how is the instance`

## Response Format
```
@theoffice_ YYYY‑MM‑DD HH:MM UTC
├ cpu [▁▂▃▄▅▆▇█····] load
├ ram [▁▂▃▄▅▆▇█····] used/totalGB
├ dsk [▁▂▃▄▅▆▇█····] used/totalGB
└ up XdXhXm · N agents
```

## Features
- **UTF‑8 bars**: 8‑step gradient (`▁▂▃▄▅▆▇█`) for visual metrics
- **Mobile‑friendly**: 30‑character width (fits Discord mobile)
- **Monochrome only**: All icons from UTF‑8 monochrome library
- **Real‑time**: Live system metrics (CPU, RAM, disk, uptime, agents)
- **Compact format**: No word‑wrap, clean presentation

## Technical Implementation
- **Script**: `scripts/stats.sh`
- **Icons**: Box drawing (`├ ─ └`) + block elements (`▁▂▃▄▅▆▇█`)
- **Metrics**: CPU load, memory usage, disk usage, uptime, agent count
- **Policy**: CTO responds with code‑block only, no extra commentary

## Usage Example
User: `instance`
CTO:
```
` `` `
@theoffice_ 2026‑03‑26 16:37 UTC
├ cpu [▁········] 0.02
├ ram [▁········] 1.0/23.4GB
├ dsk [▁········] 5/45GB
└ up 2d0h16m · 3 agents
` `` `
```

## Version History
- **2026‑03‑26**: Upgraded to UTF‑8 format with monochrome icons
- **2026‑03‑25**: Initial ASCII implementation
- **Source**: AGENTS.md server stats specification

## Notes
- Part of CTO's core responsibilities per AGENTS.md
- Uses monochrome UTF‑8 library exclusively
- Maintains consistent cross‑platform display
- Available to all channel participants