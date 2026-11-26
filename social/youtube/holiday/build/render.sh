#!/bin/bash
# Renders each Short: frames at 30 fps, then mux with its mix.
cd "$(dirname "$0")"
for k in "$@"; do
  total=$(python3 -c "import json;print(json.load(open('tl-$k.json'))['total'])")
  rm -rf fr-$k && S=$k node shoot.cjs fr-$k all 30 $total > log-$k.txt 2>&1
  ffmpeg -loglevel error -y -framerate 30 -i fr-$k/%05d.jpg -i mix-$k.wav -c:v libx264 -pix_fmt yuv420p -crf 19 -preset medium -c:a aac -b:a 192k -shortest -movflags +faststart holiday-$k.mp4
  echo "done $k $(du -h holiday-$k.mp4 | cut -f1)"
done
