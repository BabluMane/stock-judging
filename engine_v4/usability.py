"""§4 usability gate = data-quality / input-integrity only (fraud-screen role killed).

U1 basis assertion (carried from V3_7 §4.1; machinery = v3.11 runner `basis_diagnostic`),
U2 non-positive sourced FY EPS -> VETOED-DATA, U3 check (a') at the results week.
U4 (check b) and U5 (financial exemption) are DEAD and intentionally absent: financial
names face U1-U3 on identical mechanics; no EPS series -> UNCOMPUTABLE -> VETOED-DATA.
All three checks are evaluated and logged; attribution = first failure in U1 -> U2 -> U3.
"""
import statistics
from datetime import date, timedelta

from . import constants as C
from .common import SpecScopeError, iso
from .pit import cell

NAMED_BASIS = "vendor (screener) series basis: post every corporate action to the fetch date"


def _fy_end(y):
    return date(y, 3, 31)


def basis_diagnostic(fy, scoring_fy, actions):
    """Is the sourced FY EPS row already on the named (vendor post-action) basis?
    Implied shares = NP/EPS at the scoring FY vs at the first FY ending after the last
    action ex-date that follows the scoring FY-end. Nearest of {1, cumulative factor F}
    decides; ties / indeterminate -> no restatement. Only the side NOT on the named
    basis is transformed; never choose whichever basis passes."""
    fe = _fy_end(scoring_fy)
    later = [a for a in actions if a["ex_date"] > fe]
    base = {"named_basis": NAMED_BASIS}
    if not later:
        return {**base, "actions_after_fy_end": [], "factor": 1.0, "restate": False,
                "basis": "no action after FY-end"}
    F = 1.0
    for a in later:
        F *= a["numerator"] / a["denominator"]
    last_ex = max(a["ex_date"] for a in later)
    out = {**base, "actions_after_fy_end": [(iso(a["ex_date"]), a.get("ratio_text")) for a in later],
           "cumulative_factor": round(F, 4)}
    ref = next((y for y in sorted(fy) if _fy_end(y) > last_ex), None)
    if ref is None:
        return {**out, "factor": 1.0, "restate": False,
                "basis": "indeterminate: no FY after last ex-date; no restatement"}

    def shares(y):
        np_, eps = cell(fy, y, "net_profit"), cell(fy, y, "eps")
        return None if np_ is None or not eps else np_ / eps
    s0, s1 = shares(scoring_fy), shares(ref)
    ratio = s1 / s0 if s0 and s1 is not None else None
    if ratio is None or ratio <= 0:
        return {**out, "factor": 1.0, "restate": False,
                "basis": "indeterminate (non-positive / missing NP/EPS); no restatement"}
    if abs(ratio - 1) <= abs(ratio - F):
        return {**out, "implied_shares_ratio": round(ratio, 3), "factor": 1.0, "restate": False,
                "basis": f"already on vendor post-action basis (implied shares x{ratio:.2f} ~ 1, not x{F:.2f})"}
    return {**out, "implied_shares_ratio": round(ratio, 3), "factor": F, "restate": True,
            "basis": f"unadjusted: implied shares x{ratio:.2f} ~ cumulative factor {F:.2f}; sourced EPS restated /F"}


def u1_basis(fy, scoring_fy, actions, audited_eps_by_fy=None):
    """Returns (check, sourced_eps_on_named_basis|None). The audited/sourced ratio per FY is
    REPORTED when an independent audited series is supplied (documentation of any residual
    convention factor such as ESOP drift); it gates nothing and has no tolerance."""
    sourced = cell(fy, scoring_fy, "eps")
    diag = basis_diagnostic(fy, scoring_fy, actions or [])
    if sourced is not None and diag["restate"]:
        sourced = sourced / diag["factor"]
    if audited_eps_by_fy:
        diag["audited_over_sourced_by_fy"] = {
            y: (a / cell(fy, y, "eps")) if cell(fy, y, "eps") else None for y, a in audited_eps_by_fy.items()}
    return {"status": "PASS", **diag}, sourced


