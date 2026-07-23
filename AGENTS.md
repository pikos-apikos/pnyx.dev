# Site rules

Build `pnyx.dev` from HTML files.

Read `README.md` and `ARCHITECTURE.md` first.

## Sources

- Head: `site/fragments/head.<lang>.html`
- Header: `site/fragments/header.<lang>.html`
- Footer: `site/fragments/footer.<lang>.html`
- Pages: `site/content/**/index.<lang>.html`
- Builder: `site/build.py`

The builder contains no page list, metadata, or site content.

A page path defines its route:

- `site/content/index.en.html` → `/index.html`
- `site/content/index.el.html` → `/el/index.html`
- `site/content/journal/index.en.html` → `/journal/index.html`
- `site/content/journal/index.el.html` → `/el/journal/index.html`

Always create both language files. The builder discovers them.

Generated pages are outputs. Do not edit them.

## Build order

```text
head → header → content → footer
```

The builder only reads, includes, and writes HTML files.

## Commands

```bash
python3 site/build.py
python3 site/build.py --check
python3 site/build.py serve
```

For preview: edit a source file, refresh the printed URL, review the rebuilt page.

## Rules

- Keep English and Greek routes paired.
- Keep old Journal entries.
- List Journal entries newest first.
- Keep state in files and Git.
- Keep runtime static and offline.
- Do not require a model, cloud service, network, or external runtime asset.
- Do not state inference as observed fact.
- Do not claim merged, deployed, or live without verification.
- Run build and check before finishing.

Small models are replaceable components. HTML artifacts are the persistent state. The builder is deterministic plumbing.
