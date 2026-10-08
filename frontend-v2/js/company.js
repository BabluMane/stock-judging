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
        "reviews/" + escapeHTML(reviewSlug(symbol)) + ".json does not exist yet, or could not be loaded."
      )}
    `;
    return;
  }

  document.title = `${review.name || symbol} — Stock-Judging`;
  const e = normalizeEntry(review);
  const news = await loadNews(symbol); // silent if missing — section just won't render
  const moves = await loadMoves(); // silent if missing — block just won't render
  const shp = await loadShp(); // silent if missing — block just won't render
  const audit = await loadAudit(symbol); // silent if missing — promise section shows empty state
  host.innerHTML = renderCompanyDetail(review, e, news, moves, shp, audit);
  mountPriceChart(symbol, review, e); // async — fills #price-chart-host when ready
  wirePromiseTracker(host); // class filters + quote expanders for the promise section

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

function renderCompanyDetail(review, e, news, moves, shp, audit) {
  // A1: the "buy at what price" answer — fair value, ACC/INV triggers, and
  // margin of safety — must read FIRST, before score breakdown or anything
  // else. This decision panel sits directly under the header.
  const newsSection = renderNewsSection(news);
  const dealsSection = renderDealsSection(news);
  const movesSection = renderMovesSection(moves, review.symbol || e.symbol);
  const shpSection = renderShpSection(shp, review.symbol || e.symbol);
  return `
    ${renderHero(review, e)}
    ${renderDecisionPanel(e)}

    <h2>Price &amp; triggers</h2>
    ${renderPriceHistoryChart(review, e)}

    <h2>Score breakdown</h2>
    ${renderScoreBreakdown(review.scores)}
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

    <h2>Promise tracker</h2>
    <p class="panel-note pt-sub">Management's word vs. delivery — graded 2 (met) / 1 (partly) / 0 (missed), recency-weighted.</p>
    ${renderPromiseTracker(audit, review)}
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
  const note = noteByCategory[catKey(e.category)] || "Category not set — treat any figures below as unconfirmed.";

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

/* v2 hero — Editorial Trading Desk: flat surface, category top-rule,
   serif display, flat dials, hairline-divided price strip. */
