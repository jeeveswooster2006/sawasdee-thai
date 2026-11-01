# Read Thai audio (letters, vowels, tones, tone marks)

Recorded 27 Oct 2026 with ElevenLabs "Anna-Thailand-Female" (`brM9iIbwDREZaWL8luun`, `eleven_v4`) so the Read Thai track no longer depends on the phone's built-in Thai voice.

- `build_groups.py` lists the 73 items exactly as the app's `src/data/read-thai.ts` defines them (ids like `rt-letter-ก`, `rt-vowel-อา`, `rt-tone-mid`, `rt-mark-khaa-ek`; letters say the name, e.g. "กอ ไก่") and writes `audio_groups.json` (3 batches, 67 recordings) and `copies.json` (items that share a sound: ไอ/ใอ, and the five ก tones used in both the tone and tone-mark lessons).
- Split: from this folder, `NOISE=-40dB MIN_GAP=0.2 python3 ../split_audio.py 0 1 2`, then `bash ../pad_short_clips.sh audio_out`.
- Files: `audio/{id}.mp3` in the repo root (same folder as the course words). Tone clips were checked by pitch contour (mid level, low falling low, falling starts high, high rises, rising dips then rises).

## More vowels (1 Nov 2026)
17 more vowels for lessons vowels-4 to vowels-7 (แอะ โอะ เอาะ ออ อึ อือ เออะ เออ เอีย เอือ อัว เอา เอียะ เอือะ อัวะ ฤ ฤๅ), same voice and model. Batch 3 was appended to `audio_groups.json` by hand (build_groups.py still describes the first 73 items). Split with `NOISE=-40dB MIN_GAP=0.2 python3 ../split_audio.py 3`, then only the 17 new clips were padded (pad_short_clips.sh is not safe to re-run on clips already padded).
