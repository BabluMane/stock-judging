#!/usr/bin/env python3
"""v5 Phase-D LOCKED RUNNER — one-shot execution of the frozen engine_v5 on the 24 frozen inputs.

Discipline (V5_OOS_PREREG.md + Amendment 1):
- engine_v5/ is NEVER modified by this script (read-only import).
- Each of the 24 manifest name-dates is executed EXACTLY ONCE via run_name_date.
- No aggregation, no bar verdict, no interpretation here — raw engine outputs only.
  Aggregation/audit happens independently after the run.
- Mid-run code changes are forbidden: if this script fails, fix-forward is a new
  pre-registered run, never an edit-and-rerun of the same set.
"""
import hashlib
import json
import os
import subprocess
import sys
from datetime import date, datetime, timezone

PORT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PORT)

from engine_v5.run import NameDate, run_name_date  # noqa: E402

INPUTS = os.path.join(PORT, "validation", "v5_oos", "phase_d_inputs")
RESULTS = os.path.join(PORT, "validation", "v5_oos",
                        sys.argv[1] if len(sys.argv) > 1 else "phase_d_results")
MANIFEST = os.path.join(PORT, "validation", "v5_oos", "SET_MANIFEST.json")


def parse(d):
    return date.fromisoformat(d) if isinstance(d, str) else d


def load_input(path):
    with open(path) as f:
        data = json.load(f)
    return NameDate(**{**data,
                       "d0": parse(data["d0"]),
                       "as_of": parse(data["as_of"]) if data.get("as_of") else None,
                       "fy": {int(y): {**r, "results_published":
                                       (parse(r["results_published"]) if r.get("results_published") else None)}
                              for y, r in data["fy"].items()},
                       "prices": [(parse(d), float(p)) for d, p in data["prices"]],
                       "pledge": [{**q, "quarter_end": parse(q["quarter_end"])}
                                   for q in data.get("pledge", [])],
                       "eps_series": [(parse(d), v) for d, v in data.get("eps_series", [])],
                       "corp_actions": [{**a, "ex_date": parse(a["ex_date"])}
                                         for a in data.get("corp_actions", [])],
                       "events": [{**e, "event_date": parse(e["event_date"])}
                                   for e in data.get("events", [])],
                       "audited_prints": [{**p, "results_date": parse(p["results_date"]),
                                           "fy_end": parse(p["fy_end"])}
                                           for p in data.get("audited_prints", [])]})


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    os.makedirs(RESULTS, exist_ok=True)
    with open(MANIFEST) as f:
        manifest = json.load(f)
    name_dates = [n["name_date"] for n in manifest["name_dates"]]
    assert len(name_dates) == 24, f"manifest has {len(name_dates)} name-dates, expected 24"

    engine_tree = subprocess.run(
        ["git", "rev-parse", "HEAD:engine_v5"], cwd=PORT,
        capture_output=True, text=True).stdout.strip()
    spec_hash = sha256_file(os.path.join(PORT, "engine_v5", "V5_SPEC.md"))

    run_log = {
        "run_started_utc": datetime.now(timezone.utc).isoformat(),
        "engine_tree": engine_tree,
        "spec_sha256": spec_hash,
        "manifest_sha256": sha256_file(MANIFEST),
        "inputs": {},
        "results": {},
    }

    for nd_key in sorted(name_dates):
        path = os.path.join(INPUTS, f"{nd_key}.json")
        run_log["inputs"][nd_key] = sha256_file(path)
        nd = load_input(path)          # construction only
        res = run_name_date(nd)        # THE single locked execution per name-date
        out = os.path.join(RESULTS, f"{nd_key}.json")
        with open(out, "w") as f:
            json.dump(res, f, indent=1, default=str)
        run_log["results"][nd_key] = sha256_file(out)
        print(f"RAN {nd_key}: excluded={res['excluded']} "
              f"filled={[t for t, l in res['legs'].items() if l['status'] == 'FILLED']}")

    run_log["run_finished_utc"] = datetime.now(timezone.utc).isoformat()
    with open(os.path.join(RESULTS, "RUN_LOG.json"), "w") as f:
        json.dump(run_log, f, indent=1)
    print(f"\n24/24 executed. engine_tree={engine_tree}")


if __name__ == "__main__":
    sys.exit(main())