def u2_nonpositive(sourced):
    """Sourced (basis-corrected) FY EPS <= 0 -> VETOED-DATA (a sign flip cannot be a basis
    residual; a data-defect flag, explicitly not a fraud judgment). Missing EPS excludes too."""
    if sourced is None:
        return {"status": "UNCOMPUTABLE", "reason": "no sourced FY EPS"}
    if sourced <= 0:
        return {"status": "STOP", "reason": f"sourced FY EPS non-positive ({sourced})"}
    return {"status": "PASS", "sourced_eps": sourced}


def results_week_ttm(eps_series, scoring_fy):
    """Publication-dated (unlagged) series. FY-TTM identification: the first publication in
    [Mar 31, Aug 31] of the scoring FY's year, applying the >10%-jump skip rule (a Mar-31
    point that jumps >10% to the next point is stale/pre-results and skipped; a small-jump
    Mar-31 point is the back-dated FY value). TTM = median over results-week .. +21d.
    SPEC-SILENT: 'jumps >10%' is read as the absolute relative change to the next point."""
    lo, hi = date(scoring_fy, 3, 31), date(scoring_fy, 8, 31)
    pts = sorted(p for p in eps_series if lo <= p[0] <= hi)
    skipped = None
    if len(pts) > 1 and pts[0][0] == lo:
        (d0_, v0), (_, v1) = pts[0], pts[1]
        if v0 == 0 or abs((v1 - v0) / v0) > C.U3_JUMP_SKIP:
            skipped = (iso(d0_), v0)
            pts = pts[1:]
    if not pts:
        return None
    r0 = pts[0][0]
    win = [v for d, v in eps_series if r0 <= d <= r0 + timedelta(days=C.U3_MEDIAN_WINDOW_DAYS)]
    return {"results_week": r0, "ttm": statistics.median(win), "n_points": len(win), "skipped_mar31_point": skipped}


def u3_check_a_prime(eps_series, scoring_fy, sourced):
    if not eps_series:
        return {"status": "UNCOMPUTABLE", "reason": "no vendor EPS series (missing data excludes; it does not exempt)"}
    rw = results_week_ttm(eps_series, scoring_fy)
    if rw is None:
        return {"status": "UNCOMPUTABLE", "reason": "no publication in [Mar 31, Aug 31]"}
    if sourced is None or sourced <= 0:
        return {"status": "NOT_EVALUATED", "reason": "no positive sourced EPS (U2 owns this stop)", "results_week": iso(rw["results_week"])}
    gap = abs(rw["ttm"] - sourced) / sourced
    out = {"results_week": iso(rw["results_week"]), "vendor_ttm": rw["ttm"], "sourced_eps": sourced,
           "gap": gap, "skipped_mar31_point": rw["skipped_mar31_point"], "n_points": rw["n_points"]}
    if gap > C.U3_TOLERANCE:
        return {"status": "STOP", "reason": f"|TTM - audited|/audited = {gap:.1%} > {C.U3_TOLERANCE:.0%}", **out}
    return {"status": "PASS", **out}


def evaluate(fy, scoring_fy, eps_series, corp_actions, audited_eps_by_fy=None):
    if scoring_fy is None:
        dead = {"status": "UNCOMPUTABLE", "reason": "no FY published >=63d before d0"}
        return {"verdict": "STOP", "label": "VETOED-DATA", "checks": {"U1": dead, "U2": dead, "U3": dead}}
    if scoring_fy not in fy:
        raise SpecScopeError(f"scoring FY {scoring_fy} not in FY table")
    u1, sourced = u1_basis(fy, scoring_fy, corp_actions, audited_eps_by_fy)
    checks = {"U1": u1, "U2": u2_nonpositive(sourced),
              "U3": u3_check_a_prime(eps_series, scoring_fy, sourced)}
    first = next((k for k in ("U1", "U2", "U3") if checks[k]["status"] in ("STOP", "UNCOMPUTABLE")), None)
    return {"verdict": "PASS" if first is None else "STOP",
            "label": "PASS" if first is None else "VETOED-DATA",
            "deciding_check": first, "checks": checks}
