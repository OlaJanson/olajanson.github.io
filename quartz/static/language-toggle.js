// Language toggle — SV/EN
(function () {
  const STORAGE_KEY = "preferred-lang";

  function applyLang(lang) {
    if (lang === "en") {
      document.body.classList.add("lang-en");
    } else {
      document.body.classList.remove("lang-en");
    }
  }

  function injectButton() {
    if (document.querySelector(".language-toggle")) return;

    const hasBothLangs =
      document.querySelector(".lang-sv") && document.querySelector(".lang-en");
    if (!hasBothLangs) return;

    const btn = document.createElement("button");
    btn.className = "language-toggle";
    btn.setAttribute("aria-label", "Växla språk");
    btn.innerHTML = '<span class="lang-sv">SV/EN</span><span class="lang-en">EN/SV</span>';

    btn.addEventListener("click", () => {
      const isEn = document.body.classList.contains("lang-en");
      const next = isEn ? "sv" : "en";
      localStorage.setItem(STORAGE_KEY, next);
      applyLang(next);
    });

    // Insert in toolbar (right sidebar) or fallback to body
    const toolbar = document.querySelector(".right > .toolbar, header, nav");
    const target = toolbar || document.querySelector(".page-header") || document.body;
    target.appendChild(btn);
  }

  // Apply saved preference immediately
  const saved = localStorage.getItem(STORAGE_KEY) || "sv";
  applyLang(saved);

  // Inject button after DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", injectButton);
  } else {
    injectButton();
  }

  // Re-inject on SPA navigation
  document.addEventListener("nav", injectButton);
})();
