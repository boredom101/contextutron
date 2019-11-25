#!/bin/bash
while true; do sleep 1 && xdotool getwindowpid `xdotool getactivewindow` 2>/dev/null; done
