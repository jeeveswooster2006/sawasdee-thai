#!/bin/sh
# usage: fetch_split.sh GROUP URL  -> downloads the batch, splits it, copies clips into courses/fr/audio
set -e
cd "$(dirname "$0")"
f=$(printf "audio_raw/group%02d.mp3" "$1")
curl -sS -o "$f" "$2"
NOISE=-35dB MIN_GAP=0.1 python3 split_fr.py "$1" | python3 -c "
import json,sys; r=json.load(sys.stdin); k=list(r)[0]; v=r[k]
if not v['ok']: print('batch',k,'FAILED:',v['why']); sys.exit(1)
g=json.load(open('audio_groups.json'))[int(k)]
print('batch',k,'ok', len(v['segs']), 'clips |', ' | '.join(f'{t} {b-a:.2f}' for t,(a,b) in zip(g['texts'],v['segs'])))"
python3 -c "
import json,shutil; g=json.load(open('audio_groups.json'))[$1]
[shutil.copy(f'audio_out/{i}.mp3', f'../../../courses/fr/audio/{i}.mp3') for i in g['ids']]"
