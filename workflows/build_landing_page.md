# Workflow: Build / Update the Keyper Landing Page

## Objective
Produce and maintain `index.html` (plus `robots.txt` and `sitemap.xml`) for
the Keyper property management landing page — a single static, SEO-optimized
page — without ever hand-editing generated HTML directly.

## Required inputs
- `content/site_content.yaml` — every piece of editable text on the site:
  business info & contact details, SEO metadata, hero copy, services, "why
  us" points, process steps, plans, service areas, FAQ, contact section,
  footer, legal (last-updated date for Privacy/Terms). This is the only file
  a content change should touch.
- `brand_assents/keyper_logo_centered.png` — the source brand logo (flat
  background, not transparent). Only touch this if the logo itself changes.
- `tools/icons.py` — the icon library. Every icon used anywhere on the site
  is defined here once, referenced by name from the YAML (e.g. `icon: key`).
  Only touch this to add a new icon or fix an existing glyph.
- `templates/index.html.j2`, `templates/privacy.html.j2`,
  `templates/terms.html.j2`, `templates/robots.txt.j2`,
  `templates/sitemap.xml.j2` — one Jinja source per generated page/file.
  Only touch these to change a page's structure (new section, reordered
  blocks, new schema field) — not for text changes, which belong in the YAML.
- `templates/_header.html.j2`, `templates/_footer.html.j2`,
  `templates/_head-assets.html.j2` — shared partials included by every page
  template (top bar with email + social icons, nav/footer markup, favicons,
  font preload, stylesheet link). Edit these once to change something that
  appears on every page. They rely on a `subpage` context variable (see
  "Adding a new page" below) to know whether in-page anchors like
  `#services` need an `index.html` prefix. `footer.social` in the YAML
  drives both the top bar's icons and the footer's — one list, two
  placements — so adding/removing a social link only needs one edit.
- `assets/css/styles.css`, `assets/js/main.js` — static design system and
  interaction logic (brand colors/typography, mobile nav, FAQ accordion,
  scroll reveal, post-submit confirmation banner). Hand-edited directly; not
  templated, since design tokens change far less often than content and
  don't need YAML indirection.
- `assets/fonts/*.woff2` — self-hosted Inter/Poppins (Latin subset only,
  weights 400/500/600/700). Loaded via `@font-face` in `styles.css`, not
  Google's font CDN — see "Known issues" below for why.
