"""Small shared helpers. No spec logic lives here."""
from datetime import date, timedelta
import calendar


class SpecScopeError(ValueError):
    """An input outside what the frozen spec defines (e.g. non-March FY-end for U3)."""


def add_months(d, n):
    """Calendar month arithmetic with day clamping (Feb-29 -> Feb-28)."""
    m0 = d.year * 12 + (d.month - 1) + n
    y, m = divmod(m0, 12)
    return date(y, m + 1, min(d.day, calendar.monthrange(y, m + 1)[1]))


def weekdays_between(a, b):
    """Mon-Fri days in (a, b]. Stand-in for an exchange trading calendar (no free,
    PIT holiday calendar is in the spec's input list -- see PR: SPEC-SILENT)."""
    if b <= a:
        return 0
    n, d = 0, a
    while d < b:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n += 1
    return n


def iso(d):
    return d.isoformat() if d is not None else None


def num(x):
    """None-preserving float coercion (missing stays missing, never becomes 0)."""
    if x is None or x == "":
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None
