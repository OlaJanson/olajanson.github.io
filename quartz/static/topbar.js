// topbar.js — flytta breadcrumb + toolbar-kontroller in i en sticky topbar
// (DOM-flytt, samma mönster som language-toggle.js). Körs på undersidorna;
// startsidan är hand-HTML (index2.html) och berörs inte.
(function () {
  function buildTopbar() {
    if (document.querySelector(".quartz-topbar")) return false;
    const page = document.querySelector(".page");
    if (!page || !page.parentNode) return false;

    const bar = document.createElement("div");
    bar.className = "quartz-topbar";
    bar.innerHTML =
      '<div class="quartz-topbar-inner">' +
      '<div class="quartz-topbar-left"></div>' +
      '<div class="quartz-topbar-right"></div>' +
      "</div>";
    const left = bar.querySelector(".quartz-topbar-left");
    const right = bar.querySelector(".quartz-topbar-right");

    // breadcrumb → vänster (alignar med center-kolumnen via griden).
    // Saknas breadcrumb (tagg-/mappsidor) → minst en Home-länk så man kan navigera hem.
    const bc = document.querySelector(".breadcrumb-container");
    if (bc) {
      left.appendChild(bc);
    } else {
      const home = document.createElement("a");
      home.className = "quartz-home-link";
      home.href = "/";
      home.textContent = "❮ Home";
      left.appendChild(home);
    }

    // toolbar-gruppen (search + darkmode, + ev. språkknapp) → höger
    const toolbar = document.querySelector(".right .flex-component, .sidebar.right .flex-component");
    if (toolbar) right.appendChild(toolbar);

    // H1 lyfts ut till en hero-band OVANFÖR topbaren — rubriken ligger
    // överst, scrollar bort normalt, medan topbaren under den fäster sticky.
    let hero = null;
    const h1 = document.querySelector(".page-header .article-title, .page-header h1");
    if (h1) {
      hero = document.createElement("div");
      hero.className = "quartz-hero";
      hero.innerHTML =
        '<div class="quartz-hero-inner"><div class="quartz-hero-title"></div></div>';
      hero.querySelector(".quartz-hero-title").appendChild(h1);
    }

    // full viewport-bredd: lägg hero + bar ovanför .page (syskon, ej i .page-boxen)
    if (hero) page.parentNode.insertBefore(hero, page);
    page.parentNode.insertBefore(bar, page);
    return true;
  }

  function moveLang() {
    const right = document.querySelector(".quartz-topbar-right");
    if (!right) return;
    const grp = right.querySelector(".flex-component") || right;
    const lt = document.querySelector(".language-toggle");
    if (lt && !grp.contains(lt)) grp.appendChild(lt);
  }

  function init() {
    // SPA-nav: bygg bara om ifall den aktuella sidans breadcrumb INTE redan ligger i baren.
    // (På initial load fyrar init två gånger — buildTopbar:s egen guard hanterar det.)
    const bar = document.querySelector(".quartz-topbar");
    const bc = document.querySelector(".breadcrumb-container");
    if (bar && bc && !bar.contains(bc)) {
      bar.remove(); // stale bar från föregående sida
      const hero = document.querySelector(".quartz-hero");
      if (hero) hero.remove();
    }
    buildTopbar();
    moveLang();
    // språkknappen kan injiceras av language-toggle.js efter oss
    setTimeout(moveLang, 200);
  }

  document.addEventListener("nav", init);
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
