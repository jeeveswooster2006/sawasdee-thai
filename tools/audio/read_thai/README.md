# Read Thai audio (letters, vowels, tones, tone marks)

Recorded 27 Oct 2026 with ElevenLabs "Anna-Thailand-Female" (`brM9iIbwDREZaWL8luun`, `eleven_v4`) so the Read Thai track no longer depends on the phone's built-in Thai voice.

- `build_groups.py` lists the 73 items exactly as the app's `src/data/read-thai.ts` defines them (ids like `rt-letter-ก`, `rt-vowel-อา`, `rt-tone-mid`, `rt-mark-khaa-ek`; letters say the name, e.g. "กอ ไก่") and writes `audio_groups.json` (3 batches, 67 recordings) and `copies.json` (items that share a sound: ไอ/ใอ, and the five ก tones used in both the tone and tone-mark lessons).
- Split: from this folder, `NOISE=-40dB MIN_GAP=0.2 python3 ../split_audio.py 0 1 2`, then `bash ../pad_short_clips.sh audio_out`.
- Files: `audio/{id}.mp3` in the repo root (same folder as the course words). Tone clips were checked by pitch contour (mid level, low falling low, falling starts high, high rises, rising dips then rises).
