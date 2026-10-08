/* leaderboard.js (v2) — Editorial Trading Desk ledger.
   Hairline-divided rows: index, identity, verdict, score, price, spark, chips.
   Presentational markup only; data flow, filters, sort, stars unchanged. */

function skeletonCardsHTML() {
  const rows = Array.from({ length: 8 }, () => `<div class="skeleton-row"></div>`).join("");
  return `<div class="skeleton-rows" aria-hidden="true" aria-label="Loading leaderboard">${rows}</div>`;
}

const LB_SORTS = [
  { key: "composite", label: "Composite", tip: "Overall engine score 0–1: blends quality and valuation. Higher = stronger overall case." },
  { key: "quality", label: "Quality", tip: "Business quality 0–1: earnings strength, cash conversion, balance sheet, governance. Higher = better company." },
  { key: "priceScore", label: "Value", tip: "Valuation score 0–1: how attractive the current price is vs fair value. Higher = cheaper vs what it's worth." },
  { key: "marginOfSafetyPct", label: "Margin of Safety", tip: "How far below fair value the price sits, as a %. Positive = trading at a discount; negative = trading at a premium." },
  { key: "price", label: "Price", tip: "Market price at the time of review (₹)." },
  { key: "name", label: "Name", tip: "Company name — click a row to open the full review." },
];

const LB_COLS = [
  { key: "idx", label: "", cls: "idxcol", sortable: false },
  { key: "name", label: "Company", cls: "", sortable: true },
  { key: "category", label: "Verdict", cls: "verdictcol", sortable: false },
  { key: "composite", label: "Score", cls: "num", sortable: true },
  { key: "price", label: "Price vs FV", cls: "num", sortable: true },
  { key: "spark", label: "Trend", cls: "sparkcol", sortable: false },
];

let LB_STATE = { entries: [], sortKey: "composite", sortDir: "desc", filter: "ALL", sparks: {} };

async function initLeaderboardPage() {
  const errorHost = document.getElementById("error-host");
  const tableHost = document.getElementById("table-host");
  const filtersHost = document.getElementById("filters");

  tableHost.innerHTML = skeletonCardsHTML();
  const { ok, companies, error } = await loadLeaderboard();
  const sparks = await loadSparklines();

  if (!ok) {
    errorHost.innerHTML = `<div class="error-state">${escapeHTML(error)}</div>`;
    tableHost.innerHTML = emptyStateHTML(
      "No leaderboard data loaded",
      "The leaderboard could not be read. See the notice above."
    );
    return;
  }

  if (companies.length === 0) {
    tableHost.innerHTML = emptyStateHTML(
      "No reviews yet",
      "leaderboard.json is currently empty — no companies have been reviewed. Queue one from the “Run a Company” page."
    );
    return;
  }

  LB_STATE.entries = companies.map(normalizeEntry);
  LB_STATE.sparks = sparks.ok ? sparks.series : {};
  filtersHost.style.display = "flex";
  wireFilters();
  renderTicker();
  renderLeaderboardCards();
}

function wireFilters() {
  const filtersHost = document.getElementById("filters");
  filtersHost.querySelectorAll(".filter-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      filtersHost.querySelectorAll(".filter-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      LB_STATE.filter = btn.dataset.cat;
      renderLeaderboardCards();
    });
  });
}

/** Signature ticker strip: SYM price ±chg% for every covered name, duplicated for the marquee loop. */
function renderTicker() {
  const host = document.getElementById("ticker-host");
  if (!host) return;
  const items = LB_STATE.entries.map((e) => {
    const series = LB_STATE.sparks[(e.symbol || "").toUpperCase()];
    let chg = null;
    if (Array.isArray(series) && series.length >= 2 && series[0]) {
      chg = ((series[series.length - 1] - series[0]) / series[0]) * 100;
    }
    const cls = chg === null ? "" : chg >= 0 ? "up" : "dn";
    const chgTxt = chg === null ? "—" : (chg >= 0 ? "+" : "") + chg.toFixed(1) + "%";
    return `<span class="ticker-item"><span class="tsym">${escapeHTML(e.symbol || "")}</span><span class="tprice">${fmtPrice(e.price)}</span><span class="tchg ${cls}">${chgTxt}</span></span>`;
  }).join("");
  host.innerHTML = `<div class="ticker-track">${items}${items}</div>`;
}

