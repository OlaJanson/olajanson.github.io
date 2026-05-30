// Language toggle — URL-based SV/EN navigation + tag page filtering
(function () {
  const STORAGE_KEY = "preferred-lang";

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

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      injectButton();
      filterListingPages(localStorage.getItem(STORAGE_KEY) || "sv");
    });
  } else {
    injectButton();
    filterListingPages(localStorage.getItem(STORAGE_KEY) || "sv");
  }

  document.addEventListener("nav", () => {
    document.querySelectorAll(".language-toggle").forEach((el) => el.remove());
    injectButton();
    filterListingPages(localStorage.getItem(STORAGE_KEY) || "sv");
  });
})();
