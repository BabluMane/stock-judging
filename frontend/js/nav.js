/* nav.js — renders the shared provisional banner + top nav into every page.
   Kept as JS (not a server-side include) since this is a static, no-build
   site that must also work from file://. */

function renderChrome(activePage) {
  const bannerHost = document.getElementById("provisional-banner");
  if (bannerHost) {
    bannerHost.innerHTML =
      '<strong>PROVISIONAL — v3 is NOT LIVE.</strong> ' +
      "Validation bar unpassed. Nothing on this site is an investable call. No live execution hooks exist here.";
  }

  const navHost = document.getElementById("topnav");
  if (!navHost) return;

  const links = [
    { href: "index.html", id: "leaderboard", label: "Leaderboard" },
    { href: "best-overall.html", id: "best-overall", label: "Best Overall" },
    { href: "best-today.html", id: "best-today", label: "Best Today" },
    { href: "run.html", id: "run", label: "Run a Company" },
  ];

  const linkHTML = links
    .map(
      (l) =>
        `<a href="${l.href}" class="${l.id === activePage ? "active" : ""}">${l.label}</a>`
    )
    .join("");

  navHost.innerHTML =
    `<span class="brand">Stock-Judging<span class="sub">v3 · research only</span></span>` +
    linkHTML;
}
