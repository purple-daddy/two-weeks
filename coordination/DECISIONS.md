# 2 weeks — decisions
- **D-001 (2026-10-23):** Host on GitHub Pages (free, public repo `purple-daddy/two-weeks`, source `docs/`), not on Tailscale. Jay: "its own URL … off Tailscale".
  Project docs live outside `docs/` (`coordination/`) so Pages doesn't serve them.
- **D-002:** Data is hand-curated JSON. No free reliable X/Twitter feed exists; scraping is brittle and against X's terms. A chat adds entries with
  `scripts/add.py` when Jay sends a link.
- **D-003:** A custom domain is an option only. If Jay buys one, add a `docs/CNAME` file and the DNS records; nothing is bought by a chat.
- **D-004:** Counters are computed in the browser at view time, so no scheduled rebuild or launchd job is needed.
