# Course audio pipeline

Thai pronunciation for every word in `data/curriculum.json`, voiced by ElevenLabs ("Anna – Thailand", model `eleven_v4`).

- `audio_groups.json` — the 16 batches: each lists word ids, the original Thai, and the exact text sent to the voice (words separated by `[long pause]`; `...` placeholders removed, `555` spoken as ห้าห้าห้า).
- `split_audio.py` — splits each batch clip into one file per word by cutting at the longest silences (one boundary per word), merging silences broken by tiny clicks, trimming edge silence, and encoding mono 96 kbps mp3 to `audio/{wordId}.mp3`.

Each batch is also transcribed independently (speech-to-text on a standalone copy of the clip) to confirm the voice said the right words.
