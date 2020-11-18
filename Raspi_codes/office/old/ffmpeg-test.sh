#!/bin/sh

raspivid -o - -w 1280 -h 720 -t 0 -fps 30 -b 2000000 |
ffmpeg -r 30 -i - -vcodec copy \
-f segment -strftime 1 -segment_time 60 \
-segment_format_options movflags=+faststart -segment_format mp4 \
-reset_timestamps 1 \
/home/pi/%Y-%m-%d_%H-%M.mp4

