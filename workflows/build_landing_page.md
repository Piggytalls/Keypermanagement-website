# Workflow: Build / Update the Keyper Landing Page

## Objective
Produce and maintain `index.html` (plus `robots.txt` and `sitemap.xml`) for
the Keyper property management landing page — a single static, SEO-optimized
page — without ever hand-editing generated HTML directly.

## Required inputs
- `content/site_content.yaml` — every piece of editable text on the site:
  business info & contact details, SEO metadata, hero copy, services, "why
  us" points, process steps, plans, service areas, FAQ, contact section,
  footer. This is the only file a content change should touch.
- `brand_assents/keyper_logo_centered.png` — the source brand logo (flat
  background, not transparent). Only touch this if the logo itself changes.
- `tools/icons.py` — the icon library. Every icon used anywhere on the site
  is defined here once, referenced by name from the YAML (e.g. `icon: key`).
  Only touch this to add a new icon or fix an existing glyph.
- `templates/index.html.j2`, `templates/robots.txt.j2`,
  `templates/sitemap.xml.j2` — page structure/layout. Only touch these to
  change the page's structure (new section, reordered blocks, new schema
  field) — not for text changes, which belong in the YAML.
- `assets/css/styles.css`, `assets/js/main.js` — static design system and
  interaction logic (brand colors/typography, mobile nav, FAQ accordion,
  scroll reveal). Hand-edited directly; not templated, since design tokens
  change far less often than content and don't need YAML indirection.

## Tools (in order of use)

### 1. `tools/prepare_brand_assets.py`
Derives every logo/favicon asset from the one source file in
`brand_assents/`. Only needs re-running when the source logo changes.

```
python3 tools/prepare_brand_assets.py
```

Produces in `assets/img/`:
- `keyper-logo.png` — verbatim copy of the source
- `keyper-logo-transparent.png` — background color-keyed out, used in the
  header (on light bg) and footer (inverted to white via CSS `filter` —
  this only works because the background is actually transparent, not just
  the same color as the page)
- `favicon-512.png`, `favicon-32.png`, `favicon-16.png`,
  `apple-touch-icon.png` — square crops of just the house+key mark

**Known constraint:** the icon-mark crop uses a hardcoded search window
(`ICON_SEARCH_Y`, `ICON_SEARCH_X_MAX` in the script) tuned to the current
logo's layout. If a redesigned logo has the glyph in a different position,
re-tune those two constants (or crop manually) before re-running.

### 2. `tools/build_site.py`
Renders `content/site_content.yaml` through the Jinja2 templates in
`templates/` into `index.html`, `robots.txt`, and `sitemap.xml` at the
project root.

```
python3 tools/build_site.py
```

This is the **only** thing that should ever write those three files. They
each carry a "GENERATED FILE — do not hand-edit" header; if you find
yourself about to edit `index.html` directly, stop — the change belongs in
`content/site_content.yaml` (text/data) or `templates/index.html.j2`
(structure), then rerun this script.

### Dependencies
```
pip install -r requirements.txt   # Jinja2, PyYAML, Pillow
```

## Standard operating procedure

**To change site text, contact info, services, plans, FAQ, or SEO copy:**
1. Edit `content/site_content.yaml`.
2. Run `python3 tools/build_site.py`.
3. Verify (see below).

**To change page structure or add a new section:**
1. Edit `templates/index.html.j2` (and add any new content fields to
   `content/site_content.yaml`).
2. If new icons are needed, add them to `tools/icons.py` first, then
   reference by name from the YAML/template.
3. Run `python3 tools/build_site.py`.
4. Verify.

**To change the logo:**
1. Replace `brand_assents/keyper_logo_centered.png`.
2. Run `python3 tools/prepare_brand_assets.py`.
3. Check `assets/img/keyper-logo-transparent.png` visually — if the crop
   is off, adjust `ICON_SEARCH_Y`/`ICON_SEARCH_X_MAX` in
   `tools/prepare_brand_assets.py` and rerun.
4. Run `python3 tools/build_site.py` (in case any logo-derived text/paths
   changed) and verify.

**To change brand colors/fonts:**
Edit the CSS custom properties at the top of `assets/css/styles.css`
directly (`:root { --bark: ...; }` etc.) — no rebuild needed, it's static.

## Verification
No test suite exists for a static marketing page — verify visually:
```
python3 -m http.server 8791 &
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --screenshot=.tmp/preview.png \
  --window-size=1440,4600 http://localhost:8791/index.html
```
Then read `.tmp/preview.png` (or view http://localhost:8791/ in a normal
browser) and check the changed section renders as expected before
considering the change done. Kill the server afterward
(`pkill -f "http.server 8791"`).

## Known issues / lessons learned
- **Flat-background logo + CSS invert filter = blank box.** The source
  brand logo has an opaque background rectangle, not transparency. Applying
  `filter: brightness(0) invert(1)` (to show it in white on the dark
  footer) to the *opaque* version turns the entire rectangle solid white,
  not just the mark. Fix: always use
  `assets/img/keyper-logo-transparent.png` (produced by
  `prepare_brand_assets.py`) anywhere the logo needs to sit on a non-Paper
  background or be color-inverted.
- **Favicons need the icon mark alone, not the full wordmark.** A favicon
  built from the full "house+key + Keyper + tagline" lockup scaled down to
  16–32px is illegible. `prepare_brand_assets.py` crops just the house+key
  glyph before generating favicon sizes.

## Outstanding items owned by the business, not this pipeline
- `business.domain` in `content/site_content.yaml` is a placeholder
  (`https://www.keyperpaphos.com`) until a real domain is registered —
  update it there (feeds canonical URL, Open Graph, robots.txt, sitemap).
- The contact form (`.contact-form` in the template) is front-end only —
  it needs a real backend or a form service (e.g. Formspree) wired into
  `assets/js/main.js` before launch.
