# 2 weeks — log (newest at the top)

## 2026-10-23 04:23 — Standby 09 (daily updater + history backfill)
- Daily updater `scripts/update_daily.py` (claude -p, search+fetch only, empty cwd, API key refused; page quote re-fetched and checked; only high-confidence verified PROMISES go live, everything else to gitignored `reference/review.json`). Laptop launchd job `com.purpledaddy.twoweeks.updater`, 02:30 daily; logs `~/Library/Logs/TwoWeeksUpdater/`. First real dry run found 6 (5 verified).
- History backfill (2013-2016, 2020-2022, 2023-2026 researched by read-only subagents; `scripts/verify_backfill.py` checks every quote against the live page and needs a second source for the outcome): 7 items live (34 promises now), 22 in the review file (confidence medium or an outcome page that did not verify). 2017-2019 was not researched (the agent launch was refused by the safety check; not retried).
- New status "kept" (delivered on time). `src` field = a "source" link on each auto-added entry.

## 2026-10-23 04:00 — Standby 09 (build + publish)
- Built from the claude.ai artifact (K25cArtxd91fWoBzAe4N9Z): data moved to `data/*.json`, page to `site/template.html`, `scripts/build.py` makes
  `docs/index.html`. Fixes on the way: the phone layout was 1450 px wide (the nowrap Looks strip stretched the grid; `min-width:0`), stored look/tab
  values are validated, a strict CSP (one script pinned by SHA-256, no network except Google Fonts CSS), noscript note.
- Review (Sonnet, security + correctness): CSP/escaping clean. Fixed: Museum look's selected tab/chip were invisible; day counts now use calendar days
  (no noon/DST flip); a pending promise past its date counts as missed; "1 day" plural; Receipt label; real-date validation in build.py;
  controls no longer pinned on phones; three Sketchy "why" lines reworded to what could actually be sourced. Not done: self-hosting the fonts (visitors'
  IPs reach Google Fonts; low) and full tab keyboard navigation (BACKLOG).
- Tested in a browser at 375 and 720 px: no horizontal overflow on any of the 15 looks, both tabs, no JS errors.
