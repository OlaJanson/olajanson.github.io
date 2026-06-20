---
title: Gästbok
stage: evergreen
publish: true
tags:
  - garden
  - meta
---

# ✍️ Gästbok

Lämna ett spår. Inget konto behövs — bara ett namn och ett meddelande.

<form id="gastbok-form" method="POST" action="https://api.staticman.net/v3/entry/github/OlaJanson/olajanson.github.io/v5/gastbok">
  <input type="hidden" name="options[redirect]" value="https://olajanson.se/g%C3%A4stbok?tack=1">
  <input type="hidden" name="options[slug]" value="gastbok">

  <label for="name">Namn</label>
  <input type="text" id="name" name="fields[name]" required placeholder="Ditt namn">

  <label for="message">Meddelande</label>
  <textarea id="message" name="fields[message]" required placeholder="Vad vill du säga?" rows="4"></textarea>

  <label for="url">Webbplats (valfritt)</label>
  <input type="text" id="url" name="fields[url]" placeholder="https://...">

  <button type="submit">Skicka</button>
</form>

<div id="tack" style="display:none">
  <p>Tack! Ditt meddelande visas efter granskning.</p>
</div>

<div id="gastbok-entries">
  <h2>Tidigare meddelanden</h2>
  <div id="entries-list">
    <p class="empty-hint">Inga meddelanden än — bli den första!</p>
  </div>
</div>

<script>
(function() {
  // Visa tack-meddelande om redirect med ?tack=1
  if (window.location.search.includes('tack=1')) {
    var form = document.getElementById('gastbok-form');
    var tack = document.getElementById('tack');
    if (form) form.style.display = 'none';
    if (tack) tack.style.display = 'block';
  }

  // Ladda tidigare meddelanden från JSON
  var list = document.getElementById('entries-list');
  if (!list) return;
  fetch('/static/gastbok-entries.json')
    .then(function(r) { return r.json(); })
    .then(function(entries) {
      if (!entries || !entries.length) return;
      list.innerHTML = '';
      entries.forEach(function(e) {
        var card = document.createElement('div');
        card.className = 'entry-card';
        var html = '<div class="entry-meta">';
        html += '<strong class="entry-name">' + esc(e.name) + '</strong>';
        if (e.date) html += ' <span class="entry-date">' + esc(e.date) + '</span>';
        if (e.url) html += ' <a class="entry-url" href="' + esc(e.url) + '" rel="nofollow noopener">' + esc(e.url) + '</a>';
        html += '</div>';
        html += '<p class="entry-message">' + esc(e.message) + '</p>';
        card.innerHTML = html;
        list.appendChild(card);
      });
    })
    .catch(function() { /* tom lista är OK */ });

  function esc(s) {
    var d = document.createElement('div');
    d.appendChild(document.createTextNode(s));
    return d.innerHTML;
  }
})();
</script>

<style>
  #gastbok-form {
    max-width: 600px;
    margin-top: 2rem;
  }
  #gastbok-form label {
    display: block;
    margin-bottom: 0.25rem;
    font-family: 'SKF Sans', sans-serif;
    font-size: 0.85rem;
    color: #9E9A91;
    margin-top: 1.25rem;
  }
  #gastbok-form input,
  #gastbok-form textarea {
    width: 100%;
    padding: 0.75rem;
    background: #181c1e;
    border: 1px solid #2a2a2a;
    border-radius: 4px;
    color: #EAE6DA;
    font-family: 'Fraunces', serif;
    font-size: 1rem;
  }
  #gastbok-form button {
    margin-top: 1.5rem;
    padding: 0.75rem 2rem;
    background: #d7be00;
    color: #12100e;
    border: none;
    border-radius: 4px;
    font-family: 'SKF Sans', sans-serif;
    font-size: 0.9rem;
    cursor: pointer;
    font-weight: 600;
  }
  #gastbok-form button:hover {
    background: #e8cf1a;
  }
  #tack {
    margin-top: 2rem;
    padding: 2rem;
    background: #181c1e;
    border-radius: 6px;
    text-align: center;
    font-size: 1.2rem;
    color: #d7be00;
  }
  #gastbok-entries {
    margin-top: 3rem;
  }
  #gastbok-entries h2 {
    font-family: 'Magic Romance', serif;
    font-size: 28px;
    color: #d7be00;
    margin-bottom: 1.5rem;
  }
  .entry-card {
    background: #181c1e;
    border-radius: 6px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
  }
  .entry-meta {
    margin-bottom: 0.5rem;
    font-family: 'SKF Sans', sans-serif;
    font-size: 0.8rem;
    color: #9E9A91;
  }
  .entry-name {
    color: #EAE6DA;
  }
  .entry-date {
    margin-left: 0.75rem;
  }
  .entry-url {
    margin-left: 0.75rem;
    color: #5fd7ff;
    text-decoration: none;
  }
  .entry-url:hover {
    text-decoration: underline;
  }
  .entry-message {
    color: #a8dadc;
    line-height: 1.8;
    font-size: 1.05rem;
  }
  .empty-hint {
    color: #666;
    font-style: italic;
  }
</style>
