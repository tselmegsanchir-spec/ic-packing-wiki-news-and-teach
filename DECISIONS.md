# DECISIONS.md — key decisions and dissatisfactions with AI output

## Who it is for and what problem it solves
One EECS student in Taiwan who wants to become an IC designer and is new to semiconductors. The daily newsletter is long, ad-heavy and packaging-centric; the wiki and briefing turn it into short, cited, beginner-friendly cards.

## Decisions (human)
| # | Decision | Why |
|---|---|---|
| 1 | Topic = daily "Semiconductor Packaging News" in Gmail | Real, recurring data the owner already receives |
| 2 | Lens = "packaging-aware IC designer", three tiers | Owner's career goal; keeps IC-design items deepest |
| 3 | Citations on every sentence as `[ID, date]` | Makes faithfulness checkable by script |
| 4 | Conflicts: record both, log in open-questions | Avoids the AI silently picking a winner |
| 5 | Ingest: first 2 issues one by one, then batch | Check quality before scaling |
| 6 | No daily automation; refresh on request, weight last 7 days | Owner's simpler idea replaced the AI's schedule plan |
| 7 | Build English HTML first for the teacher; owner makes the Mongolian version later from the same wiki | Teacher cannot read Mongolian |
| 8 | Human checkpoint only at the outline | Matches the course Graph pattern |

## Dissatisfactions with AI output and what changed
1. AI proposed a 5-day schedule and a daily-automation design that the owner found confusing. Owner replaced it with on-demand refresh.
2. Interview: the owner skipped two questions (lint, deadline); the AI first assumed answers, then re-asked them. Lesson: do not treat a skipped answer as consent.
3. AI first reported "83 unique items"; the real count after removing repeats was 82 (a "MORE TECH PAPERS" link had been counted). Fixed in index, log and slides.
4. The first rendered stats slide showed 0 for all tier counts (a type bug: JSON integers vs string keys). My overflow check passed it; only looking at screenshots caught it. Added a stats check to `render_check.py`.
5. The diagram label "OUTLINE (human OK)" overflowed its box; shortened.
6. Lint found 2 orphan pages on the first run; added links.
7. Linked outlet articles could not be fetched (network allowlist), so the wiki rests on newsletter blurbs only. Not hidden: stated on the last slide and in open-questions.
8. Scope choice: personal-scandal details about a named person are left out; only business impact is recorded.
9. Open assumption: deadline assumed 3-5 days; whether newsletter issues count as "sources" for the grader is unconfirmed (ask the teacher/TA).
10. AI misread the request: it first built a method deck (Graph diagram, gates) and called it the briefing. The owner wanted a short, interesting daily read: what happened, why it matters, AI take. Fixed: `index.html` is now the reader briefing; the method deck moved to `outputs/process-deck-en.html` for the teacher. Lesson: the product is what the reader opens every morning, not the explanation of how it was made.
