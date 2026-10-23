# 2 weeks — log (newest at the top)

## 2026-10-23 04:00 — Standby 09 (build + publish)
- Built from the claude.ai artifact (K25cArtxd91fWoBzAe4N9Z): data moved to `data/*.json`, page to `site/template.html`, `scripts/build.py` makes
  `docs/index.html`. Fixes on the way: the phone layout was 1450 px wide (the nowrap Looks strip stretched the grid; `min-width:0`), stored look/tab
  values are validated, a strict CSP (one script pinned by SHA-256, no network except Google Fonts CSS), noscript note.
- Review (Sonnet, security + correctness): CSP/escaping clean. Fixed: Museum look's selected tab/chip were invisible; day counts now use calendar days
  (no noon/DST flip); a pending promise past its date counts as missed; "1 day" plural; Receipt label; real-date validation in build.py;
  controls no longer pinned on phones; three Sketchy "why" lines reworded to what could actually be sourced. Not done: self-hosting the fonts (visitors'
  IPs reach Google Fonts; low) and full tab keyboard navigation (BACKLOG).
- Tested in a browser at 375 and 720 px: no horizontal overflow on any of the 15 looks, both tabs, no JS errors.
