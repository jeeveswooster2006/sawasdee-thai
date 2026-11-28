#!/bin/bash
cd /tmp/claude-0/-home-user/e3a27352-eabf-5796-b70f-fdffad55ed6a/scratchpad/shorts
P=../pierce
read T E < <(python3 -c "import json;j=json.load(open('tl-pierce.json'));print(j['total'],j['end']-0.1)")
rm -rf po-f; PAGE=pierce.html node shoot_x.cjs po-f x all 30 $T > po.log 2>&1
ffmpeg -loglevel error -y -i $P/base.mp4 -framerate 30 -i po-f/%05d.png -i mix-pierce.wav -filter_complex "[0:v][1:v]overlay=format=auto,format=yuv420p[v]" -map "[v]" -map 2:a -c:v libx264 -preset slow -crf 23 -c:a aac -b:a 192k -shortest -movflags +faststart pierce-hello.mp4
rm -rf po-c; cp -r po-f po-c; CTA=1 FROM=$E PAGE=pierce.html node shoot_x.cjs po-c x all 30 $T >> po.log 2>&1
ffmpeg -loglevel error -y -i $P/base.mp4 -framerate 30 -i po-c/%05d.png -i mix-pierce.wav -filter_complex "[0:v][1:v]overlay=format=auto,format=yuv420p[v]" -map "[v]" -map 2:a -c:v libx264 -preset slow -crf 23 -c:a aac -b:a 192k -shortest -movflags +faststart cta-pierce-hello.mp4
ls -la pierce-hello.mp4 cta-pierce-hello.mp4
