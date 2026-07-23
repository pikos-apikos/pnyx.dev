# pnyx.dev

Public website for [Pnyx](https://github.com/pikos-apikos/pnyx), an open civic protocol for public reasoning, human judgment, accountable action, and auditable public memory.

The site is dependency-free static HTML and CSS at runtime. A small Python standard-library compiler includes shared header and footer HTML fragments, composes page content, and exports the committed static HTML. It uses no external fonts, scripts, trackers, or third-party runtime assets.

The component boundaries and offline/local-model path are documented in [ARCHITECTURE.md](ARCHITECTURE.md).

## Build

Edit page metadata in `site/build.py`, shared bilingual HTML in `site/fragments/`, and page-specific semantic content in `site/content/`. Then compile:

```bash
python3 site/build.py
```

Generated HTML is committed so Cloudflare Pages remains a buildless static deployment. Verify that it is reproducible with:

```bash
python3 site/build.py --check
```

## Local preview

```bash
python3 site/build.py serve
```

The command prints a clickable preview URL when the terminal supports OSC 8 hyperlinks. Edit a source file and refresh the browser: the server detects changed build inputs and recompiles before serving the request.

Options:

```bash
python3 site/build.py serve --host 0.0.0.0 --port 8080
```

## Cloudflare Pages

- Production branch: `main`
- Framework preset: `None`
- Build command: `python3 site/build.py --check`
- Build output directory: `.`
- Root directory: `/`

Cloudflare Pages publishes every push to `main` and can create preview deployments for pull requests.

## Domain

Configure both `pnyx.dev` and `www.pnyx.dev` as custom domains in Cloudflare Pages. Redirect `www` to the apex domain.

## Validation

GitHub Actions validates required files, HTML anchors, root-relative assets, canonical sitemap references, and the machine-readable `llms.txt` entry point.

## Licensing

The website follows the Pnyx project licensing model: software and executable material use EUPL-1.2; narrative and protocol content use CC BY-SA 4.0. See the canonical licensing policy in the [Pnyx repository](https://github.com/pikos-apikos/pnyx/blob/main/LICENSING.md).
