"""Lucide-style inline SVG icon set + subtle status badges.

No emoji, no extra dependencies: icons are plain SVG strings rendered with
st.markdown(..., unsafe_allow_html=True). Stroke-based 24x24 style.
"""

# Inner SVG content per icon (paths only, shared <svg> wrapper adds styling).
_ICONS = {
    "home": (
        '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>'
        '<polyline points="9 22 9 12 15 12 15 22"/>'
    ),
    "file-plus": (
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
        '<line x1="12" y1="18" x2="12" y2="12"/>'
        '<line x1="9" y1="15" x2="15" y2="15"/>'
    ),
    "package": (
        '<path d="M16.5 9.4 7.55 4.24"/>'
        '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>'
        '<polyline points="3.29 7 12 12 20.71 7"/>'
        '<line x1="12" y1="22" x2="12" y2="12"/>'
    ),
    "search": (
        '<circle cx="11" cy="11" r="8"/>'
        '<line x1="21" y1="21" x2="16.65" y2="16.65"/>'
    ),
    "target": (
        '<circle cx="12" cy="12" r="10"/>'
        '<circle cx="12" cy="12" r="6"/>'
        '<circle cx="12" cy="12" r="2"/>'
    ),
    "map-pin": (
        '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>'
        '<circle cx="12" cy="10" r="3"/>'
    ),
    "calendar": (
        '<rect x="3" y="4" width="18" height="18" rx="2"/>'
        '<line x1="16" y1="2" x2="16" y2="6"/>'
        '<line x1="8" y1="2" x2="8" y2="6"/>'
        '<line x1="3" y1="10" x2="21" y2="10"/>'
    ),
    "droplet": '<path d="M12 2.7 17.66 8.36a8 8 0 1 1-11.31 0z"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "phone": (
        '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 '
        '19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 '
        '2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 '
        '2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>'
    ),
    "tag": (
        '<path d="M20.59 13.41 11 3H4v7l9.59 9.59a2 2 0 0 0 2.82 0l4.18-4.18a2 2 0 0 0 0-2.82z"/>'
        '<circle cx="7.5" cy="7.5" r="1.5"/>'
    ),
    "info": (
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="12" y1="16" x2="12" y2="12"/>'
        '<line x1="12" y1="8" x2="12.01" y2="8"/>'
    ),
}

# Subtle badge palette: light background + darker text. Color = status only.
_BADGE_COLORS = {
    "grey": ("#f1f5f9", "#475569"),
    "red": ("#fef2f2", "#b91c1c"),
    "green": ("#f0fdf4", "#15803d"),
    "amber": ("#fffbeb", "#b45309"),
    "blue": ("#eff6ff", "#1d4ed8"),
}


def icon(name, size=18, color="currentColor"):
    """Return an inline SVG string for the given icon name."""
    inner = _ICONS.get(name, _ICONS["info"] if "info" in _ICONS else "")
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" '
        'style="vertical-align:-3px">%s</svg>' % (size, size, color, inner)
    )


def icon_text(name, text, size=18, color="currentColor"):
    """Icon + text on one inline-flex row."""
    return (
        '<span style="display:inline-flex;align-items:center;gap:6px;">%s'
        "<span>%s</span></span>" % (icon(name, size, color), text)
    )


def badge(text, tone="grey"):
    """Subtle pill badge. Tone only conveys status (lost/found/score)."""
    bg, fg = _BADGE_COLORS.get(tone, _BADGE_COLORS["grey"])
    return (
        '<span style="display:inline-block;padding:2px 10px;border-radius:999px;'
        'font-size:12px;font-weight:600;background:%s;color:%s;">%s</span>'
        % (bg, fg, text)
    )


def type_badge(report_type):
    """Status badge for a report: red Lost, green Found."""
    if report_type == "lost":
        return badge("Lost", "red")
    return badge("Found", "green")


def score_badge(score):
    """Status badge for a match score: stronger match, stronger green."""
    if score >= 85:
        return badge("%d%% match" % score, "green")
    if score >= 70:
        return badge("%d%% match" % score, "blue")
    return badge("%d%% match" % score, "amber")


def icon_data_uri(name, color="#475569", size=18):
    """Same icon as a URL-encoded SVG data URI (for CSS background icons)."""
    from urllib.parse import quote

    inner = _ICONS.get(name, _ICONS["info"])
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">%s</svg>'
        % (size, size, color, inner)
    )
    return "data:image/svg+xml," + quote(svg, safe="")


def nav_icon_css(icon_names):
    """Scoped CSS: one matching SVG icon before each sidebar radio label.

    Keeps the native Streamlit radio (layout, spacing, active state) and
    only prepends an icon to the label text of each option, in order.
    """
    rules = [
        # Align icon + label text on one row.
        'section[data-testid="stSidebar"] div[data-testid="stRadio"] '
        'div[role="radiogroup"] > label > div:last-child {'
        "display:flex;align-items:center;gap:8px;}",
    ]
    for position, name in enumerate(icon_names, 1):
        rules.append(
            'section[data-testid="stSidebar"] div[data-testid="stRadio"] '
            'div[role="radiogroup"] > label:nth-of-type(%d) > div:last-child::before {'
            'content:"";width:18px;height:18px;flex-shrink:0;'
            'background:no-repeat center/contain url("%s");}'
            % (position, icon_data_uri(name))
        )
    return "<style>\n%s\n</style>" % "\n".join(rules)
