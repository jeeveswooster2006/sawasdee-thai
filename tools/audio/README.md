# Course audio pipeline

Thai pronunciation for every word in `data/curriculum.json`, voiced by ElevenLabs ("Anna – Thailand", model `eleven_v4`).

- `audio_groups.json` — the 16 batches: each lists word ids, the original Thai, and the exact text sent to the voice (words separated by `[long pause]`; `...` placeholders removed, `555` spoken as ห้าห้าห้า).
- `split_audio.py` — splits each batch clip into one file per word by cutting at the longest silences (one boundary per word), merging silences broken by tiny clicks, trimming edge silence, and encoding mono 96 kbps mp3 to `audio/{wordId}.mp3`.

Each batch is also transcribed independently (speech-to-text on a standalone copy of the clip) to confirm the voice said the right words.

## Audio check, 5 Nov 2026
Every lesson clip in all three courses was transcribed with local Whisper (small, then medium for doubtful ones). The results:
- **Shifted clips:** three runs had been shifted by one word: Spanish colours, French colours, and French qualities/jobs. They were moved back.
- **Re-recorded:** 90 clips with cut-off or wrong sounds, plus French "blanc", which was missing. Each word was recorded on its own (eleven_v4, same voices, no splitting), with edge silence trimmed and a 0.15 s lead-in added.
- **Lead-in added:** 787 clips that started with no silence got a 0.15 s lead-in, so iPhones don't swallow the first sound.
- For future recordings, prefer one word per generation over splitting batches.
