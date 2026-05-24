import { Translation } from "./definition"

export default {
  propertyDefaults: {
    title: "Namnlös",
    description: "Ingen beskrivning angiven",
  },
  components: {
    callout: {
      note: "Notering",
      abstract: "Sammanfattning",
      info: "Info",
      todo: "Att göra",
      tip: "Tips",
      success: "Lyckades",
      question: "Fråga",
      warning: "Varning",
      failure: "Misslyckades",
      danger: "Fara",
      bug: "Bugg",
      example: "Exempel",
      quote: "Citat",
    },
    backlinks: {
      title: "Bakåtlänkar",
      noBacklinksFound: "Inga bakåtlänkar hittades",
    },
    themeToggle: {
      lightMode: "Ljust läge",
      darkMode: "Mörkt läge",
    },
    readerMode: {
      title: "Läsarläge",
    },
    explorer: {
      title: "Utforskaren",
    },
    footer: {
      createdWith: "Skapad med",
    },
    graph: {
      title: "Grafvy",
    },
    recentNotes: {
      title: "Senaste noteringarna",
      seeRemainingMore: ({ remaining }) => `Visa ${remaining} till →`,
    },
    transcludes: {
      transcludeOf: ({ targetSlug }) => `Inbäddning av ${targetSlug}`,
      linkToOriginal: "Länk till original",
    },
    search: {
      title: "Sök",
      searchBarPlaceholder: "Sök efter något",
    },
    tableOfContents: {
      title: "Innehållsförteckning",
    },
    contentMeta: {
      readingTime: ({ minutes }) => `${minutes} min läsning`,
    },
  },
  pages: {
    rss: {
      recentNotes: "Senaste noteringarna",
      lastFewNotes: ({ count }) => `Senaste ${count} noteringarna`,
    },
    error: {
      title: "Sidan hittades inte",
      notFound: "Antingen är den här sidan privat eller så finns den inte.",
      home: "Tillbaka till startsidan",
    },
    folderContent: {
      folder: "Mapp",
      itemsUnderFolder: ({ count }) =>
        count === 1 ? "1 sak i den här mappen." : `${count} saker i den här mappen.`,
    },
    tagContent: {
      tag: "Tagg",
      tagIndex: "Taggindex",
      itemsUnderTag: ({ count }) =>
        count === 1 ? "1 sak med den här taggen." : `${count} saker med den här taggen.`,
      showingFirst: ({ count }) => `Visar de första ${count} taggarna.`,
      totalTags: ({ count }) => `Hittade ${count} taggar totalt.`,
    },
  },
} as const satisfies Translation
