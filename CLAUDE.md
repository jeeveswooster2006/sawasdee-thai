# Rules for this project (Nong Chang & Family)

## All five languages are equal in posts (Paul, 14 Nov 2026; replaces the 10 Nov "lead with Thai families" rule for posts)
- Facebook, Instagram and community posts mention all five languages (Thai, French, Spanish, Italian, English) equally. Thai is not the main focus; they are all equally important. Only a language-specific group or page gets its own language first (see "Social media and community messages").
- Background: the 10 Nov growth audit found 35 of 36 learners chose Thai, so posters and the front page were made Thai-first (front page: Nong Chang biggest; A4 poster: Thai first). Those stay as they are unless Paul asks; new posts follow the equal rule.

## To-do list (keep this up to date: the twice-weekly reminder reads it)
Tick items off here (move to the right section's notes) as they're done; add new ones as Paul agrees them.
**Waiting for Paul**
- Health check (12 Nov, report: claude.ai/artifact/2CYvRYsxHLzoQEoUe8EggG): free fixes 1–12 and Lovable 13–15 DONE 12 Nov (Lovable migration 0018 for streak dates/12-hour sessions is already live in the shared database; timers got a 60 s timeout). PUBLISHED 12 Nov (Paul: "Publish"), checked on the live site. 17 "Connect an app" REMOVED 12 Nov (Paul; nobody had used it; live, /mcp now 404); 18 DONE 12 Nov (Paul's screenshot: secure email change, re-authentication and current password for password changes, HIBP all on; minimum length stays 6 because child logins allow 6). Still for Paul: 19 turn on GitHub two-factor; 20 "teach new words before testing" (bigger change, his call). Not done: loading only the visitor's language text (needs a bigger rework) and 16 (XP totals in the database, later).
- Lovable security scan (12 Nov): AI-instructions finding fixed and PUBLISHED 12 Nov; household-ownership finding fixed directly in the live database (free, Paul: "Publish"). "Email another person" is the adult-login setup email, by design and capped: Paul to tap ⋯ → Ignore with that reason, then re-run the scan.
- Thai pronunciation check (12 Nov, Paul: "publish lessons"): all 471 Thai words/phrases checked; 6 Latin-spelling fixes (ท้อง, ห้อง, full Thursday, เท่, ก็, story น้อง). live.json → f59622b, all 2,026 content files returned 200; app BUILTIN_COMMIT updated. Hello-in-Thai guide explains sawasdee/sawatdee/sawadee (live 12 Nov).
- Design review (12 Nov, claude.ai/artifact/5imUmMWUfvryH4pQxZsRei): D1–D14, S1–S3, B1 PUBLISHED 12 Nov (Paul: "Publish"), checked on the live site (fonts cached a year, five-mascot link preview, taster start/end, spelling key, 404). Also published: speaking practice computer-only and off unless switched on (Paul doesn't want it promoted yet); extra XP for games and the word quiz (30/40 XP, 4 a day each, not the streak). B2 DONE 12 Nov: brand kit kept as a Claude design system (claude.ai/artifact/XMu91n1jb7zaQYrE8TJq6Z). B3: Paul said leave the old "Natterly" Lovable description (harmless label).
- Loy Krathong (Tue 24 Nov): 39-second 3D video MADE 13 Nov (three.js, cut-out mascots on a night river, Nong Chang explains to Coco, Torito, Lupo and Leo; voice lines about 600 ElevenLabs credits, more than the 461 Paul had; possibly some overage, Paul to check). v2 MADE 14 Nov (Paul chose 2D puppets over 3D: a Blender toy model and a Meshy model painted from his art both looked wrong to him; faces must stay exactly as painted): the pictures bend in soft zones (ears, trunk, heads, tails, Coco's wing), more hops, closer camera, Torito mirrored to face Nong Chang. Waiting for Paul's changes or "post" (plan: the saved November slot, Tue 24 Nov 7pm, Facebook and Instagram, marked AI-generated). Source: scratchpad loy/ (scene.html, music.py); copy the MP4 to the `originals` branch `social/reels/` once approved.
- Mon 16 Nov (and any later Monday): post the app in r/multilingualparenting's weekly advertising thread (mods said 14 Nov that's the only place for it; comment text drafted 14 Nov: family account, games together, kids' mode, native voices, free, all five languages, nongchang.co.uk/rd, five-mascot picture).
- Native-speaker questions from the audit (vous/tú formality, Gentili Signori, "Spare the rod", ผม/ฉัน labels, etc.).
- Check the sign-in limits: Lovable → More → Users → Settings (sign-in attempts at most 30 per 5 minutes). Email settings live under More → Users → Settings → Email.
- Put up the A4 poster (temples, Thai shops, schools) and post in community groups. Reddit: an app post on r/learnthai was removed (likely their "no promotion without mod approval" rule); Paul messaged the mods 12 Nov; they asked to see the original post and APPROVED it 13 Nov (link nongchang.co.uk/rd, so sign-ups show signup_source "rd"). Don't post it again elsewhere in the same words.
- Confirm his real login still works (a "Dad" learner from 14 Oct is under another login).
- GoGo España reply (info@).
- Add the Lovable connector to the "Morning suggestions" scheduled task (claude.ai scheduled tasks screen).
**Free, Claude can do when asked**
- Christmas guide page: "Christmas words in French, Spanish and Italian for kids" (early December).
- Weekly numbers summary each Monday (visitors, sign-ups, where from).
- Tidy the Resend contacts: remove people who never opted in to news emails (privacy; needs Paul's OK).
**Needs credits**
- ElevenLabs (reset about 5 Dec; balance used up by the Loy Krathong voice lines on 13 Nov, so nothing more until the reset): Alphabet & Numbers recordings (~850 credits, then switch on), Fun sayings pictures (~310 each × 12), colouring-sheet pictures (~310 each). Then downgrade ElevenLabs.
- Lovable: later, XP totals in the database (item 16). Phone push reminders BUILT 13 Nov (Lovable 1 credit for the tables + 1 credit security re-check, nothing serious found; app side free): PUBLISHED 13 Nov and WORKS on Paul's iPhone (11:08, "Reminders are on" arrived). Lesson: an iPhone Home Screen icon added before 10 Nov (no manifest then) silently refuses notifications; deleting and re-adding the icon fixed it (he then had to reset his password, as the new icon starts signed out). A safer switch (service worker ready before the tap, diagnostic code under errors, iPhone "delete and re-add the icon" hint) PUBLISHED 13 Nov (8be65ed). Feedback index and a 12-learner-per-family limit DONE 12 Nov (migration 0019, 1.3 credits; friendly message published 12 Nov).
**Scheduled (scheduled tasks)**
- Every night 02:57: morning suggestions for Lovable credits.
- Mon and Thu 07:47: this to-do reminder.
- 16 Nov: Quick start results · 18 Nov: Search Console "Pages" screenshot · 21 Nov: Loy Krathong · 5 Dec: ElevenLabs reset, Alphabet & Numbers · 12 Dec: colouring sheets + Christmas · 5 Jan: back-burner ideas (holiday packs, invite a family, schools and clubs) · 6 Jan: "Say it" on iPhone/iPad · 15 Mar: Songkran.

## Social media and community messages (Paul, 14 Nov 2026; applies to EVERY post, comment and message to groups or moderators)
- **Language-specific groups or pages** (e.g. a Thai, French or Spanish learning group): mention that language first, then say the app also teaches the other languages.
- **General groups** (parenting, multilingual families, language learning in general): list all five languages (Thai, French, Spanish, Italian, English) without leaning on one.
- **Always lead with what's good and different about the app**, not with one piece of content (e.g. don't make a message about a single video): built for the whole family to learn together (one free family account, up to 12 learners, kids' mode, family goal, Play together, Kids teach the grown-ups), real native-speaker voices, short 5-minute lessons, games and printables, try a lesson with no sign-up, completely free with no ads, works on any phone, made by a dad in the UK.
- **Facebook and Instagram posts too:** all languages equally, no Thai focus.
- **Feature spotlight posts:** every so often (about every 1–2 weeks), add an update post about ONE exciting feature, either an existing one (e.g. Play together, Kids teach the grown-ups, family goal, kids' mode, printables, try-a-lesson, phone reminders) or something brand new. Paul still approves with "post".
- **Always include a link to the app** (use the tracked short link for the place: /rd Reddit, /fb Facebook, /ig Instagram, /em email, /in invites) **and a picture of all five mascots** (sawasdee-family `public/share/nongchang-share-5.png`, live at nongchang.co.uk/share/nongchang-share-5.png). Where a picture can't be attached (e.g. Reddit modmail), link to it.

## Brand kit (12 Nov 2026; Claude design system claude.ai/artifact/XMu91n1jb7zaQYrE8TJq6Z, read its project/README.md before making cards, posters or videos; design review at claude.ai/artifact/5imUmMWUfvryH4pQxZsRei)
- Use the app's colours for every new card, poster, GIF and video: temple teal #007767 (buttons, links), deep ink #123B37 (headings), mint paper #EEF5F0 (background), marigold #F2A024 (stars, highlights), lotus pink #E0507A (trim), soft mint #D3EFE7, cream #F6EFE0 (picture frames, ring #F3E2B0), sage grey #4F6B66 (small print). The dotted temple trim is teal, pink, marigold. Older cards used #127D6A and the first poster #1C8A7C; use the app colours from now on (reprint the poster with them next time).
- Fonts: Mitr (headings, buttons) and Sarabun (reading text, Thai words). Lines: "Learn a language together as a family" · "Free · no ads · works on any phone" · "made by a dad in the UK". List the languages as Thai, French, Spanish, Italian, English, but give them equal weight in posts.
- Link preview picture (all five mascots): sawasdee-family `public/share/nongchang-share-5.png`.

## Pictures and videos
- **Every animal must have the correct number of limbs for its species.** Elephants, bulls and other four-legged animals have exactly four legs and no hands or arms; birds have two legs and two wings; people have two arms and two legs. No extra, missing, merged or duplicated limbs.
- **What counts as a failure (Paul, 31 Oct 2026):** extra or missing limbs, or limbs merging into other objects. An animal using its legs or wings like arms (holding a book, waving, standing upright) is fine as long as it still has the right number of limbs — don't flag or redo pictures for that.
- Write this into every image or video prompt (ComfyUI, Gemini or any other tool), and check every generated picture or clip for it before using it. Redo anything that fails.
- The ComfyUI scripts add it automatically (`ANATOMY` in `tools/art/generate_unit_art_comfyui.py`, also used by `tools/video/generate_clips_comfyui.py`).

## Use cheaper models where they're good enough (Paul's request, 28 Oct 2026)
Hand work to a Sonnet or Haiku subagent (Agent tool with `model: "sonnet"` or `"haiku"`) whenever it doesn't need the main model's judgement. Give the subagent a complete, standalone brief: it starts with no context.
- **Haiku:** mechanical, step-by-step jobs, such as:
  - recording audio batches (generate, poll, download, split with `fetch_split.sh`, check the clip count);
  - polling a running Lovable message or ElevenLabs job;
  - file and format checks;
  - git housekeeping.
- **Sonnet:** content and checking work, such as:
  - drafting or proofreading lesson word lists and translations;
  - social captions and tags;
  - summarising Lovable code files;
  - content audits (missing audio, duplicate answers, emoji give-aways).
- **Keep in the main model:**
  - writing Lovable briefs and reviewing Lovable diffs for safety;
  - estimating and spending credits;
  - anything that publishes;
  - final checks of pictures and videos (the limb rule);
  - talking to Paul.

Don't delegate tiny tasks: a subagent costs a fresh start, so it only pays off for jobs of a few minutes or more.

## App code lives on GitHub now (since 30 Oct 2026)
The Lovable app is two-way synced with **jeeveswooster2006/sawasdee-family** (branch `main`).
- Make code changes there directly. Pushing to `main` updates Lovable's editor and preview within about a minute and costs no Lovable credits. Run `npx tsc --noEmit` and `npx vitest run` first.
  - The lockfile points at Lovable's private registry, so install with `npm install --no-package-lock --legacy-peer-deps --ignore-scripts --registry=https://registry.npmjs.org`, then `npm install --no-save @testing-library/dom`.
- Live only changes when Paul says "publish": then deploy with the Lovable tool (free).
- Database migrations or Lovable-only features (email, auth providers, secrets) may still need a Lovable message. Check first.

## Working with Paul (standing rules)
- Never publish anything (app deploy, moving `live.json`, or a live database change that isn't fixing something broken) until Paul says "publish".
- Never ask for or accept passwords, API keys or other credentials. Paul types secrets into the service himself.
- Paul uses a phone and prefers short, simple messages with explicit tap-by-tap steps. Lead with the outcome.
- Before spending Lovable credits, say the realistic cost first: actual cost runs 2–3× the gut estimate. Paul gets 5 credits a day. Prefer free GitHub changes.
- Lovable also edits the app (security scans etc.). Before publishing, review any new Lovable commits and migrations on `sawasdee-family` main: on 1 Nov a Lovable security fix revoked direct writes while the app still used them, and rejected Thai word ids.
- Pictures: only extra/missing limbs or limbs merging into objects count as failures (see the top of this file).
- The live database is Lovable Cloud project `e31b84f7-44c3-4a30-92e8-dc156d90824d`; check and change it with the Lovable `query_database` tool.
- Start new Claude Code sessions from `jeeveswooster2006/sawasdee-family` (app) and add this repo; the old `which-pet-shines` repo is unrelated and may be deleted.

## Morning suggestions for Lovable credits (Paul, 11 Nov 2026)
- A scheduled task runs every night at 02:57 UK ("Morning suggestions for Lovable credits"), after Paul's 5 daily Lovable credits refresh. It spends NO credits itself: it does the free checks (timer job errors in `net._http_response`, new feedback, new sign-ups and `signup_source`, live site up) and prepares up to 3 suggestions for using that day's credits, each with a realistic cost and risk, plus at most 2 free ideas. Paul answers "yes"/"no" (or the numbers) in that session in the morning, and only then is anything done.
- Suggestions only for things that genuinely need Lovable (database or auth investigation, security scans, Lovable-only features). Never busywork; "nothing worth spending credits on today" is a fine answer. Anything that can be done free on GitHub is done that way.
- Even after a "yes": migrations and settings changes only for the exact approved item; code changes go to the preview; publishing still needs "publish".
- The scheduled task was created without the Lovable connector (it couldn't be passed from the chat). If the morning message says the connector was missing, Paul needs to add Lovable to the scheduled task in the claude.ai scheduled tasks screen.

## Parked ideas (Paul, 1 Nov 2026)
Not started. Only pick these up when Paul asks.
- Maybe move the domain (nongchang.co.uk) and email to Cloudflare or Proton. Left for now.
- A "Sounds of French" / "Sounds of Spanish" track in the app, like Read Thai.
- Facebook posts that Paul publishes himself.
- **Alphabet & Numbers sections (Paul, 9 Nov; parked until ElevenLabs credits reset ~5 Dec, reminder set):** home-page tabs Lessons · Alphabet · Numbers for every language, never gating main lessons. Numbers: reuse the 20 recorded per language + ~10 more each (0, 16–19, 60–90, 1000) ≈ 300 credits. Alphabet: Thai = Read Thai; record ~26 letters each for fr/es/it/en ≈ 550 credits. **Code built 9 Nov (preview only; `extraTracksEnabled()` keeps it off the live site even when other things are published — Paul's instruction). Still to do after the reset: record the clips (ids in AGENTS.md of sawasdee-family), then switch it on.**

## Inactive accounts (Paul, 9 Nov 2026; switched on 10 Nov)
- Live and on (`INACTIVE_CLEANUP = "on"` in sawasdee-family `src/lib/features.ts`; set to "report" to pause). Rules: unconfirmed sign-ups deleted after 30 days (no email); no learning ever: 6 months unused; some learning: 12 months. Warning emails 2 months, 1 month and 2 days before, then an "account deleted" email; signing in or opening the app resets the clock. At most 10 deletions a day. Details in AGENTS.md of sawasdee-family.
- Daily timer: pg_cron job `inactive-accounts-daily` (04:23 UTC) POSTs to /api/public/inactive-accounts. It was made for free by copying the weekly-email job's command with the address swapped (same cron secret, never read out). If Lovable ever rotates the cron secret and this job starts getting 401s (check `net._http_response`), recreate it the same way from a weekly job.
- First test run 10 Nov: 33 accounts checked, nothing to do. The 6 unconfirmed sign-ups go when they reach 30 days old (late Nov/early Dec); first warnings about Feb 2027.

## Audit (10 Nov 2026)
- Full read-only audit run with four sub-agents (content, code health, security, front-end); the database access rules were checked directly. Nothing critical. Fixed and live 10 Nov: clean-up capped at 10 deletions per 24 hours and reading in pages, race-safe rate limits (strict for AI), quiz words checked on the server, no lesson/profile loading for signed-out visitors, delete account by emailed code for Google/Apple/Microsoft sign-ins, kids' mode Me screen with a "Grown-ups" sum in front of settings and profiles (AI buttons kept in kids' mode: Paul's choice). Details in AGENTS.md of sawasdee-family.
- Second round, published 10 Nov (evening): colour picture tab buttons (🎯 for Practice), "tap to hear" hint, about 120 hard-coded English strings translated, XP only for the first 25 sessions an hour / 80 a day, session-start and password-reset limits, old lesson sessions cleared after a month, page language tag, finger-sized front-page links.
- Checked, nothing to do: "you" formal/informal and "my name is" accepting the same typed answer is correct; a package scan (lockfile made in a scratch folder) found only developer-tool and low-severity issues.
- Done 10 Nov via Lovable (2.2 credits): leaked-password protection on; learners can no longer delete their own progress rows directly (migration 0017); owner index added. Lovable couldn't read the sign-in rate limits: Paul can check them in Lovable → More → Users → Auth settings (sign-in attempts should be at most 30 per 5 minutes). The friendly leaked-password message went live 11 Nov.
- Still open, needs outside help: pictures for the 12 Fun sayings units in th/fr/es/it (about 310 ElevenLabs credits each, after the reset). Watch: main content is 43.9 MB of the 50 MB limit.
- Roadmap built early and released 10 Nov (evening; Paul: "do all the parts that are all code", then "Do number 1" and "publish"): Memory match, Play together, Kids teach the grown-ups, Look after your mascot (kids' mode), Install as an app, an opt-in daily reminder EMAIL and Printables (flashcards, fridge words) are all LIVE. A "Games" button on the lesson map opens the menu (/play). Each has a switch in `NEW_FEATURES` (sawasdee-family `src/lib/features.ts`): set one to "preview" and publish to hide it again. Daily reminder timer: pg_cron job `daily-reminder` (16:07 and 17:07 UTC; the route only sends 17:00–17:59 London), made free by copying the weekly job; nobody had opted in at release. The Friday tasks for 14 Nov, 28 Nov and 5 Dec (install) are switched off; 21 Nov is now Loy Krathong only and 12 Dec is colouring sheets + Christmas only. These screens were tested by automated tests only (the preview needs a sign-in): if Paul reports a problem, hide that one feature first, then fix.
- Roadmap still to do (needs outside help or a decision): Loy Krathong special (Paul to choose the form now Stories are paused; a few ElevenLabs credits for words, about 310 for a picture; "post" for the social post; festival is 24 Nov); colouring sheets and Fun sayings pictures (ElevenLabs credits, after the reset about 5 Dec); Alphabet & Numbers recordings (same reset); Christmas material (Paul to choose how to use it); phone push reminders (a key Paul adds in Lovable plus a Lovable database change); "Say it" on iPhone/iPad (moved to January 2027); quick start results (16 Nov).

## Privacy and the ICO (9 Nov 2026)
- Privacy page at nongchang.co.uk/privacy (text in sawasdee-family `src/data/privacy.ts`, five languages). Update it whenever the app starts keeping something new, uses a new service, or the inactive-account timings change.
- ICO data protection fee: Paul did the ICO self-assessment on 9 Nov. No fee is needed while the app isn't trading (no income). If it ever earns money (ads, subscriptions, donations, sponsorship), remind Paul to retake the assessment at ico.org.uk.

## ElevenLabs
- Paul upgraded to the **Creator** plan (5 Nov 2026): about 121,000 credits a month. Voices: Thai `brM9iIbwDREZaWL8luun` (Anna), Spanish `GB7fZx4ubHWxbBE05abF` (Marina), French `ICk609TItINMseDpChFt` (Léa). A word costs about 5 credits and a sentence about 10–20.
- **Nong Chang's own voice:** `C98kHdjEdJfyY7tmFiT5` ("Nong Chang (baby elephant)", designed 6 Nov 2026, Paul picked it). Use it for the mascot speaking: Reels, greetings, "Talk to Nong Chang". Lesson words keep the native course voices.
- **Coco's voice (French mascot):** `cnC556Nwu8ld2zYCI7Tj` (designed). **Torito's voice (Spanish mascot):** `CPv3Zr3CQCqE4ZzuCgBP` (library voice "Lulu"; voice design kept blocking "cute, high" requests). French stories star Coco, Spanish stories star Torito, never Nong Chang.
- **Italian (live 6 Nov 2026):** lesson voice Alina `wOXFTxgu7FQDBb1dsL7I`; mascot **Lupo** the grey wolf cub (four legs, green-white-red neckerchief), `courses/it/art/mascot.png`. Italian stories (if made) star Lupo. Lesson pictures were made with ElevenLabs `gemini-3.1-flash-lite-image` and the Lupo reference (about 310 credits each); Whisper check uses `verify2.py` (knows `it-`).
- **Lupo's voice (Italian mascot):** `Z9LM7NBnQ8aOZKIXkd5S` (library voice "Carlotta - Fairy Princess", Paul picked it 6 Nov; designed voices didn't sound Italian).
- Reels are on the `originals` branch in `social/reels/` (the Thai one uses Nong Chang, French uses Coco, Spanish uses Torito, Italian uses Lupo).
- Record one word or sentence per generation (no batch splitting); see `tools/audio/README.md`.
- **Before ANY ElevenLabs generation, ask Paul for his current credit balance and say the cost (Paul, 13 Nov 2026).** The connector can't read the balance. Use ONE take per line (`generations_count: 1`) unless Paul asks for more; two takes doubles the cost. On 13 Nov the Loy Krathong voice lines cost about 600 credits (two takes each) when Paul had said only 461 were left; the last takes finished after the balance ran out, so they may have gone into overage.

## Email (set up 2 Nov 2026)
- News emails go through **Resend** (Claude connector) from `Nong Chang & Family <hello@news.nongchang.co.uk>`, replies to `info@nongchang.co.uk` (Fasthosts mailbox). Domain `news.nongchang.co.uk` is verified (EU region, no open/click tracking).
- DNS is at **Cloudflare**; the Cloudflare connector can edit records. Root mail (MX/SPF) stays with Fasthosts; don't touch it.
- App opt-in: "News emails" tick box at sign-up and switch in Me & settings (`news_emails` in user metadata). Before each send, copy only opted-in accounts to Resend; Resend handles unsubscribes.
- Sent so far: 2 Nov "sorry you couldn't get in" (one-off account help, 7 unconfirmed sign-ups) and "While you were away" broadcast to 26 existing users (segment "App users (Nov 2026)"). Future news emails go to opted-in users only.
- 7 Nov: asked the GoGo España Spanish Facebook group (info@gogoespana.com) for permission to post about the app; replies go to info@. If they agree, write a Spanish-focused post with Torito.
- 7 Nov: one-off welcome (service) email to a new Spanish sign-up. UK rule (PECR/ICO): "what's new" emails are marketing, so they go only to opted-in accounts; service emails (account help, one-off welcome, security, terms changes) are fine. Use the in-app news and social posts for everyone else.
- 7 Nov (evening): one-off service emails about the fixed sign-in emails: "one step left" to the 6 unconfirmed sign-ups and "Sign-in emails are fixed" to 26 confirmed account owners (not Paul's own accounts, member logins or the new Spanish sign-up). No more account emails to these people unless they ask.
- Paul approves every email ("send") before it goes out; send a test to info@ first. Hotmail/Outlook currently files our mail in Junk (new sender); Gmail delivers to Important. Keep subjects plain, no emoji.

## Facebook page (set up 4 Nov 2026)
- Page "Nong Chang" (Education) and Instagram **@nong_chang26** (Professional, linked to the page). Posts are scheduled through the **Metricool** connector (brand id 7865277, free plan: 20 posts/month). Instagram is connected with an Instagram login (connecting via Facebook didn't pick up the account).
- Paul approves every batch with "post" before anything is scheduled. Keep personal details out: "a dad in the UK" is the only personal line.
- Pictures and post texts live in `social/facebook/` (cards are made with the brand fonts Mitr/Sarabun; `nov-2026-posts.json` holds the November plan). Images are served from jsDelivr at the commit they were added in.
- November 2026: 16 posts scheduled to both Facebook and Instagram, weekdays 7pm UK, 5–26 Nov (4 spare). Metricool accepted all 16 on both networks, so one post to both seems to count once; check after the first ones publish. Instagram captions can't hold links, so the profile link matters. Weekly pattern: Mon Thai word, Tue French/Spanish word, Wed Read Thai letter, Thu family tip/question, Fri fun fact. Language content is proofread by a Sonnet subagent before scheduling.
- November Reels (scheduled 6 Nov, both networks, marked AI-generated): Sat 7 Nov 10am French with Coco, Sat 14 Nov Spanish with Torito, Sat 21 Nov Thai with Nong Chang. 19 of 20 November posts are now used; the last one is kept for Loy Krathong (Tue 24 Nov).
- December 2026 (scheduled 6 Nov, both networks): Tue 1 Dec 7pm Italian "Ciao" card (`fb-italian-hello.png`), Sat 5 Dec 10am Italian Reel with Lupo. All 20 December posts are now used: the other 18 (weekdays 7pm, 2–30 Dec, equal mix of the four languages, each card showing its own mascot) were scheduled 6 Nov from `social/facebook/dec-2026-posts.json`; cards are on the `originals` branch in `social/facebook/dec-2026/` (made with `tools/social/make_cards_dec.py`).

## Weekly family email (live 5 Nov 2026)
- First Sunday run checked (8 Nov): the 17:00 UTC call was skipped as outside the window, the 18:00 UTC call sent 1 email to 1 opted-in family, no failures.
- Goes out Sundays 18:00 London to opted-in adult account owners only (code: `src/lib/weekly-email*.ts` in sawasdee-family). Database timer: Lovable-managed pg_cron jobs `weekly-family-email-utc17` and `-utc18` POST to /api/public/weekly-email with the cron secret (set up by Lovable 5 Nov); the route ignores calls outside the window, and a family gets at most one per week.
- Needs the `RESEND_API_KEY` secret in Lovable (Paul adds it himself).
- When something important ships (e.g. a new language), add a line to `src/lib/whats-new.ts` so it appears in that week's email.

## App roadmap (Paul, 5 Nov 2026)
Build in this order. Each one is free on GitHub, shown in the preview, and only published when Paul says "publish".
- **Done (top three, live 5 Nov):** 1 Family goal (shared weekly points jar, reward on Sunday, in the weekly email) · 10 Share cards ("Mia learned 50 Thai words!" picture to share, with app link) · 5 Picture stories (short illustrated stories with native voices using learned words; limb rule applies to art).
- **UPDATE 10 Nov: items 2, 4, 6, 7 and 9 below (games, Kids teach, Look after Nong Chang, Install + email reminder, Printables without colouring sheets) were built and released early; see the Audit section. What follows is the original plan.** **Then one a week, released on Fridays so the app visibly improves each week (scheduled tasks build it that day; Paul still says "publish"):** 14 Nov evening: 2 Play together (pass-the-phone quiz) + Memory match game · 21 Nov afternoon: 4 Kids teach the grown-ups + Loy Krathong special (festival Tue 24 Nov; story, words, social post) · 28 Nov evening: 6 Look after Nong Chang (feed/outfits), **kids' mode only** · 5 Dec afternoon: 7 Install as an app + daily reminder (Lovable's 7 Nov plan, `.lovable/plan.md` in sawasdee-family: install needs nothing new; phone reminders need web push keys, the private one added by Paul as a Lovable secret, plus a subscriptions table and hourly timer set up through Lovable, Workers-safe push library, iPhone only when installed on iOS 16.4+; a daily email reminder via Resend is the simpler option, so ask Paul which first) · 12 Dec evening: 9 Printables (flashcards, fridge words, colouring sheets) + Christmas for France, Spain and Italy (story material made 6 Nov: `tools/content/christmas-stories.json`; stories are paused, so ask Paul how to use it). Songkran special: reminder 15 Mar 2027. Build each one only on its Friday, so a publish never ships next week's feature early.
- **Back burner, reminder 5 Jan 2027:** 8 Holiday packs · 11 Invite a family · 12 Schools and clubs.
- **No:** grandparent link; "Talk to Nong Chang" (dropped 6 Nov: too costly to run, and Paul may lower his ElevenLabs tier after November).
- **"Why was I wrong?" AI hints** (Paul picked it 7 Nov, built free on GitHub, live 7 Nov, Paul tested it): a tap-to-ask button on wrong answers; each hint uses Lovable AI credits (4 free a month, then daily, then monthly credits; never billed to card; when out, the app says hints are resting).
- **Fun sayings (live 8 Nov):** 3 bonus idiom units per language (`fun1-3`, `es-/fr-/it-fun1-3`; 7 idioms each, 84 total) at the end of Beginner, Elementary and Intermediate. Bonus units never block the main path (app: `bonus: true`). Source `tools/content/fun-sayings.json`, inserted with `tools/content/insert_fun_sayings.py`; recorded one per generation with the course voices and Whisper-checked. Live at content commit d6c8da6 (live.json moved 8 Nov; all 1,937 content files returned 200). Main is now about 46 MB of the 50 MB jsDelivr limit.
- **Stories paused (Paul, 7 Nov):** "almost just a listening exercise". Hidden with `STORIES_ENABLED = false` in `src/lib/features.ts` (sawasdee-family); code, story data and recordings kept. Don't add new stories unless Paul brings them back.
- **Italian stories** (it-hello, it-hungry, it-colours with Lupo, read by Alina): live 6 Nov.
- **Travel video** (all four mascots meet; Kling 3 Pro, about 43,000 ElevenLabs credits): `social/reels/reel-travel-friends.mp4` on the `originals` branch; Paul uploads it himself (6 Nov).
- **Classroom video** (owl teacher; each mascot says "I'm ..., nice to be your friend" in their own language; Kling 3 Pro, about 28,000 ElevenLabs credits): `social/reels/reel-classroom-friends.mp4` on the `originals` branch; owl voice `BBfN7Spa3cqLPH1xAS22`. Paul uploads it himself (6 Nov).
- Mark items done here as they ship.

## English course (live 8 Nov 2026, content 178723172f26637d7b3e5e254e55e9845e4733f3)
- Mascot **Leo** the lion cub (St George neckerchief), voice Alice (British). Content lives on the `english` branch; courses.json `base` points at its commit.
- Leo unit pictures: all 46 units done 8 Nov (ElevenLabs gemini-3.1-flash-lite-image with the Leo reference, ~309 credits each, ~14,200 in total, limb-checked; scenes in `courses/en/art/unit_illustrations.json`). Paul chose these over Perchance (no reference picture, no API). ElevenLabs credits are nearly used up until the monthly reset.
- Preview and live share one database: switching a learner to English in the preview makes the live app show "We couldn't load your lessons" for that learner until English is published (happened to Paul's "Dad" on 8 Nov). Test English on a spare learner.

## Repo size (5 Nov 2026)
- jsDelivr serves content only reliably while the repo is under 50 MB per commit. Over that, files randomly return 403 until purged, so pictures and sounds go missing.
- Full-size source pictures (`courses/*/art/originals/`) and social video clips (`social/clips/`) were moved off `main` to the **`originals`** branch. Keep big source files there, not on main.
- If main nears 50 MB again (about the 4th–5th language, ~10–15 MB each), move content to Cloudflare R2 (free to 10 GB, no download fees, e.g. content.nongchang.co.uk) or one repo per language; tell Paul first.
- After moving `live.json`, request every content file at the new commit and purge any non-200 (`https://purge.jsdelivr.net/gh/jeeveswooster2006/sawasdee-thai@<commit>/<path>`).

## Marketing tracking (built 5 Nov 2026)
- **Cloudflare Web Analytics** (free, no cookies) runs on nongchang.co.uk through a script in the app. The domain isn't proxied through Cloudflare (Lovable hosts it), so don't turn on the orange cloud. See visits in Cloudflare → Analytics & Logs → Web Analytics.
- **Short links:** nongchang.co.uk/fb, /ig, /rd (Reddit) and /em (email) remember the source. New accounts get `signup_source` in user metadata. Count them with `select raw_user_meta_data->>'signup_source', count(*) from auth.users group by 1`.
- Use /fb in Facebook posts, /ig in the Instagram bio, /rd on Reddit and /em in emails.

## Growth audit (10 Nov 2026)
- Full read-only audit published as a Claude artifact ("Nong Chang Growth Audit"). Main finding: the app is good but few people find it (1 sign-up a week, 10 Google visits a month, social pages have 9 followers in total). Focus on acquisition, not new features.
- Paul's decisions on the five opportunities: (1) Search Console is set up, sitemap read 9 Nov (19 URLs); SEO fixes live 11 Nov. Reminder set for 18 Nov to ask Paul for a screenshot of the Search Console "Pages" report. (2) "Try a lesson" with no sign-up: LIVE 11 Nov (nongchang.co.uk/try; links use ?course=xx, never ?lang=, which sets the screen language). Played through on the live site at phone size. Count visits to /try in Lovable analytics. (3) Paul posts in community groups himself; don't schedule more page posts for January unless asked. (4) Lead with Thai families (see top). (5) Website line on flashcards/fridge sheets and guide-page footer live 11 Nov. A4 poster: Paul picked B (Thai first, English underneath), 11 Nov. Print-ready PDF and its HTML source are on the `originals` branch in `social/print/` (nong-chang-poster-A4.pdf); the QR code was checked to scan to nongchang.co.uk/qr (source "poster", opens /try?course=th). 7-day family challenge: left for now (Family goal covers most of it).
- Published 11 Nov (Paul: "Publish"): content fixes from the audit's proofreading (live.json → 35b33d6; English `base` → ff8368b; all 2,364 content files returned 200), SEO fixes (titles, Coco the cockerel, structured data), the /in invite link and the friendly leaked-password message. Native-speaker questions (vous/tú formality, Gentili Signori, "Spare the rod", etc.) are listed in the audit for Paul.
- "Invite a friend" shares now use the short link /in (signup_source "invite").
- 11 Nov: Lovable security and database health check (plan mode, 1.8 credits): no critical, high or medium findings; report saved in sawasdee-family `.lovable/`. Low items: optional index on feedback.learner_profile_id; the date-only family XP read (fixed in app code). "Say it" on iPhone/iPad moved to January 2027 (Paul: few use it). Sign-up by code LIVE 11 Nov; Paul tested it on the live site (code arrived, Confirm worked), and also confirmed delete-account and the leaked-password message work.
- 11 Nov (afternoon, Paul: "B and publish"): front page option B LIVE (five mascots, each opening that language's taster lesson, Thai biggest; Google first and the email form folded away on phones). New guide pages LIVE: French/Spanish/Italian phrases for travel and English for kids (meanings in Thai, French, Spanish, Italian).
- Budget: Paul said about £10 a month; Lovable Pro + ElevenLabs Creator is roughly £35–40. Plan: downgrade ElevenLabs after the December recording batch.

