# Sounds of Spanish (Spanish alphabet track)

The Spanish version of "Read Thai". Content and audio live in this repo; the app needs one small Lovable job to show it.

## Content
`courses/es/sounds-of-spanish.json`: one level, "Sounds of Spanish", same shape as `READ_THAI_LEVELS` but with Spanish word fields (`text` instead of `thai`, `note` as the intro tip):

| Unit | Lessons | Items |
|---|---|---|
| The five vowels | 1 | A E I O U |
| The alphabet | 4 | 22 letter names with an example word (B to Z, including Ñ) |
| Tricky sounds | 3 | ñ, ll, r/rr, ch · c/z/qu in Spain · j, g, gue/gui, silent h |
| Accents and marks | 2 | stress (casa, café, árbol, música, avión) · ¿? ¡! ü sí tú |
| Read real words | 3 | greetings, numbers, family (reuse course recordings via `audioId`) |

Item fields: `id` (all start `es-sp-`), `kind` (letter / sound / word / mark / reading), `text`, `roman` (simple sound-alike), `en`, `emoji`, `say` (what the recording says), `note` (tip shown on the intro card), optional `audioId` (play another clip), `accept`.

Audio: `courses/es/audio/{id}.mp3` for every item without `audioId`.

## Lovable brief (send after Spanish part 2b; about 1–2 credits)

> Add the Spanish second track, "Sounds of Spanish", the Spanish equivalent of Read Thai. Thai must not change.
> 1. Load `courses/es/sounds-of-spanish.json` from CONTENT_BASE_URL (same caching as the curriculum, cache key includes the course and pin). Map `text`→`thai`, `note`→`intro`, keep `roman`, `emoji`, `audioId`, `kind`; tone is empty. Build it with `buildCourse` like `buildReadThaiCourse` (no tone drills, no reading-id lookup needed: reading items already carry `audioId`).
> 2. Wherever the app shows the Read Thai track (Learn page levels list, Progress), show "Sounds of Spanish" instead when the active course is Spanish, using `buildReadThaiQueue` for its lessons (toneDrills false). Progress is stored by lesson id as now (ids start `es-sp-`).
> 3. Audio: `es-sp-` items play `courses/es/audio/{audioId ?? id}.mp3` (the `rt-` browser-voice rule must not apply to them); fallback voice es-ES.
> 4. Tests: the track loads and builds; a Spanish profile sees "Sounds of Spanish" and a Thai profile still sees Read Thai; audio URL for `es-sp-vowel-a` and for a reading item with `audioId`. Then bump CONTENT_BASE_URL to the commit containing the audio.

## Also planned
An "Alphabet & Numbers" shortcut card near the top of the Learn page, linking to the second track (Read Thai / Sounds of Spanish) and the number units for the active course (Thai: numbers1, numbers2, classifiers; Spanish: es-numbers1, es-numbers2).