function sortEntries(entries, key, dir) {
  const sorted = [...entries].sort((a, b) => {
    let av = a[key];
    let bv = b[key];
    if (av === null || av === undefined) return 1;
    if (bv === null || bv === undefined) return -1;
    if (typeof av === "string") av = av.toLowerCase();
    if (typeof bv === "string") bv = bv.toLowerCase();
    if (av < bv) return dir === "asc" ? -1 : 1;
    if (av > bv) return dir === "asc" ? 1 : -1;
    return 0;
  });
  return sorted;
}

function scoreColor(v) {
  if (v === null || v === undefined) return "var(--text-faint)";
  return v >= 0.7 ? "var(--pos)" : v >= 0.45 ? "var(--warn)" : "var(--neg)";
}

/** Semicircular score gauge: visual first, digits second.
 *  Arc sweeps 180°, number sits inside. Animates on mount. */
function scoreGaugeHTML(score) {
  const v = (score === null || score === undefined || Number.isNaN(Number(score))) ? null : Math.max(0, Math.min(1, Number(score)));
  const w = 76, h = 46, r = 32, cx = 38, cy = 40;
  const circ = Math.PI * r; // semicircle length
  const frac = v === null ? 0 : v;
  const color = v === null ? "#6e6a61" : v >= 0.7 ? "#3fb950" : v >= 0.45 ? "#d29922" : "#f85149";
  const dashTarget = (circ * (1 - frac)).toFixed(1);
  // semicircle path: M left-arc to right-arc
  const d = `M ${cx - r} ${cy} A ${r} ${r} 0 0 1 ${cx + r} ${cy}`;
  return `
  <div class="score-gauge" role="img" aria-label="Score ${v === null ? "n/a" : v.toFixed(2)}">
    <svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
      <path class="gauge-bg" d="${d}" stroke-width="6"/>
      <path class="gauge-fg" d="${d}" stroke-width="6" style="--gauge-color:${color};"
        stroke-dasharray="${circ.toFixed(1)}" stroke-dashoffset="${circ.toFixed(1)}"
        data-gauge-target="${dashTarget}"/>
    </svg>
    <span class="gauge-num">${v === null ? "—" : v.toFixed(2)}</span>
    <span class="gauge-lbl">Score</span>
  </div>`;
}

/** Animate gauges in after paint (same pattern as score rings). */
function animateGauges(host) {
  const els = (host || document).querySelectorAll(".gauge-fg[data-gauge-target]");
  requestAnimationFrame(() => requestAnimationFrame(() => {
    els.forEach((el) => el.setAttribute("stroke-dashoffset", el.dataset.gaugeTarget));
  }));
}

/** Price-vs-FV meter: visual bar showing where price sits relative to
 *  fair value. The "buy zone" (below FV) is shaded; the price dot glides
 *  to its position. Replaces the MoS text chip — position > digits. */
