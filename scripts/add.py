#!/usr/bin/env python3
"""Add one entry to the site's data, then rebuild.

  python3 scripts/add.py promise --topic Robotaxi --said 2026-10-01 --where "X post" --claim "..." --due 2027-06-30 \
      --query "google search words" [--note "..."] [--status pending|missed|late|contested] [--done 2027-07-02]
  python3 scripts/add.py sketchy --by tesla|musk --topic "Self-driving" --said 2026-10-01 --where "X post" \
      --claim "..." --why "why it is sketchy" --query "google search words"
Then:  bash scripts/publish.sh "add: <short name>"
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["promise", "sketchy"])
    ap.add_argument("--topic", required=True)
    ap.add_argument("--said", required=True)
    ap.add_argument("--where", required=True)
    ap.add_argument("--claim", required=True)
    ap.add_argument("--query", required=True)
    ap.add_argument("--due")
    ap.add_argument("--status", default="pending")
    ap.add_argument("--done")
    ap.add_argument("--note", default="")
    ap.add_argument("--by")
    ap.add_argument("--why")
    a = ap.parse_args()
    if a.kind == "promise":
        if not a.due:
            sys.exit("--due is required for a promise")
        entry = {"c": a.topic, "said": a.said, "where": a.where, "claim": a.claim, "due": a.due, "done": a.done,
                 "s": a.status, "note": a.note, "q": a.query}
        path = ROOT / "data" / "promises.json"
    else:
        if not (a.by and a.why):
            sys.exit("--by and --why are required for a sketchy claim")
        entry = {"by": a.by, "c": a.topic, "said": a.said, "where": a.where, "claim": a.claim, "why": a.why, "q": a.query}
        path = ROOT / "data" / "sketchy.json"
    rows = json.loads(path.read_text())
    rows.append(entry)
    new = json.dumps(rows, indent=1, ensure_ascii=False) + "\n"
    old = path.read_text()
    path.write_text(new)
    if subprocess.call([sys.executable, str(ROOT / "scripts" / "build.py")]) != 0:
        path.write_text(old)          # an invalid entry never stays in the data
        sys.exit("entry rejected; data left as it was")


main()
