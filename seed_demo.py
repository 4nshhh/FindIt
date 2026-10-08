"""Demo/test data seeder for FindIt. DEV ONLY — not part of the normal app flow.

Usage:
    python seed_demo.py          # clear all reports and insert the 8 demo test cases
    python seed_demo.py --clear  # remove all reports without inserting anything

Idempotent: seeding always deletes existing reports first, so running it
multiple times never creates duplicates. Uses only database.add_report(),
so production code paths stay unchanged. The matching algorithm is NOT
touched — this script only inserts data to test it naturally.
"""

import sys

import database
from database import add_report, get_connection, get_reports, init_db
from matching import find_matches

# (type, item_name, category, color, location, description, report_date)
SEED_REPORTS = [
    # Case 1 — strong/exact match
    ("lost", "Wallet", "Personal", "Black", "Computer Lab",
     "Black leather wallet with a small scratch", "2026-10-05"),
    ("found", "Wallet", "Personal", "Black", "Computer Lab",
     "Black leather wallet found near computers", "2026-10-05"),
    # Case 2 — similar but not identical
    ("lost", "Water Bottle", "Bottle", "Blue", "Canteen",
     "Blue Milton water bottle with black cap", "2026-10-05"),
    ("found", "Milton Bottle", "Bottle", "Blue", "Canteen",
     "Blue water bottle with black lid", "2026-10-05"),
    # Case 3 — same item, different location
    ("lost", "AirPods", "Electronics", "White", "Library",
     "White AirPods in a small charging case", "2026-10-05"),
    ("found", "AirPods", "Electronics", "White", "Canteen",
     "White wireless earbuds in charging case", "2026-10-05"),
    # Case 4 — same item, different color
    ("lost", "Backpack", "Bag", "Black", "Block A",
     "Black backpack with a Nike logo", "2026-10-04"),
    ("found", "Backpack", "Bag", "Blue", "Block A",
     "Blue backpack with a Nike logo", "2026-10-04"),
    # Case 5 — completely unrelated
    ("lost", "Calculator", "Electronics", "Black", "Room 204",
     "Casio scientific calculator", "2026-10-05"),
    ("found", "Umbrella", "Personal", "Red", "Parking Area",
     "Red folding umbrella", "2026-10-02"),
    # Case 6 — different wording, same thing
    ("lost", "Phone", "Electronics", "Black", "Library",
     "Black Samsung smartphone with cracked screen", "2026-10-05"),
    ("found", "Samsung Mobile", "Electronics", "Black", "Library",
     "Black Samsung phone found on a library table", "2026-10-05"),
    # Case 7 — same item, different dates
    ("lost", "Calculator", "Electronics", "Black", "Room 204",
     "Casio FX-991ES Plus calculator", "2026-10-05"),
    ("found", "Calculator", "Electronics", "Black", "Room 204",
     "Casio scientific calculator", "2026-09-20"),
    # Case 8 — one lost, three found (ranking test)
    ("lost", "Wallet", "Personal", "Black", "Computer Lab",
     "Black leather wallet", "2026-10-05"),
    ("found", "Black Wallet", "Personal", "Black", "Computer Lab",
     "Black leather wallet", "2026-10-05"),
    ("found", "Black Wallet", "Personal", "Black", "Library",
     "Black wallet found near a table", "2026-10-04"),
    ("found", "Red Wallet", "Personal", "Red", "Canteen",
     "Red wallet", "2026-10-01"),
]


def clear_reports():
    """Remove all reports (demo reset)."""
    conn = get_connection()
    try:
        conn.execute("DELETE FROM reports")
        # Reset autoincrement so demo IDs are always 1..N for presentation.
        conn.execute("DELETE FROM sqlite_sequence WHERE name = 'reports'")
        conn.commit()
    finally:
        conn.close()


def seed():
    """Clear the DB and insert all demo reports. Returns the inserted rows."""
    init_db()
    clear_reports()  # guarantees no duplicates on re-runs
    for rep in SEED_REPORTS:
        add_report(*rep)
    return get_reports()


def print_match_summary():
    """Show each lost report with its ranked found matches."""
    lost = get_reports("lost")
    found = get_reports("found")
    print("Lost: %d, Found: %d" % (len(lost), len(found)))
    for item in lost:
        matches = find_matches(item, found)
        print("\nLost #%d '%s' (%s, %s, %s): %d match(es)"
              % (item["id"], item["item_name"], item["color"],
                 item["location"], item["report_date"], len(matches)))
        for m in matches:
            f = m["report"]
            print("  -> %d%% Found #%d '%s' (%s, %s, %s)"
                  % (m["score"], f["id"], f["item_name"], f["color"],
                     f["location"], f["report_date"]))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        init_db()
        clear_reports()
        print("All reports cleared.")
    else:
        rows = seed()
        print("Seeded %d demo reports (idempotent: old reports cleared first)." % len(rows))
        print_match_summary()
