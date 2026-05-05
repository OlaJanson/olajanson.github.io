import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "En mytomaniens lögndetektorfabrik",
    pageTitleSuffix: " — Slumpmässiga tankar från en schweizisk armékniv",
    enableSPA: true,
    enablePopovers: true,
    locale: "sv-SE",
    baseUrl: "olajanson.se",
    ignorePatterns: ["private", "templates", ".obsidian"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Labrada",
        body: "Labrada",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#d4c8b8",
          lightgray: "#e5ddd0",
          gray: "#c2b8a8",
          darkgray: "#6b6258",
          dark: "#3d352e",
          secondary: "#b55a3e",
          tertiary: "#5e8c5e",
          highlight: "rgba(181, 90, 62, 0.15)",
          textHighlight: "#e8c84a88",
        },
        darkMode: {
          light: "#2a2520",
          lightgray: "#3a342e",
          gray: "#5a524a",
          darkgray: "#b8b0a8",
          dark: "#e8e0d8",
          secondary: "#d47a5e",
          tertiary: "#7aac7a",
          highlight: "rgba(212, 122, 94, 0.15)",
          textHighlight: "#d4b84a88",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.CNAME(),
      Plugin.NotFoundPage(),
      // Comment out CustomOgImages to speed up build time
      Plugin.CustomOgImages(),
    ],
  },
}

export default config
