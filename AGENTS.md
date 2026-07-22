# AGENTS.md

This file is the working agreement for coding agents contributing to `pnyx.dev`.

## Purpose

`pnyx.dev` is the public website for Pnyx, an open civic protocol for public reasoning, human judgment, accountable action, and auditable public memory.

The site itself should model those values: claims must be attributable, uncertainty must remain visible, and changes must leave an understandable public record.

## Repository shape

- `/index.html` — English homepage.
- `/el/index.html` — Greek homepage.
- `/styles.css` — shared styles for both languages and the journal.
- `/assets/` — production images and other static assets.
- `/journal/` and `/el/journal/` — English and Greek records of significant decisions and production work.
- `/llms.txt` — machine-readable entry point.
- `/_headers`, `/robots.txt`, and `/sitemap.xml` — deployment and discovery metadata.

This is a dependency-free static site. Do not add a framework, build system, external font, tracker, client-side dependency, or third-party runtime asset unless the change explicitly requires it and the trade-off is documented.

## Core principles

- We love humanity.
- Citizens retain political judgment. Models assist; they do not rule.
- Preserve dissent, uncertainty, rejected warnings, provenance, and outcomes.
- Do not turn funding, visibility, technical expertise, or model confidence into civic authority.
- Public work should return to public memory.
- Pnyx should be developed using the same transparent civic loop it proposes.

## Working workflow

1. Read this file, `README.md`, and every file directly affected by the task.
2. Inspect the current branch and working tree. Preserve unrelated user changes.
3. State the intended change and any meaningful assumptions before editing.
4. Make the smallest coherent change in plain HTML and CSS.
5. Keep the English and Greek experiences structurally aligned. Do not use machine-looking literal translation when the surrounding prose has a distinct voice.
6. When a change represents a meaningful design, research, or governance decision, update the corresponding journal record in both languages.
7. Validate locally before committing.
8. Commit only files in scope, with a terse description of the actual change.
9. Push to a feature branch and update or open a pull request. Do not push directly to `main` unless the user explicitly requests it.
10. Verify the deployed or preview URL before saying that a production change is live. A commit, merged PR, and deployment are different states.

## Content and evidence rules

- Never present a generated reconstruction, estimate, inference, or simulated result as an observed fact.
- Prefer primary sources for historical, technical, legal, and geographic claims.
- Keep source links close to the claims they support.
- If a source supports only part of a statement, narrow the statement or expose the gap.
- Distinguish clearly between a source artifact, a derived geometric/data artifact, and an artistic interpretation.
- Do not silently erase an earlier error from the journal. Record the correction and what changed.
- Preserve the pronunciation as `Pnyx (pronounced "p-nix")` where pronunciation guidance is needed.

## Adding a journal entry

The journal is the public production memory of the project. Add an entry when the reasoning, evidence, human criticism, rejected direction, correction, or outcome would be lost in a Git diff. Do not create an entry merely to restate a commit.

1. Choose one short, stable, lowercase slug. Create both `/journal/<slug>/index.html` and `/el/journal/<slug>/index.html`; neither language is an optional follow-up.
2. Start from the structure of an existing entry, but write the record from the available evidence. Do not copy claims, dates, sources, pull-request numbers, or implementation status from the example.
3. Give each page its own translated title, description, visible publication date, canonical URL, Open Graph metadata, and `en`/`el`/`x-default` alternate links. Use an absolute public URL in social metadata and root-relative URLs for site navigation and assets.
4. Preserve the actual sequence of work: scope and goal; sources or inputs; model contribution; human judgment and criticism; rejected or failed directions; correction or decision; implementation and outcome; remaining uncertainty. Attribute quoted words and do not invent missing conversation history.
5. Keep provenance beside the relevant claim. Separate observed facts, source material, derived artifacts, model inferences, and artistic interpretations. If an artifact or rejected candidate no longer exists, say so instead of reconstructing it silently.
6. Put reusable entry-specific material under `/journal/<slug>/artifacts/`. The Greek entry may link to the same artifacts. Use descriptive filenames and explain what each artifact proves, how it was derived, and any important limitation.
7. Link to the exact implementation evidence when it exists: the relevant pull request, commit, deployed page, or source artifact. Describe its real state accurately; `opened`, `committed`, `merged`, `deployed`, and `verified live` are different claims.
8. Make the new entry discoverable in both `sitemap.xml` and `llms.txt`. If navigation or a journal link currently points directly to one entry, review it deliberately so the previous record is not made unreachable by accident.
9. Validate both language pages: titles and heading hierarchy, canonical and alternate URLs, dates, internal links, fragment IDs, assets, source links, responsive layout, and the relationship between the two versions. Run the repository checks before committing.
10. When correcting a published entry, preserve the substance of the earlier error and add the correction or revision context. Public memory should show learning, not a silently rewritten past.

Dates describe publication, not when an agent happened to start drafting. Never publish a future or guessed date. If the exact publication date or factual boundary is unknown, stop and ask.

## Image workflow

Images are part of the public record, not decoration without provenance.

- Keep original references, prompts, derived data, and final production assets separate.
- For historically or geographically grounded scenes, establish geometry and orientation before image generation.
- Label generated images as artistic interpretations even when constrained by real data.
- Never claim pixel-level historical or geodetic accuracy for a generated image.
- Use versioned filenames while exploring. Replace a production filename only after the user selects the exact candidate.
- After replacement, verify the HTML reference, file hash, responsive crop, social preview, and deployed result. Account for browser/CDN caching, but do not blame cache without checking the deployed asset.
- Optimize production raster assets (normally WebP for the page and JPEG where required for social previews) without discarding the higher-quality working source prematurely.
- Do not render meaningful page copy into an image. Keep it as accessible, responsive HTML.

## Design rules

- Preserve the restrained editorial character of the site.
- Prefer typography, spacing, rhythm, and photography over ornamental UI containers.
- Avoid dashboard aesthetics, gratuitous cards, gradients, and decorative motion.
- Check desktop and narrow mobile layouts.
- Maintain semantic heading order, keyboard access, readable contrast, useful alt text, and `prefers-reduced-motion` behavior.
- Reuse existing design tokens in `:root` before introducing new colors, radii, shadows, or widths.

## Validation

At minimum, verify:

- required files remain present;
- internal and root-relative links resolve;
- IDs and fragment links exist and are unique;
- English and Greek navigation paths remain valid;
- referenced assets exist with the expected filename and format;
- `sitemap.xml` and `llms.txt` remain consistent with public entry points;
- the page renders at desktop and mobile widths;
- no external runtime request was introduced unintentionally.

Use the repository's GitHub Actions checks as the final automated guardrail, not as a substitute for local inspection.

## Handoff

Report:

- what changed;
- which files changed;
- what was validated;
- what remains uncertain or intentionally deferred;
- the branch, commit, and PR/deployment state when applicable.

Never report a guessed tool result, successful push, merged PR, cache state, or live deployment as fact.
