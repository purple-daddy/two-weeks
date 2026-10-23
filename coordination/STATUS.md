# 2 weeks — status (start here)
Updated: 2026-10-23 04:00 by Standby 09 ("2 weeks · own public URL")

- **Live (2026-10-23):** https://purple-daddy.github.io/two-weeks/ (GitHub Pages from `docs/` on `main`; not on Tailscale). 27 promises + 11 sketchy claims.
- **Updates:** daily updater (laptop launchd `com.purpledaddy.twoweeks.updater`, 02:30) adds verified items; review file for the rest; hand-curated additions still work via `scripts/add.py`. (old note:) Jay sends a post link to the Coordinator; a chat runs `scripts/add.py` + `scripts/publish.sh`. X/Twitter has no free
  reliable feed, so there is no automatic updater (D-002).
- **Open:** nothing blocking. Optional: a custom domain (Jay buys it; see D-003).
- NOTE (2026-10-23 05:2x): the daily updater is a LAPTOP LaunchAgent (com.purpledaddy.twoweeks.updater, 02:30). It only runs while the laptop is on; a run missed while it sleeps fires when it wakes, a run missed while it is shut down is skipped until the next 02:30. Moving it to the mini needs the Coordinator's OK.
