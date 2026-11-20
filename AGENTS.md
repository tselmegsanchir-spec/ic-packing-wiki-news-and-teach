# AGENTS.md — IC-Packaging Wiki (rules for any AI agent working in this repo)

## 1. Purpose and reader
- Reader: ONE person, an EECS student in Taiwan, semiconductor beginner, goal = IC designer.
- Problem solved: the daily newsletter "Semiconductor Packaging News" (SPN) is long, ad-heavy and packaging-centric. This wiki turns it into a small, cited, growing knowledge base, then into a short HTML briefing (3–5 min read) that explains IC-design-relevant news from the basics.
- Lens: "packaging-aware IC designer". Tier 1 = IC design (EDA, RTL, verification, physical design, IP, AI accelerator architecture, chiplets/3D integration as they change design). Tier 2 = process, packaging, memory, foundry capacity (brief). Tier 3 = market/geopolitics (one line).

## 2. Folder map
- `raw/` — immutable cleaned newsletter text. PRIVATE (git-ignored, never published, never edited by the agent).
- `wiki/sources/` — one page per newsletter issue (`spn-YYYY-MM-DD.md`) with numbered items.
- `wiki/concepts/`, `wiki/companies/`, `wiki/events/`, `wiki/ic-design-link/` — synthesized pages.
- `wiki/glossary.md` — terms (English; short Mongolian gloss allowed).
- `wiki/open-questions.md` — conflicts, gaps, things to verify.
- `index.md` (catalog), `log.md` (append-only change log), `DECISIONS.md` (human decisions and AI dissatisfactions), `README.md` (for humans).
- `tools/` — small scripts. `outputs/` — generated HTML.

## 3. Language
- Wiki pages: English. Glossary entries may add a Mongolian gloss in parentheses.
- Briefing HTML: v1 English (for the teacher). The owner translates/regenerates the Mongolian version later from the same wiki; keep technical terms in English.

## 4. Page format
Every wiki page starts with front matter:
```
---
title: ...
type: source | concept | company | event | ic-link | glossary
tier: 1 | 2 | 3
updated: YYYY-MM-DD
sources: [SPN-1119-01, ...]
---
```
Then: a 1–2 line summary, details, a "Related" list with `[[page-name]]` links (every page links to at least one other page and is linked from index.md).

## 5. Citation rule (hard rule)
- Every factual sentence ends with `[ITEM-ID, YYYY-MM-DD]`, e.g. `[SPN-1119-01, 2026-11-19]`.
- ITEM-ID = `SPN-MMDD-NN`: issue date + item number on that issue's source page.
- Interpretation or beginner explanation that is NOT in a source must be labeled `(Explainer)` for background knowledge or `(AI hypothesis)` for outlook. Never mix these into factual sentences.
- Source of truth for a claim is the newsletter blurb plus the linked outlet named on the source page. The agent only knows what the blurb says; it must not add numbers, names or causes that the blurb does not state.

## 6. Ingest workflow (one issue)
1. Read the issue from the Gmail connector (READ-ONLY; never send, delete, label or modify mail).
2. Save cleaned text to `raw/`: strip sponsor blocks, ads, quiz/cartoon, footer, e-mail address and tracking tokens.
3. Create `wiki/sources/spn-YYYY-MM-DD.md`: numbered items with title, outlet, URL, one-line paraphrase (own words), tier.
4. Update (append, never overwrite) concept/company/event pages; add new glossary terms.
5. Duplicate check: an item already seen in an earlier issue is marked `repeat of <ID>` and not counted again.
6. Conflict check: if two sources disagree, record BOTH with citations and add an entry to `open-questions.md`. Do not pick a winner.
7. Update `index.md`, append to `log.md`.
- First two issues are ingested one at a time (review checkpoint); later issues in batch.

## 7. Briefing workflow (Graph; each node sees only its allowed input)
`select items → tier → evidence card → OUTLINE (human approves) → draft per card → faithfulness check → render → render check → deliver`
- Recency: items from the last 7 days get priority; older wiki facts may be used only with their date shown.
- Evidence card = item ID + claim + source. A draft sentence without a card is deleted.
- Faithfulness check (Loop, max 3 passes): every number, name and verb in the draft must appear in its evidence card. Fix or delete; after 3 failed passes, drop the card.
- Render check (Loop, max 3 passes): no text overflow, every slide has a citation line, every cited ID exists in wiki.
- AI outlook is allowed only in a box labeled "AI hypothesis (not a fact)".
- Human checkpoint exists only at the OUTLINE.

