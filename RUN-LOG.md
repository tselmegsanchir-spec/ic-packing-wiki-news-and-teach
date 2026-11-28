# RUN-LOG — one real execution (2026-11-20 to 2026-11-21)

Input: 7 newsletter issues (2026-11-12 to 2026-11-20) read from Gmail (read-only). Output: wiki (7 source pages, 20 synthesized pages), `index.html` (EN + MN in one page with a language switch), `graph.html`.

## Node-by-node record
| # | Node | Gate / check | Result on first run | What I did | Result after |
|---|---|---|---|---|---|
| 1 | Read mail | tool output size | each message exceeded the tool limit (about 100k characters) | read the saved JSON files with a script instead of printing | 7 of 7 issues read |
| 2 | Clean to raw/ | grep for e-mail address and tokens | footer with the owner's address and tracking ids still present | cut text at the footer line, replaced address with `[redacted]` | grep finds 0 matches |
| 3 | Extract items | item count | I reported 83 unique items | found a "MORE TECH PAPERS" link counted as an item; recount = 91 items, 82 unique; moved ID assignment into `extract_items.py` | 82; rerun gives identical `items.json` |
| 4 | Tier + notes | manual | none | wrote own-word paraphrase and tier for each unique item (`notes.json`) | 82 notes |
| 5 | Wiki pages | link check | none | 20 pages written append-only with `[ID, date]` on every fact | 0 broken links |
| 6 | Lint gate (4 checks) | uncited, conflicts, outdated, orphans | 2 failures: `ai-accelerator-architecture` and `co-packaged-optics` had no inbound link | added Related links | 0 failures |
| 7 | Outline (human) | owner approval | approved a 9-slide method deck | later the owner said this was not the daily briefing they wanted | returned to Pick stories; built reader briefing instead |
| 8 | Faithfulness (slides) | numbers and names must appear in the cited card | 1 failure: `Taiwan's` vs `Taiwan` | false alarm from possessive; fixed the normalisation, did not loosen the rule | 0 failures |
| 9 | Faithfulness (briefing) | same | 0 failures on first run | none | 0 |
| 10 | Consistency (MN vs EN) | digits and Latin names must match | 12 flags like `HBM-` | false alarm: Mongolian suffix attached by a hyphen; fixed the regex | 0 failures |
| 11 | Render gate | overflow, broken images and links, anchors, stats, phone 390 px and desktop 1280 px | passed with 0 failures but screenshots showed 0 in every tier-count tile; later a diagram label overflowed; later the phone header was unreadable on the bright background | added a numeric assertion (tile values must equal values computed from the data); shortened label; added a dark panel behind the header; later fixed a selector that counted lesson cards as news cards | 0 failures, screenshots checked |
| 12 | Deliver | files written to the owner's folder | none | 55 files then updates | all written |

## Wiki to briefing correspondence (examples)
| Card or lesson part | Cited IDs | Wiki pages |
|---|---|---|
| Samsung hybrid bonding | SPN-1112-01, SPN-1116-03, SPN-1120-03 | `concepts/chiplets-and-hybrid-bonding`, `ic-design-link/packaging-aware-design` |
| AI agents in chip design | SPN-1113-10, SPN-1117-01, SPN-1119-10, SPN-1112-11 | `concepts/ai-in-chip-design`, `ic-design-link/ai-agents-in-eda` |
| Memory wall | SPN-1113-02, SPN-1113-09, SPN-1118-05, SPN-1117-07 | `concepts/hbm-and-memory-wall`, `ic-design-link/memory-aware-architecture` |
| Packaging capacity | SPN-1120-01, SPN-1116-02, SPN-1119-01 | `concepts/advanced-packaging-capacity`, `companies/ase-spil` |
| Capacity and wafers | SPN-1117-02, SPN-1120-06 | `concepts/foundry-capacity-and-nodes` |
| Export rules | SPN-1117-06, SPN-1120-04, SPN-1119-05 | `concepts/export-controls`, `events/export-rule-tightening-2026-11` |
| Nvidia | SPN-1120-07, SPN-1116-08 | `companies/nvidia`, `events/nvidia-leadership-change-2026-11` |
| TSMC (conflicting amounts) | SPN-1112-08, SPN-1112-09, SPN-1120-02 | `events/tsmc-ai-investments-2026-11`, `open-questions` |
| Lesson part, 7 terms | no news IDs (background teaching, labelled) | each term names its wiki page |

## Honest limits of this run
- One execution only; the numbers above are from that run.
- Faithfulness checks numbers and names, not verbs or meaning; the Mongolian meaning is not machine-verified.
- Linked outlet articles were not reachable, so facts rest on newsletter blurbs.

## Refresh run (2026-11-28) — second execution, same graph
Trigger: owner asked to continue and refresh. Reading: Gmail, `from:` the newsletter after 2026-11-20 → 4 threads; 1 already ingested (11-20), so 3 new issues: 2026-11-23, 11-24, 11-25 (none on 11-26/27, Thanksgiving break). The owner waived the outline checkpoint for this run ("do everything and report"), so the outline was not approved before generation; the card list is shown in the hand-over message instead.

| Node | Check | Result |
|---|---|---|
| Read mail / Clean | no e-mail address or tracking tokens in `raw/` | grep clean; footer and sponsor blocks cut by hand (raw written directly because tool output cannot be piped to disk) |
| Extract items | old IDs unchanged | 130 items, 120 unique; the 82 old IDs identical; 1 repeat (EOTPR paper) marked |
| Tier + notes | 38 new own-word notes | 120 notes |
| Wiki pages | append only; 3 source pages, 14 pages appended, glossary +6 terms, Conflict 4 (Nvidia CEO resigned vs removed then reinstated) | lint: 0 failures |
| Faithfulness | first pass 4 false alarms: sentence-initial words ("Earlier", "Analysts", "Earlier reports") not in the evidence | reworded so each sentence starts with a name from the evidence; second pass 0 |
| Consistency (MN) | numbers and names equal to EN | 0 failures on first pass; I then fixed 3 wording errors by reading (rare-earth, spy, derivative) that no script can catch |
| Render gate | 390 and 1280 px, EN and MN, 8 visible cards each, no overflow, anchors | 0 failures |

New problem found in this run: `gen_sources.py` had a hard-coded `updated: 2026-11-20`; changed to the issue date. The lexical faithfulness check again could not see meaning, so the Mongolian text still needs a human read.
