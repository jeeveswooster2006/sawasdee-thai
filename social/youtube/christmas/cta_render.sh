#!/bin/bash
cd /tmp/claude-0/-home-user/e3a27352-eabf-5796-b70f-fdffad55ed6a/scratchpad/shorts
kind=$1; k=$2
if [ $kind = x ]; then
  rm -rf yc-x$k; cp -r yf-x$k yc-x$k; CTA=1 FROM=16.1 node shoot_x.cjs yc-x$k $k all 30 20.6 > yc-x$k.log 2>&1
  ffmpeg -loglevel error -y -i base-x$k.mp4 -framerate 30 -i yc-x$k/%05d.png -i mix-x$k.wav -filter_complex "[0:v][1:v]overlay=format=auto,format=yuv420p[v]" -map "[v]" -map 2:a -c:v libx264 -preset slow -crf 19 -c:a aac -b:a 192k -shortest -movflags +faststart cta-xmas-$k.mp4
elif [ $kind = x5 ]; then
  rm -rf yc-x5; cp -r yf-x5 yc-x5; CTA=1 FROM=51.9 node shoot_x5.cjs yc-x5 x all 30 57.0 > yc-x5.log 2>&1
  ffmpeg -loglevel error -y -i x5/base.mp4 -framerate 30 -i yc-x5/%05d.png -i mix-x5.wav -filter_complex "[0:v][1:v]overlay=format=auto,format=yuv420p[v]" -map "[v]" -map 2:a -c:v libx264 -preset slow -b:v 2300k -maxrate 2600k -bufsize 5000k -c:a aac -b:a 160k -shortest -movflags +faststart cta-xmas-in-5.mp4
else
  read d e < <(python3 -c "import json;j=json.load(open('tl-$k.json'));print(j['total'],j['end']-0.1)")
  rm -rf bc-$k; cp -r bf-$k bc-$k; CTA=1 FROM=$e S=$k node shoot_b.cjs bc-$k all 30 $d > bc-$k.log 2>&1
  ffmpeg -loglevel error -y -framerate 30 -i bc-$k/%05d.jpg -i mix-$k.wav -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart cta-$k.mp4
fi
echo done $kind $k
