/* calibration.js — renders the Calibration page: backtested anchor stats +
   live forward-tracking table. Reads data/calibration.json and
   data/forward.json via fetchJSON. Hand-rolled SVG bars, no libraries. */

async function initCalibrationPage() {
  const host = document.getElementById("calib-host");
  const [cal, fwd, mv] = await Promise.all([
    fetchJSON("data/calibration.json"),
    fetchJSON("data/forward.json"),
    fetchJSON("data/moves.json"),
  ]);

  let html = "";
  html += renderBacktestSection(cal);
  html += renderForwardSection(fwd, mv);
  host.innerHTML = html;
}

function emptyState(title, body) {
  return `<div class="empty-state"><div class="icon">📊</div><h3>${escapeHTML(title)}</h3><p>${escapeHTML(body)}</p></div>`;
}

/* ---------- SVG horizontal bar ---------- */
function hbar(label, pct, note, good) {
  const v = Math.max(0, Math.min(100, Number(pct) || 0));
  const cls = good === true ? "calib-bar-good" : good === false ? "calib-bar-bad" : "calib-bar-neutral";
  return `
    <div class="calib-bar-row">
      <span class="calib-bar-label">${escapeHTML(label)}</span>
      <div class="calib-bar-track"><div class="calib-bar-fill ${cls}" style="width:${v}%"></div></div>
      <span class="calib-bar-val num">${pct === null || pct === undefined ? "—" : v.toFixed(1) + "%"}</span>
      ${note ? `<span class="calib-bar-note">${escapeHTML(note)}</span>` : ""}
    </div>`;
}

/* ---------- Section 1: Backtested ---------- */
function renderBacktestSection(res) {
  if (!res.ok || !res.data) {
    return `<h2>Backtested</h2>` + emptyState(
      "Calibration data not loaded",
      res.error || "Run tools/build_calibration_json.py to generate data/calibration.json."
    );
  }
  const d = res.data;
  const dir = d.direction || {};

  let html = `<h2>Backtested</h2>
  <p class="page-sub">Historical engine calls vs 12-month forward returns. n=${d.n} name-dates, updated ${escapeHTML(d.updated_at || "—")}.</p>`;

  // Hit-rate bars
  html += `<div class="panel"><h3 class="panel-title">Direction: did the call work?</h3>`;
  html += hbar("CHEAP → rose (n=" + (dir.cheap?.n ?? "—") + ")", dir.cheap?.rose_pct, "median " + (dir.cheap?.median_ret_pct ?? "—") + "%", true);
  html += hbar("OVERVALUED → fell (n=" + (dir.overvalued?.n ?? "—") + ")", dir.overvalued?.fell_pct, "median " + (dir.overvalued?.median_ret_pct ?? "—") + "%", false);
  html += hbar("FAIR → rose (n=" + (dir.fair?.n ?? "—") + ")", dir.fair?.rose_pct, null, null);
  html += `<p class="panel-note">Correlation(premium, 12m return) = ${dir.premium_ret_corr ?? "—"} — the premium has no linear relationship with forward returns.</p></div>`;

  // Magnitude buckets
  html += `<div class="panel"><h3 class="panel-title">Magnitude: premium bucket → median 12m return</h3>`;
  for (const b of d.buckets || []) {
    html += hbar(b.label + " (n=" + b.n + ")", Math.max(0, b.median_ret_pct ?? 0), null, null);
  }
  html += `</div>`;

  // By market cap
  html += `<div class="panel"><h3 class="panel-title">By market cap</h3><div class="table-wrap"><table class="data-table">
    <thead><tr><th>Cap</th><th class="num">n</th><th class="num">Cheap hit %</th><th class="num">Overval fall %</th></tr></thead><tbody>`;
  for (const m of ["LARGECAP", "MIDCAP", "SMALLCAP", "MICROCAP"]) {
    const r = (d.by_mcap || {})[m];
    if (!r) continue;
    const warn = m === "MICROCAP" ? ' <span class="warn-chip">⚠️ value traps</span>' : "";
    html += `<tr><td>${m}${warn}</td><td class="num">${r.n}</td><td class="num">${r.cheap_hit_pct ?? "—"}</td><td class="num">${r.overval_fall_pct ?? "—"}</td></tr>`;
  }
  html += `</tbody></table></div></div>`;

  // By sector
  html += `<div class="panel"><h3 class="panel-title">By sector (top 8)</h3><div class="table-wrap"><table class="data-table">
    <thead><tr><th>Sector</th><th class="num">n</th><th class="num">Cheap hit %</th><th class="num">Overval fall %</th></tr></thead><tbody>`;
  for (const [s, r] of Object.entries(d.by_sector || {})) {
    html += `<tr><td>${escapeHTML(s)}</td><td class="num">${r.n}</td><td class="num">${r.cheap_n ? r.cheap_hit_pct + " (" + r.cheap_n + ")" : "—"}</td><td class="num">${r.overval_n ? r.overval_fall_pct + " (" + r.overval_n + ")" : "—"}</td></tr>`;
  }
  html += `</tbody></table></div></div>`;

  // By regime
  html += `<div class="panel"><h3 class="panel-title">By regime (d0 cohort)</h3><div class="table-wrap"><table class="data-table">
    <thead><tr><th>Cohort</th><th>Next-12m regime</th><th class="num">n</th><th class="num">Cheap hit %</th><th class="num">Overval fall %</th></tr></thead><tbody>`;
  for (const [y, r] of Object.entries(d.by_regime || {})) {
    html += `<tr><td class="num">${escapeHTML(y)}</td><td>${escapeHTML(r.regime || "—")}</td><td class="num">${r.n}</td><td class="num">${r.cheap_hit_pct ?? "—"}</td><td class="num">${r.overval_fall_pct ?? "—"}</td></tr>`;
  }
  html += `</tbody></table></div></div>`;

  // Standing rules
  html += `<div class="panel calib-rules"><h3 class="panel-title">Standing rules for using the engine</h3><ol>`;
  for (const rule of d.standing_rules || []) {
    html += `<li>${escapeHTML(rule)}</li>`;
  }
  html += `</ol></div>`;

  return html;
}

