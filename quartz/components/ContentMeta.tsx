import { Date, getDate } from "./Date"
import { QuartzComponentConstructor, QuartzComponentProps } from "./types"
import readingTime from "reading-time"
import { classNames } from "../util/lang"
import { i18n } from "../i18n"
import { JSX } from "preact"
import { useEffect, useState } from "preact/hooks"
import style from "./styles/contentMeta.scss"

interface ContentMetaOptions {
  /**
   * Whether to display reading time
   */
  showReadingTime: boolean
  showComma: boolean
}

const defaultOptions: ContentMetaOptions = {
  showReadingTime: true,
  showComma: true,
}

export default ((opts?: Partial<ContentMetaOptions>) => {
  // Merge options with defaults
  const options: ContentMetaOptions = { ...defaultOptions, ...opts }

  function ContentMetadata({ cfg, fileData, displayClass }: QuartzComponentProps) {
    const text = fileData.text

    if (text) {
      const segments: (string | JSX.Element)[] = []

      if (fileData.dates) {
        segments.push(<Date date={getDate(cfg, fileData)!} locale={cfg.locale} />)
      }

      // Display reading time if enabled
      if (options.showReadingTime) {
        const { minutes, words: _words } = readingTime(text)
        const displayedTime = i18n(cfg.locale).components.contentMeta.readingTime({
          minutes: Math.ceil(minutes),
        })
        segments.push(<span>{displayedTime}</span>)
      }

      return (
        <p show-comma={options.showComma} class={classNames(displayClass, "content-meta")}>
          {segments}
          <WebmentionCount />
        </p>
      )
    } else {
      return null
    }
  }

  function WebmentionCount() {
    const [count, setCount] = useState<number | null>(null)
    const url = typeof window !== "undefined" ? window.location.href : ""

    useEffect(() => {
      if (!url) return
      const api = `https://webmention.io/api/count?target=${encodeURIComponent(url)}`
      fetch(api)
        .then((r) => r.json())
        .then((d) => setCount(d.count ?? 0))
        .catch(() => setCount(0))
    }, [url])

    if (count === null) return null
    if (count === 0) return null

    return (
      <span>
        {" · "}
        <a href={`https://webmention.io?target=${encodeURIComponent(url)}`} target="_blank" rel="noopener">
          {count} mention{count !== 1 ? "s" : ""}
        </a>
      </span>
    )
  }

  ContentMetadata.css = style

  return ContentMetadata
}) satisfies QuartzComponentConstructor
