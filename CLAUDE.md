# 2 weeks

A public site tracking Elon Musk's dated promises (deadline vs what happened) plus a "Sketchy" tab for Tesla / Tesla AI /
Tesla North America claims. Static page on GitHub Pages, hand-curated data, counters computed in the reader's browser.

House rules: `~/VibeCodingisFun/CLAUDE.md`. Read `coordination/STATUS.md` first, then the top of `coordination/LOG.md`.

## Layout
```
data/promises.json, data/sketchy.json   THE content. Edit these (or `scripts/add.py`).
site/template.html                      the page (look picker, 15 looks, all CSS/JS). No data inside.
scripts/build.py                        validates data, inlines it, pins the one script in the CSP by SHA-256 -> docs/index.html
scripts/add.py / publish.sh             add an entry; rebuild + commit + push
docs/                                   the BUILT site served by GitHub Pages (never edit by hand)
coordination/ release-notes/            project docs (outside docs/ so they are not served)
```
## Rules
- Public repo: no secrets, no private data, ever. Content is public posts only.
- After any change to `data/` or `site/`: `python3 scripts/build.py`, then `bash scripts/publish.sh "message"`.
- Text from posts is only ever inserted escaped (`esc()`); never use innerHTML with raw data. The CSP allows exactly one script.
- Free only. No paid API, no purchase (a custom domain is an option for Jay, not something a chat buys).
- Add a release note in `release-notes/` for each visible change.
