/* data.js — shared data access + formatting helpers.
   Reads only: ./leaderboard.json and ./reviews/*.json. Never writes them.
   All fetches are defensive: file:// blocks XHR/fetch to local files in most
   browsers (Chrome/Edge refuse cross-origin file: reads), so every call here
   catches and reports instead of throwing. */

const CATEGORY_META = {
  INVEST_NOW: { label: "INVEST NOW", cls: "badge-invest-now" },
  AT_TRIGGER: { label: "INVEST AT TRIGGER", cls: "badge-at-trigger" },
  WATCH: { label: "WATCH", cls: "badge-watch" },
  PASS: { label: "PASS", cls: "badge-pass" },
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
  const { ok, data, error } = await fetchJSON("./leaderboard.json");
  if (!ok) return { ok, companies: [], generatedAt: null, error };
  const companies = Array.isArray(data.companies) ? data.companies : [];
  return { ok: true, companies, generatedAt: data.generated_at || null, error: null };
}

/** Load a single review card by symbol from reviews/<symbol>.json. */
async function loadReview(symbol) {
  const { ok, data, error } = await fetchJSON(`./reviews/${encodeURIComponent(symbol)}.json`);
  return { ok, review: ok ? data : null, error };
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
  const fairValue = numOrNull(dcf.fair_value);
  const accTrigger = numOrNull(dcf.acc_trigger);
  const invTrigger = numOrNull(dcf.inv_trigger);

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
