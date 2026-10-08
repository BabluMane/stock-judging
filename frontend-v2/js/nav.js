/* nav.js — renders the shared provisional banner + top nav into every page.
   Kept as JS (not a server-side include) since this is a static, no-build
   site that must also work from file://. */

function renderChrome(activePage) {
  const bannerHost = document.getElementById("provisional-banner");
  if (bannerHost) {
    bannerHost.innerHTML =
      '<span class="icon" aria-hidden="true">&#9888;&#65039;</span>' +
      '<span><strong>Engine v6 LIVE.</strong> ' +
      "Research outputs, not investment advice. Verify before acting.</span>";
  }

  const navHost = document.getElementById("topnav");
  if (!navHost) return;

  const links = [
    { href: "index.html", id: "leaderboard", label: "Leaderboard" },
    { href: "best-overall.html", id: "best-overall", label: "Best Overall" },
    { href: "best-today.html", id: "best-today", label: "Best Today" },
    { href: "calibration.html", id: "calibration", label: "Calibration" },
    { href: "run.html", id: "run", label: "Run a Company" },
  ];

  const linkHTML = links
    .map(
      (l) =>
        `<a href="${l.href}" class="${l.id === activePage ? "active" : ""}">${l.label}</a>`
    )
    .join("");

  // Investor tracking (Kacholia / Mukul Agrawal / Quant holdings, etc.) has
  // no data source or schema yet (see PLATFORM_SCOPE.md "planned modules").
  // Rather than a dead link or a silently missing page, show it inertly in
  // the nav as a "coming soon" item so it reads as planned, not broken (A6).
  const investorHTML =
    `<a href="javascript:void(0)" class="investor-soon" tabindex="-1" aria-disabled="true" ` +
    `title="Investor tracking (tracked investors' holdings vs. review cards) is a planned module — not built yet.">` +
    `Investors <span class="soon-chip">Soon</span></a>`;

  navHost.innerHTML =
    `<span class="brand">Stock-Judging<span class="sub">Engine v6 · Research only</span></span>` +
    linkHTML +
    investorHTML;
}
