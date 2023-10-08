#!/bin/bash

VOICE="Tessa"
IDLE_THRESHOLD=60000 # Idle time threshold in milliseconds, 60000 ms = 1 minute
DELAY=600 # Interval between warnings, in seconds

while true; do
    # Get the idle time in milliseconds
    idle_time=$(/usr/sbin/ioreg -c IOHIDSystem | awk '/HIDIdleTime/ {print $NF/10^9; exit}')
    
    # Check if the idle time is less than the threshold
    if (( $(echo "$idle_time < $IDLE_THRESHOLD" | bc -l) )); then
        say -v $VOICE "Time for a break"
    fi

    sleep $DELAY
done
