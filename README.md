# FindIt — Campus Lost & Found

## 1. Problem Statement
Students frequently lose personal belongings on campus. Even when another
student finds the item, there is no simple way to connect the lost-item
report with the found-item report.

## 2. Proposed Solution
FindIt is a small Streamlit + SQLite app that lets users report lost and
found items, browse/search reports, and automatically see possible matches
between lost and found reports with an explainable match score.

## 3. Features
- Report a lost item (name, category, color, location, date, description, optional contact)
- Report a found item (same fields)
- Browse/search reports by item name, category, location, type
- Possible Matches: pick a lost item, see found items scoring 60%+ with reasons
- Home dashboard with lost / found / match counts
- Basic validation and friendly error messages

## 4. Technology Stack
- Python 3.x (standard library: `sqlite3`, `re`, `os`, `datetime`)
- Streamlit (only external dependency)
- SQLite (file-based, auto-created at `database/findit.db`)

## 5. Project Structure
```
FindIt/
├── app.py          # Streamlit UI + sidebar navigation
├── database.py     # SQLite connect, init, insert, fetch, search
├── matching.py     # rule-based match scorer (MATCH_THRESHOLD = 60)
├── icons.py        # inline SVG icon set + status badges (no emoji, no deps)
├── utils.py        # categories, text cleanup, form validation
├── seed_demo.py    # DEV ONLY: loads 8 demo test cases (not part of app flow)
├── requirements.txt
├── README.md
├── AGENTS.md
└── database/
    └── findit.db   # auto-created on first run (gitignored)
```

## 6. How the Matching System Works
Rule-based score out of 100, no AI/ML:

| Check | Points |
|---|---|
| Category match | 25 |
| Item name word overlap | 25 |
| Color match | 15 |
| Location word overlap | 20 |
| Description keyword overlap | 10 |
| Date proximity (≤3d=5, ≤7d=3, ≤30d=1) | 5 |

Text is lowercased, punctuation removed, and compared by word overlap, so
"Black Leather Wallet" matches "black wallet". Score ≥ 60 is a Possible Match.
The UI lists which factors contributed (e.g. ✓ Category matched).

## 7. Installation
```bash
cd FindIt
pip install -r requirements.txt
```

## 8. How to Run
```bash
streamlit run app.py
```
The database and tables are created automatically on first start.

## 9. Demo Flow (2 minutes)
1. Open FindIt → Home.
2. Report Lost: Wallet / Personal / Black / Computer Lab / today / "Black leather wallet with a small scratch".
3. Report Found: Wallet / Personal / Black / Computer Lab / today / "Black leather wallet found near the computers".
4. Possible Matches → select the lost wallet → see ~90% match with reasons.
5. Report an unrelated item (Red Backpack / Canteen) and show it does NOT match.

## 10. Demo Data (for testing/presentation only)
```bash
python seed_demo.py          # reset DB and load 8 demo test cases (18 reports)
python seed_demo.py --clear  # remove all reports
```
Idempotent: re-running never creates duplicates (old reports are cleared
first). The matching algorithm is untouched — the data only exercises it.
Covers: exact match (100%), similar wording (87%/75%), different location
(80%), different color (85%), unrelated (5%, excluded), date gap (96%), and
a 3-way ranking test (100/80/63).

## 11. Future Improvements
- Mark item as claimed/resolved
- Delete a report
- Simple report-count chart
