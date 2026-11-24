#!/bin/bash
cd /tmp/claude-0/-home-user/e3a27352-eabf-5796-b70f-fdffad55ed6a/scratchpad/shorts
k=$1
rm -rf yf-x$k; node shoot_x.cjs yf-x$k $k all 30 20.6 > yx$k.log 2>&1
ffmpeg -loglevel error -y -i base-x$k.mp4 -framerate 30 -i yf-x$k/%05d.png -i mix-x$k.wav -filter_complex "[0:v][1:v]overlay=format=auto,format=yuv420p[v]" -map "[v]" -map 2:a -c:v libx264 -preset slow -crf 19 -c:a aac -b:a 192k -shortest -movflags +faststart xmas-$k.mp4
echo done $k $(ls yf-x$k | wc -l)
