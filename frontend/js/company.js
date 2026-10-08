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

    <h2>Engine gates — the "why"</h2>
    ${renderEngineGates(review.engine)}

    <h2>Valuation breakdown</h2>
    ${renderValuationBreakdown(review.dcf, e)}

    <h2>Unified model status</h2>
    ${renderUnifiedModelStatus(review, e)}

    <h2>Price vs. trigger history</h2>
    ${renderPriceHistoryChart(review, e)}

    <h2>All metrics</h2>
    ${renderAllMetrics(review.key_metrics)}
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

/* ------------------------------------------------------------------
   Engine gates — the "why". Each gate (distress, event_lane, usability,
   anchor) renders as a PASS/FAIL card with its explanation text. The
   deciding gate is highlighted.
   ------------------------------------------------------------------ */
function renderEngineGates(engine) {
  if (!engine || typeof engine !== "object") {
    return emptyState("No engine data", "This review card has no `engine` breakdown.");
  }
  const gateOrder = ["distress", "event_lane", "usability", "anchor"];
  const gateLabels = {
    distress: "Distress screen",
    event_lane: "Event lane",
    usability: "Usability",
    anchor: "Anchor / valuation",
  };
  const deciding = (engine.deciding_gate || "").toLowerCase();
  const cards = gateOrder
    .filter((g) => engine[g] !== undefined && engine[g] !== null && engine[g] !== "")
    .map((g) => {
      const text = String(engine[g]);
      const up = text.toUpperCase();
      const verdict = up.startsWith("PASS") ? "pass" : up.startsWith("FAIL") || up.startsWith("VETO") ? "fail" : "other";
      const body = text.replace(/^(PASS|FAIL|VETO)\s*[—–-]\s*/i, "");
      const isDeciding = g === deciding;
      return `
        <div class="gate-card gate-${verdict}${isDeciding ? " gate-deciding" : ""}">
          <div class="gate-head">
            <span class="gate-name">${escapeHTML(gateLabels[g] || g)}</span>
            <span class="gate-verdict">${verdict === "other" ? "—" : verdict.toUpperCase()}</span>
            ${isDeciding ? `<span class="gate-deciding-tag">deciding gate</span>` : ""}
          </div>
          <div class="gate-body">${escapeHTML(body)}</div>
        </div>`;
    })
    .join("");
  let extra = "";
  if (engine.deciding_stop) extra += `<p class="panel-note">Deciding stop: ${escapeHTML(String(engine.deciding_stop))}</p>`;
  if (engine.excluded_on) extra += `<p class="panel-note">Excluded on: ${escapeHTML(String(engine.excluded_on))}</p>`;
  if (engine.watch_condition) extra += `<p class="panel-note">Watch condition: ${escapeHTML(String(engine.watch_condition))}</p>`;
  if (engine.version) extra += `<p class="panel-note">Engine version: ${escapeHTML(String(engine.version))}</p>`;
  if (!cards) return emptyState("No gates recorded", "This review card's `engine` block has no gate results.");
  return `<div class="gate-grid">${cards}</div>${extra}`;
}

/* ------------------------------------------------------------------
   Valuation breakdown — DCF fair value, triggers on a visual price
   scale, and the model description in plain English.
   ------------------------------------------------------------------ */
function renderValuationBreakdown(dcf, e) {
  if (!dcf || typeof dcf !== "object" || !isFinite(Number(dcf.fair_value))) {
    return emptyState("No valuation data", "This review card has no `dcf` breakdown.");
  }
  const fv = Number(dcf.fair_value);
  const price = isFinite(Number(dcf.current_price)) ? Number(dcf.current_price) : null;
  const inv = isFinite(Number(dcf.inv_trigger)) ? Number(dcf.inv_trigger) : null;
  const acc = isFinite(Number(dcf.acc_trigger)) ? Number(dcf.acc_trigger) : null;
  const premium = price !== null ? ((price - fv) / fv) * 100 : null;

  // Price scale: position markers on a 0..max line
  const vals = [fv, price, inv, acc].filter((v) => isFinite(v));
  const lo = Math.min(...vals) * 0.9;
  const hi = Math.max(...vals) * 1.05;
  const span = hi - lo || 1;
  const pct = (v) => (((v - lo) / span) * 100).toFixed(1);
  const marker = (v, label, cls) =>
    isFinite(v)
      ? `<div class="scale-marker ${cls}" style="left:${pct(v)}%"><span class="scale-pin"></span><span class="scale-label">${label}<br><b>${fmtPrice(v)}</b></span></div>`
      : "";
  const scale = `
    <div class="price-scale">
      ${marker(fv, "Fair value", "m-fv")}
      ${marker(acc, "ACC trigger", "m-acc")}
      ${marker(inv, "INV trigger", "m-inv")}
      ${marker(price, "Current price", "m-price")}
      <div class="scale-track"></div>
    </div>`;

  const rank = valuationRank(premium);
  const modelPlain = plainEnglishModel(String(dcf.model || ""));

  return `
    <div class="panel">
      <div class="val-grid">
        <div class="stat"><span class="label">DCF fair value</span><span class="value">${fmtPrice(fv)}</span></div>
        <div class="stat"><span class="label">Current price</span><span class="value">${price !== null ? fmtPrice(price) : "—"}</span></div>
        <div class="stat"><span class="label">Premium / discount</span><span class="value hero ${premium !== null && premium < 0 ? "pos" : "neg"}">${premium !== null ? fmtPct(premium) : "—"}</span></div>
        <div class="stat"><span class="label">Valuation rank</span><span class="value">${rank.label}</span></div>
      </div>
      ${scale}
      <p class="panel-note"><strong>Model:</strong> ${escapeHTML(modelPlain)}</p>
    </div>`;
}

