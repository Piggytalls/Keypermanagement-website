#!/usr/bin/env python3
"""
Render the Keyper landing page from content/site_content.yaml + templates/.

This is the ONLY thing that should ever write index.html, robots.txt or
sitemap.xml. To change site text, contact details, services, plans, FAQ,
etc. — edit content/site_content.yaml and rerun this script. Do not
hand-edit the generated files; they carry a header saying so, but the
build will silently clobber any manual edits next time it runs.

Usage:
    python3 tools/build_site.py
    python3 tools/build_site.py --content content/site_content.yaml --out .
"""

import argparse
import datetime
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

sys.path.insert(0, str(Path(__file__).parent))
from icons import render_icon  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def load_content(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def icon_global(name, stroke_width=None, viewbox=None, cls=None):
    return Markup(render_icon(name, stroke_width=stroke_width, viewbox=viewbox, cls=cls))


def build(content_path: Path, templates_dir: Path, out_dir: Path,
          landing_path: Path) -> None:
    content = load_content(content_path)

    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.globals["icon"] = icon_global
    env.globals["current_year"] = datetime.date.today().year
    env.globals["build_date"] = datetime.date.today().isoformat()

    # SEO landing pages live in their own content file — one entry per page,
    # each rendered through templates/landing.html.j2. Exposed to every
    # template as `landing_pages` (for nav/footer/sitemap links) and
    # `pages_by_slug` (so a page can look up its `related` siblings).
    landing = load_content(landing_path) if landing_path.exists() else {"pages": []}
    landing_pages = landing.get("pages") or []
    content["landing_pages"] = landing_pages
    content["pages_by_slug"] = {p["slug"]: p for p in landing_pages}

    targets = {
        "index.html.j2": out_dir / "index.html",
        "privacy.html.j2": out_dir / "privacy.html",
        "terms.html.j2": out_dir / "terms.html",
        "robots.txt.j2": out_dir / "robots.txt",
        "sitemap.xml.j2": out_dir / "sitemap.xml",
    }

    for template_name, out_path in targets.items():
        template = env.get_template(template_name)
        rendered = template.render(**content)
        out_path.write_text(rendered, encoding="utf-8")
        print(f"  wrote {out_path.relative_to(ROOT)}")

    landing_template = env.get_template("landing.html.j2")
    for page in landing_pages:
        out_path = out_dir / f"{page['slug']}.html"
        rendered = landing_template.render(page=page, **content)
        out_path.write_text(rendered, encoding="utf-8")
        print(f"  wrote {out_path.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--content",
        default=str(ROOT / "content" / "site_content.yaml"),
        help="Path to the YAML content file",
    )
    parser.add_argument(
        "--templates",
        default=str(ROOT / "templates"),
        help="Path to the templates directory",
    )
    parser.add_argument(
        "--out",
        default=str(ROOT),
        help="Directory to write generated files into",
    )
    parser.add_argument(
        "--landing",
        default=str(ROOT / "content" / "landing_pages.yaml"),
        help="Path to the SEO landing-page content file",
    )
    args = parser.parse_args()

    print("Building Keyper site...")
    build(Path(args.content), Path(args.templates), Path(args.out),
          Path(args.landing))
    print("Done.")


if __name__ == "__main__":
    main()
