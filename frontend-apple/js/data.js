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

function categoryMeta(category) {
  return CATEGORY_META[category] || { label: category || "UNKNOWN", cls: "badge-unknown" };
}

function categoryBadgeHTML(category) {
  const meta = categoryMeta(category);
  return `<span class="badge ${meta.cls}">${escapeHTML(meta.label)}</span>`;
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

/** Load a single review card by symbol from reviews/<symbol>.json. */
async function loadReview(symbol) {
  const { ok, data, error } = await fetchJSON(`../reviews/${encodeURIComponent(symbol)}.json`);
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
  const { ok, data } = await fetchJSON(`../news/${encodeURIComponent(symbol)}.json`);
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

  // Quality/composite: engine_v3 exposes these as scores.Q (quality) and
  // scores.P_today / scores.P_trigger (composite "price-adjusted" score).
  // review_card.schema.json leaves `scores` untyped, so we read defensively.
  const quality = numOrNull(scores.Q ?? raw.quality);
  const composite = numOrNull(
    scores.P_today ?? scores.P ?? verdict.conviction ?? raw.composite
  );
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
