#!/bin/bash
# Pad very short clips with 0.2 s of leading silence (iPhones clip the start)
# and lift quiet ones so the loudest point is about -3 dB (max +8 dB boost).
set -e
dir="$1"; tmp=$(mktemp -d)
for f in "$dir"/*.mp3; do
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  awk -v d="$d" 'BEGIN{exit !(d<0.8)}' || continue
  peak=$(ffmpeg -hide_banner -i "$f" -af volumedetect -f null - 2>&1 | grep -oE "max_volume: [-0-9.]+" | awk '{print $2}')
  gain=$(awk -v p="$peak" 'BEGIN{g=-3-p; if(g<0)g=0; if(g>8)g=8; printf "%.1f", g}')
  ffmpeg -v error -y -i "$f" -af "adelay=200:all=1,volume=${gain}dB" -ar 44100 -ac 1 -c:a libmp3lame -b:a 96k "$tmp/$(basename "$f")"
  mv "$tmp/$(basename "$f")" "$f"
  echo "$(basename "$f" .mp3) dur=$d peak=$peak gain=+${gain}dB"
done
rmdir "$tmp"
