# French course audio

All 354 words in `courses/fr/curriculum.json`, voiced by ElevenLabs "Léa formatrice" (`ICk609TItINMseDpChFt`, Paris French, calm teacher voice, model `eleven_v4`), saved as `courses/fr/audio/{wordId}.mp3`.

- `audio_groups.json`: 20 batches. Each lists word ids, texts and the exact prompt sent (words separated by `...`).
- `split_fr.py`: splits each batch at the pauses (run with `NOISE=-35dB MIN_GAP=0.1`).
- `fetch_split.sh GROUP URL`: downloads one finished batch, splits it and copies the clips into `courses/fr/audio/`.

Send batches **one at a time** (several at once hit ElevenLabs' rate limit when Spanish was recorded).
Rebuild the word list with `python3 tools/content/build_french.py` and the batches from it before recording again.