function renderHero(review, e) {
  const initials = logoInitials(review.name || e.name, e.symbol);
  const mos = e.marginOfSafetyPct;
  const mosCls = mos === null ? "" : mos >= 0 ? "pos" : "neg";
  const catCls = `hero-${catKey(e.category)}`;

  const dialDefs = [
    ["Composite", e.composite, "Blended quality × valuation"],
    ["Quality", e.quality, "Earnings, cash, balance sheet"],
    ["Value", e.priceScore, "Price vs fair value"],
  ];
  const dials = dialDefs.map(([label, v, note]) => `
    <div class="dial">
      ${scoreRingHTML(v, label, 84)}
      <div class="dial-text">
        <span class="dial-val">${v === null || v === undefined ? "—" : Number(v).toFixed(2)}</span>
        <span class="dial-name">${escapeHTML(label)}</span>
        <span class="dial-note">${escapeHTML(note)}</span>
      </div>
    </div>`).join("");

  const stats = [
    ["Price", fmtPrice(e.price), e.asOf ? `as of ${e.asOf}` : "", ""],
    ["Fair value", fmtPrice(e.fairValue), e.fairValue && e.price ? `${fmtPct(((e.price - e.fairValue) / e.fairValue) * 100, 0)} vs price` : "", ""],
    ["Margin of safety", fmtPct(mos, 1), mos !== null && mos >= 0 ? "discount to FV" : "premium to FV", mosCls],
  ].map(([lbl, val, sub, cls]) => `
    <div class="hero-stat">
      <span class="lbl">${lbl}</span>
      <span class="val ${cls}">${val}</span>
      ${sub ? `<span class="sub">${escapeHTML(sub)}</span>` : ""}
    </div>`).join("");

  // dial draw-on-load is additive (rings render at 0, animate to value)
  setTimeout(() => animateScoreRings(document.getElementById("content-host")), 60);

  return `
  <section class="hero ${catCls}">
    <div class="hero-inner">
      <div class="hero-kicker"><span>Review</span><span>·</span><span>${escapeHTML(e.symbol || "")}</span><span>·</span><span>${escapeHTML(e.asOf || "")}</span></div>
      <div class="hero-top">
        <div class="hero-logo">${escapeHTML(initials)}</div>
        <div class="hero-titles">
          <h1>${escapeHTML(review.name || e.symbol)}</h1>
          <p class="page-sub">
            ${review.tier ? escapeHTML(review.tier) + " tier" : ""}
            ${review.status ? " &middot; status: " + escapeHTML(review.status) : ""}
            ${e.sector ? " &middot; " + escapeHTML(e.sector) : ""}
          </p>
          <div class="hero-badge-row">
            ${verdictHTML(e.category)}
            ${e.symbol ? starButtonHTML(e.symbol, isStarred(e.symbol)) : ""}
          </div>
        </div>
      </div>
      <div class="dial-row">${dials}</div>
      <div class="hero-price-strip">${stats}</div>
    </div>
  </section>`;
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
 * Price-vs-trigger chart. review_card.schema.json has no field for a
 * historical trigger/price series — only point-in-time dcf.current_price /
 * acc_trigger / inv_trigger / fair_value as of `as_of` (schema gap flagged
 * in frontend/README.md for phase 4). Until `trigger_history` exists, the
 * chart plots the recent price series from data/sparklines.json with the
 * current valuation levels as reference lines. History accumulates as
 * re-reviews are added.
 *
 * Renders a mount placeholder synchronously; mountPriceChart() fills it
 * in after the page HTML is in the DOM.
 */
function renderPriceHistoryChart(review, e) {
  return `<div id="price-chart-host" class="price-chart-hero"><div class="skeleton-row" style="height:320px;"></div></div>
    <p class="panel-note" id="price-chart-note"></p>`;
}

/** Business-day ISO dates ending today, oldest first. */
function businessDaysBack(n) {
  const out = [];
  const d = new Date();
  while (out.length < n) {
    const dow = d.getDay();
    if (dow !== 0 && dow !== 6) out.unshift(d.toISOString().slice(0, 10));
    d.setDate(d.getDate() - 1);
  }
  return out;
}

/** Fill the #price-chart-host placeholder with a Lightweight Charts chart.
 *  Falls back to the honest empty state when the CDN or the data is missing. */
async function mountPriceChart(symbol, review, e) {
  const host = document.getElementById("price-chart-host");
  const note = document.getElementById("price-chart-note");
  const noHistory = () => {
    if (host)
      host.innerHTML = emptyState(
        "No history yet",
        "This review card has no trigger-history series (only the current point-in-time price and triggers). " +
          "A single point is plotted below once enough data exists — history accumulates as re-reviews are added."
      );
    if (note) note.remove();
  };
  if (!host) return;
  if (!window.LightweightCharts) return noHistory();

  const history = Array.isArray(review.trigger_history) ? review.trigger_history : null;
  let pricePts = null;
  let label = "";

  if (history && history.length >= 2) {
    // Full history path: price + trigger series from the review card.
    const dates = history.map((p) => p.date).filter(Boolean);
    pricePts = history
      .map((p, i) => (typeof p.price === "number" ? { time: dates[i] || businessDaysBack(history.length)[i], value: p.price } : null))
      .filter(Boolean);
    label = "Price and trigger history from re-reviews.";
  } else {
    // Phase 1: recent price series + current valuation reference lines.
    const sym = (symbol || "").toUpperCase();
    let series = null;
    try {
      const res = await fetchJSON("data/sparklines.json");
      if (res.ok && res.data && res.data.series) series = res.data.series[sym];
    } catch {
      series = null;
    }
    if (!Array.isArray(series) || series.length < 2) return noHistory();
    const days = businessDaysBack(series.length);
    pricePts = series.map((v, i) => ({ time: days[i], value: v }));
    label = "Recent price series with current valuation levels. Trigger history accumulates as re-reviews are added.";
  }

  const up = pricePts[pricePts.length - 1].value >= pricePts[0].value;
  const lineColor = up ? "#3fb950" : "#f85149";
  let chart;
  try {
    chart = window.LightweightCharts.createChart(host, {
      width: host.clientWidth || 640,
      height: 320,
      layout: {
        background: { type: "solid", color: "transparent" },
        textColor: "#8a8f98",
        fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
        fontSize: 11,
      },
      grid: {
        vertLines: { color: "rgba(236,233,226,0.06)" },
        horzLines: { color: "rgba(236,233,226,0.06)" },
      },
      rightPriceScale: { borderColor: "rgba(236,233,226,0.12)" },
      timeScale: { borderColor: "rgba(236,233,226,0.12)", timeVisible: false },
    });
    const area = chart.addAreaSeries({
      lineColor,
      topColor: hexA(lineColor, 0.22),
      bottomColor: hexA(lineColor, 0.0),
      lineWidth: 2,
      priceLineVisible: false,
      lastValueVisible: true,
    });
    area.setData(pricePts);
    const refLine = (price, color, title) => {
      if (typeof price !== "number") return;
      area.createPriceLine({
        price,
        color,
        lineWidth: 1,
        lineStyle: window.LightweightCharts.LineStyle.Dashed,
        axisLabelVisible: true,
        title,
      });
    };
    refLine(e.fairValue, "#5b9dd9", "FV");
    refLine(e.accTrigger, "#f0c96b", "ACC");
    refLine(e.invTrigger, "#6fe39a", "INV");
    chart.timeScale().fitContent();
    new ResizeObserver(() => chart.applyOptions({ width: host.clientWidth })).observe(host);
  } catch {
    if (chart) chart.remove();
    return noHistory();
  }
  if (note) note.textContent = label;
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
/* ---------- Promise tracker (Claude PROMISES audits) ----------
   Data: data/audits/<slug>.json — verbatim copies of
   ~/workspace/stock-judging/promise-tracking/audits/*.json
   (see tools/build_audits.py). The credibility score is computed
   client-side here, mirroring promise-tracking/scorer.py:
   recency weights 8..1 by position, null grades excluded with positions
   kept (G8), <3 scored calls => not executable (G7). */

const PROMISE_CLASSES = {
  1: "Revenue",
  2: "Margin",
  3: "EPS / KPI",
  4: "Capex",
  5: "Debt path",
  6: "ETR",
  7: "Timelines",
  8: "Multi-year",
  9: "Withdrawn",
  10: "Assurances",
};

async function loadAudit(symbol) {
  const { ok, data } = await fetchJSON(
    `data/audits/${encodeURIComponent(reviewSlug(symbol))}.json`
  );
  if (!ok || !data) return { ok: false, audit: null };
  return { ok: true, audit: data };
}

function numGrade(g) {
  const n = Number(g);
  return Number.isFinite(n) ? n : null;
}

/** Delivery color class from an item or call grade: pos/warn/neg/idle. */
function deliveryCls(g) {
  const n = numGrade(g);
  if (n === null) return "idle";
  return n >= 1.5 ? "pos" : n >= 0.5 ? "warn" : "neg";
}

function deliveryLabel(g) {
  const n = numGrade(g);
  if (n === null) return "pending";
  return n >= 1.5 ? "met" : n >= 0.5 ? "partly" : "missed";
}

function c5BadgeHTML(c5) {
  if (c5 === null || c5 === undefined)
    return `<span class="badge badge-unknown">C5 · n/a</span>`;
  const cls = c5 === 2 ? "badge-invest-now" : c5 === 1 ? "badge-at-trigger" : "badge-avoid";
  return `<span class="badge ${cls}">C5 · ${c5}</span>`;
}

function quarterStatusText(q) {
  const st = String(q.status || "");
  if (st === "graded") return `graded ${fmtNum(numGrade(q.grade), 1)}`;
  if (st === "pending") return "pending outcome";
  if (st === "no_promises") return "no promises";
  if (st === "no_call") return "no call";
  if (st === "not_retrieved") return "not retrieved";
  return st || "—";
}

/** Entry point: renders the full promise-tracker section. Falls back to the
 *  legacy review.promises list when no audit file exists for the company. */
function renderPromiseTracker(auditResult, review) {
  if (!auditResult || !auditResult.ok || !auditResult.audit) {
    if (review && Array.isArray(review.promises) && review.promises.length) {
      return `<div class="promise-list">${review.promises.map(renderPromiseCard).join("")}</div>`;
    }
    return emptyState(
      "No promise data yet",
      "Promise-tracking hasn't covered this company yet. Audits land here automatically once a PROMISES run completes."
    );
  }
  const audit = auditResult.audit;
  const qs = Array.isArray(audit.quarters) ? audit.quarters.slice(0, 8) : [];
  let scored = 0,
    totalPromises = 0,
    num = 0,
    den = 0;
  qs.forEach((q, i) => {
    totalPromises += (q.promises || []).length;
    const g = numGrade(q.grade);
    if (g === null) return;
    const w = 8 - i;
    num += g * w;
    den += w;
    scored += 1;
  });
  const executable = scored >= 3;
  const score = den > 0 ? (num / (2 * den)) * 10 : null;
  const c5 = !executable || score === null ? null : score >= 7 ? 2 : score >= 5 ? 1 : 0;

  if (totalPromises === 0 && scored === 0) {
    const allNoCall = qs.length > 0 && qs.every((q) => q.status === "no_call");
    return `
      <div class="panel pt-panel">
        ${renderQuarterStrip(qs)}
        ${emptyState(
          allNoCall ? "No guidance found" : "Nothing gradable yet",
          allNoCall
            ? "No earnings calls found in the last 8 quarters — this company doesn't guide publicly, so there is nothing to score."
            : "Quarters were checked but no gradable promises were found yet."
        )}
      </div>`;
  }

  return `
    <div class="panel pt-panel" id="promise-tracker">
      ${renderPromiseHeader(audit, { score, c5, scored, totalPromises, executable })}
      ${renderQuarterStrip(qs)}
      ${renderClassFilters(qs)}
      ${renderPromiseTimeline(qs)}
    </div>`;
}

function renderPromiseHeader(audit, cred) {
  const gauge =
    cred.score !== null && cred.executable
      ? scoreRingHTML(cred.score / 10, "Credibility", 84)
      : `<div class="pt-nogauge" role="img" aria-label="Credibility n/a"><span>n/a</span></div>`;
  const scoreLine =
    cred.score !== null && cred.executable
      ? `<span class="pt-score num">${fmtNum(cred.score, 1)}</span><span class="pt-scale">/ 10</span>`
      : `<span class="pt-score num muted">n/a</span>`;
  const note = audit.summary_note || audit.method_note || audit.note || "";
  return `
    <div class="pt-head">
      <div class="pt-gauge">${gauge}</div>
      <div class="pt-headtext">
        <div class="pt-scoreline">${scoreLine} ${c5BadgeHTML(cred.c5)}</div>
        <div class="pt-meta">
          <span><strong class="num">${cred.scored}</strong> calls scored</span>
          <span><strong class="num">${cred.totalPromises}</strong> promises</span>
          ${audit.review_date ? `<span>as of ${escapeHTML(audit.review_date)}</span>` : ""}
        </div>
        ${cred.executable ? "" : `<div class="pt-warnline">Too few scored calls for a credibility score — showing the raw record.</div>`}
        ${note ? `<div class="pt-note">${escapeHTML(note)}</div>` : ""}
      </div>
    </div>`;
}

function renderQuarterStrip(qs) {
  const dots = qs
    .map((q, i) => {
      const tip = `${q.label || "Q?"} — ${quarterStatusText(q)} (weight ${8 - i})`;
      return `<span class="pt-qdot ${deliveryCls(q.grade)}" title="${escapeHTML(tip)}"></span>`;
    })
    .join("");
  return `
    <div class="pt-strip">
      <span class="pt-strip-label">Quarters</span>
      <span class="pt-qdots">${dots}</span>
      <span class="pt-strip-hint">most recent →</span>
    </div>`;
}

function renderClassFilters(qs) {
  const present = [];
  qs.forEach((q) =>
    (q.promises || []).forEach((p) => {
      if (p.class && PROMISE_CLASSES[p.class] && !present.includes(p.class)) present.push(p.class);
    })
  );
  present.sort((a, b) => a - b);
  if (present.length <= 1) return "";
  const chips = [`<button class="pt-chip active" data-filter="all" type="button">All</button>`]
    .concat(
      present.map(
        (c) =>
          `<button class="pt-chip" data-filter="${c}" type="button">${escapeHTML(PROMISE_CLASSES[c])}</button>`
      )
    )
    .join("");
  return `<div class="pt-filters" role="group" aria-label="Filter promises by class">${chips}</div>`;
}

function renderPromiseTimeline(qs) {
  return qs
    .map((q) => {
      const rows = (q.promises || []).map((p) => renderPromiseRow(p)).join("");
      if (!rows) return "";
      return `
        <div class="pt-group">
          <div class="pt-grouphead">
            <span class="pt-qlabel">${escapeHTML(q.label || "")}</span>
            <span class="pt-qgrade ${deliveryCls(q.grade)}">${quarterStatusText(q)}</span>
          </div>
          ${rows}
        </div>`;
    })
    .join("");
}

function renderPromiseRow(p) {
  const clsNum = p.class;
  const clsName = PROMISE_CLASSES[clsNum] || "Other";
  const quote = String(p.quote || "—");
  const long = quote.length > 180;
  const outcome = p.outcome ? String(p.outcome) : "";
  const bits = [];
  if (p.period) bits.push(`<span class="pt-tag">${escapeHTML(p.period)}</span>`);
  if (p.date) bits.push(`<span class="pt-dim">${escapeHTML(p.date)}</span>`);
  if (p.speaker) bits.push(`<span class="pt-dim">${escapeHTML(p.speaker)}</span>`);
  return `
    <div class="pt-row" data-cls="${escapeHTML(String(clsNum || ""))}">
      <span class="pt-dot ${deliveryCls(p.item_grade)}" title="${deliveryLabel(p.item_grade)}"></span>
      <div class="pt-main">
        <p class="pt-quote${long ? " clamp" : ""}"${long ? ' title="Click to expand"' : ""}>${escapeHTML(quote)}</p>
        <div class="pt-meta"><span class="pt-class">${escapeHTML(clsName)}</span>${bits.join("")}</div>
        ${outcome ? `<p class="pt-outcome"><span class="pt-arrow">&rarr;</span> ${escapeHTML(outcome)}${p.outcome_source ? ` <span class="pt-dim">(${escapeHTML(p.outcome_source)})</span>` : ""}</p>` : ""}
        ${p.note ? `<p class="pt-note">${escapeHTML(p.note)}</p>` : ""}
      </div>
      <span class="pt-grade ${deliveryCls(p.item_grade)}">${deliveryLabel(p.item_grade)}</span>
    </div>`;
}

/** Wire class-filter chips and quote expanders after render. */
function wirePromiseTracker(host) {
  const section = (host || document).querySelector("#promise-tracker");
  if (!section) return;
  section.querySelectorAll(".pt-quote.clamp").forEach((el) => {
    el.addEventListener("click", () => el.classList.toggle("open"));
  });
  const chips = section.querySelectorAll(".pt-chip");
  if (!chips.length) return;
  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      chips.forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");
      const f = chip.dataset.filter;
      section.querySelectorAll(".pt-row").forEach((row) => {
        row.style.display = f === "all" || row.dataset.cls === f ? "" : "none";
      });
      section.querySelectorAll(".pt-group").forEach((g) => {
        const visible = [...g.querySelectorAll(".pt-row")].some(
          (r) => r.style.display !== "none"
        );
        g.style.display = visible ? "" : "none";
      });
    });
  });
}
