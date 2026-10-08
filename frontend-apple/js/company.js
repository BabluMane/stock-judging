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
  const news = await loadNews(symbol); // silent if missing — section just won't render
  const moves = await loadMoves(); // silent if missing — block just won't render
  const shp = await loadShp(); // silent if missing — block just won't render
  host.innerHTML = renderCompanyDetail(review, e, news, moves, shp);

  const starBtn = host.querySelector(".star-btn");
  if (starBtn) {
    starBtn.addEventListener("click", () => {
      const sym = starBtn.dataset.starSymbol;
      if (!sym) return;
      const now = toggleStarred(sym);
      starBtn.classList.toggle("starred", now);
      starBtn.textContent = now ? "★" : "☆";
      starBtn.setAttribute("aria-label", `${now ? "Unstar" : "Star"} ${sym}`);
    });
  }
}

function renderCompanyDetail(review, e, news, moves, shp) {
  // A1: the "buy at what price" answer — fair value, ACC/INV triggers, and
  // margin of safety — must read FIRST, before score breakdown or anything
  // else. This decision panel sits directly under the header.
  const newsSection = renderNewsSection(news);
  const dealsSection = renderDealsSection(news);
  const movesSection = renderMovesSection(moves, review.symbol || e.symbol);
  const shpSection = renderShpSection(shp, review.symbol || e.symbol);
  return `
    ${renderHeader(review, e)}
    ${renderDecisionPanel(e)}

    <h2>Score breakdown</h2>
    ${renderScoreBreakdown(review.scores)}

    <h2>Price vs. trigger history</h2>
    ${renderPriceHistoryChart(review, e)}
${movesSection ? `
    <h2>Recent big moves</h2>
    ${movesSection}
` : ""}
${shpSection ? `
    <h2>Shareholding &amp; flows</h2>
    ${shpSection}
` : ""}

    <h2>Thesis</h2>
    ${renderThesis(review.thesis)}

    <h2>Risks</h2>
    ${renderRisks(review.risks)}

    <h2>Promise vs. delivery</h2>
    ${renderPromises(review.promises)}
${newsSection ? `
    <h2>News &amp; corporate actions</h2>
    ${newsSection}
` : ""}${dealsSection ? `
    <h2>Bulk &amp; block deals</h2>
    ${dealsSection}
` : ""}
  `;
}

function renderDecisionPanel(e) {
  const noteByCategory = {
    INVEST_NOW: "Price is at or below the INV trigger — the entry condition is currently met.",
    AT_TRIGGER: "Price is above fair value's entry triggers — this name is not a today-buy yet.",
    WATCH: "Price has not reached the ACC trigger yet — watch, don't buy.",
    PASS: "This name passed on quality/valuation grounds — no entry price applies.",
    AVOID: "This name is an active avoid — the engine or reviewer sees reasons to stay away, not just reasons not to buy.",
  };
  const note = noteByCategory[e.category] || "Category not set — treat any figures below as unconfirmed.";

  return `
    <div class="decision-panel">
      <div class="decision-title">Buy at what price — entry snapshot</div>
      <div class="decision-grid">
        <div class="stat"><span class="label">Current price</span><span class="value hero">${fmtPrice(e.price)}</span></div>
        <div class="stat"><span class="label">DCF fair value</span><span class="value">${fmtPrice(e.fairValue)}</span></div>
        <div class="stat"><span class="label">ACC trigger (&minus;12.5%)</span><span class="value">${fmtPrice(e.accTrigger)}</span></div>
        <div class="stat"><span class="label">INV trigger (&minus;30%)</span><span class="value">${fmtPrice(e.invTrigger)}</span></div>
        <div class="stat"><span class="label">Margin of safety</span><span class="value hero">${fmtPct(e.marginOfSafetyPct)}</span></div>
        <div class="stat"><span class="label">Composite</span><span class="value">${fmtNum(e.composite, 2)}</span></div>
        <div class="stat"><span class="label">Quality</span><span class="value">${fmtNum(e.quality, 2)}</span></div>
        <div class="stat"><span class="label">Best-today rank</span><span class="value">${e.bestTodayRank !== null ? String(e.bestTodayRank) : "—"}</span></div>
      </div>
      <p class="decision-note">${escapeHTML(note)}</p>
    </div>
  `;
}

