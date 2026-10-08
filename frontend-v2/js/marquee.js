/* marquee.js — Marquee Investors tab.
   Renders investor cards, conviction overlap, per-investor holdings with
   sparklines + composite gauges, and the recent-moves feed.
   Data: data/marquee.json (built by tools/build_marquee_json.py). */

async function loadMarquee() {
  const { ok, data, error } = await fetchJSON("data/marquee.json");
  if (!ok || !data) return { ok: false, data: null, error };
  return { ok: true, data, error: null };
}

function credChip(h) {
  if (h.credibility === null || h.credibility === undefined) {
    return `<span class="mq-muted">—</span>`;
  }
  const v = Number(h.credibility);
  const cls = v >= 7 ? "mq-pos" : v >= 5 ? "mq-warn" : "mq-neg";
  return `<span class="mq-cred ${cls}" title="Promise-keeping score, ${h.credibility_c5 !== null ? "C5=" + h.credibility_c5 : ""}">${v.toFixed(1)}</span>`;
}

function pledgeFlag(h) {
  if (h.pledge_pct === null || h.pledge_pct === undefined) return `<span class="mq-muted">—</span>`;
  const v = Number(h.pledge_pct);
  if (v <= 0) return `<span class="mq-muted">0%</span>`;
  const cls = v >= 10 ? "mq-neg" : v >= 5 ? "mq-warn" : "";
  return `<span class="${cls}">${v.toFixed(1)}%</span>`;
}

function holdingRow(h, i) {
  const spark = sparklineHTML(h.spark, 120, 36);
  const reviewBit = h.in_review
    ? `<a class="mq-review-link" href="company.html?symbol=${encodeURIComponent(h.slug)}">review →</a>`
    : `<span class="mq-muted">not reviewed</span>`;
  const gauge = h.composite !== null && h.composite !== undefined
    ? scoreRingHTML(h.composite / 10, "composite", 46)
    : `<span class="mq-muted">—</span>`;
  const compNum = h.composite !== null && h.composite !== undefined
    ? `<span class="rv-num num">${fmtNum(h.composite, 2)}</span>` : "";
  return `
    <div class="mq-row" style="animation-delay:${Math.min(i * 38, 600)}ms">
      <span class="mq-spark">${spark}</span>
      <span class="mq-id">
        <span class="rank-name">${escapeHTML(h.name)}<span class="ticker">${escapeHTML(h.symbol)}</span></span>
        <span class="rank-meta">${escapeHTML(h.sector || h.holder_label || "")} &middot; ${reviewBit}</span>
      </span>
      <span class="mq-stake"><span class="rv-num num">${fmtNum(h.holding_pct, 2)}<span class="mq-pct">%</span></span></span>
      <span class="mq-gauge">${gauge}${compNum}</span>
      <span class="mq-cred-cell">${credChip(h)}</span>
      <span class="mq-pledge">${pledgeFlag(h)}</span>
    </div>`;
}

function investorSection(inv, idx) {
  const byStake = [...inv.holdings].sort((a, b) => b.holding_pct - a.holding_pct);
  const byScore = [...inv.holdings].sort((a, b) => {
    const ac = a.composite === null || a.composite === undefined ? -Infinity : a.composite;
    const bc = b.composite === null || b.composite === undefined ? -Infinity : b.composite;
    return bc - ac;
  });
  const rows = (list) => list.map((h, i) => holdingRow(h, i)).join("");
  const moves = (inv.moves || []).map((m) => `
    <div class="investor-deal">
      <span class="mq-move-date">${escapeHTML(m.date || "")}</span>
      <strong>${escapeHTML(m.action || "")}</strong> — ${escapeHTML(m.company || m.symbol || "")}
      ${m.detail ? `<span class="mq-move-detail">${escapeHTML(m.detail)}</span>` : ""}
      ${m.status ? `<span class="soon-chip">${escapeHTML(m.status)}</span>` : ""}
    </div>`).join("");

  return `
  <section class="mq-investor" id="inv-${escapeHTML(inv.id)}">
    <div class="sec-head">
      <span class="sec-idx">${String(idx + 3).padStart(2, "0")}</span>
      <h2 class="sec-title">${escapeHTML(inv.name)}</h2>
      <p class="sec-sub">${escapeHTML(inv.type)} &middot; ${inv.positions} position${inv.positions === 1 ? "" : "s"}${inv.in_review_count ? ` &middot; ${inv.in_review_count} in our coverage` : ""}</p>
    </div>
    ${inv.note ? `<p class="page-sub">${escapeHTML(inv.note)}</p>` : ""}
    <div class="mq-sort">
      <span class="filters-label">Sort</span>
      <button class="filter-btn active" data-mq-sort="stake" data-mq-inv="${escapeHTML(inv.id)}">By stake</button>
      <button class="filter-btn" data-mq-sort="score" data-mq-inv="${escapeHTML(inv.id)}">By our score</button>
    </div>
    <div class="mq-list" id="mq-list-${escapeHTML(inv.id)}">
      <div class="mq-head" aria-hidden="true">
        <span></span><span>Company</span>
        <span class="rh-num">Stake</span><span class="rh-num">Our score</span>
        <span class="rh-num">Cred</span><span class="rh-num">Pledged</span>
      </div>
      <div class="mq-rows" data-rows-stake="${escapeHTML(rows(byStake))}" data-rows-score="${escapeHTML(rows(byScore))}">
        ${rows(byStake)}
      </div>
    </div>
    ${moves ? `<div class="mq-moves"><h3 class="mq-moves-head">Recent moves</h3>${moves}</div>` : ""}
  </section>`;
}

