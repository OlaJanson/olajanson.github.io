import { computeDisplay } from "../util/lang"

const STORAGE_KEY = "garden-lang"

function getCurrentLang(): string {
  return localStorage.getItem(STORAGE_KEY) || (navigator.language.startsWith("sv") ? "sv" : "en")
}

function setLang(lang: string) {
  localStorage.setItem(STORAGE_KEY, lang)
  document.documentElement.lang = lang
  document.querySelectorAll(".lang-sv, .lang-en").forEach((el) => {
    el.classList.toggle("active", el.classList.contains(`lang-${lang}`))
  })
  // Redirect to appropriate version if .en.md / .sv.md exists
  const slug = document.body.dataset.slug
  if (slug) {
    const targetSlug = lang === "en" ? `${slug}.en` : slug.replace(/\.en$/, "")
    if (targetSlug !== slug) {
      window.history.replaceState(null, "", `/${targetSlug}`)
    }
  }
}

document.addEventListener("nav", () => {
  const btn = document.querySelector<HTMLButtonElement>(".language-toggle")
  const current = getCurrentLang()
  setLang(current)
  btn?.addEventListener("click", () => {
    const lang = getCurrentLang() === "sv" ? "en" : "sv"
    setLang(lang)
  })
})
