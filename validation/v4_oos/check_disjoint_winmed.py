#!/usr/bin/env python3
"""Disjointness assertion for the v4 Phase-D winner/mediocrity set (20 name-dates).

Asserts the selected set is disjoint from:
  - the five prior sets (in-sample 25/50; v3.8/v3.9/v3.10/v3.11), at COMPANY and NAME-DATE level,
    via the canonical lists in port/validation/v3_10_oos/check_disjoint_v310.py and
    port/validation/v3_11_oos/check_disjoint_v311.py (imported, never retyped)
  - the Phase-C R1-R7 burn list (v3/validation/v4_oos/burn_list_winmed.json), at company level
  - the 5 certified blow-up name-dates (supremeeng x2, pbm x2, varroc x1)

Prints DISJOINT: True / False and exits 0 / 1.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = os.path.expanduser("~/workspace/stock-judging/port")
sys.path.insert(0, os.path.join(PORT, "validation", "v3_10_oos"))
sys.path.insert(0, os.path.join(PORT, "validation", "v3_11_oos"))

import check_disjoint_v310 as c10  # canonical prior lists
import check_disjoint_v311 as c11  # canonical prior lists

WINMED = [
    # winners: 5 companies x 2 name-dates
    "infy_2020-03-31", "infy_2021-03-31",
    "sbin_2021-03-31", "sbin_2022-03-31",
    "srf_2019-03-31", "srf_2020-03-31",
    "lt_2021-03-31", "lt_2022-03-31",
    "endurance_2020-03-31", "endurance_2021-03-31",
    # mediocrities: 5 companies x 2 name-dates
    "drreddy_2019-03-31", "drreddy_2020-03-31",
    "dabur_2020-03-31", "dabur_2021-03-31",
    "maruti_2019-03-31", "maruti_2020-03-31",
    "cyient_2020-03-31", "cyient_2021-03-31",
    "auropharma_2019-03-31", "auropharma_2020-03-31",
]

BLOWUPS = [
    "supremeeng_2020-03-31", "supremeeng_2021-03-31",
    "pbm_2019-03-31", "pbm_2020-03-31",
    "varroc_2019-03-31",
]


def company_of(nd):
    return nd.rsplit("_", 1)[0].lower()


def main():
    assert len(WINMED) == 20, f"expected 20 name-dates, got {len(WINMED)}"
    assert len(set(WINMED)) == 20, "duplicate name-dates in set"
    assert len({company_of(nd) for nd in WINMED}) == 10, "expected 10 companies"

    prior_lists = {
        "in_sample": c10.INSAMPLE,
        "v3_8": c10.V3_8,
        "v3_9": c10.V3_9,
        "v3_10": c10.V3_10,
        "v3_11": c11.V3_11,
    }
    violations = []

    # 1) prior sets: name-date level AND company level
    for label, lst in prior_lists.items():
        nd_set = set(lst)
        co_set = {company_of(nd) for nd in lst}
        for nd in WINMED:
            if nd in nd_set:
                violations.append(f"name-date collision with {label}: {nd}")
            if company_of(nd) in co_set:
                violations.append(f"company collision with {label}: {company_of(nd)}")

    # 2) blow-up set: name-date level AND company level
    blow_co = {company_of(nd) for nd in BLOWUPS}
    for nd in WINMED:
        if nd in BLOWUPS:
            violations.append(f"name-date collision with blow-up set: {nd}")
        if company_of(nd) in blow_co:
            violations.append(f"company collision with blow-up set: {company_of(nd)}")

    # 3) burn list: company level (normalized tokens)
    burn = json.load(open(os.path.join(HERE, "burn_list_winmed.json")))
    burn_tokens = set(burn["tokens"] if isinstance(burn, dict) else burn)
    for nd in WINMED:
        if company_of(nd) in burn_tokens:
            violations.append(f"company collision with burn list: {company_of(nd)}")

    if violations:
        print("DISJOINT: False")
        for v in violations:
            print("  VIOLATION:", v)
        sys.exit(1)
    print("DISJOINT: True")
    sys.exit(0)


if __name__ == "__main__":
    main()
