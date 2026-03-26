#!/bin/bash

NOW=$(date -u '+%Y-%m-%d %H:%M UTC')
UPTIME=$(awk '{d=int($1/86400);h=int(($1%86400)/3600);m=int(($1%3600)/60); if(d>0) printf "%dd%dh%dm",d,h,m; else if(h>0) printf "%dh%dm",h,m; else printf "%dm",m}' /proc/uptime)

LOAD=$(awk '{print $1}' /proc/loadavg)
RAM_TOTAL=$(awk '/MemTotal/ {printf "%.1f", $2/1024/1024}' /proc/meminfo)
RAM_USED=$(awk '/MemTotal/{t=$2} /MemAvailable/{a=$2} END{printf "%.1f", (t-a)/1024/1024}' /proc/meminfo)
RAM_PCT=$(awk '/MemTotal/{t=$2} /MemAvailable/{a=$2} END{printf "%d", int((t-a)/t*100)}' /proc/meminfo)
DISK_USED=$(df / --output=used -BG | tail -1 | tr -d 'G ')
DISK_TOTAL=$(df / --output=size -BG | tail -1 | tr -d 'G ')
DISK_PCT=$(df / --output=pcent | tail -1 | tr -d ' %')
AGENTS=$(openclaw agents list 2>/dev/null | grep -c '^\-' || echo "?")
SESSIONS=$(openclaw sessions --all-agents 2>/dev/null | grep -c '^[a-z]' || echo "?")

bar() {
  local pct=$1
  local steps=8  # UTF-8 block steps: ▁▂▃▄▅▆▇█
  local filled=$(( pct * steps / 100 ))
  [ $filled -gt $steps ] && filled=$steps
  local empty=$(( steps - filled ))
  local result=""
  
  # UTF-8 block gradient: ▁▂▃▄▅▆▇█
  case $filled in
    1) result="▁";;
    2) result="▂";;
    3) result="▃";;
    4) result="▄";;
    5) result="▅";;
    6) result="▆";;
    7) result="▇";;
    8) result="█";;
    0) result="▁";;  # Minimum visible
  esac
  
  # Add empty dots
  for i in $(seq 1 $empty); do result="${result}·"; done
  printf '%s' "$result"
}

CPU_BAR=$(bar ${LOAD%.*})
RAM_BAR=$(bar $RAM_PCT)
DISK_BAR=$(bar $DISK_PCT)

printf '@theoffice_ %s\n' "$NOW"
printf '├ cpu [%s] %s\n'          "$CPU_BAR"  "$LOAD"
printf '├ ram [%s] %s/%sGB\n'     "$RAM_BAR"  "$RAM_USED"  "$RAM_TOTAL"
printf '├ dsk [%s] %s/%sGB\n'     "$DISK_BAR" "$DISK_USED" "$DISK_TOTAL"
printf '└ up %s · %s agents · %s sess.\n' "$UPTIME" "$AGENTS" "$SESSIONS"
