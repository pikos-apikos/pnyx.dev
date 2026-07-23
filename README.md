# pnyx.dev

Public website for [Pnyx](https://github.com/pikos-apikos/pnyx), an open civic protocol for public reasoning, human judgment, accountable action, and auditable public memory.

The runtime is dependency-free static HTML and CSS. See [ARCHITECTURE.md](ARCHITECTURE.md).

## Sources

- `site/fragments/head.<lang>.html`
- `site/fragments/header.<lang>.html`
- `site/fragments/footer.<lang>.html`
- `site/content/**/index.<lang>.html`

The content directory mirrors public routes. The Python builder discovers pages; it contains no page registry or metadata.

## Build

```bash
python3 site/build.py
python3 site/build.py --check
```

Generated HTML is committed for transparent review and buildless static hosting.

## Local preview

```bash
python3 site/build.py serve
```

The CLI prints the preview URL as an OSC 8 terminal link when supported. Edit HTML, refresh the browser, and the request rebuilds changed sources before serving.

```bash
python3 site/build.py serve --host 0.0.0.0 --port 8080
```

## Cloudflare Pages

- Production branch: `main`
- Framework preset: `None`
- Build command: `python3 site/build.py --check`
- Build output directory: `.`
- Root directory: `/`

## Validation

GitHub Actions checks deterministic output, required files, HTML anchors, local assets, sitemap references, and `llms.txt`.

## Licensing

Software and executable material use EUPL-1.2; narrative and protocol content use CC BY-SA 4.0. See the [Pnyx licensing policy](https://github.com/pikos-apikos/pnyx/blob/main/LICENSING.md).
