# Architecture

## Goal

`pnyx.dev` is buildable and reviewable on a laptop or homelab with Python, a filesystem, and no network.

Models are optional, replaceable authoring components. HTML artifacts are the source of truth.

## Static build

```text
site/content/**/index.<lang>.html
+ site/fragments/head.<lang>.html
+ site/fragments/header.<lang>.html
+ site/fragments/footer.<lang>.html
                ↓
         site/build.py
                ↓
      committed static HTML
```

The content path is the route registry. Adding a paired `index.en.html` and `index.el.html` adds a route. The builder discovers pages recursively.

The builder has no page list, titles, descriptions, canonical URLs, navigation markup, footer text, or page content. It only discovers, validates pairs, includes fragments, and writes outputs.

## Components

| Component | Owns |
|---|---|
| `head.<lang>.html` | Document head and shared metadata |
| `header.<lang>.html` | Skip link, brand, navigation |
| `index.<lang>.html` | One route's semantic content |
| `footer.<lang>.html` | Shared footer |
| `build.py` | Discovery, pairing, composition, check, preview |
| Generated HTML | Exact deployable artifact |
| Git | Durable change and review memory |

## Offline review loop

```text
edit HTML → refresh browser → detect source change → rebuild → review
```

Run `python3 site/build.py serve`. It prints a clickable OSC 8 URL when supported. Each browser request fingerprints the source files and rebuilds only when they changed. No watcher dependency or polling loop is required.

## Optional model pipeline

```text
request → one small component → HTML proposal → deterministic build → human review
```

A component may use deterministic code, a local model through vLLM/GPUStack/llama.cpp, or an optional cloud model. The file contract does not change. No model is required to compile, preview, validate, or publish.

## Invariants

1. Content and shared HTML live outside the builder.
2. English and Greek page artifacts are paired.
3. Generated pages are never edited directly.
4. Unchanged inputs produce byte-identical outputs.
5. A failed build preserves its inputs.
6. Local review works without internet or credentials.
7. Human approval remains the meaning gate.
