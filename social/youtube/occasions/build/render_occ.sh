#!/bin/bash
cd /tmp/claude-0/-home-user/e3a27352-eabf-5796-b70f-fdffad55ed6a/scratchpad/shorts
k=$1; T=$(python3 -c "import json;print(json.load(open('tl-x$k.json'))['total'])"); E=$(python3 -c "import json;print(json.load(open('tl-x$k.json'))['end']-0.1)")
rm -rf yf-x$k; PAGE=occ.html node shoot_x.cjs yf-x$k $k all 30 $T > yx$k.log 2>&1
ffmpeg -loglevel error -y -i base-x$k.mp4 -framerate 30 -i yf-x$k/%05d.png -i mix-x$k.wav -filter_complex "[0:v][1:v]overlay=format=auto,format=yuv420p[v]" -map "[v]" -map 2:a -c:v libx264 -preset slow -crf 20 -c:a aac -b:a 192k -shortest -movflags +faststart occ-$k.mp4
rm -rf yc-x$k; cp -r yf-x$k yc-x$k; CTA=1 FROM=$E PAGE=occ.html node shoot_x.cjs yc-x$k $k all 30 $T > yc-x$k.log 2>&1
ffmpeg -loglevel error -y -i base-x$k.mp4 -framerate 30 -i yc-x$k/%05d.png -i mix-x$k.wav -filter_complex "[0:v][1:v]overlay=format=auto,format=yuv420p[v]" -map "[v]" -map 2:a -c:v libx264 -preset slow -crf 20 -c:a aac -b:a 192k -shortest -movflags +faststart cta-occ-$k.mp4
echo done $k $(ls -la occ-$k.mp4 cta-occ-$k.mp4 | awk '{print $5}' | tr '\n' ' ')
