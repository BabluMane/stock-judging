/* run.js — company input / run-request queue.
   This is a static frontend with no backend, so it cannot write a file to
   the repo directly. It instead builds the run-request JSON and offers it
   as a download; the person (or a future automated watcher) commits that
   file into runs/queue/ for the pipeline to pick up. See
   frontend/README.md "Run-request contract" for the full path and schema.

   Locally, this page tracks queued requests in localStorage purely as a
   per-viewer convenience (what have I asked for on this device) — it is
   NOT the real queue and is never presented as one. "Done" is only ever
   claimed when reviews/<symbol>.json is confirmed to exist. */

const RUN_QUEUE_DIR = "runs/queue/"; // relative to repo root, not to frontend/
const LOCAL_STORAGE_KEY = "stock-judging.local-run-requests.v1";

function slugify(name) {
  return name
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function todayISODate() {
  return new Date().toISOString().slice(0, 10);
}

function readLocalQueue() {
  try {
    const raw = localStorage.getItem(LOCAL_STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (err) {
    return [];
  }
}

function writeLocalQueue(list) {
  try {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(list));
  } catch (err) {
    // localStorage unavailable (private mode, blocked) — degrade silently,
    // the download still works without the local tracker.
  }
}

function initRunPage() {
  const form = document.getElementById("run-form");
  const input = document.getElementById("company-name");
  const statusHost = document.getElementById("status-host");

  form.addEventListener("submit", (evt) => {
    evt.preventDefault();
    const name = input.value.trim();
    statusHost.innerHTML = "";
    if (!name) {
      statusHost.innerHTML = `<div class="error-state">Enter a company name first.</div>`;
      return;
    }

    const date = todayISODate();
    const slug = slugify(name);
    const filename = `${slug}_${date}.json`;
    const requestBody = {
      company: name,
      requested_at: new Date().toISOString(),
      requested_date: date,
      status: "queued",
    };

    downloadJSON(filename, requestBody);

    const list = readLocalQueue();
    list.unshift({ company: name, slug, filename, requested_at: requestBody.requested_at, status: "queued" });
    writeLocalQueue(list);

    statusHost.innerHTML = `
      <div class="panel">
        <h3 style="margin-top:0;">Run-request file downloaded — here's what to do next</h3>
        <div class="steps">
          <div class="step done"><span class="dot"></span> Request file <code>${escapeHTML(filename)}</code> generated and downloaded</div>
          <div class="step active"><span class="dot"></span> Save it into <code>${escapeHTML(RUN_QUEUE_DIR)}</code> and commit/push it</div>
          <div class="step"><span class="dot"></span> Pipeline picks it up and runs the review (not built yet)</div>
          <div class="step"><span class="dot"></span> Review card lands at <code>reviews/${escapeHTML(slug.toUpperCase())}.json</code></div>
        </div>
        <div class="next-step-callout">
          <strong>You're not done yet.</strong> Nothing happens automatically from here — this page has no backend.
          Find <code>${escapeHTML(filename)}</code> in your downloads, move it into <code>${escapeHTML(RUN_QUEUE_DIR)}</code>
          in the repo, then <code>git add</code>, commit, and push it. The "Queued on this device" list below will keep
          checking for you: once <code>reviews/${escapeHTML(slug.toUpperCase())}.json</code> exists, it flips from
          <strong>QUEUED (local)</strong> to <strong>DONE</strong> with a link to the review — no need to keep this tab open,
          just come back and reload later.
        </div>
      </div>
    `;

    input.value = "";
    renderLocalQueue();
  });

  renderLocalQueue();
}

function downloadJSON(filename, obj) {
  const blob = new Blob([JSON.stringify(obj, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

async function renderLocalQueue() {
  const host = document.getElementById("queue-host");
  const list = readLocalQueue();

  if (list.length === 0) {
    host.innerHTML = `<div class="empty-state"><div class="icon">&#128203;</div><h3>Nothing queued yet</h3><p>Requests you queue from this device will appear here.</p></div>`;
    return;
  }

  host.innerHTML = `<div class="skeleton-rows skeleton-table" aria-hidden="true" aria-label="Checking status"><div class="skeleton-row"></div></div>`;

  // Pre-check against the leaderboard so polling for a not-yet-reviewed
  // symbol doesn't fire a fetch() the browser logs as a 404 — most queued
  // items won't have a review yet, and that's the expected common case.
  const lb = await loadLeaderboard();
  const knownSymbols = new Set(lb.ok ? lb.companies.map((c) => (c.symbol || "").toUpperCase()) : []);

  const rows = await Promise.all(
    list.map(async (item) => {
      const symbol = item.slug.toUpperCase();
      let done = false;
      if (knownSymbols.has(symbol)) {
        const { ok, review } = await loadReview(symbol);
        done = ok && review;
      }
      return `
        <tr>
          <td class="name-cell">${escapeHTML(item.company)}</td>
          <td>${escapeHTML(item.filename)}</td>
          <td>${done ? `<span class="badge badge-invest-now">DONE</span>` : `<span class="badge badge-watch">QUEUED (local)</span>`}</td>
          <td>${done ? `<a href="company.html?symbol=${encodeURIComponent(symbol)}">View review &rarr;</a>` : "—"}</td>
        </tr>
      `;
    })
  );

  host.innerHTML = `
    <div class="table-wrap">
      <table>
        <thead><tr><th>Company</th><th>Request file</th><th>Status</th><th></th></tr></thead>
        <tbody>${rows.join("")}</tbody>
      </table>
    </div>
  `;
}
