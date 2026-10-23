#!/usr/bin/env python3
"""Build docs/index.html (the public site) from site/template.html + data/*.json.

Run:  python3 scripts/build.py
Checks every entry, inlines the data, and pins the page's one script in its Content-Security-Policy by SHA-256, so the
site runs no other script, ever. The counters are computed in the reader's browser, so the page never needs a daily rebuild.
"""
import base64
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STATUS = {"missed", "late", "pending", "contested"}
BY = {"musk", "tesla"}


def load(name, required, extra=None):
    rows = json.loads((ROOT / "data" / name).read_text())
    problems = []
    for i, r in enumerate(rows):
        for k in required:
            if not isinstance(r.get(k), str) or (not r[k] and k not in ("note",)):
                problems.append(f"{name}[{i}] missing/empty '{k}'")
        for k in ("said", "due", "done"):
            if r.get(k) is not None and k in r:
                try:
                    if not (isinstance(r[k], str) and DATE.match(r[k])):
                        raise ValueError
                    datetime.date.fromisoformat(r[k])
                except ValueError:
                    problems.append(f"{name}[{i}] '{k}' must be a real date, YYYY-MM-DD")
        if extra:
            problems += [f"{name}[{i}] {m}" for m in extra(r)]
    return rows, problems


def check_promise(r):
    out = []
    if r.get("s") not in STATUS:
        out.append("'s' must be one of " + "/".join(sorted(STATUS)))
    if r.get("s") == "late" and not r.get("done"):
        out.append("a 'late' promise needs a 'done' date")
    if r.get("done") and r.get("due") and r["done"] < r["due"]:
        out.append("'done' is before 'due'")
    if r.get("due") and r.get("said") and r["due"] < r["said"]:
        out.append("'due' is before 'said'")
    return out


def check_sketchy(r):
    return [] if r.get("by") in BY else ["'by' must be musk or tesla"]


def main():
    promises, p1 = load("promises.json", ["c", "said", "where", "claim", "due", "s", "note", "q"], check_promise)
    sketchy, p2 = load("sketchy.json", ["by", "c", "said", "where", "claim", "why", "q"], check_sketchy)
    if p1 + p2:
        print("\n".join(p1 + p2))
        return 1
    page = (ROOT / "site" / "template.html").read_text()

    def js(v):   # JSON that is also safe inside <script>: no "<" can ever close the tag
        return json.dumps(v, ensure_ascii=False, indent=1).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")

    page = page.replace("/*DATA*/[]", js(promises)).replace("/*SKETCHY*/[]", js(sketchy))
    m = re.search(r"<script>(.*?)</script>", page, re.S)
    digest = base64.b64encode(hashlib.sha256(m.group(1).encode()).digest()).decode()
    page = page.replace("__SCRIPT_HASH__", digest)
    assert "__SCRIPT_HASH__" not in page and page.count("<script") == 1
    out = ROOT / "docs"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(page)
    (out / ".nojekyll").write_text("")
    print(f"built docs/index.html: {len(promises)} promises, {len(sketchy)} sketchy claims, script sha256-{digest[:12]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
