/* company.js — company detail page: review card, metrics, score breakdown,
   promise-vs-delivery tracker, thesis, risks, price-vs-trigger chart. */

function getQueryParam(name) {
  const params = new URLSearchParams(window.location.search);
  return params.get(name);
}

async function initCompanyPage() {
  const host = document.getElementById("content-host");
  const symbol = getQueryParam("symbol");

  if (!symbol) {
    host.innerHTML = emptyState(
      "No company specified",
      "Open this page from the Leaderboard, Best Overall, or Best Today list."
    );
    return;
  }

  // Pre-check against the leaderboard when possible so navigating to a
  // symbol that was never reviewed doesn't fire a fetch() the browser would
  // log as a 404 network error — we already know it isn't there.
  const lb = await loadLeaderboard();
  if (lb.ok && !lb.companies.some((c) => (c.symbol || "").toUpperCase() === symbol.toUpperCase())) {
    host.innerHTML = emptyState(
      `No review found for ${escapeHTML(symbol)}`,
      "This symbol isn't on the leaderboard yet."
    );
    return;
  }

  const { ok, review, error } = await loadReview(symbol);

  if (!ok) {
    host.innerHTML = `
      <div class="error-state">${escapeHTML(error)}</div>
      ${emptyState(
        `No review found for ${escapeHTML(symbol)}`,
        "reviews/" + escapeHTML(symbol) + ".json does not exist yet, or could not be loaded."
      )}
    `;
    return;
  }

  document.title = `${review.name || symbol} — Stock-Judging`;
  const e = normalizeEntry(review);
  host.innerHTML = renderCompanyDetail(review, e);
}

function renderCompanyDetail(review, e) {
  return `
    ${renderHeader(review, e)}
    <div class="grid-3">
      ${statCard("Composite", fmtNum(e.composite, 2))}
      ${statCard("Quality", fmtNum(e.quality, 2))}
      ${statCard("Margin of Safety", fmtPct(e.marginOfSafetyPct))}
    </div>

    <h2>Score breakdown</h2>
    ${renderScoreBreakdown(review.scores)}

    <h2>Valuation &amp; trigger</h2>
    ${renderValuation(e)}

    <h2>Price vs. trigger history</h2>
    ${renderPriceHistoryChart(review, e)}

    <h2>Thesis</h2>
    ${renderThesis(review.thesis)}

    <h2>Risks</h2>
    ${renderRisks(review.risks)}

    <h2>Promise vs. delivery</h2>
    ${renderPromises(review.promises)}
  `;
}

function renderHeader(review, e) {
  return `
    <div class="detail-header">
      <h1>${escapeHTML(review.name || e.symbol)}
        ${e.symbol ? `<span class="ticker-chip">${escapeHTML(e.symbol)}</span>` : ""}
        ${categoryBadgeHTML(e.category)}
      </h1>
    </div>
    <p class="page-sub">
      ${review.tier ? escapeHTML(review.tier) + " tier" : ""}
      ${review.as_of ? " &middot; as of " + escapeHTML(review.as_of) : ""}
      ${review.status ? " &middot; status: " + escapeHTML(review.status) : ""}
    </p>
  `;
}

function statCard(label, value) {
  return `<div class="panel stat"><span class="label">${escapeHTML(label)}</span><span class="value">${value}</span></div>`;
}

function renderScoreBreakdown(scores) {
  if (!scores || typeof scores !== "object" || Object.keys(scores).length === 0) {
    return emptyState("No score breakdown", "This review card has no `scores` data yet.");
  }
  const rows = Object.entries(scores)
    .filter(([, v]) => typeof v === "number")
    .map(([k, v]) => {
      const pct = Math.max(0, Math.min(100, (v / 10) * 100));
      return `
        <div class="score-row">
          <span class="score-row-label">${escapeHTML(k)}</span>
          <div class="score-bar-wrap">
            <div class="score-bar"><span style="width:${pct}%"></span></div>
            <span class="score-row-value">${fmtNum(v, 2)}</span>
          </div>
        </div>
      `;
    })
    .join("");
  if (!rows) return emptyState("No numeric scores", "This review card's `scores` object has no numeric dimensions.");
  return `<div class="panel score-breakdown">${rows}</div>`;
}

function renderValuation(e) {
  return `
    <div class="grid-3">
      ${statCard("Current price", fmtPrice(e.price))}
      ${statCard("DCF fair value", fmtPrice(e.fairValue))}
      ${statCard("ACC trigger (−12.5%)", fmtPrice(e.accTrigger))}
    </div>
    <div class="grid-3">
      ${statCard("INV trigger (−30%)", fmtPrice(e.invTrigger))}
      ${statCard("Best-today rank", e.bestTodayRank !== null ? String(e.bestTodayRank) : "—")}
      ${statCard("Conviction", fmtNum(e.conviction, 2))}
    </div>
  `;
}

