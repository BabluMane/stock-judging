/* data.js — shared data access + formatting helpers.
   Reads only: ../leaderboard.json and ../reviews/*.json. Never writes them.
   All fetches are defensive: file:// blocks XHR/fetch to local files in most
   browsers (Chrome/Edge refuse cross-origin file: reads), so every call here
   catches and reports instead of throwing. */

const CATEGORY_META = {
  INVEST_NOW: { label: "INVEST NOW", cls: "badge-invest-now" },
  AT_TRIGGER: { label: "INVEST AT TRIGGER", cls: "badge-at-trigger" },
  WATCH: { label: "WATCH", cls: "badge-watch" },
  PASS: { label: "PASS", cls: "badge-pass" },
  AVOID: { label: "AVOID", cls: "badge-avoid" },
};

/** Normalize a category string ("INVEST NOW" / "invest-now") to the
 *  canonical key form ("INVEST_NOW"). Data uses spaces; code uses keys. */
function catKey(category) {
  return String(category || "").toUpperCase().replace(/[\s-]+/g, "_") || "UNKNOWN";
}

/** Review/news files are keyed by lowercase slug ("J&KBANK" -> "jkbank"),
 *  while leaderboard symbols are exchange tickers. Normalize before fetch —
 *  without this, company.html 404s on any ticker with non-alphanumerics. */
function reviewSlug(symbol) {
  return String(symbol || "").toLowerCase().replace(/[^a-z0-9]/g, "");
}

function categoryMeta(category) {
  return CATEGORY_META[catKey(category)] || { label: category || "UNKNOWN", cls: "badge-unknown" };
}

function categoryBadgeHTML(category) {
  const meta = categoryMeta(category);
  return `<span class="badge ${meta.cls}">${escapeHTML(meta.label)}</span>`;
}

/** Flat verdict marker: 8px square + uppercase label. Swiss, semantic. */
function verdictHTML(category) {
  const key = catKey(category).toLowerCase().replace(/_/g, "-");
  const meta = categoryMeta(category);
  return `<span class="verdict v-${key}">${escapeHTML(meta.label)}</span>`;
}

