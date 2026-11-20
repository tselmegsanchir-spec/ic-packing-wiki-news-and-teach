# IC-Packaging Wiki and Briefing

A small LLM Wiki (Karpathy-style) built from the daily newsletter *Semiconductor Packaging News*, plus an HTML briefing generated from it.

- Open `index.html` (English) or `index-mn.html` (Mongolian): a lesson (7 terms and a quiz) followed by the news. `graph.html` shows the graph and loop design for the teacher; `RUN-LOG.md` is the execution record; `REFLECTION.md` is the reflection.
- `wiki/` holds the pages, `index.md` is the catalog, `log.md` the change log, `AGENTS.md` the rules, `DECISIONS.md` the decisions, `REFLECTION.md` the reflection.
- `assets/` holds the background images and icons (made from the owner's own generated images); upload it with `index.html`. The three large original `Gemini_Generated_Image_*.jpg` files are not needed online.
- `raw/` (cleaned newsletter text) is private and is not in this repo.
- Quality gates: `python3 tools/lint.py` (wiki lint), `python3 tools/faithfulness_briefing.py` and `python3 tools/render_check_briefing.py` (need the private items file to rebuild).
- Contains no API keys and no personal data.

## Publish on GitHub Pages
1. Create a new empty public repo (no README, no .gitignore).
2. Upload or push all files in this folder (`raw/` is excluded by `.gitignore`).
3. Settings, Pages, Deploy from branch `main`, folder `/ (root)`.
4. Open the Pages URL in an Incognito window and check every slide.
