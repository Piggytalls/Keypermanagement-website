"""
Shared line-icon library for the Keyper site.

Every icon is a minimal, single-stroke SVG in the visual language set out in
brand_assents/keyper_board.png (round caps/joins, currentColor stroke, no fill).
Keyed by name so content/site_content.yaml can reference icons without any
markup living outside this file.

Usage (from tools/build_site.py, exposed to Jinja as the `icon()` global):
    icon("key")                    -> default 24x24, stroke-width 1.7
    icon("check", stroke_width=2)  -> per-call override
"""

ICONS = {
    # --- trust / status ---
    "phone": {
        "paths": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/>',
    },
    "shield-check": {
        "paths": '<path d="M12 2 3 7v6c0 5 3.8 8.7 9 9 5.2-.3 9-4 9-9V7l-9-5Z"/><path d="m9 12 2 2 4-4"/>',
    },
    "shield": {
        "paths": '<path d="M12 2 3 7v6c0 5 3.8 8.7 9 9 5.2-.3 9-4 9-9V7l-9-5Z"/>',
    },
    "shield-clock": {
        "paths": '<path d="M12 2 3 7v6c0 5 3.8 8.7 9 9 5.2-.3 9-4 9-9V7l-9-5Z"/><path d="M12 7v5l3 3"/>',
    },
    "clock": {
        "paths": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
    },
    "grid": {
        "paths": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 3v18M9 9h12"/>',
    },
    "check": {
        "paths": '<path d="m20 6-11 11-5-5"/>',
    },

    # --- services ---
    "search": {
        "paths": '<circle cx="10" cy="10" r="6.5"/><path d="m20.5 20.5-4.8-4.8"/><path d="m8 10 1.5 1.5L13 8"/>',
    },
    "search-plain": {
        "paths": '<circle cx="9" cy="9" r="6.5"/><path d="m19.5 19.5-4.8-4.8"/>',
    },
    "key": {
        "paths": '<circle cx="8" cy="15" r="4"/><path d="M11 12 20 3"/><path d="M16 7l3 3"/><path d="M13 10l2.5 2.5"/>',
    },
    "clean": {
        "paths": '<path d="M6 3v6M10 3v6M6 9c0 3-2 3-2 6a4 4 0 0 0 8 0c0-3-2-3-2-6"/><path d="M17 21v-6"/><path d="M14 13c0-3 3-3 3-6 0 3 3 3 3 6a3 3 0 0 1-6 0Z"/>',
    },
    "waves": {
        "paths": '<path d="M2 12c1.5 1.5 3 1.5 4.5 0s3-1.5 4.5 0 3 1.5 4.5 0 3-1.5 4.5 0"/><path d="M2 18c1.5 1.5 3 1.5 4.5 0s3-1.5 4.5 0 3 1.5 4.5 0 3-1.5 4.5 0"/><path d="M12 3v6"/><path d="M9 6h6"/>',
    },
    "leaf": {
        "paths": '<path d="M4 20c8-1 12-6 12-16 -10 0-15 4-16 12 -1 6 0 4 4 4Z"/><path d="M9 15c2-3 4-6 9-9"/>',
    },
    "window": {
        "paths": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M12 3v18M4 12h16"/>',
    },
    "climate": {
        "paths": '<path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/><circle cx="12" cy="12" r="4"/>',
    },
    "mail": {
        "paths": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    },
    "wrench": {
        "paths": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.1-3.1a4 4 0 0 1-4.9 4.9L4.1 22 2 19.9 12.1 9.1a4 4 0 0 1 4.9-4.9Z"/>',
    },
    "gift": {
        "paths": '<path d="M20 12v9H4v-9M2 7h20v5H2zM12 22V7M12 7c-1.5-3-6-3.5-6-1s3 1 6 1M12 7c1.5-3 6-3.5 6-1s-3 1-6 1"/>',
    },
    "report-check": {
        "paths": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 2v4M16 2v4"/><path d="m8 15 2.5 2.5L16 12"/>',
    },

    # --- location / social ---
    "pin": {
        "paths": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
    },
    "facebook": {
        "paths": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    },
    "instagram": {
        "paths": '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/>',
    },
    "whatsapp": {
        "paths": '<path d="M21 11.5a8.5 8.5 0 0 1-12.3 7.6L3 20l1-5.5A8.5 8.5 0 1 1 21 11.5Z"/><path d="M8.5 10.5c.5 2.5 2.5 4.5 5 5"/>',
    },

    # --- one-off hero mark (house + key), wider viewBox, thicker stroke ---
    "hero-glyph": {
        "viewbox": "0 0 200 130",
        "stroke_width": 7,
        "paths": '<path d="M15 75 65 30 90 52"/><path d="M35 75v35"/><path d="M90 52h68"/><path d="M128 52v22"/><path d="M144 52v22"/>',
    },
}


def render_icon(name, stroke_width=None, viewbox=None, cls=None):
    """Return a self-contained <svg> string for the named icon."""
    try:
        data = ICONS[name]
    except KeyError:
        raise KeyError(
            f"Unknown icon '{name}'. Available icons: {', '.join(sorted(ICONS))}"
        )
    vb = viewbox or data.get("viewbox", "0 0 24 24")
    sw = stroke_width or data.get("stroke_width", 1.7)
    class_attr = f' class="{cls}"' if cls else ""
    return (
        f'<svg{class_attr} viewBox="{vb}" fill="none" stroke="currentColor" '
        f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
        f'{data["paths"]}</svg>'
    )
