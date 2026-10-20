# Plan: adding Spanish to Nong Chang & Family

Status: **parked until Lovable credits renew (17 Nov)**. All content (curriculum, art, audio) can be prepared before then without Lovable credits.

---

## 1. The idea in one line

Nong Chang's friend **Torito** (the little bull) teaches Spanish. Each family member picks which language(s) they learn; progress is kept separately per language.

## 2. Mascot: Torito the little bull

- Spain has **no official national animal**. The **bull** is its best-known unofficial symbol (the Osborne bull is protected as cultural heritage). The **Iberian lynx** is a second, conservation-themed symbol.
- **Choice: a friendly baby bull called Torito** ("little bull"). It pairs naturally with Nong Chang ("little elephant") and everyone recognises it as Spain.
- Style rules (same storybook style as Nong Chang):
  - Chubby baby bull, soft brown/cream fur, small **rounded** horns, big friendly eyes, rosy cheeks.
  - A **red-and-yellow neckerchief** (Spanish flag colours) instead of Nong Chang's teal scarf.
  - **No bullfighting imagery**: no matadors, capes, arenas, swords or anger. Torito is gentle and playful.
  - Avoid copying the "bull who sits under a cork tree smelling flowers" story (Ferdinand).
- Backup choice if you prefer: **Lía the Iberian lynx kitten**.

## 3. Where people choose a language (recommended)

1. **Language chip in the top bar** (flag + ▾, e.g. 🇹🇭 ▾), next to the streak. Tap → switch language or "Add a language". Always visible, one tap — the pattern people know from Duolingo.
2. **Me page → "My languages"** section: see your languages, add or remove one, and set your starting level for each.
3. **New learners**: "What would you like to learn?" (Thai / Spanish) is the first step, before the level choice and placement test.

Each profile chooses independently and can learn both.

## 4. How it fits the app (technical)

What stays the same:
- `lesson_progress` and `word_srs` are keyed by lesson/word IDs. Spanish IDs start with `es-`, so **no changes** to those tables.
- Thai content stays exactly where it is in this repo (no file moves, nothing breaks).
- Streaks, XP, badges and the family leaderboard stay **shared across languages** (time spent learning anything counts).

Database (one small migration):
- `learner_profiles.active_course text not null default 'th'` (check: `th`, `es`).
- New table `learner_courses (profile_id, course, start_level, added_at)`, primary key `(profile_id, course)`. RLS same as `learner_profiles` (owner/household via `can_write_profile`). Copy each profile's existing `start_level` into a `th` row.
- RPCs `set_active_course(profile, course)` and `set_start_level(profile, level, course)` (extend the existing one with an optional course, default `th`).

Content repo layout (new files only):
```
courses.json                       ← list of languages (done)
courses/es/curriculum.json         ← Spanish course (same shape as Thai)
courses/es/audio/{wordId}.mp3
courses/es/art/units/{unitId}.webp
courses/es/art/mascot.png
```
`courses.json` (in the repo root) lists each language with its flag, mascot, speech language and the paths to its curriculum, audio, pictures and mascot image.

Word format for Spanish (same as Thai, minus Thai-only fields):
```json
{"id":"es-b1-l1-0","text":"Hola","en":"Hello","accept":["hello","hi"],"emoji":"👋","gender":null,"note":"The h is silent"}
```
When loading, the app maps `text` to its internal `thai` field (one line in `buildCourse`: `thai: w.thai ?? w.text`), so the lesson engine needs no other changes. `roman` and `tone` are optional and simply hidden when missing.

Spanish-specific app details:
- Speech practice and the fallback voice use `es-ES`.
- Typing exercises ask for the **English** meaning, so Spanish accents never need typing.
- Speech practice: compare lower-case, without accents or ¿¡ marks (the Thai check is case-sensitive and keeps accents).
- The second track "Read Thai" becomes **"Sounds of Spanish"** for Spanish (vowels, ñ, rr, ll/y, j/g, c/z, silent h, accent marks). Phase 2.
- Mascot component, unit pictures and loading screen use the current course's mascot.
- Kids' mode, feedback flags, placement test, daily goals all work per course unchanged.

## 5. The Spanish course (content)

Same shape as Thai so families can switch easily: **6 levels, ~43 units, ~63 lessons, ~350 words and phrases**, with an emoji per word.

- **Beginner** (14 units): greetings, numbers 1–20, family, colours, food & drink, everyday phrases, days & time, places & directions, shopping, travel, weather, feelings, at school, first sentences.
- **Elementary** (6): el/la & un/una (gender), ser vs estar, present-tense verbs (-ar/-er/-ir), "me gusta", ordering in a café/restaurant, making plans.
- **Intermediate** (6): connectors (y, pero, porque, si), giving directions, describing people, jobs, short conversations, health & emergencies.
- **Upper-Intermediate** (6): opinions, the past (pretérito: fui, comí, hablé), storytelling, polite usted vs tú, phone calls, everyday idioms.
- **Advanced** (5): work & business, news words, future & conditional, famous sayings (refranes), discussion.
- **Fluency & Mastery** (6): Spain slang (vale, guay, ¡qué va!), humour & reactions, reading a paragraph, formal register, songs & poetry words, regional words.

