#!/bin/bash

kill $(ps aux | grep '/break_timer.sh' | awk '{print $2}')
