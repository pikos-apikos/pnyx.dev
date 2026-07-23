#!/usr/bin/env python3
"""Deterministically compile pnyx.dev from shared components and page content."""

from __future__ import annotations

import argparse
import difflib
import html
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Raw:
    value: str


@dataclass(frozen=True)
class Node:
    tag: str
    attrs: tuple[tuple[str, str | None], ...] = ()
    children: tuple["Node | Raw | str", ...] = ()

    def render(self, level: int = 0) -> str:
        pad = "  " * level
        attributes = "".join(
            f" {name}" if value is None else f' {name}="{html.escape(value, quote=True)}"'
            for name, value in self.attrs
        )
        if self.tag in {"meta", "link", "img"}:
            return f"{pad}<{self.tag}{attributes}>"
        if not self.children:
            return f"{pad}<{self.tag}{attributes}></{self.tag}>"
        if all(isinstance(child, str) for child in self.children):
            text = "".join(html.escape(child) for child in self.children)
            return f"{pad}<{self.tag}{attributes}>{text}</{self.tag}>"
        rendered = []
        for child in self.children:
            if isinstance(child, Node):
                rendered.append(child.render(level + 1))
            elif isinstance(child, Raw):
                rendered.append(child.value.rstrip())
            else:
                rendered.append("  " * (level + 1) + html.escape(child))
        return f"{pad}<{self.tag}{attributes}>\n" + "\n".join(rendered) + f"\n{pad}</{self.tag}>"


def element(tag: str, *children: Node | Raw | str, **attrs: str | None) -> Node:
    normalized = tuple((key.rstrip("_ ").replace("_", "-"), value) for key, value in attrs.items())
    return Node(tag, normalized, tuple(children))


@dataclass(frozen=True)
class Page:
    output: str
    content: str
    lang: str
    title: str
    description: str
    og_title: str
    og_description: str
    canonical: str
    alternate_en: str
    alternate_el: str
    x_default: str
    theme: str = "#f8f6f3"
    journal: bool = False


PAGES = (
    Page("index.html", "site/content/home.en.html", "en", "The Ascent of the Pnyx", "The story of Pnyx: a public civic memory and deliberation system where citizens remain sovereign, AI produces auditable artifacts, and society learns from outcomes.", "The Ascent of the Pnyx", "A civic story about public reasoning, human judgment, accountable action, and shared memory.", "https://pnyx.dev/", "https://pnyx.dev/", "https://pnyx.dev/el/", "https://pnyx.dev/", "#f4efe4"),
    Page("el/index.html", "site/content/home.el.html", "el", "Η Ανάβαση στην Πνύκα", "Η ιστορία της Pnyx: ένα δημόσιο σύστημα διαβούλευσης και πολιτειακής μνήμης, όπου οι πολίτες παραμένουν κυρίαρχοι, η τεχνητή νοημοσύνη παράγει ελέγξιμα τεκμήρια και η κοινωνία μαθαίνει από τα αποτελέσματα.", "Η Ανάβαση στην Πνύκα", "Μια πολιτειακή αφήγηση για τη δημόσια σκέψη, την ανθρώπινη κρίση, τη λογοδοσία και την κοινή μνήμη.", "https://pnyx.dev/el/", "https://pnyx.dev/", "https://pnyx.dev/el/", "https://pnyx.dev/"),
    Page("journal/index.html", "site/content/journal.en.html", "en", "Journal — Pnyx", "The public production memory of Pnyx: decisions, failures, human corrections, and outcomes that do not fit in a Git diff.", "Pnyx journal", "Public records of how Pnyx is researched, challenged, corrected, and built.", "https://pnyx.dev/journal/", "https://pnyx.dev/journal/", "https://pnyx.dev/el/journal/", "https://pnyx.dev/journal/", journal=True),
    Page("el/journal/index.html", "site/content/journal.el.html", "el", "Ημερολόγιο — Pnyx", "Η δημόσια μνήμη παραγωγής της Pnyx: αποφάσεις, αστοχίες, ανθρώπινες διορθώσεις και αποτελέσματα που δεν χωρούν σε ένα Git diff.", "Ημερολόγιο Pnyx", "Δημόσιες καταγραφές για το πώς η Pnyx ερευνάται, αμφισβητείται, διορθώνεται και υλοποιείται.", "https://pnyx.dev/el/journal/", "https://pnyx.dev/journal/", "https://pnyx.dev/el/journal/", "https://pnyx.dev/journal/", journal=True),
    Page("journal/horizon/index.html", "site/content/horizon.en.html", "en", "From the assembly to the horizon — Pnyx journal", "A public record of how conversation, archaeological sources, criticism, and implementation produced the horizon hero for pnyx.dev.", "From the assembly to the horizon — Pnyx journal", "The production record behind the horizon hero of pnyx.dev.", "https://pnyx.dev/journal/horizon/", "https://pnyx.dev/journal/horizon/", "https://pnyx.dev/el/journal/horizon/", "https://pnyx.dev/journal/horizon/", journal=True),
    Page("el/journal/horizon/index.html", "site/content/horizon.el.html", "el", "Από τη συνέλευση στον ορίζοντα — Ημερολόγιο Pnyx", "Η δημόσια καταγραφή του τρόπου με τον οποίο η συνομιλία, οι αρχαιολογικές πηγές, η κριτική και η υλοποίηση παρήγαγαν το hero του ορίζοντα για το pnyx.dev.", "Από τη συνέλευση στον ορίζοντα — Ημερολόγιο Pnyx", "Το ιστορικό παραγωγής πίσω από το hero του ορίζοντα στο pnyx.dev.", "https://pnyx.dev/el/journal/horizon/", "https://pnyx.dev/journal/horizon/", "https://pnyx.dev/el/journal/horizon/", "https://pnyx.dev/journal/horizon/", journal=True),
    Page("journal/generated-menu/index.html", "site/content/generated-menu.en.html", "en", "One menu, generated everywhere — Pnyx journal", "How a missing mobile link led pnyx.dev from copied navigation to a deterministic shared header and static page compiler.", "One menu, generated everywhere — Pnyx journal", "The public implementation record of the generated responsive navigation on pnyx.dev.", "https://pnyx.dev/journal/generated-menu/", "https://pnyx.dev/journal/generated-menu/", "https://pnyx.dev/el/journal/generated-menu/", "https://pnyx.dev/journal/generated-menu/", journal=True),
    Page("el/journal/generated-menu/index.html", "site/content/generated-menu.el.html", "el", "Ένα μενού, παραγόμενο παντού — Ημερολόγιο Pnyx", "Πώς ένα κρυμμένο mobile link οδήγησε το pnyx.dev από αντιγραμμένη πλοήγηση σε κοινό deterministic header και static page compiler.", "Ένα μενού, παραγόμενο παντού — Ημερολόγιο Pnyx", "Η δημόσια καταγραφή της generated responsive πλοήγησης του pnyx.dev.", "https://pnyx.dev/el/journal/generated-menu/", "https://pnyx.dev/journal/generated-menu/", "https://pnyx.dev/el/journal/generated-menu/", "https://pnyx.dev/journal/generated-menu/", journal=True),
)