function plainEnglishModel(model) {
  // Keep the engine's raw model string; translate the jargon pieces.
  return model
    .replace(/inverse excess-return/i, "inverse excess-return (backs out the growth the current price implies)")
    .replace(/g_sus/i, "sustainable growth")
    .replace(/w /i, "discount rate ");
}

/* ------------------------------------------------------------------
   Unified model status — valuation rank, entry timing, position
   guidance. Entry timing needs live 52w data not yet in review JSONs.
   ------------------------------------------------------------------ */
function valuationRank(premiumPct) {
  if (premiumPct === null || !isFinite(premiumPct)) return { rank: null, label: "—" };
  if (premiumPct < -50) return { rank: 1, label: "Rank 1 · Deep cheap" };
  if (premiumPct < -20) return { rank: 2, label: "Rank 2 · Cheap" };
  if (premiumPct <= 20) return { rank: 3, label: "Rank 3 · Fair" };
  return { rank: 4, label: "Rank 4 · Expensive" };
}

function renderUnifiedModelStatus(review, e) {
  const dcf = review.dcf || {};
  const fv = Number(dcf.fair_value);
  const price = Number(dcf.current_price);
  const premium = isFinite(fv) && isFinite(price) ? ((price - fv) / fv) * 100 : null;
  const rank = valuationRank(premium);
  const cat = e.category || (review.verdict && review.verdict.category) || "—";

  // Position guidance from UNIFIED_MODEL.md: no hard stop; size for −30%
  // DD; scale out 1/3 at +50% and +100%; speed check at 25 trading days.
  const so1 = isFinite(price) ? price * 1.5 : null;
  const so2 = isFinite(price) ? price * 2.0 : null;
  const stop = isFinite(price) ? price * 0.7 : null;
  const conviction = review.conviction !== undefined ? Number(review.conviction) : null;
  const sizeNote = conviction !== null && isFinite(conviction)
    ? (conviction >= 0.7 ? "Full size" : conviction >= 0.5 ? "Standard size" : "Reduced size")
    : "Standard size";

  return `
    <div class="panel">
      <div class="um-grid">
        <div class="um-step">
          <div class="um-step-label">1 · Review</div>
          <div class="um-step-value">${escapeHTML(cat.replace(/_/g, " "))}</div>
          <div class="um-step-note">engine verdict</div>
        </div>
        <div class="um-step">
          <div class="um-step-label">2 · Valuation rank</div>
          <div class="um-step-value">${escapeHTML(rank.label)}</div>
          <div class="um-step-note">${premium !== null ? fmtPct(premium) + " vs fair value" : "premium unknown"}</div>
        </div>
        <div class="um-step">
          <div class="um-step-label">3 · Entry timing</div>
          <div class="um-step-value um-pending">Data pending</div>
          <div class="um-step-note">needs live 52w high/low — not yet wired</div>
        </div>
        <div class="um-step">
          <div class="um-step-label">4 · Position</div>
          <div class="um-step-value">${escapeHTML(sizeNote)}</div>
          <div class="um-step-note">no hard stop · size for −30% DD</div>
        </div>
      </div>
      <p class="panel-note">Scale out: 1/3 at ${so1 !== null ? fmtPrice(so1) : "—"} (+50%) and 1/3 at ${so2 !== null ? fmtPrice(so2) : "—"} (+100%). Sizing stop: ${stop !== null ? fmtPrice(stop) : "—"} (−30%). Speed check: +20% within ~25 trading days or re-evaluate.</p>
    </div>`;
}

/* ------------------------------------------------------------------
   Full metrics table — every key_metric in a dense two-column table.
   ------------------------------------------------------------------ */
function humanizeMetricKey(k) {
  let s = String(k)
    .replace(/_pct$/i, " %")
    .replace(/_rs$/i, " (₹)")
    .replace(/_cr$/i, " (₹ cr)")
    .replace(/_fy(\d+)/i, " FY$1")
    .replace(/_/g, " ");
  s = s.replace(/\b\w/g, (c) => c.toUpperCase());
  return s
    .replace(/\bEps\b/, "EPS").replace(/\bRoa\b/, "RoA").replace(/\bRoe\b/, "RoE")
    .replace(/\bNim\b/, "NIM").replace(/\bGnpa\b/, "GNPA").replace(/\bNnpa\b/, "NNPA")
    .replace(/\bPcr\b/, "PCR").replace(/\bCasa\b/, "CASA").replace(/\bCar\b/, "CAR")
    .replace(/\bPb\b/, "P/B").replace(/\bPe\b/, "P/E").replace(/\bPat\b/, "PAT")
    .replace(/\bMcap\b/, "M-cap");
}

function renderAllMetrics(keyMetrics) {
  if (!keyMetrics || typeof keyMetrics !== "object" || Object.keys(keyMetrics).length === 0) {
    return emptyState("No metrics", "This review card has no `key_metrics`.");
  }
  const rows = Object.entries(keyMetrics)
    .map(([k, v]) => {
      const val = typeof v === "number" ? fmtNum(v, 2) : String(v);
      return `<tr><td class="metric-key">${escapeHTML(humanizeMetricKey(k))}</td><td class="metric-val num">${escapeHTML(val)}</td></tr>`;
    })
    .join("");
  return `<div class="panel panel-tight"><table class="metrics-table"><tbody>${rows}</tbody></table></div>`;
}