Spain Spanish (Castilian) throughout: coche, móvil, ordenador, zumo, vale, vosotros.

## 6. Audio (ElevenLabs, your 10,000 free credits)

- One credit ≈ one character for the standard models; Flash/Turbo ≈ half. The Spanish words and phrases are about **5,000 characters**, so the whole course fits in **≈ 5,000–7,000 credits** (or ≈ 3,000 with Flash), leaving a buffer.
- Voice: a **Spain (Castilian) Spanish** voice, picked from your ElevenLabs voice list.
- Same proven pipeline as Thai (`tools/audio`): batches of ~25 words separated by short pauses (cheap punctuation pauses instead of `[long pause]` tags to save credits), auto-split into one mp3 per word.
- Licence note: the ElevenLabs free plan is for **non-commercial use and needs attribution** ("Voices by ElevenLabs" on the Me page). Fine for a free family app; check before ever charging or adding ads.

## 7. Pictures (ComfyUI on your PC, free)

- Reuse `tools/art/generate_unit_art_comfyui.py` with a Torito character description and a new `courses/es/art/unit_illustrations.json` (one scene per unit, Spain-flavoured: paella, a beach, a plaza, olive trees, a train, a market…).
- Same picker window for redoing bad ones, same auto-upload folder.
- ElevenLabs images cost ~400 credits each (43 × 400 = too much), so ComfyUI it is.

## 8. Lovable build (after 17 Nov)

Estimated **8–12 credits** in total (the feedback feature cost 6.3, so this is a guess with margin).

**Phase 1 (~6–8 credits): languages + Spanish course**
1. Migration + RPCs (section 4).
2. `courses.json` loader; per-course curriculum, audio and art URLs; per-course cache keys.
3. Language chip in the top bar, "My languages" on Me, language step for new learners.
4. Per-course mascot and speech language (Spanish speech check ignores case and accents).
5. Tests: course switching, progress kept separate, Thai unchanged.

**Phase 2 (~2–4 credits): polish**
1. "Sounds of Spanish" track.
2. Public `/learn-spanish` page for Google, plus a Spanish preview picture.
3. Feedback/report button works the same (already ID-based — check only).

**Ready-to-send message for Phase 1** — see section 9.

## 9. Lovable message for Phase 1 (send when credits are back)

> Add multi-language support with Spanish as the second course. Thai must keep working exactly as now (same content URLs, same progress).
>
> 1. **Database:** add `learner_profiles.active_course text not null default 'th'` with a check for 'th' or 'es'; new table `learner_courses (profile_id uuid references learner_profiles on delete cascade, course text check in ('th','es'), start_level text, added_at timestamptz default now(), primary key (profile_id, course))` with RLS matching learner_profiles (use can_write_profile for writes, household read). Backfill a 'th' row per profile from its current start_level. Add SECURITY DEFINER RPCs `set_active_course(p_profile uuid, p_course text)` and extend `set_start_level` with an optional `p_course text default 'th'`, both checking can_write_profile.
> 2. **Content:** load `courses.json` from CONTENT_BASE_URL. Each entry gives the `curriculum` file, the `audio` folder (`{audio}{wordId}.mp3`), the `art` folder (`{art}{unitId}.webp`) and `mascotImage`. Cache keys include the course id.
> 3. **Choosing a language:** a flag chip in the AppHeader (current course flag + ▾) opening a menu to switch or "Add a language"; a "My languages" card on /me (add, remove, starting level per language); and a "What would you like to learn?" step before the starting-level / placement step for new learners. Per profile.
> 4. **Per course:** mascot (Nong Chang for th, Torito for es, image from `{base}art/mascot.png`), speech recognition and fallback TTS language from `speechLang`, the second track only for Thai for now. In buildCourse map `text` to `thai` when `thai` is missing and treat `roman`/`tone` as optional (hide them when absent). For speech matching on Spanish, compare lower-case with accents and ¿¡ removed.
> 5. Streaks, XP, badges and leaderboard stay shared. Review and Practice only show the active course's words.
> 6. Tests for: switching course, separate progress per course, Thai unchanged, Spanish speech matching. Then bump CONTENT_BASE_URL to commit `<NEW COMMIT>`.

## 10. What can be done now (free)

| Step | Who | Cost |
|---|---|---|
| Write the Spanish curriculum (`courses/es/curriculum.json`) — 6 levels, 43 units, 63 lessons, 354 words | Claude | **done** |
| Write Torito's character + 43 scene descriptions; adapt the ComfyUI script (`--course es`) | Claude | **done** |
| Generate Torito pictures in ComfyUI, pick, upload | Paul's PC | free |
| Generate Spanish audio | Claude via ElevenLabs | ~5–7k of your 10k credits (ask first) |
| `courses.json` | Claude | **done** |
| Lovable Phase 1 + 2 | after 17 Nov | ~8–12 Lovable credits |
