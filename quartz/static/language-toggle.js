// Language toggle — navigates between /slug (SV) and /slug.en (EN)
(function () {
  const STORAGE_KEY = "preferred-lang";

  function getCurrentLang() {
    return window.location.pathname.endsWith(".en") ? "en" : "sv";
  }

  function getOppositeUrl() {
    const path = window.location.pathname.replace(/\/$/, "");
    if (path.endsWith(".en")) {
      return path.slice(0, -3) || "/";
    }
    return path + ".en";
  }

  function injectButton() {
    if (document.querySelector(".language-toggle")) return;

    const oppositeUrl = getOppositeUrl();

    // Only show button if opposite-language version exists
    fetch(oppositeUrl, { method: "HEAD" }).then((res) => {
      if (!res.ok) return;

      const currentLang = getCurrentLang();
      const btn = document.createElement("button");
      btn.className = "language-toggle";
      btn.setAttribute("aria-label", "Växla språk / Toggle language");
      btn.textContent = currentLang === "sv" ? "EN" : "SV";

      btn.addEventListener("click", () => {
        const pref = currentLang === "sv" ? "en" : "sv";
        localStorage.setItem(STORAGE_KEY, pref);
        window.location.href = oppositeUrl;
      });

      const target =
        document.querySelector(".right > .toolbar") ||
        document.querySelector(".page-header") ||
        document.querySelector("header") ||
        document.body;
      target.appendChild(btn);
    }).catch(() => {/* no opposite version */});
  }

  // On load: redirect to preferred language if a different version exists
  function applyPreference() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return;
    const current = getCurrentLang();
    if (saved === current) return;

    const target = getOppositeUrl();
    fetch(target, { method: "HEAD" }).then((res) => {
      if (res.ok) window.location.replace(target);
    }).catch(() => {});
  }

  applyPreference();

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", injectButton);
  } else {
    injectButton();
  }

  // Re-inject on Quartz SPA navigation
  document.addEventListener("nav", () => {
    document.querySelectorAll(".language-toggle").forEach((el) => el.remove());
    injectButton();
  });
})();
