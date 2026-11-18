# Handoff: ElevenLabs batch (started 18 Nov 2026)

Paul (18 Nov): "I've got 121k you may as well do them all." Credits reset on the 18th of each month, so the full
121,000 were available on 18 Nov. Expected spend for everything below is about 38,000. He has already approved it,
so don't ask again. Still use ONE take per line (`generations_count: 1`) and stop to tell him if it runs far over.

Nothing was recorded on 18 Nov because ElevenLabs had an incident ("Increased latency and API errors"): both
connectors timed out and then dropped out of the session. Check status.elevenlabs.io says it is resolved, then make
one small test generation before starting the batches.

## Already done (pushed; nothing is live)
- Content repo `main`:
  - Main was slimmed from 43.9 to 37.5 MB by moving social/, docs/gemini, art/social and art/share to the `originals`
    branch. Social card paths in CLAUDE.md now live on `originals`.
  - "At the beach" bonus unit (15 words) after Weather in Beginner, for th/fr/es/it (ids `beach-l1-0` …,
    `fr-beach-l1-0` …), with a unit picture cropped from Paul's beach painting.
  - Commit c20ba0c.
- Content repo `english` branch: `en-beach` unit, commit 2e8d1a9. courses.json `base` for English still points at
  ff8368b; move it to the new english commit when publishing.
- App repo (sawasdee-family `main`, commit bf43845):
  - Beach place in Night Market Dash (`src/lib/market-places.ts`, tap areas checked over the picture) behind the
    feature `beach: "preview"`.
  - 15 beach items in `src/data/market-items.json`.
  - `marketPlaceBeach` added to i18n.
  - Fill-the-gap sentences have ids `xx-gs-NNN` in `src/data/gap-sentences.json`. GapCard plays the whole sentence
    after a pick, but only when `SENTENCE_COMMIT` (src/lib/content.ts) is set and the feature `sentenceAudio` is on.
    It falls back to the word.
  - New features in features.ts, all "preview": `beach`, `colouring`, `sentenceAudio`.
- Recording lists (id, lang, text) are in `tools/audio/batch-nov18/`:
  - sentences.json (778)
  - alphabet-numbers.json (156 = Numbers not already in the courses + all letters)
  - beach-words.json (75)

## Still to do
1. **Test one batch first.** Record, save as mono mp3 with a 0.15 s lead-in (see tools/audio/README.md), then
   Whisper-check with faster-whisper (installed).
   - Rule: one word or sentence per generation.
   - If that's too slow, batches split at long pauses have worked before (tools/audio/es/fetch_split.sh), but
     Whisper-check every clip afterwards.
2. **Voices.** These are lesson voices, eleven_v4:
   - th Anna `brM9iIbwDREZaWL8luun`
   - fr Léa `ICk609TItINMseDpChFt`
   - es Marina `GB7fZx4ubHWxbBE05abF`
   - it Alina `wOXFTxgu7FQDBb1dsL7I`
   - en Alice (British): find the id with creative_list_voices, search "Alice", the English "Clear, Engaging Educator".
3. **Beach words (75).**
   - Files go to `audio/<id>.mp3` (Thai), `courses/<lang>/audio/<id>.mp3` (fr/es/it) and, on the english branch,
     `courses/en/audio/<id>.mp3`.
   - The beach crab (src/assets/places/beach.webp in the app, around x 55–180, y 1440–1550 of 900×2001) has 6
     legs. Edit it to 8 walking legs plus 2 claws (image edit; limb rule), or paint it out and remove the `crab` spot.
   - Then the `beach` feature can go "live" at publish.
4. **Alphabet & Numbers (156).**
   - Same folders as the beach words.
   - Letters: the text is the letter's name (e.g. "bé"). Check that each clip says the letter name.
   - Then switch the sections on: `extraTracksEnabled()` in the app's features.ts is preview-only.
5. **Sentences (778, ~29k characters).**
   - Put them on a NEW orphan branch `sentences` in this repo at `sentences/<id>.mp3`. Main must stay under 50 MB.
   - Then set `SENTENCE_COMMIT` in the app's content.ts to that branch's commit.
   - Consider playing the sentence in Sentence Train too.
6. **Fun sayings pictures (12).**
   - Units fun1–3 for th/fr/es/it, saved as art/units/fun1.webp and courses/<lang>/art/units/<lang>-fun1.webp,
     960×644 WebP.
   - Model gemini-3.1-flash-lite-image with the course mascot as the reference picture (about 310 credits each), as
     for the English Leo pictures (courses/en/art/unit_illustrations.json shows the prompt style).
   - Limb-check every one.
7. **Colouring sheets (about 8).**
   - Black-and-white line art, no mascots needed.
   - Each sheet shows market-items words to find and colour, labelled in the learner's course language. Ideas:
     breakfast table, fruit bowl, street, travel day, family picnic, night sky, beach, pets and books.
   - Add a Colouring part to /printables behind `colouring`.
   - Limb rule.
8. **Wrap up.**
   - Run `npx tsc --noEmit` and `npx vitest run`.
   - Add a What's new line.
   - Update the to-do list in CLAUDE.md.
   - Show Paul.
   - **Publish only when he says "publish"**:
     - move live.json;
     - update the app's BUILTIN_COMMIT and the bundled src/data/curriculum.json copy;
     - check every content file returns 200.
