# CLAUDE.md

This file guides Claude Code when working in this repo. Project rules live in `AGENTS.md`; an exhaustive map of what to edit for every UI change lives in `PROJECT_MAP.md`. Read both before making changes.

## Project overview

Personal static site built with **Hugo** (v0.163.2+) and the **Blowfish** theme (vendored under `themes/blowfish`), deployed to Cloudflare Pages at `https://lyrumu.top`.

- Default site language is `en`, but individual articles may be written in Chinese.
- `/Vault` is a **read-only** Obsidian vault mirror (source of truth for notes). Never modify it.
- Many Blowfish templates are overridden in `layouts/`; styles are split into numbered `assets/css/_*.css` files.

## Commands

```bash
# Local development (run in the user's terminal, not the IDE sandbox — sandboxed Hugo output is broken)
hugo server --themesDir themes --theme blowfish --config hugo.toml --bind 127.0.0.1 --port 8080

# Production build (outputs to public/)
hugo --minify --themesDir themes --theme blowfish --config hugo.toml

# New notes article (uses archetypes/notes.md)
hugo new content/notes/<slug>/index.md
```

There is no linting, test suite, or package-manager build step; Hugo is the only build tool.

## Architecture in one screen

- **Content** — Markdown in `content/` (sections `about`, `notes`, `works`, `life`, each with an `_index.md`). Notes articles use the `notes` archetype and inherit cascade defaults (taxonomies, edit, pagination, views, likes) from `content/notes/_index.md`.
- **Data** — `data/*.yaml` consumed by custom shortcodes/partials (e.g. `cover.yaml`, `home_highlights.yaml`, `life.yaml`, `works.yaml`, `projects.yaml`, `resources.yaml`, `music.yaml`, `about_timeline.yaml`, `site.yaml`).
- **Layout overrides** — `layouts/_default/{baseof,list,single}.html`, `layouts/page.html`, and `layouts/partials/{home/custom,head,vendor}.html` are project-level overrides of the theme; don't change them without understanding the design contract.
- **Shortcodes** — project-specific ones in `layouts/shortcodes/` (e.g. `life-grid`, `works-grid`, `projects-list`, `resources-list`, `music-list`, `about-timeline`, `about-contact`, `page-hero`, `icon`, `site-stats`, `section-rule`, `file-tree`).
- **Icons** — Simple Icons SVGs in `assets/icons/`, rendered via `{{< icon "name" >}}`.
- **Static assets** — `static/fonts/` (self-hosted fonts), `static/image/`, `static/works-resources/`.

## CSS loading (critical gotcha)

Do **not** use `@import` inside a custom stylesheet — the theme's `resources.Get "css/custom.css"` appends raw bytes without resolving imports, causing 404s. The override at `layouts/partials/head.html` instead concats everything matched by `resources.Match "css/_*.css"` into `custom.css`.

- Put new CSS in `assets/css/_NN_module.css` where `NN` is the next number (current sequence: `_01_tokens.css`–`_12_custom-cursor.css`); files are picked up automatically.
- `assets/css/custom.css` is an index/backup only, no longer loaded by the build.
- Never edit `themes/blowfish/`.

## Design system

Tokens live in `assets/css/_01_tokens.css` and drive everything: home cover, cards, Blowfish utilities.

- Light: bg `#FAF9F5`, text `#1F1E1D`, accent `#D97757`. Dark: bg `#141413`, text `#FAF9F5`, accent `#E08769`.
- Fonts: `Fraunces` (display serif), `Newsreader` (body serif), `Inter` (sans), self-hosted in `static/fonts/`.
- Decorative dividers: `✦` and `──`.

## Navigation

Top-level menu items live in `hugo.toml` under `[[menu.main]]`: `ABOUT ME`, `DOCS`, `WORKS`, `DAILY`. To add a section: add a menu entry in `hugo.toml` and create `content/<slug>/_index.md`. Section landing pages pick their layout via frontmatter (`layout: "list"` vs `"page"` with `showChildList: false`).

## Firebase, comments, and references

- Firebase credentials are exposed in `hugo.toml` under `[params.firebase]`; the real security boundary is Firestore Rules + Anonymous Auth (see `FIREBASE_SECURITY.md`). Views/likes are enabled only for home and notes via the overridden `vendor.html`.
- Giscus comments load via `layouts/partials/extend-footer.html`; theme switching handled by `assets/js/giscus-loader.js`.

## When asked to change content

First decide: a data-driven UI update (usually `data/*.yaml` + shortcode) or a page content update (`content/**/*.md`). Then consult `PROJECT_MAP.md` to confirm the exact file. Follow the conventions in `AGENTS.md`; after a major milestone, update `DONE.md`.
