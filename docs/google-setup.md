# Google setup — the off-site half of the SEO work

Everything in this file needs a login to a Google account, so it can't be
done from this repo. The site-side wiring is already in place; what's left
is paste-and-click work.

Order matters: **Search Console first** (so indexing starts as early as
possible — it takes weeks), **Business Profile second**, **reviews
ongoing**.

---

## 1. Google Search Console — get the site indexed

Until this is done, nothing you publish is on a timetable you control.

1. Go to <https://search.google.com/search-console>
2. **Add property → URL prefix →** `https://www.keypermanagement.com`
3. Choose the **HTML tag** verification method. Google shows you something like:
   ```html
   <meta name="google-site-verification" content="AbC123xyz..." />
   ```
4. Copy **only the token** — the `AbC123xyz...` part, not the whole tag.
5. Paste it into `content/site_content.yaml`:
   ```yaml
   seo:
     google_site_verification: "AbC123xyz..."
   ```
6. Rebuild and publish:
   ```
   python3 tools/build_site.py && python3 tools/check_seo.py
   git add -A && git commit -m "Add Search Console verification" && git push
   ```
7. Wait ~1 minute for Vercel to deploy, then click **Verify** in Search Console.
8. Once verified: **Sitemaps →** enter `sitemap.xml` → Submit.
9. **URL Inspection →** paste the homepage URL → **Request Indexing**. Repeat
   for the landing pages you care most about. This is the fastest way to get
   a brand-new page looked at.

The meta tag renders on all 11 pages automatically and disappears if the
token is left empty, so there's nothing to clean up later.

> If you'd rather not put a token in the repo, the **DNS** verification
> method works too (a TXT record at your domain registrar) and needs no
> site change at all. Either is fine — DNS is slightly more robust because
> it survives site rebuilds.

---

## 2. Google Business Profile — the biggest lever you have

The listing already exists ("Keyper Property Management Paphos"). It needs
filling out completely. For local searches this outranks everything on the
website.

Manage it at <https://business.google.com>.

### Do not do these — they risk suspension, not just poor ranking

- **Don't put keywords in the business name.** "Keyper Property Management
  Paphos – Villa Care & Damp Specialists" is a guideline violation and a
  common cause of suspended listings. The name must be the real-world
  business name.
- **Don't use stock photos.** Real photos of real work only.
- **Don't offer anything in exchange for reviews** (discounts, entries into
  a draw). Against policy and grounds for review removal.

### Business name

```
Keyper Property Management
```

### Categories

Pick from Google's dropdown — these are the ones to look for, not exact
strings you can paste:

- **Primary:** Property management company
- Secondary: Property maintenance · Cleaning service · Waterproofing service ·
  Swimming pool repair service · Handyman · Air conditioning repair service ·
  Painter · Landscaper

Primary category carries by far the most weight. Leave it as property
management even though you do repair work — that's the search you want.

### Description (750 character limit — this is 723)

```
Keyper is a property management company in Paphos, Cyprus, looking after
villas, apartments and holiday homes for owners who live abroad. We handle
the routine care — scheduled inspections with photo reports, secure key
holding, cleaning and guest changeovers, pool and garden maintenance, air
conditioning servicing and post collection — and the work most managers
subcontract. Our own maintenance team carries out general repairs, damp
treatment and waterproofing, and renovations from tiling and plastering
through to full bathroom and kitchen refits. We cover Paphos town, Peyia,
Coral Bay, Tala, Polis Chrysochous, Kissonerga, Chlorakas and Emba. One
local contact, quoted before we start, photographed when it's done.
```

### Service areas

Paphos · Peyia · Coral Bay · Tala · Polis Chrysochous · Kissonerga ·
Chlorakas · Emba

### Services

Add each as a service with its own short description. These match the
website exactly, which is what you want — consistency between the profile
and the site is itself a ranking signal.

