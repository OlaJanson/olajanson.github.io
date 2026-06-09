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

    // breadcrumb → vänster (alignar med center-kolumnen via griden)
    const bc = document.querySelector(".breadcrumb-container");
    if (bc) left.appendChild(bc);

    // toolbar-gruppen (search + darkmode, + ev. språkknapp) → höger
    const toolbar = document.querySelector(".right .flex-component, .sidebar.right .flex-component");
    if (toolbar) right.appendChild(toolbar);

    // full viewport-bredd: lägg baren ovanför .page (syskon, ej i .page-boxen)
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
    if (bar && bc && !bar.contains(bc)) bar.remove(); // stale bar från föregående sida
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
