"""Rule-based lost-vs-found matching. Simple, deterministic, easy to explain.

Scoring (max 100):
    Category match        25
    Item name similarity  25
    Color match           15
    Location similarity   20
    Description keywords  10
    Date proximity         5
"""

import re
from datetime import datetime

# Single place for the threshold: score >= 60 shows as a possible match.
MATCH_THRESHOLD = 60

CATEGORY_POINTS = 25
NAME_POINTS = 25
COLOR_POINTS = 15
LOCATION_POINTS = 20
DESC_POINTS = 10
DATE_POINTS = 5


def normalize(text):
    """Lowercase, drop punctuation, collapse spaces: 'Black  Wallet!' -> 'black wallet'."""
    if not text:
        return ""
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return " ".join(text.split())


def word_overlap(a, b):
    """Fraction of words in 'a' also found in 'b' (0.0 to 1.0)."""
    words_a = set(normalize(a).split())
    words_b = set(normalize(b).split())
    if not words_a or not words_b:
        return 0.0
    return len(words_a & words_b) / len(words_a)


def _date_points(lost_date, found_date):
    """Closer dates score higher: <=3 days full, <=7 partial, <=30 small."""
    try:
        d1 = datetime.fromisoformat(str(lost_date)).date()
        d2 = datetime.fromisoformat(str(found_date)).date()
    except (ValueError, TypeError):
        return 0
    gap = abs((d1 - d2).days)
    if gap <= 3:
        return DATE_POINTS
    if gap <= 7:
        return 3
    if gap <= 30:
        return 1
    return 0


def score_match(lost, found):
    """Compare one lost and one found report. Returns (score, reasons dict)."""
    reasons = {}
    score = 0

    # Category: exact match after cleanup (e.g. "personal" == "Personal ").
    if normalize(lost.get("category")) == normalize(found.get("category")):
        score += CATEGORY_POINTS
        reasons["Category matched"] = True

    # Item name: proportional word overlap, so "wallet" matches "black leather wallet".
    name_sim = word_overlap(lost.get("item_name"), found.get("item_name"))
    name_pts = round(name_sim * NAME_POINTS)
    if name_pts > 0:
        score += name_pts
        if name_sim >= 0.99:
            reasons["Item name matched"] = True
        else:
            reasons["Item name similar (%d%% words overlap)" % round(name_sim * 100)] = True

    # Color: exact match after cleanup.
    if normalize(lost.get("color")) == normalize(found.get("color")):
        score += COLOR_POINTS
        reasons["Color matched"] = True

    # Location: overlap, so "Computer Lab" matches "lab, computer block".
    loc_sim = word_overlap(lost.get("location"), found.get("location"))
    loc_pts = round(loc_sim * LOCATION_POINTS)
    if loc_pts > 0:
        score += loc_pts
        reasons["Location matched" if loc_sim >= 0.99 else
                "Location similar (%d%% overlap)" % round(loc_sim * 100)] = True

    # Description: any shared meaningful word (>2 letters) earns the points.
    lost_words = {w for w in normalize(lost.get("description")).split() if len(w) > 2}
    found_words = {w for w in normalize(found.get("description")).split() if len(w) > 2}
    if lost_words & found_words:
        score += DESC_POINTS
        reasons["Description keywords matched"] = True

    # Date: nearer dates score more.
    date_pts = _date_points(lost.get("report_date"), found.get("report_date"))
    if date_pts > 0:
        score += date_pts
        reasons["Date close" if date_pts == DATE_POINTS else "Date nearby"] = True

    return min(score, 100), reasons


def find_matches(lost_report, found_reports):
    """Score one lost report against every found report, keep >= threshold."""
    results = []
    for found in found_reports:
        score, reasons = score_match(lost_report, found)
        if score >= MATCH_THRESHOLD:
            results.append({"report": found, "score": score, "reasons": reasons})
    results.sort(key=lambda r: r["score"], reverse=True)
    return results
