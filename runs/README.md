# runs/ — run-request queue (frontend v1)

`queue/` holds run-request files produced by `frontend/run.html`: one JSON
file per queued company research run.

## Contract

- Path: `runs/queue/<slug>_<YYYY-MM-DD>.json`, where `<slug>` is the company
  name lowercased, non-alphanumerics collapsed to single hyphens.
- Shape:
  ```json
  {
    "company": "Reliance Industries",
    "requested_at": "2026-09-24T12:34:56.000Z",
    "requested_date": "2026-09-24",
    "status": "queued"
  }
  ```
- The frontend has no backend and cannot write into the repo directly, so
  `run.html` downloads this file to the browser's Downloads folder. A person
  (or, later, an automated watcher) moves/commits it into `runs/queue/`.
- The review pipeline (phase 4, not built yet) is expected to: pick up files
  from `runs/queue/`, run the research + engine_v3, write
  `reviews/<SYMBOL>.json` (+ `.md`), regenerate `leaderboard.json`, and then
  remove or archive the queue file (e.g. move it to `runs/done/`).

This directory and its contract are new in the frontend-v1 branch — nothing
in `PLATFORM_SCOPE.md` fixed the queue location before this, so treat the
path as a proposal for the pipeline to confirm in phase 4, not a locked spec.