function fvMeterHTML(entry) {
  const price = entry.price, fv = entry.fairValue;
  if (!price || !fv) {
    return `<div class="fv-meter"><div class="fv-meter-labels">
      <span class="fv-meter-price-lbl">${fmtPrice(price)}</span>
      <span class="fv-meter-mos">—</span></div></div>`;
  }
  const mos = entry.marginOfSafetyPct;
  const mosCls = mos === null ? "" : mos >= 0 ? "pos" : "neg";
  // scale: map [0.5×FV, 1.5×FV] → [0%, 100%]; price dot position
  const lo = fv * 0.5, hi = fv * 1.5;
  const clamp = (x) => Math.max(0, Math.min(100, ((x - lo) / (hi - lo)) * 100));
  const pricePct = clamp(price);
  const fvPct = clamp(fv);
  const zoneLeft = clamp(lo), zoneRight = clamp(fv);
  const over = price > fv;
  return `
  <div class="fv-meter" role="img" aria-label="Price ${fmtPrice(price)}, fair value ${fmtPrice(fv)}, margin of safety ${mos === null ? "n/a" : fmtPct(mos, 0)}">
    <div class="fv-meter-track">
      <div class="fv-meter-zone" style="left:${zoneLeft.toFixed(1)}%;width:${(zoneRight - zoneLeft).toFixed(1)}%;"></div>
      <div class="fv-meter-fv" style="left:${fvPct.toFixed(1)}%;"></div>
      <div class="fv-meter-price${over ? " over" : ""}" data-price-target="${pricePct.toFixed(1)}" style="left:${pricePct.toFixed(1)}%;"></div>
    </div>
    <div class="fv-meter-labels">
      <span class="fv-meter-price-lbl">${fmtPrice(price)}</span>
      <span class="fv-meter-mos ${mosCls}">${mos === null ? "—" : fmtPct(mos, 0) + " MoS"}</span>
    </div>
  </div>`;
}

function coRowHTML(e, idx) {
  const initials = logoInitials(e.name, e.symbol);
  const series = LB_STATE.sparks[(e.symbol || "").toUpperCase()];

  return `
  <div class="co-row vrow-${catKey(e.category).toLowerCase()}" data-symbol="${escapeHTML(e.symbol || "")}" tabindex="0" role="link" style="--row-i:${idx};" aria-label="${escapeHTML(e.name)} — ${escapeHTML(categoryMeta(e.category).label)}">
    <span class="row-idx">${String(idx + 1).padStart(2, "0")}</span>
    <div class="co-id">
      <div class="co-logo">${escapeHTML(initials)}</div>
      <div class="co-name-block">
        <div class="co-name">${escapeHTML(e.name)}</div>
        <div class="co-meta"><span>${escapeHTML(e.symbol || "")}</span>${e.symbol ? starButtonHTML(e.symbol, isStarred(e.symbol)) : ""}${e.asOf ? `<span>${escapeHTML(e.asOf)}</span>` : ""}</div>
      </div>
    </div>
    <div class="verdictcell">${verdictHTML(e.category)}</div>
    <div class="co-score num">${scoreGaugeHTML(e.composite)}</div>
    <div class="co-priceblock num">${fvMeterHTML(e)}</div>
    <div class="co-sparkcell">${sparklineHTML(series, 230, 56)}</div>
  </div>`;
}