/* ---------- Big Moves feed ---------- */
/* Big moves are NOT news. News = routine company updates (results, dividends,
   deals). A big move = a >=10% price move over any rolling 5 trading days,
   with a "why did this happen" explanation and sources. The weekly
   forward-tracking cron appends entries here when its 10% alert fires. */
function renderMovesFeed(res) {
  const moves = (res.ok && res.data && res.data.moves) || [];
  if (!moves.length) return "";
  const sorted = [...moves].sort((a, b) => (b.date || "").localeCompare(a.date || ""));
  let html = `<div class="panel"><h3 class="panel-title">Big moves — what happened and why</h3><div class="moves-feed">`;
  for (const m of sorted) {
    const pct = Number(m.move_pct) || 0;
    const cls = pct >= 0 ? "pos" : "neg";
    const sign = pct >= 0 ? "+" : "";
    const sources = (m.sources || []).map((u, i) =>
      `<a href="${escapeHTML(u)}" target="_blank" rel="noopener">[${i + 1}]</a>`).join(" ");
    html += `<div class="move-item">
      <span class="move-date num">${escapeHTML(m.date || "—")}</span>
      <span class="name-cell"><a href="company.html?symbol=${encodeURIComponent(m.symbol || "")}">${escapeHTML(m.symbol || "?")}</a></span>
      <span class="move-badge ${cls}">${sign}${pct.toFixed(1)}%</span>
      <span class="move-window">${escapeHTML(m.window || "5d")}</span>
      <div class="move-why">${escapeHTML(m.why || "")} ${sources}</div>
    </div>`;
  }
  html += `</div></div>`;
  return html;
}

/* ---------- Section 2: Forward testing ---------- */
function renderForwardSection(res, mvRes) {
  if (!res.ok || !res.data) {
    return `<h2>Forward testing</h2>` + emptyState(
      "Forward-tracking data not loaded",
      res.error || "Run tools/build_calibration_json.py to generate data/forward.json."
    );
  }
  const d = res.data;
  const rows = d.companies || [];
  let html = `<h2>Forward testing</h2>
  <p class="page-sub">Live-reviewed companies tracked from their review date. n=${d.n}, updated ${escapeHTML(d.updated_at || "—")}. Sorted by return since review.</p>`;

  html += renderMovesFeed(mvRes || { ok: false, data: null });

  if (!rows.length) {
    return html + emptyState("No companies tracked yet", "Reviews feed this table automatically.");
  }

  html += `<div class="panel"><div class="table-wrap"><table class="data-table">
    <thead><tr><th>Symbol</th><th>Category</th><th class="num">At review</th><th class="num">Latest</th><th class="num">Return</th><th class="num">vs FV</th><th class="num">Days</th></tr></thead><tbody>`;
  for (const c of rows) {
    const retCls = c.ret_since_review === null || c.ret_since_review === undefined ? "" : c.ret_since_review >= 0 ? "pos" : "neg";
    html += `<tr>
      <td class="name-cell"><a href="company.html?symbol=${encodeURIComponent(c.symbol)}">${escapeHTML(c.symbol)}</a></td>
      <td>${categoryBadgeHTML(c.category)}</td>
      <td class="num">${fmtPrice(c.price_at_review)}</td>
      <td class="num">${fmtPrice(c.latest_price)}</td>
      <td class="num ${retCls}">${c.ret_since_review === null || c.ret_since_review === undefined ? "—" : fmtPct(c.ret_since_review)}</td>
      <td class="num">${c.vs_fv === null || c.vs_fv === undefined ? "—" : fmtPct(c.vs_fv)}</td>
      <td class="num">${c.days_tracked ?? "—"}</td>
    </tr>`;
  }
  html += `</tbody></table></div>
  <p class="panel-note">Prices snapshotted weekly by the forward-tracking job. "vs FV" is the latest price vs the DCF fair value at review.</p></div>`;
  return html;
}