function renderHeader(review, e) {
  return `
    <div class="detail-header">
      <h1>${escapeHTML(review.name || e.symbol)}
        ${e.symbol ? `<span class="ticker-chip">${escapeHTML(e.symbol)}</span>` : ""}
        ${categoryBadgeHTML(e.category)}
      </h1>
      ${e.symbol ? starButtonHTML(e.symbol, isStarred(e.symbol)) : ""}
    </div>
    <p class="page-sub">
      ${review.tier ? escapeHTML(review.tier) + " tier" : ""}
      ${review.as_of ? " &middot; as of " + escapeHTML(review.as_of) : ""}
      ${review.status ? " &middot; status: " + escapeHTML(review.status) : ""}
    </p>
  `;
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

/* Recent big moves block. Big moves are NOT news — a big move is a >=10%
   price move over any rolling 5 trading days, with a "why did this happen"
   explanation. Renders "" when there are no moves for this symbol (max 5). */
function renderMovesSection(movesResult, symbol) {
  if (!movesResult || !movesResult.ok) return "";
  const sym = (symbol || "").toUpperCase();
  const mine = (movesResult.moves || [])
    .filter((m) => (m.symbol || "").toUpperCase() === sym)
    .sort((a, b) => (b.date || "").localeCompare(a.date || ""))
    .slice(0, 5);
  if (!mine.length) return "";
  let html = `<div class="panel"><div class="moves-feed">`;
  for (const m of mine) {
    const pct = Number(m.move_pct) || 0;
    const cls = pct >= 0 ? "pos" : "neg";
    const sign = pct >= 0 ? "+" : "";
    const sources = (m.sources || []).map((u, i) =>
      `<a href="${escapeHTML(u)}" target="_blank" rel="noopener">[${i + 1}]</a>`).join(" ");
    html += `<div class="move-item">
      <span class="move-date num">${escapeHTML(m.date || "—")}</span>
      <span class="move-badge ${cls}">${sign}${pct.toFixed(1)}%</span>
      <span class="move-window">${escapeHTML(m.window || "5d")}</span>
      <div class="move-why">${escapeHTML(m.why || "")} ${sources}</div>
    </div>`;
  }
  return html + `</div></div>`;
}

/* Shareholding & flows. Latest quarter promoter/FII/DII/public bars with QoQ
   pp-change badges + a one-line read. Renders "" when shp.json is missing
   or has no entry for this symbol. */
function renderShpSection(shpResult, symbol) {
  if (!shpResult || !shpResult.ok) return "";
  const sym = (symbol || "").toUpperCase();
  const s = shpResult.companies[sym];
  if (!s) return "";
  const bar = (label, val) => {
    const v = Number(val);
    if (!isFinite(v)) return "";
    const w = Math.max(0, Math.min(100, v));
    return `<div class="shp-row"><span class="shp-label">${label}</span>
      <span class="shp-bar"><span class="shp-fill" style="width:${w.toFixed(1)}%"></span></span>
      <span class="shp-val num">${v.toFixed(2)}%</span></div>`;
  };
  const badge = (pp) => {
    if (pp === null || pp === undefined || !isFinite(Number(pp))) return "";
    const v = Number(pp);
    const cls = Math.abs(v) >= 1 ? (v > 0 ? "pos" : "neg") : "flat";
    const sign = v > 0 ? "+" : "";
    return ` <span class="qoq-badge ${cls}">${sign}${v.toFixed(2)}pp</span>`;
  };
  // one-line read: the biggest QoQ mover among promoter/FII/DII
  const flows = [
    ["Promoters", s.qoq_promoter_pp], ["FIIs", s.qoq_fii_pp], ["DIIs", s.qoq_dii_pp],
  ].filter(([, v]) => v !== null && v !== undefined && isFinite(Number(v)));
  flows.sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]));
  let read = "No material QoQ change in institutional holders.";
  if (flows.length && Math.abs(flows[0][1]) >= 1) {
    const [who, v] = flows[0];
    read = `${who} ${v > 0 ? "added" : "trimmed"} ${Math.abs(v).toFixed(2)}pp last quarter${s.quarter ? ` (${escapeHTML(s.quarter)})` : ""}.`;
    if (s.pledge_pct) read += ` Promoter pledge ${s.pledge_pct.toFixed(1)}%.`;
  } else if (s.pledge_pct) {
    read = `Promoter pledge ${s.pledge_pct.toFixed(1)}%.`;
  }
  return `<div class="panel"><div class="shp-block">
    ${bar("Promoter", s.promoter)}${badge(s.qoq_promoter_pp)}
    ${bar("FII", s.fii)}${badge(s.qoq_fii_pp)}
    ${bar("DII", s.dii)}${badge(s.qoq_dii_pp)}
    ${bar("Public", s.public)}
    <div class="shp-read">${escapeHTML(read)}</div>
    <div class="shp-src">SHP ${escapeHTML(s.quarter || "")} · via screener.in</div>
  </div></div>`;
}

