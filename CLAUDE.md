# Rules for this project (Nong Chang & Family)

## Mix the languages (Paul, 5 Nov 2026)
- The app started Thai-only, but French and Spanish likely bring more interest. Give French, Spanish and (since 6 Nov) Italian an equal share in marketing (social posts, emails, Reddit), and in new features and content (stories, festival specials, games). Don't default to Thai-only.

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

## Parked ideas (Paul, 1 Nov 2026)
Not started. Only pick these up when Paul asks.
- Maybe move the domain (nongchang.co.uk) and email to Cloudflare or Proton. Left for now.
- A "Sounds of French" / "Sounds of Spanish" track in the app, like Read Thai.
- Facebook posts that Paul publishes himself.
- **Alphabet & Numbers sections (Paul, 9 Nov; parked until ElevenLabs credits reset ~5 Dec, reminder set):** home-page tabs Lessons · Alphabet · Numbers for every language, never gating main lessons. Numbers: reuse the 20 recorded per language + ~10 more each (0, 16–19, 60–90, 1000) ≈ 300 credits. Alphabet: Thai = Read Thai; record ~26 letters each for fr/es/it/en ≈ 550 credits.

## ElevenLabs
- Paul upgraded to the **Creator** plan (5 Nov 2026): about 121,000 credits a month. Voices: Thai `brM9iIbwDREZaWL8luun` (Anna), Spanish `GB7fZx4ubHWxbBE05abF` (Marina), French `ICk609TItINMseDpChFt` (Léa). A word costs about 5 credits and a sentence about 10–20.
- **Nong Chang's own voice:** `C98kHdjEdJfyY7tmFiT5` ("Nong Chang (baby elephant)", designed 6 Nov 2026, Paul picked it). Use it for the mascot speaking: Reels, greetings, "Talk to Nong Chang". Lesson words keep the native course voices.
- **Coco's voice (French mascot):** `cnC556Nwu8ld2zYCI7Tj` (designed). **Torito's voice (Spanish mascot):** `CPv3Zr3CQCqE4ZzuCgBP` (library voice "Lulu"; voice design kept blocking "cute, high" requests). French stories star Coco, Spanish stories star Torito, never Nong Chang.
- **Italian (live 6 Nov 2026):** lesson voice Alina `wOXFTxgu7FQDBb1dsL7I`; mascot **Lupo** the grey wolf cub (four legs, green-white-red neckerchief), `courses/it/art/mascot.png`. Italian stories (if made) star Lupo. Lesson pictures were made with ElevenLabs `gemini-3.1-flash-lite-image` and the Lupo reference (about 310 credits each); Whisper check uses `verify2.py` (knows `it-`).
- **Lupo's voice (Italian mascot):** `Z9LM7NBnQ8aOZKIXkd5S` (library voice "Carlotta - Fairy Princess", Paul picked it 6 Nov; designed voices didn't sound Italian).
- Reels are on the `originals` branch in `social/reels/` (the Thai one uses Nong Chang, French uses Coco, Spanish uses Torito, Italian uses Lupo).
- Record one word or sentence per generation (no batch splitting); see `tools/audio/README.md`.

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
- Goes out Sundays 18:00 London to opted-in adult account owners only (code: `src/lib/weekly-email*.ts` in sawasdee-family). Database timer: Lovable-managed pg_cron jobs `weekly-family-email-utc17` and `-utc18` POST to /api/public/weekly-email with the cron secret (set up by Lovable 5 Nov); the route ignores calls outside the window, and a family gets at most one per week.
- Needs the `RESEND_API_KEY` secret in Lovable (Paul adds it himself).
- When something important ships (e.g. a new language), add a line to `src/lib/whats-new.ts` so it appears in that week's email.

## App roadmap (Paul, 5 Nov 2026)
Build in this order. Each one is free on GitHub, shown in the preview, and only published when Paul says "publish".
- **Done (top three, live 5 Nov):** 1 Family goal (shared weekly points jar, reward on Sunday, in the weekly email) · 10 Share cards ("Mia learned 50 Thai words!" picture to share, with app link) · 5 Picture stories (short illustrated stories with native voices using learned words; limb rule applies to art).
- **Then one a week, released on Fridays so the app visibly improves each week (scheduled tasks build it that day; Paul still says "publish"):** 14 Nov evening: 2 Play together (pass-the-phone quiz) + Memory match game · 21 Nov afternoon: 4 Kids teach the grown-ups + Loy Krathong special (festival Tue 24 Nov; story, words, social post) · 28 Nov evening: 6 Look after Nong Chang (feed/outfits), **kids' mode only** · 5 Dec afternoon: 7 Install as an app + daily reminder (Lovable's 7 Nov plan, `.lovable/plan.md` in sawasdee-family: install needs nothing new; phone reminders need web push keys, the private one added by Paul as a Lovable secret, plus a subscriptions table and hourly timer set up through Lovable, Workers-safe push library, iPhone only when installed on iOS 16.4+; a daily email reminder via Resend is the simpler option, so ask Paul which first) · 12 Dec evening: 9 Printables (flashcards, fridge words, colouring sheets) + Christmas for France, Spain and Italy (story material made 6 Nov: `tools/content/christmas-stories.json`; stories are paused, so ask Paul how to use it). Songkran special: reminder 15 Mar 2027. Build each one only on its Friday, so a publish never ships next week's feature early.
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
