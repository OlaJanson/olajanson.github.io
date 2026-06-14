// webmentions.js — client-side webmention.io-integration för olajanson.se
// Renderar en räknare + "Vem har länkat hit"-lista längst ner på varje artikel.
// Helt client-side. Tyst (renderar inget) om API:et är nere eller saknar svar.
// Löser korten: webmention-counter (P1) + webmention-mentions-list (P1).

(function () {
  "use strict";

  var API = "https://webmention.io/api";
  var SITE = "https://olajanson.se";

  // Designpalett (DESIGN_INVARIANTS): creme text, guld accent, dämpad, kant.
  var C = {
    text: "#EAE6DA",
    gold: "#F2D024",
    muted: "#9E9A91",
    border: "#2a2a2a",
  };

  var REACTIONS = {
    "like-of": { label: "gillade", icon: "♥" },
    "repost-of": { label: "delade", icon: "⟲" },
    "bookmark-of": { label: "bokmärkte", icon: "🔖" },
    "mention-of": { label: "nämnde", icon: "💬" },
    "in-reply-to": { label: "svarade", icon: "↩" },
    "rsvp": { label: "svarade på inbjudan", icon: "📅" },
  };

  function esc(s) {
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  // Kanonisk mål-URL för aktuell sida (utan hash/query).
  function targetUrl() {
    var path = location.pathname.replace(/index\.html$/, "");
    return SITE + path;
  }

  // Var ska sektionen in? Sist i mittenkolumnen, annars i article/body.
  function mountPoint() {
    return (
      document.querySelector(".center") ||
      document.querySelector("article") ||
      document.body
    );
  }

  function injectStylesOnce() {
    if (document.getElementById("webmentions-style")) return;
    var css =
      ".webmentions{margin:3rem 0 1rem;padding-top:1.5rem;border-top:1px solid " +
      C.border +
      ";font-family:var(--skfFont,var(--bodyFont),sans-serif)}" +
      ".webmentions__count{font-size:.95rem;color:" +
      C.muted +
      ";margin-bottom:1rem}" +
      ".webmentions__count b{color:" +
      C.gold +
      "}" +
      ".webmentions__list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.75rem}" +
      ".webmentions__item{display:flex;gap:.6rem;align-items:flex-start;font-size:.9rem;color:" +
      C.text +
      "}" +
      ".webmentions__avatar{width:32px;height:32px;border-radius:50%;flex:0 0 32px;object-fit:cover;background:" +
      C.border +
      "}" +
      ".webmentions__body{flex:1;min-width:0}" +
      ".webmentions__name{color:" +
      C.text +
      ";font-weight:600;text-decoration:none}" +
      ".webmentions__name:hover{color:" +
      C.gold +
      "}" +
      ".webmentions__type{color:" +
      C.muted +
      ";font-size:.8rem}" +
      ".webmentions__quote{color:" +
      C.muted +
      ";margin-top:.2rem;font-style:italic}";
    var el = document.createElement("style");
    el.id = "webmentions-style";
    el.textContent = css;
    document.head.appendChild(el);
  }

  function reactionFor(mention) {
    var p = mention["wm-property"];
    return REACTIONS[p] || { label: "nämnde", icon: "💬" };
  }

  function renderItem(m) {
    var author = m.author || {};
    var r = reactionFor(m);
    var name = author.name || "Någon";
    var url = author.url || m.url || "#";
    var photo = author.photo || "";
    var quote = "";
    // Visa citat bara för faktiska kommentarer/omnämnanden, inte likes/reposts.
    if (m["wm-property"] === "mention-of" || m["wm-property"] === "in-reply-to") {
      var content = m.content || {};
      var text = (content.text || "").trim();
      if (text) quote = text.length > 200 ? text.slice(0, 200) + "…" : text;
    }
    var avatar = photo
      ? '<img class="webmentions__avatar" src="' +
        esc(photo) +
        '" alt="" loading="lazy">'
      : '<span class="webmentions__avatar" aria-hidden="true"></span>';
    return (
      '<li class="webmentions__item">' +
      avatar +
      '<div class="webmentions__body">' +
      '<a class="webmentions__name" href="' +
      esc(url) +
      '" rel="nofollow">' +
      esc(name) +
      "</a> " +
      '<span class="webmentions__type">' +
      r.icon +
      " " +
      r.label +
      "</span>" +
      (quote ? '<div class="webmentions__quote">' + esc(quote) + "</div>" : "") +
      "</div>" +
      "</li>"
    );
  }

  function render(mentions) {
    if (!mentions || !mentions.length) return; // tyst om inga
    injectStylesOnce();

    // Räknare per typ för sammanfattningsraden.
    var counts = {};
    mentions.forEach(function (m) {
      var p = m["wm-property"];
      counts[p] = (counts[p] || 0) + 1;
    });
    var parts = [];
    Object.keys(REACTIONS).forEach(function (p) {
      if (counts[p]) {
        var r = REACTIONS[p];
        parts.push(counts[p] + " " + r.label);
      }
    });
    var summary =
      "<b>" +
      mentions.length +
      "</b> " +
      (mentions.length === 1 ? "reaktion" : "reaktioner") +
      (parts.length ? " — " + parts.join(", ") : "");

    var section = document.createElement("section");
    section.className = "webmentions";
    section.innerHTML =
      '<div class="webmentions__count">📡 ' +
      summary +
      "</div>" +
      '<ul class="webmentions__list">' +
      mentions.map(renderItem).join("") +
      "</ul>";
    mountPoint().appendChild(section);
  }

  function load() {
    // Undvik dubbelrendering vid SPA-navigering.
    var existing = document.querySelector(".webmentions");
    if (existing) existing.remove();

    var target = targetUrl();
    var url =
      API +
      "/mentions.jf2?target=" +
      encodeURIComponent(target) +
      "&per-page=100";

    fetch(url)
      .then(function (r) {
        return r.ok ? r.json() : null;
      })
      .then(function (data) {
        if (!data) return;
        render(data.children || []);
      })
      .catch(function () {
        /* tyst — inga brutna sidor om API:et är nere */
      });
  }

  // Kör vid första laddning och vid Quartz SPA-navigering.
  if (document.readyState !== "loading") load();
  else document.addEventListener("DOMContentLoaded", load);
  document.addEventListener("nav", load);
})();
