// @ts-ignore
import languageToggleScript from "./scripts/languageToggle.inline"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

const LanguageToggle: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
  return (
    <button class={classNames(displayClass, "language-toggle")} aria-label="Växla språk">
      <span class="lang-sv active">SV</span>
      <span class="lang-separator">/</span>
      <span class="lang-en">EN</span>
    </button>
  )
}

LanguageToggle.beforeDOMLoaded = languageToggleScript

export default (() => LanguageToggle) satisfies QuartzComponentConstructor
