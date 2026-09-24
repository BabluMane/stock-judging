# AGENTS.md — durable notes for agents working this repo

- `frontend/` ships with `leaderboard.json` seeded empty and no `reviews/*.json`
  committed, so any local visual QA of populated states (leaderboard rows,
  company-detail decision panel, etc.) needs throwaway fixture data served
  from a scratch directory *outside* the repo (e.g. `/tmp/...`) — never
  overwrite the tracked `leaderboard.json`/`reviews/` seed files, even
  temporarily, to preview real data.
- This is a static, no-build frontend that must keep working from a bare
  `file://` open, not just a local server — `js/data.js`'s `fetchJSON()`
  short-circuits under `location.protocol === "file:"` specifically to avoid
  a browser-logged CORS console error that a try/catch cannot suppress.
  Don't "fix" that branch away; it's load-bearing for the zero-console-error
  requirement.
- Playwright + Chromium are preinstalled globally (not as a repo/npm dep) at
  `/opt/pw-browsers/chromium`, importable via
  `NODE_PATH=/opt/node22/lib/node_modules node script.js` — no
  `npm install`/`playwright install` needed or allowed given the
  no-new-dependencies constraint.
