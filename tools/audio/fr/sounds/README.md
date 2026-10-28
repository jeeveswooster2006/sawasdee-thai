# Sounds of French (alphabet track) audio

`build_sounds.py` writes `courses/fr/sounds-of-french.json` (the French alphabet track: vowels, the other letters, tricky sounds, accents and marks, and reading practice) and `audio_groups.json` (3 recording batches). Run it from the repo root.

Voice: ElevenLabs "Léa formatrice" (`ICk609TItINMseDpChFt`, Paris French, `eleven_v4`). Each letter clip says the letter name then the example word ("bé, bateau"). Reading items reuse the course recordings through `audioId`, so they are not in the batches. Clips go to `courses/fr/audio/{id}.mp3`.

Split a batch: copy it to `audio_raw/groupNN.mp3`, then from this folder `NOISE=-35dB MIN_GAP=0.1 python3 ../split_fr.py N` with this folder's `audio_groups.json`.