/* News & corporate actions section. Renders "" when the news JSON is
   missing or the `news` array is empty — the caller also hides the section
   header, so nothing appears on the page at all. Type badges stay in this
   section only. */
function renderNewsSection(newsResult) {
  if (!newsResult || !newsResult.ok || !newsResult.news) return "";

  const items = (newsResult.news.news || []).slice(0, 20);
  if (items.length === 0) return "";

  const rows = items
    .map((item) => {
      const type = String(item.type || "news").toLowerCase();
      const typeCls = type === "announcement" ? "announcement" : "news";
      const typeLabel = typeCls === "announcement" ? "ANNOUNCEMENT" : "NEWS";
      const headline = item.headline || "(no headline)";
      const headlineHTML = item.url
        ? `<a href="${escapeHTML(item.url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(headline)}</a>`
        : escapeHTML(headline);
      return `
        <div class="news-item">
          <span class="news-date">${escapeHTML(item.date || "")}</span>
          <span class="badge news-type-${typeCls}">${typeLabel}</span>
          <span class="news-headline">${headlineHTML}</span>
          ${item.source ? `<span class="news-source">${escapeHTML(item.source)}</span>` : ""}
        </div>
      `;
    })
    .join("");

  return `<div class="news-list">${rows}</div>${newsUpdatedHTML(newsResult)}`;
}

/* Bulk & block deals section. Renders "" when the news JSON is missing or
   the `deals` array is empty. Buyer→seller flow styling, no type badges. */
function renderDealsSection(newsResult) {
  if (!newsResult || !newsResult.ok || !newsResult.news) return "";

  const deals = (newsResult.news.deals || []).slice(0, 20);
  if (deals.length === 0) return "";

  const rows = deals
    .map((d) => {
      const buyer = d.buyer ? String(d.buyer) : "";
      const seller = d.seller ? String(d.seller) : "";
      let flowHTML = "";
      if (seller || buyer) {
        flowHTML = `
          <span class="deal-flow">
            ${seller ? `<span class="deal-party seller">${escapeHTML(seller)}</span>` : `<span class="deal-party unknown">?</span>`}
            <span class="deal-arrow">&rarr;</span>
            ${buyer ? `<span class="deal-party buyer">${escapeHTML(buyer)}</span>` : `<span class="deal-party unknown">?</span>`}
          </span>`;
      }
      const meta = [d.qty, d.price ? "@ " + d.price : ""].filter(Boolean).join(" ");
      const headline = d.headline || "Bulk/block deal";
      const headlineHTML = d.url
        ? `<a href="${escapeHTML(d.url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(headline)}</a>`
        : escapeHTML(headline);
      return `
        <div class="deal-item">
          <span class="news-date">${escapeHTML(d.date || "")}</span>
          ${flowHTML}
          ${meta ? `<span class="deal-meta">${escapeHTML(meta)}</span>` : ""}
          <span class="news-headline">${headlineHTML}</span>
          ${d.source ? `<span class="news-source">${escapeHTML(d.source)}</span>` : ""}
        </div>
      `;
    })
    .join("");

  return `<div class="deal-list">${rows}</div>${newsUpdatedHTML(newsResult)}`;
}

function newsUpdatedHTML(newsResult) {
  const updated = newsResult.news && newsResult.news.updatedAt;
  return updated ? `<p class="news-updated">Updated ${escapeHTML(updated)}</p>` : "";
}

function emptyState(title, body) {
  return `<div class="empty-state"><div class="icon">&#128203;</div><h3>${escapeHTML(title)}</h3><p>${escapeHTML(body)}</p></div>`;
}