- `assets/img/photos/*.jpg` — AI-generated (Higgsfield `soul_location`)
  photography woven into the page as "spotlight" panels (see `spotlights` in
  the YAML and `templates/_spotlight.html.j2`), not a real photo gallery.
  These are illustrative, not photos of actual managed properties — see
  "Known issues" below for the generation process and "Outstanding items"
  for when to replace them with real photography.

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
`templates/` into `index.html`, `privacy.html`, `terms.html`, `robots.txt`,
and `sitemap.xml` at the project root. Also injects `current_year` and
`build_date` (today's date, used for sitemap `<lastmod>`) as template
globals.

```
python3 tools/build_site.py
```

This is the **only** thing that should ever write those five files. They
each carry a "GENERATED FILE — do not hand-edit" header; if you find
yourself about to edit `index.html` directly, stop — the change belongs in
`content/site_content.yaml` (text/data) or the relevant `templates/*.j2`
file (structure), then rerun this script.

**Adding a new top-level page** (e.g. a future blog or About page):
1. Add a `templates/<name>.html.j2` that includes `_head-assets.html.j2` in
   its `<head>`, sets `{% set subpage = true %}` before including
   `_header.html.j2`, then includes `_footer.html.j2` before `</body>`.
   `subpage = true` makes the header/footer partials prefix in-page anchors
   (e.g. `#services`) with `index.html` so nav links still work from a
   subpage — omit it only for `index.html.j2` itself.
2. Add it to the `targets` dict in `tools/build_site.py`.
3. Add a `<url>` entry for it in `templates/sitemap.xml.j2`.
4. Link to it from wherever makes sense (e.g. `footer.columns` in the YAML).

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
considering the change done. Also spot-check `privacy.html`/`terms.html` if
a shared partial (`_header`, `_footer`, `_head-assets`) or `styles.css`
changed, since they render on every page. Kill the server afterward
(`pkill -f "http.server 8791"`).

**Don't trust `--screenshot ... --window-size=W,H` for narrow/mobile
widths on this machine's Chrome (149.x).** It renders at some other
internal width (observed: floors around 390-500px) and then scales the
output PNG down to the requested `W,H` — so a `--window-size=390,140`
screenshot can show elements as "cut off past the right edge" that are
actually fine at a real 390px viewport. This looks exactly like a
horizontal-overflow bug but isn't one. To check real narrow-viewport
layout, drive Chrome via CDP instead: launch with
`--remote-debugging-port=<port>`, open its websocket from
`GET localhost:<port>/json/list`, send
`Emulation.setDeviceMetricsOverride` with explicit `width`, `height`,
`deviceScaleFactor` (2, not 1 — needed to get a true sub-450px result
in practice) and `mobile: true`, *then* `Page.captureScreenshot` or
`Runtime.evaluate` for `getBoundingClientRect()`/`innerWidth`. Node 20+'s
built-in global `WebSocket` can drive this with no extra packages.

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
- **Google Fonts CDN is a GDPR risk for an EU-based site.** Loading fonts
  from `fonts.googleapis.com`/`fonts.gstatic.com` sends every visitor's IP
  to Google before consent — this was the subject of real EU court rulings.
  Fonts are self-hosted instead: `assets/fonts/*.woff2` were pulled once
  with `curl -A "<modern browser UA>" "https://fonts.googleapis.com/css2?..."`
  to get the actual `fonts.gstatic.com` file URLs, downloaded, and wired
  into `@font-face` rules at the top of `styles.css` (Latin subset only —
  this site has no non-Latin content). If a new weight/family is ever
  needed, repeat that process rather than re-adding the CDN `<link>`.
- **Contact form → FormSubmit, not Formspree.** Formspree now requires a
  signup to get a form ID; the genuinely no-signup option is FormSubmit
  (`https://formsubmit.co/<email>`, form `action` in `index.html.j2`). It
  redirects to `_next` (set to `{{ business.domain }}/?sent=true#contact`)
  on success; `main.js` detects `?sent=true` on load, swaps the form note
  for a success message, and cleans the URL via `history.replaceState`.
  First-ever submission triggers a one-time confirmation email to
  `business.email` that must be clicked to activate delivery.

- **AI-generated photography needs a "no people" prompt and still needs a
  visual check.** `assets/img/photos/*.jpg` were generated with
  `higgsfield generate create soul_location --prompt "..." --aspect_ratio 3:2
  --wait`, then resized to 1400px-wide JPEG (quality 82) with Pillow — the
  raw 2016px PNGs are ~3-5MB, far too heavy for a page image. First attempts
  at the villa-exterior and bedroom shots came back with unwanted people and
  a rendering artifact (a blank rectangle) respectively; re-prompting with
  explicit "no people, no figures, no humans", "no blank patches", and a
  changed camera angle fixed both. Always view generated images at full
  size before shipping them — don't assume the first result is clean.

## Outstanding items owned by the business, not this pipeline
- The `spotlights` photos in `content/site_content.yaml` are AI-generated
  illustrative imagery (see above), not real photos of properties Keyper
  manages. Swap in real photography as soon as it exists — genuine photos of
  actual managed villas/pools would be a meaningful trust upgrade over
  synthetic images, the same way real testimonials would beat having none.
- No live social pages exist yet — `footer.social` only lists WhatsApp
  (a real, working link). Add Facebook/Instagram entries once those pages
  exist; don't link to placeholder `#` hrefs, they read as broken/unfinished.
- No real testimonials/reviews exist yet, so none are featured. Once you
  have genuine ones (with attribution), a testimonials section with
  `Review`/`AggregateRating` schema would be a meaningful SEO/trust addition
  — don't fabricate reviews in the meantime.
- `privacy.html` / `terms.html` are standard boilerplate covering the
  contact form's data flow (FormSubmit as processor, GDPR rights, Cyprus
  jurisdiction). Have a lawyer review before relying on them.
- No analytics/Search Console verification is wired in. Add a Google
  Search Console `<meta>` verification tag and/or an analytics snippet to
  `templates/_head-assets.html.j2` if/when you want traffic data — note
  this reopens the third-party-request/consent question the font
  self-hosting was solving, so a cookie-consent banner would likely be
  needed alongside it.
