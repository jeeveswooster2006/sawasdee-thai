# Fill-the-gap sentence recordings

One mp3 per sentence in the app's `src/data/gap-sentences.json`, named by its id (`sentences/<id>.mp3`, e.g. `fr-gs-012`).
Kept on this orphan branch so `main` stays under jsDelivr's 50 MB per-commit limit. The app pins a commit of this
branch as `SENTENCE_COMMIT` in `src/lib/content.ts`.

Recorded 18–19 Nov 2026 (all 778) with ElevenLabs eleven_v4, one take each, the course voices (th Anna, fr Léa, es Marina,
it Alina, en Alice), trimmed with a 0.15 s lead-in, mono 96 kbps, and checked with Whisper.
