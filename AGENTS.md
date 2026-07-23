# Site rules

Build `pnyx.dev` as a deterministic static site.

Read `README.md` and `ARCHITECTURE.md` before changing the site.

## Sources

- Page registry and compiler: `site/build.py`
- Header: `site/fragments/header.<lang>.html`
- Footer: `site/fragments/footer.<lang>.html`
- Page content: `site/content/*.html`
- Shared styles: `styles.css`
- Generated pages: `index.html`, `el/`, `journal/`
- Architecture: `ARCHITECTURE.md`

Generated pages are outputs. Do not edit them by hand.

## Build a page

1. Read the page metadata.
2. Include the header for the page language.
3. Include the page content.
4. Include the footer for the page language.
5. Write the static HTML.

The order is always:

```text
metadata → header → content → footer → static HTML
```

## Shared navigation

All pages in one language use the same header file.

To change the menu:

1. Edit `site/fragments/header.en.html`.
2. Edit `site/fragments/header.el.html`.
3. Rebuild every page.

Do not create page-specific navigation.

Journal links:

- English: `/journal/`
- Greek: `/el/journal/`

The journal index lists every entry, newest first.
Do not remove an older entry when adding a new one.

## Commands

Build:

```bash
python3 site/build.py
```

Check:

```bash
python3 site/build.py --check
```

Preview:

```bash
python3 -m http.server 8080
```

Before finishing:

1. Run the build.
2. Run the check.
3. Check local links and assets.
4. Check English and Greek pages.
5. Report changed files and validation results.

## Content rules

- Never state an inference or generated result as an observed fact.
- Keep sources beside supported claims.
- Keep uncertainty, corrections, and rejected directions visible.
- Models assist. Humans retain judgment.
- Keep English and Greek structure aligned.
- Use `Pnyx (pronounced "p-nix")` when pronunciation is needed.
- Do not claim a commit is merged, deployed, or live without verification.

## Site constraints

- Keep runtime output static and dependency-free.
- Do not require network access.
- Do not add trackers or external runtime assets.
- Preserve semantic HTML, keyboard access, contrast, and mobile layout.
- Prefer existing design tokens and styles.
- Keep unchanged inputs byte-identical.
- Keep persistent state in files and Git.

## Model constraints

Assume a small local model may perform a task.

- Give one component one small task.
- Use short instructions.
- Name exact input and output files.
- Request structured output when possible.
- Validate every output before the next step.
- Prefer deterministic code over model reasoning.
- Do not require a cloud model.
- Do not assume internet access.

Models are replaceable components.
Artifacts are persistent state.
The deterministic compiler is the final authority.
