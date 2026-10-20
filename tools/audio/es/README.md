# Spanish course audio

All 354 words in `courses/es/curriculum.json`, voiced by ElevenLabs "Marina" (Spain Spanish, model `eleven_v4`), saved as `courses/es/audio/{wordId}.mp3`.

- `audio_groups.json` — 16 batches; each lists word ids, texts and the exact prompt sent (words separated by `...`, which is cheaper than `[long pause]` tags).
- `split_es.py` — splits each batch at the pauses (run with `NOISE=-35dB MIN_GAP=0.1`).
- `fetch_split.sh GROUP URL` — downloads one finished batch, splits it and copies the clips into `courses/es/audio/`.

Send batches **one at a time**: several at once triggered ElevenLabs' rate limit and a temporary free-tier block.
