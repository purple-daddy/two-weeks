#!/usr/bin/env python3
"""Check a batch of researched history items, add the ones that verify, queue the rest for review. No AI is called here.

  python3 scripts/verify_backfill.py reference/backfill-2013-2016.json [--dry-run]

An item goes LIVE only if: the fields are clean, it isn't a duplicate, confidence is "high", the quote's words really appear on the
cited page (we fetch it ourselves), and its outcome is settled: a pending promise needs a future deadline; kept / late / missed need a
second page whose quote is also found. Everything else goes to reference/review.json (never published).
"""
import datetime
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import update_daily as U  # noqa: E402  (only its helper functions are used)

ROOT = U.ROOT


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if not args:
        sys.exit(__doc__)
    today = datetime.date.today()
    items = json.loads(Path(args[0]).read_text())
    promises = json.loads((U.DATA / "promises.json").read_text())
    sketchy = json.loads((U.DATA / "sketchy.json").read_text())
    known = [{"claim": e["claim"], "said": e["said"]} for e in promises + sketchy]
    live, review, dup, bad = [], [], 0, 0
    for x in items:
        it = {k: U.clean(x.get(k), n) for k, n in (("claim", 240), ("said", 10), ("where", 100), ("topic", 30), ("source_url", 500),
              ("quote", 300), ("confidence", 10), ("note", 240), ("due", 10), ("outcome", 10), ("done", 10),
              ("outcome_url", 500), ("outcome_quote", 300))}
        it["confidence"] = it["confidence"].lower()
        it["outcome"] = it["outcome"].lower()
        if it["topic"] not in U.TOPICS:
            it["topic"] = "Other"
        if not (it["claim"] and it["where"] and U.valid_date(it["said"]) and U.valid_date(it["due"]) and it["quote"]
                and it["said"] <= today.isoformat() and it["due"] >= it["said"] and U.public_https(it["source_url"])):
            bad += 1
            continue
        if U.is_duplicate(it, known):
            dup += 1
            continue
        found, why = U.quote_on_page(it["source_url"], it["quote"])
        it["quote_check"] = why
        status = done = None
        if found and it["confidence"] == "high":
            if it["due"] >= today.isoformat():
                status = "pending"
            elif it["outcome"] in ("kept", "late", "missed"):
                ok = True
                if it["outcome"] in ("kept", "late"):
                    ok = U.valid_date(it["done"]) and ((it["outcome"] == "kept") == (it["done"] <= it["due"]))
                f2, why2 = U.quote_on_page(it["outcome_url"], it["outcome_quote"]) if ok else (False, "bad done date")
                it["outcome_check"] = why2
                if ok and f2:
                    status, done = it["outcome"], (it["done"] if it["outcome"] != "missed" else None)
        if status:
            it["status"], it["done_final"] = status, done
            live.append(it)
            known.append({"claim": it["claim"], "said": it["said"]})
        else:
            review.append(it)
    print(f"{args[0]}: {len(items)} researched -> {len(live)} verified for the live site, {len(review)} to review, {dup} duplicates, {bad} invalid")
    if dry:
        return
    if live:
        old = (U.DATA / "promises.json").read_text()
        for it in live:
            promises.append({"c": it["topic"], "said": it["said"], "where": it["where"], "claim": it["claim"], "due": it["due"],
                             "done": it["done_final"], "s": it["status"], "note": it["note"], "q": U.clean(it["claim"], 80),
                             "src": it["source_url"]})
        (U.DATA / "promises.json").write_text(json.dumps(promises, indent=1, ensure_ascii=False) + "\n")
        b = subprocess.run([sys.executable, str(ROOT / "scripts" / "build.py")], capture_output=True, text=True)
        if b.returncode != 0:
            (U.DATA / "promises.json").write_text(old)
            print("build failed, data reverted:", b.stdout[-300:], b.stderr[-300:])
            review += live
            live = []
    if review:
        U.REVIEW.parent.mkdir(exist_ok=True)
        try:
            cur = json.loads(U.REVIEW.read_text())
        except (OSError, ValueError):
            cur = []
        for q in review:
            q["queued"] = today.isoformat()
        U.REVIEW.write_text(json.dumps(cur + review, indent=1, ensure_ascii=False) + "\n")
    print(f"written: {len(live)} added to data/promises.json (not yet committed), {len(review)} appended to reference/review.json")


main()
