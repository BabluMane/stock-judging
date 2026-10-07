/* leaderboard.js — table of all reviewed companies, sortable, filterable. */

function skeletonTableHTML() {
  const rows = Array.from({ length: 6 }, () => `<div class="skeleton-row"></div>`).join("");
  return `<div class="skeleton-rows skeleton-table" aria-hidden="true" aria-label="Loading leaderboard">${rows}</div>`;
}

const LEADERBOARD_COLUMNS = [
  { key: "name", label: "Company", sortable: true, type: "name" },
  { key: "category", label: "Category", sortable: false, type: "badge" },
  { key: "composite", label: "Composite", sortable: true, type: "score" },
  { key: "quality", label: "Quality", sortable: true, type: "score" },
  { key: "price", label: "Price", sortable: true, type: "price" },
  { key: "marginOfSafetyPct", label: "Margin of Safety", sortable: true, type: "pct" },
  { key: "asOf", label: "As of", sortable: true, type: "text" },
];

let LB_STATE = { entries: [], sortKey: "composite", sortDir: "desc", filter: "ALL" };

async function initLeaderboardPage() {
  const errorHost = document.getElementById("error-host");
  const tableHost = document.getElementById("table-host");
  const filtersHost = document.getElementById("filters");

  tableHost.innerHTML = skeletonTableHTML();
  const { ok, companies, error } = await loadLeaderboard();

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
  filtersHost.style.display = "flex";
  wireFilters();
  renderLeaderboardTable();
}

function wireFilters() {
  const filtersHost = document.getElementById("filters");
  filtersHost.querySelectorAll(".filter-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      filtersHost.querySelectorAll(".filter-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      LB_STATE.filter = btn.dataset.cat;
      renderLeaderboardTable();
    });
  });
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

function renderLeaderboardTable() {
  const tableHost = document.getElementById("table-host");
  let entries = LB_STATE.entries;
  if (LB_STATE.filter !== "ALL") {
    entries = entries.filter((e) => e.category === LB_STATE.filter);
  }
  entries = sortEntries(entries, LB_STATE.sortKey, LB_STATE.sortDir);

  if (entries.length === 0) {
    tableHost.innerHTML = emptyStateHTML(
      "No companies in this category",
      "Try a different filter above."
    );
    const countHostEmpty = document.getElementById("filter-count");
    if (countHostEmpty) countHostEmpty.textContent = `0 of ${LB_STATE.entries.length} shown`;
    return;
  }

  const headHTML = LEADERBOARD_COLUMNS.map((col) => {
    const isSorted = col.key === LB_STATE.sortKey;
    const arrow = isSorted ? (LB_STATE.sortDir === "asc" ? "▲" : "▼") : "";
    const numClass = col.type === "score" || col.type === "price" || col.type === "pct" ? "num" : "";
    return `<th class="${col.sortable ? "sortable" : ""} ${numClass}" data-key="${col.key}" data-sortable="${col.sortable}">${escapeHTML(col.label)}${arrow ? `<span class="sort-arrow">${arrow}</span>` : ""}</th>`;
  }).join("");

  const rowsHTML = entries
    .map((e) => {
      const cells = LEADERBOARD_COLUMNS.map((col) => {
        if (col.type === "name") {
          return `<td class="name-cell"><a href="company.html?symbol=${encodeURIComponent(e.symbol || "")}">${escapeHTML(e.name)}</a>${e.symbol ? `<span class="ticker">${escapeHTML(e.symbol)}</span>` : ""}</td>`;
        }
        if (col.type === "badge") {
          return `<td>${categoryBadgeHTML(e.category)}</td>`;
        }
        if (col.type === "score") {
          return `<td class="num">${fmtNum(e[col.key], 2)}</td>`;
        }
        if (col.type === "price") {
          return `<td class="num">${fmtPrice(e[col.key])}</td>`;
        }
        if (col.type === "pct") {
          return `<td class="num">${fmtPct(e[col.key])}</td>`;
        }
        return `<td>${escapeHTML(e[col.key])}</td>`;
      }).join("");
      return `<tr data-symbol="${escapeHTML(e.symbol || "")}">${cells}</tr>`;
    })
    .join("");

  tableHost.innerHTML = `
    <div class="table-wrap">
      <table>
        <thead><tr>${headHTML}</tr></thead>
        <tbody>${rowsHTML}</tbody>
      </table>
    </div>
  `;

  const countHost = document.getElementById("filter-count");
  if (countHost) {
    countHost.textContent = `${entries.length} of ${LB_STATE.entries.length} shown`;
  }

  tableHost.querySelectorAll("th.sortable").forEach((th) => {
    th.addEventListener("click", () => {
      const key = th.dataset.key;
      if (LB_STATE.sortKey === key) {
        LB_STATE.sortDir = LB_STATE.sortDir === "asc" ? "desc" : "asc";
      } else {
        LB_STATE.sortKey = key;
        LB_STATE.sortDir = "desc";
      }
      renderLeaderboardTable();
    });
  });

  tableHost.querySelectorAll("tbody tr").forEach((tr) => {
    tr.addEventListener("click", (evt) => {
      if (evt.target.tagName === "A") return;
      const symbol = tr.dataset.symbol;
      if (symbol) window.location.href = `company.html?symbol=${encodeURIComponent(symbol)}`;
    });
    tr.style.cursor = "pointer";
  });
}

function emptyStateHTML(title, body) {
  return `
    <div class="empty-state">
      <div class="icon">&#128203;</div>
      <h3>${escapeHTML(title)}</h3>
      <p>${escapeHTML(body)}</p>
    </div>
  `;
}
