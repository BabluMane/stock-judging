#!/usr/bin/env python3
"""Copy promise-tracking audit JSONs into the frontend data dir.

Source:  ~/workspace/stock-judging/promise-tracking/audits/<slug>.json
Target:  <repo>/frontend-v2/data/audits/<slug>.json

Files are copied verbatim (no mutation) — the company page computes the
credibility score client-side from the quarter grades, mirroring
promise-tracking/scorer.py. Re-run whenever new audits land.
"""
import json
import shutil
import sys
from pathlib import Path

AUDITS_SRC = Path.home() / "workspace/stock-judging/promise-tracking/audits"
DST = Path(__file__).resolve().parent.parent / "data" / "audits"


def main() -> int:
    if not AUDITS_SRC.is_dir():
        print(f"source dir missing: {AUDITS_SRC}", file=sys.stderr)
        return 1
    DST.mkdir(parents=True, exist_ok=True)
    copied = 0
    for src in sorted(AUDITS_SRC.glob("*.json")):
        # validate it parses before copying
        try:
            with open(src, encoding="utf-8") as f:
                d = json.load(f)
            assert isinstance(d.get("quarters"), list), "quarters must be a list"
        except Exception as e:  # noqa: BLE001
            print(f"SKIP {src.name}: {e}", file=sys.stderr)
            continue
        shutil.copy2(src, DST / src.name)
        copied += 1
    print(f"copied {copied} audit file(s) -> {DST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
