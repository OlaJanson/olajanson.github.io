import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
import { i18n } from "../i18n"
import style from "./styles/backlinks.scss"

export default (() => {
  const WebmentionMentions: QuartzComponent = ({
    displayClass,
    cfg,
    fileData,
  }: QuartzComponentProps) => {
    return (
      <div class={classNames(displayClass, "backlinks")}>
        <h3>Webmentions</h3>
        <div id="webmention-mentions">
          <p class="loading">Laddar webmentions…</p>
        </div>
      </div>
    )
  }

  WebmentionMentions.css = style
  WebmentionMentions.afterDOMLoaded = `
    (function() {
      const container = document.getElementById('webmention-mentions');
      if (!container) return;
      const url = window.location.href;

      fetch('https://webmention.io/api/mentions.jf2?target=' + encodeURIComponent(url))
        .then(function(r) { return r.json(); })
        .then(function(data) {
          if (!data.children || data.children.length === 0) {
            container.innerHTML = '<p>Inga webmentions än.</p>';
            return;
          }
          var html = '<ul class="mention-list">';
          data.children.forEach(function(mention) {
            var author = mention.author || {};
            var name = author.name || 'Anonym';
            var photo = author.photo || '';
            var avatar = photo ? '<img src="' + photo + '" alt="" class="mention-avatar" />' : '';
            var type = mention['wm-property'] || 'mention';
            var content = mention.content ? mention.content.text : '';
            var url = mention.url || '';
            var published = mention.published ? new Date(mention.published).toLocaleDateString('sv-SE') : '';
            html += '<li class="mention-item">';
            html += '<div class="mention-header">' + avatar + '<strong>' + name + '</strong> <span class="mention-type">(' + type + ')</span> <span class="mention-date">' + published + '</span></div>';
            if (content) {
              html += '<p class="mention-text">' + content.substring(0, 200) + '</p>';
            }
            html += '</li>';
          });
          html += '</ul>';
          container.innerHTML = html;
        })
        .catch(function() {
          container.innerHTML = '<p>Kunde inte ladda webmentions.</p>';
        });
    })();
  `

  return WebmentionMentions
}) satisfies QuartzComponentConstructor