### Reader briefing format (the main product)
- Page order: Part 1 LESSON (7 terms from the news: one sentence, picture it, why a designer cares, seen in which card, wiki page) then 5-question quiz, then Part 2 NEWS. Lesson text is labelled background teaching; edit `tools/lesson.json` (+ `lesson_mn.json`).
- `index.html` = the daily reader briefing: 20-second summary, then cards. Each card: headline, "What happened" (facts with `[ID, date]`), "New to this?" (Explainer, IC-design cards), "AI take" box labeled hypothesis, optional "Heads up" box for logged conflicts.
- `graph.html` = the graph, the three loop questions and the design reasons (also `outputs/process-deck-en.html`, same file); `RUN-LOG.md` = execution record; `REFLECTION.md` = reflection.
- Gates: `faithfulness_briefing.py` and `render_check_briefing.py` (mobile 390 px and desktop 1280 px, no overflow, every card has a source).

## 7b. REFRESH procedure (exact steps when the owner says "refresh" / "шинэчил")
Requires: Python 3 with `playwright` (set env `CHROME_PATH` to a Chrome/Chromium exe if Playwright's own browser is not installed). Run commands from the repo root.
1. Fetch: with a Gmail connector, search `from:today@semiconductorpackagingnews.com newer_than:7d` and read each message as plain text, saving each JSON to a temp folder; then `python3 tools/ingest_raw.py <tempfolder> raw`. WITHOUT Gmail access: ask the owner to paste or save each issue as `raw/YYYY-MM-DD_x.txt` with the header lines `ISSUE:`, `DATE:`, `MSGID:`. Never write the owner's e-mail address into any file.
2. `python3 tools/extract_items.py` builds `tools/items.json` (IDs `SPN-MMDD-NN`, repeats marked). Skip issues already in `wiki/sources/`.
3. For every NEW item add `"ID": [tier, "own-words paraphrase"]` to `tools/notes.json` (tier 1/2/3 per section 1; never copy blurb wording), then `python3 tools/gen_sources.py`.
4. Update concept/company/event pages (append only), glossary, `open-questions.md` (log conflicts), `index.md`, `log.md`. Then `python3 tools/lint.py` must print 0 failures.
5. Briefing: choose 6-8 stories, last 7 days weighted first. Edit `tools/briefing.json` (cards: head, topic, happened[{t,c:[IDs]}], basics, ai, optional flag). Show the owner the OUTLINE (card headlines) and wait for approval.
6. After approval run `python3 tools/faithfulness_briefing.py` (fix until 0), write `tools/briefing_mn.json` with the same structure and card order, run `python3 tools/consistency_mn.py`, then `python3 tools/render_briefing.py` (builds ONE index.html containing both languages with an EN/МН switch), then `python3 tools/render_check_briefing.py index.html` (checks both languages at 390 and 1280 px). Look at screenshots (`/tmp/*.png`) before delivering.
7. Deliver `index.html` (one page, EN/МН switch; `?lang=mn` opens Mongolian), `index-mn.html` (redirect only), and `assets/`. Do not publish `raw/`.
Known limits: linked outlet articles are usually not fetchable, so facts rest on newsletter blurbs; say so.

## 8. Lint (run before generating slides)
1. Uncited statements: factual sentence without `[ID, date]`.
2. Conflicting sources not logged in `open-questions.md`.
3. Outdated information: facts older than 30 days flagged "check for update".
4. Orphan pages: not linked from index.md or by any other page.
Run `python3 tools/lint.py`; fix failures before delivering.

## 9. Forbidden
- Inventing facts, numbers, quotes; filling gaps from memory in factual sentences.
- Using sponsor ads, paid press releases ("Industry Press") or the quiz/cartoon as evidence.
- Publishing `raw/`, e-mail address, tokens, API keys, or any personal data. No localhost links in outputs.
- Sending, deleting or modifying e-mail.
- Repeating personal-scandal details about named people; keep to business impact only.
- Editing existing wiki text to hide an earlier mistake; corrections are appended and logged.

## 10. Style for outputs
Short cards, plain words, one idea per card, define each term the first time. IC-design items get a "Basics" line (Explainer) before the news line.
