#!/usr/bin/env python3
"""
Post-build SEO checks for the Keyper site.

Run after tools/build_site.py. Catches the failures that are invisible in a
browser but cost rankings — duplicate copy across landing pages, thin pages,
broken internal links, malformed JSON-LD, missing canonicals, orphaned pages.

    python3 tools/check_seo.py

Exits non-zero if any check fails, so it can gate a commit.
"""

import glob
import itertools
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# A landing page below this many words reads as thin content to Google.
MIN_WORDS = 400
# Jaccard similarity between two pages' body copy. Above this and the pages
# are effectively the same page with the place name swapped.
MAX_SIMILARITY = 0.45
# Google truncates SERP titles past roughly this width.
MAX_TITLE_CHARS = 70
MAX_DESCRIPTION_CHARS = 165

failures = []
notes = []


def fail(msg):
    failures.append(msg)
    print(f"  FAIL  {msg}")


def ok(msg):
    print(f"  ok    {msg}")


def note(msg):
    notes.append(msg)
    print(f"  note  {msg}")


def body_words(page):
    text = " ".join(
        [page["lede"], " ".join(page["intro_body"])]
        + [
            s["heading"] + " " + s["body"] + " " + " ".join(s.get("points", []))
            for s in page["sections"]
        ]
    )
    return set(re.findall(r"[a-z']+", text.lower()))


def word_count(page):
    text = " ".join(
        [page["lede"]]
        + page["intro_body"]
        + [
            s["heading"] + " " + s["body"] + " " + " ".join(s.get("points", []))
            for s in page["sections"]
        ]
        + [q["question"] + " " + q["answer"] for q in page.get("faq", [])]
    )
    return len(re.findall(r"\S+", text))


def check_landing_content():
    print("\nLanding page content")
    path = ROOT / "content" / "landing_pages.yaml"
    if not path.exists():
        note("no landing_pages.yaml — skipping")
        return []
    pages = yaml.safe_load(path.read_text(encoding="utf-8"))["pages"] or []

    for field in ("title", "description", "h1", "slug"):
        dupes = [k for k, v in Counter(p[field] for p in pages).items() if v > 1]
        if dupes:
            fail(f"duplicate {field} across landing pages: {dupes}")
    if not failures:
        ok(f"{len(pages)} pages, all titles/descriptions/H1s/slugs unique")

    questions = [q["question"] for p in pages for q in p.get("faq", [])]
    dupe_q = [k for k, v in Counter(questions).items() if v > 1]
    if dupe_q:
        fail(f"FAQ question reused across pages (splits FAQ rich results): {dupe_q}")
    else:
        ok(f"{len(questions)} FAQ questions, none repeated")

    for p in pages:
        if len(p["title"]) > MAX_TITLE_CHARS:
            note(f"title {len(p['title'])} chars, may truncate in SERP: {p['slug']}")
        if len(p["description"]) > MAX_DESCRIPTION_CHARS:
            note(f"description {len(p['description'])} chars, may truncate: {p['slug']}")

    thin = [(p["slug"], word_count(p)) for p in pages if word_count(p) < MIN_WORDS]
    if thin:
        for slug, n in thin:
            fail(f"thin page ({n} words, want >{MIN_WORDS}): {slug}")
    else:
        ok(f"no thin pages (min {min(word_count(p) for p in pages)} words)")

    worst = (0.0, "", "")
    for a, b in itertools.combinations(pages, 2):
        wa, wb = body_words(a), body_words(b)
        j = len(wa & wb) / len(wa | wb)
        if j > worst[0]:
            worst = (j, a["slug"], b["slug"])
        if j > MAX_SIMILARITY:
            fail(f"near-duplicate copy ({j:.2f}): {a['slug']} vs {b['slug']}")
    if worst[0] <= MAX_SIMILARITY:
        ok(f"copy distinct (highest similarity {worst[0]:.2f}: {worst[1]} vs {worst[2]})")

    return pages


def check_built_html(pages):
    print("\nBuilt HTML")
    html_files = sorted(glob.glob(str(ROOT / "*.html")))
    for path in html_files:
        name = os.path.basename(path)
        html = Path(path).read_text(encoding="utf-8")

        h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        if len(h1s) != 1:
            fail(f"{name}: expected exactly 1 <h1>, found {len(h1s)}")

        if not re.search(r'<link rel="canonical"', html):
            fail(f"{name}: no canonical link")

        for block in re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', html, re.S
        ):
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                fail(f"{name}: malformed JSON-LD — {exc}")

        for href in re.findall(r'href="([^"]+)"', html):
            if href.startswith(("http", "mailto:", "tel:", "#")):
                continue
            target = href.split("#")[0]
            if target and not (ROOT / target).exists():
                fail(f"{name}: broken link -> {href}")
        for src in re.findall(r'src="([^"]+)"', html):
            if not src.startswith("http") and not (ROOT / src).exists():
                fail(f"{name}: broken asset -> {src}")

    ok(f"{len(html_files)} pages: one H1 each, canonical present, JSON-LD parses, links resolve")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>(.*?)</loc>", sitemap)
    in_sitemap = {loc.rsplit("/", 1)[-1] or "index.html" for loc in locs}
    missing = {os.path.basename(f) for f in html_files} - in_sitemap
    if missing:
        fail(f"pages missing from sitemap.xml: {sorted(missing)}")
    else:
        ok(f"sitemap.xml covers all {len(locs)} pages")

    # Orphan check: every landing page must be linked from somewhere else.
    if pages:
        linked = set()
        for path in html_files:
            name = os.path.basename(path)
            html = Path(path).read_text(encoding="utf-8")
            for href in re.findall(r'href="([^"]+\.html)"', html):
                if href != name:
                    linked.add(href.split("#")[0])
        orphans = [p["slug"] for p in pages if f"{p['slug']}.html" not in linked]
        if orphans:
            fail(f"orphaned pages, linked from nowhere: {orphans}")
        else:
            ok("no orphaned pages — every landing page is linked")


def check_homepage_meta():
    print("\nHomepage meta")
    content = yaml.safe_load(
        (ROOT / "content" / "site_content.yaml").read_text(encoding="utf-8")
    )
    seo = content["seo"]
    for field, limit in (("title", MAX_TITLE_CHARS), ("description", MAX_DESCRIPTION_CHARS)):
        n = len(seo[field])
        if n > limit:
            fail(f"homepage {field} is {n} chars, over the {limit} limit — will truncate in SERP")
        else:
            ok(f"homepage {field}: {n} chars")

    h1 = content["hero"]["heading"]
    if "property management" not in h1.lower():
        note(f"homepage H1 no longer contains the target phrase: {h1!r}")
    else:
        ok(f"homepage H1 carries the target phrase: {h1!r}")


def main():
    print("Keyper SEO checks")
    check_homepage_meta()
    pages = check_landing_content()
    check_built_html(pages)

    print()
    if failures:
        print(f"{len(failures)} check(s) FAILED")
        return 1
    print(f"All checks passed{f' ({len(notes)} note(s))' if notes else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