function investorCard(inv) {
  const top = inv.holdings.length
    ? `${escapeHTML(inv.holdings[0].symbol)} ${fmtNum(inv.holdings[0].holding_pct, 1)}%`
    : "—";
  return `
    <a class="mq-card" href="#inv-${escapeHTML(inv.id)}">
      <div class="mq-card-name">${escapeHTML(inv.name)}</div>
      <div class="mq-card-type">${escapeHTML(inv.type)}</div>
      <div class="mq-card-stats">
        <span class="mq-card-stat"><span class="mq-card-num">${inv.positions}</span><span class="mq-card-label">positions</span></span>
        <span class="mq-card-stat"><span class="mq-card-num">${inv.in_review_count}</span><span class="mq-card-label">reviewed</span></span>
      </div>
      <div class="mq-card-top">Top: ${top}</div>
    </a>`;
}

function overlapSection(overlap, names) {
  if (!overlap || overlap.length === 0) {
    return `
    <section>
      <div class="sec-head">
        <span class="sec-idx">02</span>
        <h2 class="sec-title">Conviction Overlap</h2>
        <p class="sec-sub">Companies held by 2+ of the four</p>
      </div>
      <div class="empty-state"><h3>No overlaps in current filings</h3>
      <p>Each investor is fishing in a different pond this quarter — no company is held by two or more of the four right now.</p></div>
    </section>`;
  }
  const rows = overlap.map((o) => `
    <div class="mq-row">
      <span class="mq-id">
        <span class="rank-name">${escapeHTML(o.name)}<span class="ticker">${escapeHTML(o.symbol)}</span></span>
        <span class="rank-meta">${o.investors.map((id) => escapeHTML(names[id] || id)).join(" &middot; ")}</span>
      </span>
      <span class="mq-gauge">${o.composite !== null && o.composite !== undefined ? scoreRingHTML(o.composite / 10, "composite", 46) : `<span class="mq-muted">—</span>`}</span>
    </div>`).join("");
  return `
    <section>
      <div class="sec-head">
        <span class="sec-idx">02</span>
        <h2 class="sec-title">Conviction Overlap</h2>
        <p class="sec-sub">${overlap.length} ${overlap.length === 1 ? "company" : "companies"} held by 2+ of the four</p>
      </div>
      <div class="mq-list">${rows}</div>
    </section>`;
}

async function initMarqueePage() {
  const errorHost = document.getElementById("error-host");
  const host = document.getElementById("marquee-host");
  host.innerHTML = `<div class="skeleton-rows" aria-hidden="true">${"<div class=\"skeleton-row\"></div>".repeat(4)}</div>`;

  const { ok, data, error } = await loadMarquee();
  if (!ok) {
    errorHost.innerHTML = `<div class="error-state">${escapeHTML(error)}</div>`;
    host.innerHTML = "";
    return;
  }

  const names = data.investor_names || {};
  host.innerHTML = `
    <div class="mq-cards">${data.investors.map(investorCard).join("")}</div>
    ${overlapSection(data.overlap, names)}
    ${data.investors.map((inv, i) => investorSection(inv, i)).join("")}
    <p class="mq-foot">Holdings as of ${escapeHTML(data.as_of || "")} &middot; updated ${escapeHTML(data.updated_at || "")}. ` +
    `&gt;1% shareholder filings; sub-1% positions are invisible. Research only, not investment advice.</p>`;

  // Sort toggles
  host.querySelectorAll("[data-mq-sort]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const invId = btn.dataset.mqInv;
      const mode = btn.dataset.mqSort;
      host.querySelectorAll(`[data-mq-sort][data-mq-inv="${invId}"]`).forEach((b) =>
        b.classList.toggle("active", b === btn));
      const rowsHost = host.querySelector(`#mq-list-${invId} .mq-rows`);
      if (rowsHost) {
        rowsHost.innerHTML = mode === "score" ? rowsHost.dataset.rowsScore : rowsHost.dataset.rowsStake;
        animateScoreRings(rowsHost);
        mountUplotSparks(rowsHost);
      }
    });
  });

  animateScoreRings(host);
  mountUplotSparks(host);
}