/**
 * Price-vs-trigger chart. review_card.schema.json (stub) has no field for
 * historical trigger/price series — only point-in-time dcf.current_price /
 * acc_trigger / inv_trigger / fair_value as of `as_of`. Flagged in
 * frontend/README.md as a schema gap for phase 4. Until a history field
 * exists (e.g. `trigger_history: [{date, price, acc_trigger, inv_trigger}]`),
 * this always renders the honest "no history" state.
 */
function renderPriceHistoryChart(review, e) {
  const history = Array.isArray(review.trigger_history) ? review.trigger_history : null;

  if (!history || history.length === 0) {
    return emptyState(
      "No history yet",
      "This review card has no trigger-history series (only the current point-in-time price and triggers). " +
        "A single point is plotted below once enough data exists — history accumulates as re-reviews are added."
    );
  }

  return renderSVGChart(history, e);
}

function renderSVGChart(history, e) {
  const w = 640, h = 220, pad = 36;
  const dates = history.map((p) => p.date);
  const allVals = history.flatMap((p) => [p.price, p.acc_trigger, p.inv_trigger, p.fair_value].filter((v) => typeof v === "number"));
  const min = Math.min(...allVals);
  const max = Math.max(...allVals);
  const range = max - min || 1;

  const x = (i) => pad + (i / Math.max(1, history.length - 1)) * (w - 2 * pad);
  const y = (v) => h - pad - ((v - min) / range) * (h - 2 * pad);

  function pathFor(key, color) {
    const pts = history
      .map((p, i) => (typeof p[key] === "number" ? `${x(i)},${y(p[key])}` : null))
      .filter(Boolean);
    if (pts.length < 2) return "";
    return `<polyline points="${pts.join(" ")}" fill="none" stroke="${color}" stroke-width="2" />`;
  }

  return `
    <div class="chart-wrap">
      <svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}" role="img" aria-label="Price vs trigger history">
        ${pathFor("price", "#e8ebef")}
        ${pathFor("fair_value", "#5b9dd9")}
        ${pathFor("acc_trigger", "#f0c96b")}
        ${pathFor("inv_trigger", "#6fe39a")}
      </svg>
      <div class="chart-legend">
        <span><span class="swatch" style="background:#e8ebef"></span>Price</span>
        <span><span class="swatch" style="background:#5b9dd9"></span>Fair value</span>
        <span><span class="swatch" style="background:#f0c96b"></span>ACC trigger</span>
        <span><span class="swatch" style="background:#6fe39a"></span>INV trigger</span>
      </div>
    </div>
  `;
}

function renderThesis(thesis) {
  if (!thesis) return emptyState("No thesis yet", "This review card has no `thesis` text.");
  return `<div class="panel thesis-text">${escapeHTML(thesis)}</div>`;
}

function renderRisks(risks) {
  if (!Array.isArray(risks) || risks.length === 0) {
    return emptyState("No risks recorded", "This review card has no `risks` entries.");
  }
  return `<ul class="risk-list">${risks.map((r) => `<li>${escapeHTML(r)}</li>`).join("")}</ul>`;
}

function renderPromises(promises) {
  if (!Array.isArray(promises) || promises.length === 0) {
    return emptyState("No promises tracked", "This review card has no `promises` entries yet.");
  }
  return `<div class="promise-list">${promises.map(renderPromiseCard).join("")}</div>`;
}

function renderPromiseCard(p) {
  const title = p.promise || p.title || p.what || "Untitled promise";
  const status = p.status || p.delivery_status || "unknown";
  const period = p.quarter || p.period || p.made_on || "";
  const detail = p.detail || p.notes || p.outcome || "";
  return `
    <div class="promise-card">
      <div class="promise-head">
        <span>${escapeHTML(title)}</span>
        <span class="promise-status">${escapeHTML(status)}</span>
      </div>
      ${period ? `<div class="promise-body">${escapeHTML(period)}</div>` : ""}
      ${detail ? `<div class="promise-body">${escapeHTML(detail)}</div>` : ""}
    </div>
  `;
}

function emptyState(title, body) {
  return `<div class="empty-state"><div class="icon">&#128203;</div><h3>${escapeHTML(title)}</h3><p>${escapeHTML(body)}</p></div>`;
}
