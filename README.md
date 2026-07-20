# pnyx.dev

Public website for [Pnyx](https://github.com/pikos-apikos/pnyx), an open civic protocol for public reasoning, human judgment, accountable action, and auditable public memory.

The site is dependency-free static HTML and CSS. It uses no external fonts, scripts, trackers, or third-party runtime assets.

## Local preview

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080`.

## Cloudflare Pages

- Production branch: `main`
- Framework preset: `None`
- Build command: `exit 0`
- Build output directory: `.`
- Root directory: `/`

Cloudflare Pages publishes every push to `main` and can create preview deployments for pull requests.

## Domain

Configure both `pnyx.dev` and `www.pnyx.dev` as custom domains in Cloudflare Pages. Redirect `www` to the apex domain.

## Validation

GitHub Actions validates required files, HTML anchors, root-relative assets, canonical sitemap references, and the machine-readable `llms.txt` entry point.

## Licensing

The website follows the Pnyx project licensing model: software and executable material use EUPL-1.2; narrative and protocol content use CC BY-SA 4.0. See the canonical licensing policy in the [Pnyx repository](https://github.com/pikos-apikos/pnyx/blob/main/LICENSING.md).