def fragment(name: str, lang: str) -> str:
    """Read a shared HTML fragment verbatim for deterministic inclusion."""
    return (ROOT / "site" / "fragments" / f"{name}.{lang}.html").read_text(encoding="utf-8").rstrip()


def head(page: Page) -> Node:
    locale = "el_GR" if page.lang == "el" else "en"
    other_locale = "en" if page.lang == "el" else "el_GR"
    children: list[Node] = [
        element("meta", charset="utf-8"), element("meta", name="viewport", content="width=device-width, initial-scale=1"),
        element("meta", name="theme-color", content=page.theme), element("meta", name="description", content=page.description),
        element("meta", property="og:title", content=page.og_title), element("meta", property="og:description", content=page.og_description),
        element("meta", property="og:type", content="article"), element("meta", property="og:url", content=page.canonical),
        element("meta", property="og:image", content="https://pnyx.dev/assets/pnyx-horizon-social.jpg"),
    ]
    if not page.journal:
        children.extend((element("meta", property="og:image:width", content="1200"), element("meta", property="og:image:height", content="675"), element("meta", property="og:image:alt", content="Πολίτες συγκεντρωμένοι στη βραχώδη Πνύκα, στραμμένοι προς έναν φωτεινό ορίζοντα." if page.lang == "el" else "Citizens gathered on the rocky Pnyx, facing a bright horizon."), element("meta", property="og:locale", content=locale), element("meta", property="og:locale:alternate", content=other_locale)))
    children.extend((element("meta", name="twitter:card", content="summary_large_image"), element("link", rel="canonical", href=page.canonical), element("link", rel="alternate", hreflang="en", href=page.alternate_en), element("link", rel="alternate", hreflang="el", href=page.alternate_el), element("link", rel="alternate", hreflang="x-default", href=page.x_default), element("link", rel="icon", href="/favicon.svg", type="image/svg+xml"), element("link", rel="stylesheet", href="/styles.css"), element("title", page.title)))
    return element("head", *children)


def compile_page(page: Page) -> str:
    content = (ROOT / page.content).read_text(encoding="utf-8").strip()
    skip = "Μετάβαση στην καταγραφή" if page.lang == "el" and page.journal else "Μετάβαση στο κυρίως περιεχόμενο" if page.lang == "el" else "Skip to the record" if page.journal else "Skip to main content"
    body = element(
        "body",
        element("a", skip, class_="skip-link", href="#main"),
        Raw(fragment("header", page.lang)),
        Raw(content),
        Raw(fragment("footer", page.lang)),
    )
    document = element("html", head(page), body, lang=page.lang)
    return "<!doctype html>\n<!-- Generated by site/build.py; edit site/content or site/fragments. -->\n" + document.render() + "\n"


def build(check: bool) -> int:
    stale: list[str] = []
    for page in PAGES:
        target = ROOT / page.output
        compiled = compile_page(page)
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current == compiled:
            continue
        if check:
            stale.append(page.output)
            print("".join(difflib.unified_diff(current.splitlines(True), compiled.splitlines(True), fromfile=page.output, tofile=f"compiled/{page.output}"))[:4000])
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(compiled, encoding="utf-8", newline="\n")
    if stale:
        print("Generated pages are stale: " + ", ".join(stale))
        return 1
    print("Generated pages are deterministic and current." if check else "Compiled bilingual static pages.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when committed output differs from a clean compile")
    raise SystemExit(build(parser.parse_args().check))
