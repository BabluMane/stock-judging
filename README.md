# stock-judging

Private research platform: type a company name → a cloud session runs the
full v3 research stack → review card committed → leaderboard updated.
Answers two questions: **best overall** and **best to invest in TODAY**.

> **v3 is NOT LIVE.** Until the validation bar passes (0 blow-ups, ≥3 winner
> names, to-T positive, 24m ≥0.8×), this repo produces research, not
> investable calls. The today-view stays labeled provisional.

## Layout
- `engine/` — v3 engine + schemas + test suite (audited, 59/59 passing)
- `specs/` — v3 spec, v3.7 delta, scoring spec, audits, forensics
- `workflows/` — research playbooks (DRAFT — rubric fixes pending)
- `data/` — fetcher layer (placeholder)
- `reviews/` — per-company review cards (md + json), git-versioned
- `frontend/` — static frontend (placeholder)
- `leaderboard.json` — generated from reviews
- `PLATFORM_SCOPE.md` — full build scope

## Repo rules
- **Frozen:** `engine/engine_v3.py`, `engine/engine_v2.py` — no changes without
  a spec version bump + revalidation note.
- No live execution hooks, anywhere, ever.
- No fabricated or forward-filled data.
- Private repo — never make public.
- Append to `STATE.md` after every piece of repo work.
