#!/bin/bash
cd /tmp/claude-0/-home-user/e3a27352-eabf-5796-b70f-fdffad55ed6a/scratchpad/shorts
s=$1; read d e < <(python3 -c "import json;j=json.load(open('tl-$s.json'));print(j['total'],j['end']-0.1)")
rm -rf af-$s; S=$s node shoot_a.cjs af-$s all 30 $d > af-$s.log 2>&1
ffmpeg -loglevel error -y -framerate 30 -i af-$s/%05d.jpg -i mix-$s.wav -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart alike-$s.mp4
rm -rf ac-$s; cp -r af-$s ac-$s; CTA=1 FROM=$e S=$s node shoot_a.cjs ac-$s all 30 $d >> af-$s.log 2>&1
ffmpeg -loglevel error -y -framerate 30 -i ac-$s/%05d.jpg -i mix-$s.wav -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart cta-alike-$s.mp4
echo done $s $(ls af-$s | wc -l)