function escapeHTML(s) {
  if (s === null || s === undefined) return "";
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function fmtNum(x, digits = 1) {
  if (x === null || x === undefined || Number.isNaN(x)) return "—";
  return Number(x).toFixed(digits);
}

function fmtPrice(x, currency = "₹") {
  if (x === null || x === undefined || Number.isNaN(x)) return "—";
  return currency + Number(x).toLocaleString("en-IN", { maximumFractionDigits: 2 });
}

function fmtPct(x, digits = 1) {
  if (x === null || x === undefined || Number.isNaN(x)) return "—";
  const v = Number(x);
  return (v > 0 ? "+" : "") + v.toFixed(digits) + "%";
}

function fmtDate(x) {
  if (!x) return "—";
  return x;
}

/**
 * Fetch JSON from a path relative to the frontend/ directory's parent
 * (i.e. the repo root). Returns { ok, data, error }.
 */
async function fetchJSON(path) {
  if (window.location.protocol === "file:") {
    // Chromium/Edge log a CORS failure to the console for any fetch() of a
    // local file from a file:// page, even when the rejection is caught —
    // the browser's network log fires before our catch block does. Skip the
    // call entirely under file:// so the console stays clean; a static
    // server is required to actually load data (documented in README).
    return {
      ok: false,
      data: null,
      error:
        `Can't load ${path} from a file:// page — browsers block local JSON ` +
        `fetches from disk. Serve the repo root with a static server instead, ` +
        `e.g. "python3 -m http.server" from the repo root, then open ` +
        `http://localhost:8000/frontend/.`,
    };
  }
  try {
    const res = await fetch(path, { cache: "no-store" });
    if (!res.ok) {
      return { ok: false, data: null, error: `HTTP ${res.status} fetching ${path}` };
    }
    const data = await res.json();
    return { ok: true, data, error: null };
  } catch (err) {
    return {
      ok: false,
      data: null,
      error:
        `Could not load ${path}. If you opened this page directly from disk ` +
        `(a file:// URL), most browsers block JSON fetches from local files. ` +
        `Serve the repo root with a static server instead, e.g. ` +
        `"python3 -m http.server" from the repo root, then open ` +
        `http://localhost:8000/frontend/. (${err && err.message ? err.message : err})`,
    };
  }
}

/** Load leaderboard.json (repo root). Normalizes to always return an array. */
async function loadLeaderboard() {
  const { ok, data, error } = await fetchJSON("../leaderboard.json");
  if (!ok) return { ok, companies: [], generatedAt: null, error };
  const companies = Array.isArray(data.companies) ? data.companies : [];
  return { ok: true, companies, generatedAt: data.generated_at || null, error: null };
}

/** Load a single review card by symbol from reviews/<slug>.json.
 *  reviewSlug() maps exchange tickers ("J&KBANK") to file slugs ("jkbank"). */
async function loadReview(symbol) {
  const { ok, data, error } = await fetchJSON(`../reviews/${encodeURIComponent(reviewSlug(symbol))}.json`);
  return { ok, review: ok ? data : null, error };
}

/**
 * Load the news feed for a symbol from news/<symbol>.json. A missing file
 * (404) is a normal state — not every company has news tracked — so callers
 * should treat !ok as "no news sections", not an error.
 *
 * Shape: { symbol, updated_at, news: [{date,type,headline,source,url}],
 *           deals: [{date,headline,buyer,seller,qty,price,source,url}] }.
 * The legacy single-array shape { items: [...] } is treated as `news`.
 */
async function loadNews(symbol) {
  const { ok, data } = await fetchJSON(`../news/${encodeURIComponent(reviewSlug(symbol))}.json`);
  if (!ok || !data) return { ok: false, news: null };
  const newsItems = Array.isArray(data.news)
    ? data.news
    : Array.isArray(data.items)
      ? data.items
      : [];
  const deals = Array.isArray(data.deals) ? data.deals : [];
  return {
    ok: true,
    news: { symbol: data.symbol || symbol, updatedAt: data.updated_at || null, news: newsItems, deals },
  };
}

/**
 * Load the big-moves feed from data/moves.json. Shape:
 * { updated_at, moves: [{date, symbol, move_pct, window, why, sources[]}] }.
 * A missing file is normal — returns an empty moves list, not an error.
 */
async function loadMoves() {
  const { ok, data } = await fetchJSON("data/moves.json");
  if (!ok || !data) return { ok: false, moves: [] };
  const moves = Array.isArray(data.moves) ? data.moves : [];
  return { ok: true, moves, updatedAt: data.updated_at || null };
}

async function loadShp() {
  const { ok, data } = await fetchJSON("data/shp.json");
  if (!ok || !data) return { ok: false, companies: {} };
  return { ok: true, companies: data.companies || {}, updatedAt: data.updated_at || null };
}

/**
 * Load sparkline price series from data/sparklines.json (v2).
 * Shape: { updated_at, series: { SYMBOL: [close, ...] | null } }.
 * A missing file is normal — cards render a neutral placeholder instead.
 */
async function loadSparklines() {
  const { ok, data } = await fetchJSON("data/sparklines.json");
  if (!ok || !data) return { ok: false, series: {} };
  return { ok: true, series: data.series || {} };
}

/** Deterministic logo initials tile — flat, hairline, serif. No gradients. */
function logoGradient(symbol) {
  return { a: null, b: null };
}

/** Two-letter logo initials from a company name. */
function logoInitials(name, symbol) {
  const n = String(name || "").trim();
  if (n) {
    const words = n.split(/\s+/).filter(Boolean);
    if (words.length >= 2) return (words[0][0] + words[1][0]).toUpperCase();
    return n.slice(0, 2).toUpperCase();
  }
  return String(symbol || "?").slice(0, 2).toUpperCase();
}

/** SVG score ring (0..1). Flat stroke, no glow. Additive draw-on-load. */
function scoreRingHTML(score, label, size) {
  const v = (score === null || score === undefined || Number.isNaN(Number(score))) ? null : Math.max(0, Math.min(1, Number(score)));
  const r = (size / 2) - 6;
  const circ = 2 * Math.PI * r;
  const frac = v === null ? 0 : v;
  const color = v === null ? "var(--text-faint)" : v >= 0.7 ? "var(--pos)" : v >= 0.45 ? "var(--warn)" : "var(--neg)";
  return `
    <div class="score-ring" style="width:${size}px;height:${size}px;--ring-color:${color};" role="img" aria-label="${escapeHTML(label)} ${v === null ? "n/a" : v.toFixed(2)}">
      <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
        <circle class="ring-bg" cx="${size/2}" cy="${size/2}" r="${r}" stroke-width="6"/>
        <circle class="ring-fg" cx="${size/2}" cy="${size/2}" r="${r}" stroke-width="6"
          stroke-dasharray="${circ.toFixed(1)}" stroke-dashoffset="${circ.toFixed(1)}"
          data-ring-target="${(circ * (1 - frac)).toFixed(1)}"/>
      </svg>
    </div>`;
}

/** Animate score rings in: set final dashoffset after paint. */
function animateScoreRings(host) {
  const rings = (host || document).querySelectorAll(".ring-fg[data-ring-target]");
  requestAnimationFrame(() => requestAnimationFrame(() => {
    rings.forEach((el) => el.setAttribute("stroke-dashoffset", el.dataset.ringTarget));
  }));
}

/** Convert #rrggbb + alpha (0-1) to an rgba() string. */
function hexA(hex, alpha) {
  const m = /^#?([0-9a-f]{6})$/i.exec(String(hex || ""));
  if (!m) return hex;
  const n = parseInt(m[1], 16);
  return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${alpha})`;
}

/** SVG sparkline from a price series. Flat 1.5px line + endpoint dot.
 *  Color encodes direction only (up/down). Dashed hairline when no data.
 *  Used as the no-JS/offline fallback; uPlot replaces it when available. */
function sparklineSVG(series, w, h) {
  if (!Array.isArray(series) || series.length < 2) {
    return `<svg class="co-spark" viewBox="0 0 ${w} ${h}" aria-hidden="true"><line x1="0" y1="${h/2}" x2="${w}" y2="${h/2}" stroke="rgba(236,233,226,0.15)" stroke-width="1" stroke-dasharray="4 4"/></svg>`;
  }
  const min = Math.min(...series), max = Math.max(...series);
  const range = max - min || 1;
  const up = series[series.length - 1] >= series[0];
  const color = up ? "var(--pos)" : "var(--neg)";
  const pts = series.map((v, i) => {
    const x = (i / (series.length - 1)) * w;
    const y = h - 4 - ((v - min) / range) * (h - 8);
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  });
  const line = pts.join(" ");
  const last = pts[pts.length - 1].split(",");
  return `<svg class="co-spark" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" aria-hidden="true">
    <polyline points="${line}" stroke="${color}"/>
    <circle class="spark-end" cx="${last[0]}" cy="${last[1]}" r="2.5"/>
  </svg>`;
}

/** HTML wrapper for a sparkline cell. Renders the SVG immediately (works
 *  offline / from file:// with no CDN), and marks the cell for a uPlot
 *  upgrade via mountUplotSparks() when the library is available. */
function sparklineHTML(series, w, h) {
  const vals = Array.isArray(series) && series.length >= 2 ? series : null;
  const svg = sparklineSVG(series, w, h);
  if (!vals) return svg; // dashed hairline — nothing to upgrade
  const up = vals[vals.length - 1] >= vals[0];
  const color = up ? "#3fb950" : "#f85149"; // matches --pos / --neg
  const compact = JSON.stringify(vals.map((v) => Math.round(v * 100) / 100));
  return `<div class="uplot-spark" data-vals='${escapeHTML(compact)}' data-color="${color}" data-w="${w}" data-h="${h}">${svg}</div>`;
}

/** Upgrade sparkline cells to uPlot (crisp line + subtle area fill).
 *  No-op when the CDN failed to load — the inline SVG stays. */
function mountUplotSparks(host) {
  if (!window.uPlot) return;
  const els = (host || document).querySelectorAll(".uplot-spark[data-vals]:not([data-mounted])");
  els.forEach((el) => {
    el.dataset.mounted = "1";
    let vals;
    try {
      vals = JSON.parse(el.dataset.vals);
    } catch {
      return;
    }
    if (!Array.isArray(vals) || vals.length < 2) return;
    const w = parseInt(el.dataset.w, 10) || 190;
    const h = parseInt(el.dataset.h, 10) || 40;
    const color = el.dataset.color || "#58a6ff";
    const prev = el.innerHTML;
    try {
      el.innerHTML = "";
      new window.uPlot(
        {
          width: w,
          height: h,
          padding: [3, 2, 3, 2],
          scales: { x: { time: false }, y: { auto: true } },
          axes: [{ show: false }, { show: false }],
          legend: { show: false },
          cursor: { show: false },
          series: [{}, { stroke: color, width: 1.5, fill: hexA(color, 0.1) }],
        },
        [vals.map((_, i) => i), vals],
        el
      );
    } catch {
      el.innerHTML = prev; // uPlot failed mid-render — restore the SVG
      delete el.dataset.mounted;
    }
  });
}

/* ---------- Starred favorites (localStorage only, no backend) ---------- */

const STAR_STORAGE_KEY = "sj_starred";

function getStarredSymbols() {
  try {
    const parsed = JSON.parse(localStorage.getItem(STAR_STORAGE_KEY));
    if (!Array.isArray(parsed)) return [];
    return parsed
      .filter((s) => typeof s === "string" && s.length > 0)
      .map((s) => s.toUpperCase());
  } catch {
    return [];
  }
}

function isStarred(symbol) {
  if (!symbol) return false;
  return getStarredSymbols().includes(String(symbol).toUpperCase());
}

function setStarred(symbol, on) {
  const sym = String(symbol).toUpperCase();
  const current = getStarredSymbols();
  const idx = current.indexOf(sym);
  if (on && idx === -1) current.push(sym);
  if (!on && idx !== -1) current.splice(idx, 1);
  try {
    localStorage.setItem(STAR_STORAGE_KEY, JSON.stringify(current));
  } catch {
    /* private-mode quota errors: star just won't persist */
  }
  return on;
}

function toggleStarred(symbol) {
  return setStarred(symbol, !isStarred(symbol));
}

function starButtonHTML(symbol, starred) {
  return `<button class="star-btn${starred ? " starred" : ""}" data-star-symbol="${escapeHTML(symbol)}" aria-label="${starred ? "Unstar" : "Star"} ${escapeHTML(symbol)}" title="${starred ? "Remove from starred" : "Star this company"}">${starred ? "★" : "☆"}</button>`;
}

/**
 * Normalize a leaderboard entry (or a full review card, since leaderboard.json's
 * per-company shape is not yet finalized upstream — see frontend/README.md
 * "Leaderboard entry shape" for the fields this UI expects and why) into a
 * flat object the table/list views can sort and render directly.
 */
function normalizeEntry(raw) {
  const dcf = raw.dcf || {};
  const verdict = raw.verdict || {};
  const scores = raw.scores || {};

  const price = numOrNull(dcf.current_price ?? raw.price);
  const fairValue = numOrNull(dcf.fair_value ?? raw.fair_value);
  const accTrigger = numOrNull(dcf.acc_trigger ?? raw.acc_trigger);
  const invTrigger = numOrNull(dcf.inv_trigger ?? raw.inv_trigger);

  // Quality/composite: review JSONs expose these as scores.quality,
  // scores.composite, scores.price (nested shape). Older shapes used
  // scores.Q / scores.P_today / scores.P — read all defensively.
  const quality = numOrNull(scores.quality ?? scores.Q ?? raw.quality);
  const composite = numOrNull(
    scores.composite ?? scores.P_today ?? scores.P ?? verdict.conviction ?? raw.composite
  );
  const priceScore = numOrNull(scores.price ?? raw.price_score);
  const conviction = numOrNull(verdict.conviction ?? composite);

  // Margin of safety is not an explicit field in review_card.schema.json;
  // derive it from fair value vs. current price (documented as derived in
  // frontend/README.md).
  const marginOfSafetyPct =
    fairValue && price ? ((fairValue - price) / fairValue) * 100 : null;

  let distanceToTriggerPct = null;
  if (verdict.category === "AT_TRIGGER" && invTrigger && price) {
    distanceToTriggerPct = ((price - invTrigger) / invTrigger) * 100;
  } else if (verdict.category === "WATCH" && accTrigger && price) {
    distanceToTriggerPct = ((price - accTrigger) / accTrigger) * 100;
  } else if (verdict.category === "INVEST_NOW") {
    distanceToTriggerPct = 0;
  }

  return {
    symbol: raw.symbol || null,
    name: raw.name || raw.company || raw.symbol || "Unknown",
    tier: raw.tier || null,
    asOf: raw.as_of || null,
    status: raw.status || null,
    category: verdict.category || raw.category || null,
    quality,
    composite,
    priceScore,
    sector: raw.sector || null,
    conviction,
    price,
    fairValue,
    accTrigger,
    invTrigger,
    marginOfSafetyPct,
    distanceToTriggerPct,
    bestTodayRank: verdict.best_today_rank ?? null,
    raw,
  };
}

function numOrNull(x) {
  if (x === null || x === undefined) return null;
  const n = Number(x);
  return Number.isNaN(n) ? null : n;
}

/**
 * "Best today" ordering: buyable conviction. INVEST_NOW names first (ranked
 * by conviction), then AT_TRIGGER / WATCH names ranked by how close price
 * sits to their entry trigger, weighted by conviction. PASS is excluded —
 * per PLATFORM_SCOPE.md, a great company far above fair value is not a
 * today-buy. Proximity factor decays with distance so a name miles from its
 * trigger never outranks one sitting on it, regardless of conviction.
 */
function bestTodayScore(entry) {
  if (entry.category === "PASS" || entry.category === null) return null;
  const conviction = entry.conviction ?? entry.composite ?? 0;
  if (entry.category === "INVEST_NOW") return conviction * 1.0;
  const dist = entry.distanceToTriggerPct;
  if (dist === null) return null;
  const proximity = 1 / (1 + Math.max(0, dist) / 10); // decays ~10%/10pp above trigger
  return conviction * proximity;
}

function isBuyableToday(entry) {
  if (entry.category === "INVEST_NOW") return true;
  if (entry.category === "AT_TRIGGER" && entry.distanceToTriggerPct !== null) {
    return entry.distanceToTriggerPct <= 10; // "within striking distance"
  }
  if (entry.category === "WATCH" && entry.distanceToTriggerPct !== null) {
    return entry.distanceToTriggerPct <= 5; // "near ACC levels"
  }
  return false;
}