| Service | Description |
|---|---|
| Property Inspections | Scheduled visits inside and out, with a full photo report sent straight to you. |
| Key Holding & Secure Access | Safe, insured key custody so we can act the moment you need us to. |
| Cleaning & Changeovers | Routine housekeeping and guest turnover cleaning, done properly every time. |
| Pool Maintenance | Chemical balancing, filter care and regular cleaning, year-round. |
| Garden & Landscaping | Regular upkeep for olive trees, lawns and outdoor spaces, in every season. |
| Villa & Window Cleaning | Interior and exterior cleaning, inside and out. |
| Air Conditioning Servicing | Seasonal checks and maintenance to keep every unit running efficiently. |
| Mail & Post Collection | We collect and safely hold your post while you're away. |
| Owner Reporting | Clear digital reports after every visit. |
| General Repairs | Plumbing, electrics, carpentry and everyday fixes by our own team. |
| Renovations & Upgrades | Tiling, plastering, painting and joinery through to full room renovations. |
| Damp Treatment & Waterproofing | We trace the source, treat the walls and waterproof roofs, terraces and balconies. |
| Maintenance Team On Call | An in-house team in Paphos, usually with you the same day or the next. |
| 24/7 Emergency Support | Around-the-clock response for anything urgent. |
| Welcome Packs & Guest Prep | Fresh linens, groceries and a warm welcome for your guests. |

### Still needed from you

These can't be written for you — they're facts only you have:

- [ ] **Opening hours** (and whether the 24/7 emergency line is listed separately)
- [ ] **Photos** — exterior, team, and genuine before/after shots of damp and
      renovation work. Before/afters are the single most persuasive thing
      you can put on the profile, and nobody else's stock photos compete.
- [ ] **Attributes** — "Online estimates", "Language spoken: English", etc.
- [ ] Confirm the website link points to `https://www.keypermanagement.com`

---

## 3. Reviews — the thing that actually moves you up

Nothing else on this page will do as much. A listing with a handful of
genuine, recent, detailed reviews outranks an empty one almost regardless
of what the websites look like.

### Your review link

Derived from the CID in the business's own Google Maps URL:

```
https://maps.google.com/?cid=10786859233864422310
```

**Click it once and confirm it opens the Keyper listing before sending it
to anyone** — I derived it from the Maps link in `site_content.yaml` but
couldn't verify the destination automatically (Google shows a consent wall
to automated requests).

The more reliable route: in Google Business Profile there's an **"Ask for
reviews"** button that generates a short `g.page/r/...` link which opens the
review box directly. Use that one if you can get it.

### How to ask

Ask **every** client, not just the happy ones — filtering for positive
reviews ("review gating") is against Google's policy. Ask soon after you've
done something visible: a completed renovation, a damp job, the first photo
report after a handover.

**WhatsApp / SMS**

> Hi [name] — glad the [job] worked out. If you have a minute, a quick
> Google review would really help us; we're a new business in Paphos and
> it makes a big difference. Takes about 30 seconds: [link]
> Thanks either way. — [your name], Keyper

**Email, after a completed job**

> Hi [name],
>
> The [bathroom / damp treatment / first inspection] is finished and the
> photos are attached.
>
> One small favour: if you're happy with how it went, would you leave us a
> Google review? We started Keyper this year and reviews are how people in
> your position decide whether to trust a management company with their
> keys. It takes under a minute: [link]
>
> If anything wasn't right, reply to this instead and we'll put it straight.
>
> Best,
> [your name] — Keyper Property Management

That last line matters. It gives an unhappy client somewhere to go that
isn't a public review, without gating anyone out of reviewing.

### Reply to every review

Google weights owner responses, and prospective clients read them. Reply to
positives briefly and specifically; reply to negatives calmly, factually,
and without arguing. A well-handled bad review costs you far less than
silence.

### Once reviews exist

Tell me and I'll add `AggregateRating` schema to the site. Worth knowing:
Google no longer shows star ratings in search results for *self-serving*
reviews (a business rating itself on its own site), so the benefit is
credibility for visitors rather than stars in the SERP. The reviews on the
Business Profile are where the ranking value sits. **Don't invent reviews
for the website** — this is the one thing here that can do real damage.

---

## Realistic timeline

| When | What to expect |
|---|---|
| Days 1–3 | Verification done, sitemap submitted, indexing requested |
| Weeks 1–4 | Pages begin appearing for very specific searches (e.g. "damp treatment Paphos") |
| Months 2–6 | Movement on area terms, if reviews are accumulating |
| Ongoing | The head term "property management Paphos" is a long game against a 15-year incumbent and an exact-match domain |

Reviews and photos are what compress that timeline. The website work is
already done.
