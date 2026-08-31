# Job packs

The base CV at `/` is never edited for an application. To tailor the page for
a specific job, add one JSON file here and share its slug:

    jobs/picadeli.json   ->   https://cv-page-mocha.vercel.app/picadeli

The slug is the filename: lowercase letters, digits and hyphens only.

## How it works

The slug URL serves the same `index.html` as the base page. `job.js` reads the
slug, fetches `jobs/<slug>.json` and rewrites the hero and the "What I do"
section before the page is shown.

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

Each entry in `points` takes `title`, `quote` and `body`. `quote` is the
requirement lifted from the ad; `body` is the evidence that you already do it.

## Adding one

1. Copy `exempel.json` to `<company>.json`.
2. Replace the hero lines, and give `points` one entry per requirement in the ad.
3. Check it at `/<company>` — or locally at `/index.html?job=<company>`.

Everything else on the page — About, What I've built, Experience, Education &
Skills, Personal, Contact — stays as it is, for every application.

## Seeing who looked

Visits are tracked per path, so the stats dashboard shows each application
page separately and you can tell whether a given company opened the link.
