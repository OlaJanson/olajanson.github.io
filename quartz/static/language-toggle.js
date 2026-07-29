// Language toggle — URL-based SV/EN navigation + tag page filtering
(function () {
  const STORAGE_KEY = "lang"; // GEMENSAM nyckel med startsidan (index2.html/index.en.html)

  // Landningssidan (index2.html/index.en.html) är rå HTML, inte Quartz-emitterad —
  // den har sin EGEN #lang-btn + redirect-logik. Denna funktions nav-lyssnare tar
  // annars bort ALLA .language-toggle-element (inkl. landningssidans egen knapp)
  // och bygger om en ny — vilket händer redan vid FÖRSTA sidladdningen, eftersom
  // Quartz-routern fyrar ett nav-event direkt vid load. ".page" finns bara på
  // Quartz-emitterade sidor, aldrig på landningssidan — säkert particionerings-villkor.
  function onLandingPage() {
    return !document.querySelector(".page");
  }

  function getCurrentLang() {
    return window.location.pathname.endsWith(".en") ? "en" : "sv";
  }

  function getOppositeUrl() {
    const path = window.location.pathname.replace(/\/$/, "");
    if (path.endsWith(".en")) return path.slice(0, -3) || "/";
    return path + ".en";
  }

  function filterListingPages(lang) {
    const items = document.querySelectorAll(".section-li");
    if (!items.length) return;
    items.forEach((item) => {
      const link = item.querySelector("a[href]");
      if (!link) return;
      const href = link.getAttribute("href") || "";
      const isEnglish = href.endsWith(".en");
      item.style.display = (lang === "en") === isEnglish ? "" : "none";
    });
  }

  // Backlinks innehåller både SV- och EN-versioner av länkande sidor. Visa bara
  // de som matchar SIDANS språk (den sida man tittar på), inte preferensen.
  function filterBacklinks() {
    const lang = getCurrentLang();
    const items = document.querySelectorAll(".backlinks ul.backlink-list > li, .backlinks ul > li");
    items.forEach((item) => {
      const link = item.querySelector("a[href]");
      if (!link) return;
      const href = (link.getAttribute("href") || "").replace(/[#?].*$/, "").replace(/\/$/, "");
      const isEnglish = href.endsWith(".en");
      item.style.display = (lang === "en") === isEnglish ? "" : "none";
    });
  }

  function injectButton() {
    if (document.querySelector(".language-toggle")) return;

    const currentLang = getCurrentLang();
    const savedLang = localStorage.getItem(STORAGE_KEY) || "sv";

    const btn = document.createElement("button");
    btn.className = "language-toggle";
    btn.setAttribute("aria-label", "Växla språk / Toggle language");
    btn.textContent = currentLang === "sv" ? "EN" : "SV";

    btn.addEventListener("click", () => {
      const next = currentLang === "sv" ? "en" : "sv";
      localStorage.setItem(STORAGE_KEY, next);

      const opposite = getOppositeUrl();
      fetch(opposite, { method: "HEAD" })
        .then((res) => {
          if (res.ok) {
            window.location.href = opposite;
          } else {
            // Listing page (tag/folder): filter in place, no navigation
            btn.textContent = next === "sv" ? "EN" : "SV";
            filterListingPages(next);
          }
        })
        .catch(() => {
          btn.textContent = next === "sv" ? "EN" : "SV";
          filterListingPages(next);
        });
    });

    // Inject into the toolbar flex group in the right sidebar
    const target =
      document.querySelector(".right .flex-component") ||
      document.querySelector(".right.sidebar") ||
      document.body;
    target.appendChild(btn);
  }

  function applyPreference() {
    if (onLandingPage()) return;
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return;
    filterListingPages(saved);
    const current = getCurrentLang();
    if (saved === current) return;
    const target = getOppositeUrl();
    fetch(target, { method: "HEAD" })
      .then((res) => { if (res.ok) window.location.replace(target); })
      .catch(() => {});
  }

  applyPreference();

  function initOnce() {
    if (onLandingPage()) return;
    injectButton();
    filterListingPages(localStorage.getItem(STORAGE_KEY) || "sv");
    filterBacklinks();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initOnce);
  } else {
    initOnce();
  }

  document.addEventListener("nav", () => {
    if (onLandingPage()) return; // rör aldrig landningssidans egen #lang-btn
    document.querySelectorAll(".language-toggle").forEach((el) => el.remove());
    applyPreference(); // språkpreferensen består även vid SPA-byten (kan omdirigera SV→EN)
    injectButton();
    filterListingPages(localStorage.getItem(STORAGE_KEY) || "sv");
    filterBacklinks();
  });
})();
