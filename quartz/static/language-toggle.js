// Language toggle — URL-based SV/EN navigation + tag page filtering
// Patch: spegla svenska länkgrafen till engelska sidor i contentIndex
(function () {
  const _origFetch = window.fetch;
  window.fetch = function (...args) {
    const url = typeof args[0] === "string" ? args[0] : (args[0]?.url || "");
    if (url.includes("contentIndex")) {
      return _origFetch.apply(this, args).then((res) => {
        const clone = res.clone();
        return clone.json().then((data) => {
          let patched = false;
          for (const [slug, entry] of Object.entries(data)) {
            if (!slug.endsWith(".en")) continue;
            if (entry.links && entry.links.length > 0) continue;
            const svSlug = slug.slice(0, -3);
            const svLinks = data[svSlug]?.links;
            if (!svLinks || svLinks.length === 0) continue;
            entry.links = svLinks.map((l) => (data[l + ".en"] ? l + ".en" : l));
            patched = true;
          }
          if (!patched) return res;
          return new Response(JSON.stringify(data), {
            status: res.status,
            statusText: res.statusText,
            headers: res.headers,
          });
        }).catch(() => res);
      });
    }
    return _origFetch.apply(this, args);
  };
})();

(function () {
  const STORAGE_KEY = "preferred-lang";

  function getCurrentLang() {
    return window.location.pathname.endsWith(".en") ? "en" : "sv";
  }

  function getOppositeUrl() {
    // Använd data-slug från body om tillgängligt (mer pålitligt än pathname)
    const slug = document.body?.dataset?.slug || "";
    if (slug) {
      if (slug.endsWith(".en")) return "/" + slug.slice(0, -3).replace(/^index$/, "") || "/";
      return "/" + slug + ".en";
    }
    // Fallback: pathname-baserat
    const path = window.location.pathname.replace(/\/$/, "") || "/index";
    if (path.endsWith(".en")) return path.slice(0, -3).replace(/\/index$/, "/") || "/";
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
    let savedLang = localStorage.getItem(STORAGE_KEY) || "sv";

    const btn = document.createElement("button");
    btn.className = "language-toggle";
    btn.setAttribute("aria-label", "Växla språk / Toggle language");
    // Visa vad man KAN byta TILL — baserat på sparad preferens, inte URL
    btn.textContent = savedLang === "sv" ? "EN" : "SV";

    btn.addEventListener("click", () => {
      const next = savedLang === "sv" ? "en" : "sv";
      localStorage.setItem(STORAGE_KEY, next);
      savedLang = next;

      if (next === currentLang) {
        btn.textContent = next === "sv" ? "EN" : "SV";
        filterListingPages(next);
        return;
      }

      const opposite = getOppositeUrl();
      fetch(opposite, { method: "HEAD" })
        .then((res) => {
          if (res.ok) {
            window.location.href = opposite;
          } else {
            // Listing page (tag/folder) eller sida utan översättning: filtrera på plats
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
