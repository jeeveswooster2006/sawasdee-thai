# Sounds of Spanish (alphabet track) audio

`build_sounds.py` writes `courses/es/sounds-of-spanish.json` (the Spanish alphabet track: vowels, the 27 letters, tricky sounds, accents, and reading practice) and `audio_groups.json` (2 recording batches).

Voice: ElevenLabs "Marina" (`GB7fZx4ubHWxbBE05abF`, Spain Spanish, `eleven_v4`). Each letter clip says the letter name then the example word ("be, barco"). Reading items reuse the course recordings through `audioId`. Clips go to `courses/es/audio/{id}.mp3`.

Split a batch: copy it to `audio_raw/groupNN.mp3`, then from this folder `NOISE=-35dB MIN_GAP=0.1 python3 ../split_es.py N` with this folder's `audio_groups.json`.
