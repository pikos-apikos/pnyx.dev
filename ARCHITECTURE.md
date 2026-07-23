# Architecture

## Goal

`pnyx.dev` must remain buildable on a laptop or homelab with no cloud service and no network access.

Models are optional, replaceable components. They may help create source artifacts, but they are not part of the published site's runtime and they never become the source of truth.

## Current system

The implemented path is:

```text
page metadata
+ language header HTML
+ semantic content HTML
+ language footer HTML
        ↓
site/build.py
        ↓
committed static HTML
        ↓
Cloudflare Pages or any static file server
```

The current implementation uses only the Python standard library. Header and footer files are included verbatim. Generated HTML remains committed so a reviewer can inspect the exact deployable artifact.

## Boundaries

| Component | Input | Output | May use a model? |
|---|---|---|---|
| Page registry | Explicit page metadata | Route definition | No |
| Header/footer | Plain bilingual HTML fragments | Shared page chrome | No |
| Content source | Plain semantic HTML | Page body artifact | Optional |
| Compiler | Registry + fragments + content | Static HTML | No |
| Validator | Source tree + generated files | Pass or explicit errors | No |
| Publisher | Validated committed files | Static deployment | No |

The model boundary ends before compilation. A model may propose or transform a source artifact. Deterministic code validates, composes, and publishes it.

## Component pipeline

Future assisted authoring should use small stages:

```text
request
  → classify
  → extract
  → validate
  → compose source artifact
  → deterministic site compiler
  → validate generated site
  → human review
  → commit
```

Each stage has one task and a file or structured value as its output. A stage can be implemented by:

- deterministic code;
- a small local model;
- a larger local model;
- an optional cloud model.

Replacing a model must not change file formats, validation rules, or build commands.

## Artifact state

State lives in inspectable artifacts, not in model memory.

```text
site/content/       page-specific semantic HTML
site/fragments/     shared bilingual HTML
site/build.py       route metadata and deterministic composition
generated HTML      exact publishable result
Git history         change, review, and correction record
journal/            selected public production memory
```

A later local-agent layer may add temporary work artifacts under a dedicated workspace, but production source enters the site only through the existing files and validation gates.

## Small-model contracts

A model instruction must name one operation, its inputs, and its output format.

Classify:

```text
Classify this request as one action:
edit_content, edit_header, edit_footer, add_page, or reject.
Return JSON only.
```

Extract:

```text
Read REQUEST.txt.
Extract title, language, slug, and body.
Do not rewrite the body.
Return JSON only.
```

Validate:

```text
Check PAGE.json against page.schema.json.
Return only validation errors.
Return [] when valid.
```

Compose:

```text
Read validated PAGE.json.
Write one semantic HTML fragment.
Do not add html, head, body, header, or footer tags.
```

These prompts are examples of component contracts, not a requirement to add an LLM to the current build.

## Offline execution

The baseline path needs:

- Python 3;
- a filesystem;
- Git;
- an optional standard-library HTTP server.

The local review loop is:

```text
edit source
  → refresh browser
  → fingerprint source mtimes and sizes
  → rebuild only when changed
  → serve generated page
  → human review
```

Run it with `python3 site/build.py serve`. The CLI prints the full preview URL, using an OSC 8 hyperlink when the terminal supports it and readable plain text otherwise. Browser requests are the trigger, so the baseline needs neither filesystem-event dependencies nor a polling build loop.

An assisted path may call an OpenAI-compatible local endpoint exposed by vLLM, GPUStack, or llama.cpp. The adapter must be optional. With no endpoint configured, deterministic build and validation continue to work.

No component may require:

- a specific model vendor;
- internet access;
- hidden conversation memory;
- a hosted vector database;
- credentials to compile or preview the site.

## Trust and validation

The trust order is:

```text
human-approved source
  → deterministic validation
  → deterministic compilation
  → generated diff
  → human review
  → publication
```

Model confidence is never validation. A model output is untrusted until a deterministic check accepts its structure and a human accepts its meaning.

Required invariants:

1. Unchanged inputs produce byte-identical outputs.
2. Generated pages are never edited directly.
3. Every public route has explicit metadata.
4. English and Greek routes remain structurally paired.
5. All same-language pages include the same header and footer files.
6. Local links and assets resolve.
7. No external runtime dependency is introduced silently.
8. A failed stage stops the pipeline and leaves its input artifacts intact.
9. Publication state is reported exactly: committed, merged, deployed, and verified live are different states.

## Why this shape

The system does not depend on one intelligent agent understanding the whole repository. Intelligence is decomposed into small replaceable operations; memory is externalized into files; correctness is enforced by deterministic boundaries.

The static compiler is the stable core. Local or cloud models can improve authoring around it without owning the architecture.
