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
    { href: "marquee.html", id: "marquee", label: "Marquee" },
    { href: "calibration.html", id: "calibration", label: "Calibration" },
    { href: "run.html", id: "run", label: "Run a Company" },
  ];

  const linkHTML = links
    .map(
      (l) =>
        `<a href="${l.href}" class="${l.id === activePage ? "active" : ""}">${l.label}</a>`
    )
    .join("");

  navHost.innerHTML =
    `<span class="brand">Stock-Judging<span class="sub">Engine v6 · Research only</span></span>` +
    linkHTML;
}
