# Job packs

The base CV at `/` is never edited for an application. To tailor the page for
a specific job, add one JSON file here and share its slug:

    jobs/picadeli.json   ->   https://marcushultberg.dev/picadeli

The slug is the filename: lowercase letters, digits and hyphens only.

## How it works

The slug URL serves the same `index.html` as the base page. `job.js` reads the
slug, fetches `jobs/<slug>.json` and rewrites the hero and the "What I do"
section before the page is shown. Colours come from an optional
`jobs/<slug>.css`, linked earlier still — see below.

Anything a pack leaves out keeps the base wording, so a pack can be as small
as a new hero line. If the slug has no file, the visitor simply gets the base
CV — nothing breaks.

Job pages are marked `noindex`, so they stay out of search results.

## Fields

Every text field takes `{ "en": "...", "sv": "..." }` so the language toggle
keeps working. A plain string is used for both languages.

| Field | What it replaces |
|---|---|
| `eyebrow` | The small line above the name — this is where "Application · Role · Company" goes |
| `role` | The italic line under the name |
| `lead` | The hero paragraph |
| `cta` | The label on the first hero button |
| `matchEyebrow`, `matchTitle`, `matchLead` | The heading block of the "What I do" section |
| `points` | The numbered cards — as many as the ad has requirements |
| `company`, `roleName` | Used to build the browser tab title |
| `pageTitle` | Sets the tab title outright, instead of `company` / `roleName` |
| `text` | Any other text on the page, keyed by CSS selector — see below |

Each entry in `points` takes `title`, `quote` and `body`. `quote` is the
requirement lifted from the ad; `body` is the evidence that you already do it.

## Retuning the rest of the page

The hero and "What I do" are what a pack normally changes. When the base page
leans the wrong way for an application — too much recruitment for a People
Partner role, say — `text` reaches everything else. It is a map of CSS selector
to wording:

```json
"text": {
  "#about .sec-title": { "en": "...", "sv": "..." },
  "#about .about-body": [ { "en": "...", "sv": "..." }, "..." ]
}
```

A string (or an `{ en, sv }` pair) rewrites the first element the selector
matches. **An array rewrites every element it matches, in order** — spare
elements are removed and missing ones cloned from the last, so a list can grow
or shrink. A selector that matches nothing is skipped, so the worst a wrong
selector can do is leave the base wording in place.

The ones worth knowing, all used by `picadeli.json`:

| Selector | What it is |
|---|---|
| `#top .stat-num`, `#top .stat-label` | The three numbers under the hero (arrays of three) |
| `#ask-chips .ask-chip` | The suggested questions for the AI bar |
| `#about .sec-title`, `#about .about-quote` | The About heading and the italic line |
| `#about .about-body` | The three About paragraphs (array of three) |
| `#about .brings-list li` | "What I'm passionate about" (array) |
| `#built .sec-lead`, `#experience .sec-lead` | The lead paragraph of either section |
| `#education .tool-group:nth-of-type(1) .pill` | Areas of expertise — an array reorders them |

Reordering matters as much as rewording: putting the areas that fit the ad
first is honest, and it is the first thing a reader's eye lands on.

Only the hero and "What I do" are held back until the pack has been applied.
Everything `text` reaches is below the fold and hidden until it scrolls into
view, which the pack beats comfortably — but keep that in mind if you ever
point a selector at something visible on load.

## The company's colours

A pack can also bring a theme: put it in `jobs/<slug>.css` and the page is
drawn in the company's palette from the first frame. The file is linked by the
head script in `index.html`, before anything is painted, so there is no flash
of the base colours — and it travels to the CV page too, because `job.js`
rewrites the CV links to `cv.html?job=<slug>`.

A theme normally only sets tokens. `style.css` keeps every colour behind a
handful of variables, so setting these repaints the whole page:

| Token | What it colours |
|---|---|
| `--bg`, `--bg2`, `--bg3`, `--white` | The paper and the alternating bands |
| `--ink`, `--ink-mid`, `--ink-light`, `--ink-dim` | Headings down to the faintest label |
| `--border`, `--border-light`, `--border-strong` | Card and divider lines |
| `--amber`, `--amber-light` | The accent, and the state it hovers to |
| `--accent-rgb` | The channels every tint, wash and glow is mixed from |
| `--white-rgb`, `--bg-rgb` | The same, for the translucent card and nav surfaces |
| `--photo-veil` | The gradient over the Gothenburg photo in the hero |
| `--icon-check` | The tick in "What I'm passionate about" |

`jobs/picadeli.css` is a worked example. A pack without a theme file keeps the
base palette; nothing else changes.

Keep the accent readable: `--amber` sits behind body-sized text and on filled
buttons, so a brand's loudest colour usually belongs on the small marks
instead — a few extra rules at the bottom of the theme, as in the Picadeli one.

## Adding one

1. Copy `exempel.json` to `<company>.json`.
2. Replace the hero lines, and give `points` one entry per requirement in the ad.
3. Optionally add `<company>.css` with the company's colours.
4. Check it at `/<company>` — or locally at `/index.html?job=<company>`.

Everything else on the page — About, What I've built, Experience, Education &
Skills, Personal, Contact — stays as it is, for every application.

## Seeing who looked

Visits are tracked per path, so the stats dashboard shows each application
page separately and you can tell whether a given company opened the link.
