/* investor.js — Investor Activity section on the leaderboard page. */

async function initInvestorSection() {
  const host = document.getElementById("investor-host");
  if (!host) return;
  const { ok, data } = await fetchJSON("data/investor_activity.json");
  if (!ok || !data || !Array.isArray(data.investors)) {
    host.innerHTML = `<p class="muted">Investor data unavailable.</p>`;
    return;
  }
  host.innerHTML = data.investors.map((inv) => {
    const acts = Array.isArray(inv.activity) ? inv.activity : [];
    const actsHTML = acts.length === 0
      ? `<p class="muted">No positions in our coverage yet.</p>`
      : `<ul class="investor-acts">` + acts.map((a) => {
          const link = a.in_coverage && a.symbol
            ? `<a href="company.html?symbol=${encodeURIComponent(a.symbol)}">${escapeHTML(a.company)}</a>`
            : escapeHTML(a.company);
          return `<li><span class="inv-action">${escapeHTML(a.action)}</span> — ${link} ` +
            `<span class="muted">${escapeHTML(a.detail || "")}</span> ` +
            `<span class="inv-date">${escapeHTML(a.date || "")}</span> ` +
            `<span class="inv-status">${escapeHTML(a.status || "")}</span></li>`;
        }).join("") + `</ul>`;
    return `<div class="investor-card"><h3>${escapeHTML(inv.name)} <span class="muted">· ${escapeHTML(inv.type || "")}</span></h3>${actsHTML}</div>`;
  }).join("");
}