function renderLeaderboardCards() {
  const tableHost = document.getElementById("table-host");
  let entries = LB_STATE.entries;
  if (LB_STATE.filter === "STARRED") {
    entries = entries.filter((e) => isStarred(e.symbol));
  } else if (LB_STATE.filter !== "ALL") {
    entries = entries.filter((e) => e.category === LB_STATE.filter);
  }
  entries = sortEntries(entries, LB_STATE.sortKey, LB_STATE.sortDir);

  const sortBarHTML = `
    <div class="sort-bar">
      <span class="sort-label">Sort</span>
      ${LB_SORTS.map((s) => {
        const active = s.key === LB_STATE.sortKey;
        const arrow = active ? `<span class="arrow">${LB_STATE.sortDir === "asc" ? "▲" : "▼"}</span>` : "";
        return `<button class="sort-opt${active ? " active" : ""}" data-sort="${s.key}" title="${escapeHTML(s.tip)}">${escapeHTML(s.label)}${arrow}</button>`;
      }).join("")}
    </div>`;

  if (entries.length === 0) {
    tableHost.innerHTML = sortBarHTML + emptyStateHTML(
      LB_STATE.filter === "STARRED" ? "No starred companies" : "No companies in this category",
      LB_STATE.filter === "STARRED"
        ? "Tap the ☆ on any row to star it — starred companies live here."
        : "Try a different filter above."
    );
    wireSortBar(tableHost);
    wireRowNav(tableHost);
    const countHostEmpty = document.getElementById("filter-count");
    if (countHostEmpty) countHostEmpty.textContent = `0 of ${LB_STATE.entries.length} shown`;
    return;
  }

  const headHTML = LB_COLS.map((c) => {
    const active = c.key === LB_STATE.sortKey;
    const arrow = active ? `<span class="sort-arrow">${LB_STATE.sortDir === "asc" ? "▲" : "▼"}</span>` : "";
    return `<span class="${c.cls}${c.sortable ? " sortable" : ""}${c.key === "composite" || c.key === "price" ? " num" : ""}" data-sort="${c.key}" data-sortable="${c.sortable}">${escapeHTML(c.label)}${arrow}</span>`;
  }).join("");

  tableHost.innerHTML = sortBarHTML + `
    <div class="ledger" role="table" aria-label="Reviewed companies">
      <div class="ledger-head" role="row">${headHTML}</div>
      ${entries.map((e, i) => coRowHTML(e, i)).join("")}
    </div>`;

  const countHost = document.getElementById("filter-count");
  if (countHost) {
    countHost.textContent = `${entries.length} of ${LB_STATE.entries.length} shown`;
  }

  wireSortBar(tableHost);
  // header sorting
  tableHost.querySelectorAll(".ledger-head .sortable").forEach((el) => {
    el.addEventListener("click", () => {
      const key = el.dataset.sort;
      if (LB_STATE.sortKey === key) {
        LB_STATE.sortDir = LB_STATE.sortDir === "asc" ? "desc" : "asc";
      } else {
        LB_STATE.sortKey = key;
        LB_STATE.sortDir = key === "name" ? "asc" : "desc";
      }
      renderLeaderboardCards();
    });
  });
  wireRowNav(tableHost);
  mountUplotSparks(tableHost); // crisp uPlot sparklines when CDN loaded; SVG fallback otherwise
  animateGauges(tableHost); // sweep the score arcs in after paint
}

function wireRowNav(tableHost) {
  tableHost.querySelectorAll(".co-row").forEach((row) => {
    const go = () => {
      const symbol = row.dataset.symbol;
      if (symbol) window.location.href = `company.html?symbol=${encodeURIComponent(symbol)}`;
    };
    row.addEventListener("click", (evt) => {
      if (evt.target.closest(".star-btn")) return;
      go();
    });
    row.addEventListener("keydown", (evt) => {
      if (evt.key === "Enter" || evt.key === " ") { evt.preventDefault(); go(); }
    });
  });
  tableHost.querySelectorAll(".star-btn").forEach((btn) => {
    btn.addEventListener("click", (evt) => {
      evt.stopPropagation();
      const symbol = btn.dataset.starSymbol;
      if (!symbol) return;
      const now = toggleStarred(symbol);
      btn.classList.toggle("starred", now);
      btn.textContent = now ? "★" : "☆";
      btn.setAttribute("aria-label", `${now ? "Unstar" : "Star"} ${symbol}`);
      if (LB_STATE.filter === "STARRED") renderLeaderboardCards();
    });
  });
}

function wireSortBar(host) {
  host.querySelectorAll(".sort-opt").forEach((btn) => {
    btn.addEventListener("click", () => {
      const key = btn.dataset.sort;
      if (LB_STATE.sortKey === key) {
        LB_STATE.sortDir = LB_STATE.sortDir === "asc" ? "desc" : "asc";
      } else {
        LB_STATE.sortKey = key;
        LB_STATE.sortDir = key === "name" ? "asc" : "desc";
      }
      renderLeaderboardCards();
    });
  });
}

function emptyStateHTML(title, body) {
  return `
    <div class="empty-state">
      <h3>${escapeHTML(title)}</h3>
      <p>${escapeHTML(body)}</p>
    </div>
  `;
}
