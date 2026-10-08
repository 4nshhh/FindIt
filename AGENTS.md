# FindIt — Campus Lost & Found

## 1. Project Overview

Build a small academic Python mini-project called **FindIt — Campus Lost & Found**.

### Problem

Students frequently lose personal belongings on campus. Even when another
student finds the item, there is no simple way to connect the lost-item report
with the found-item report.

### Solution

FindIt is a simple campus Lost & Found application that allows users to:

- Report a lost item
- Report a found item
- Browse/search existing reports
- Automatically identify possible matches between lost and found items
- View the details and match score of possible matches

The application should demonstrate how Python can be used to solve a small,
real-world problem.

---

# 2. VERY IMPORTANT — Project Scope

This is a **college PBL mini-project**.

The project must remain:

- Small
- Simple
- Understandable
- Demonstrable
- Easy for a student to explain
- Focused on one specific problem

Do NOT turn this into a production-grade application.

### Do NOT add:

- Social networking features
- Chat/messaging
- Marketplace functionality
- Payment systems
- Mobile applications
- Complex authentication
- OAuth
- JWT
- Microservices
- REST APIs unless genuinely necessary
- Docker
- Kubernetes
- Cloud infrastructure
- Redis
- PostgreSQL
- Complex DevOps
- LLM APIs
- Generative AI
- Computer vision
- Facial recognition
- Image recognition
- Web scraping
- Real-time external data integrations
- Unnecessary third-party services

Prefer the simplest solution that works.

If a feature does not directly contribute to the Lost & Found problem,
**do not implement it.**

---

# 3. Technology Stack

Use the following stack unless there is a strong technical reason not to.

### Core

- Python 3.x

### Frontend / UI

- Streamlit

### Database

- SQLite

### Python Libraries

Prefer Python's standard library whenever possible.

Additional libraries should only be introduced when they provide a clear
benefit to the project.

Avoid dependency bloat.

---

# 4. Application Architecture

Keep the architecture simple.

Preferred structure:

findit/
│
├── app.py
├── database.py
├── matching.py
├── utils.py
│
├── database/
│   └── findit.db
│
├── pages/
│   ├── report_lost.py
│   ├── report_found.py
│   ├── search.py
│   └── matches.py
│
├── assets/
│
├── requirements.txt
├── README.md
└── AGENTS.md

The exact structure may be simplified if the project remains small.

Do not create files or layers just for the sake of following an architecture
pattern.

A simple architecture is preferred over excessive abstraction.

---

# 5. Core Features

The MVP should contain the following features.

## 5.1 Report Lost Item

A user should be able to submit a lost-item report.

Suggested fields:

- Item name
- Category
- Color
- Location
- Date lost
- Description
- Optional contact information

Example:

Item: Wallet
Category: Personal
Color: Black
Location: Computer Lab
Date: 2026-10-05
Description: Black leather wallet with a small scratch

---

## 5.2 Report Found Item

A user should be able to submit a found-item report.

Suggested fields:

- Item name
- Category
- Color
- Location
- Date found
- Description
- Optional contact information

Example:

Item: Wallet
Category: Personal
Color: Black
Location: Computer Lab
Date: 2026-10-05
Description: Black leather wallet found near the computers

---

## 5.3 Browse/Search Reports

Users should be able to view existing reports.

Provide simple filtering/searching by fields such as:

- Category
- Item name
- Location
- Date
- Lost/Found type

Do not build an advanced search engine.

---

## 5.4 Possible Match Detection

The main feature of the project is matching a lost item with possible found
items.

When a lost report exists, the application should compare it against found
reports and identify likely matches.

The matching system should be:

- Simple
- Explainable
- Deterministic
- Easy to demonstrate
- Easy to explain during a college presentation

---

# 6. Matching Algorithm

Do NOT use an LLM, external AI API, or machine-learning model for the initial
version.

Use a simple rule-based scoring system.

A suggested scoring system is:

Category match       → 25 points
Item name similarity → 25 points
Color match          → 15 points
Location similarity  → 20 points
Description keywords → 10 points
Date proximity       → 5 points
--------------------------------
Maximum               100 points

The exact weights may be adjusted if there is a good reason.

### Example

Lost report:

Black wallet
Computer Lab
2026-10-05

Found report:

Black leather wallet
Computer Lab
2026-10-05

Possible result:

Possible Match
Match Score: 90%

The UI should ideally explain why the match received its score.

Example:

✓ Category matched
✓ Color matched
✓ Location matched
✓ Date matched
✓ Item name similar

This makes the algorithm easy to explain to the professor.

---

# 7. Matching Requirements

The matching system should NOT simply compare entire strings for equality.

Use reasonable normalization such as:

- Convert text to lowercase
- Remove unnecessary punctuation
- Strip extra whitespace
- Compare important words
- Handle simple word overlap

Example:

"Black Leather Wallet"

should be reasonably comparable to:

"black wallet"

The algorithm does not need to be perfect.

The goal is to demonstrate a useful and understandable solution.

---

# 8. Match Threshold

Only display meaningful matches.

A reasonable initial threshold is:

Score >= 60 → Possible Match
Score < 60  → Do not show as a match

This value can be adjusted during testing.

The threshold should be stored in one clear location rather than repeated
throughout the code.

---

# 9. Database

Use SQLite.

The database should contain the minimum required information.

A simple design can use a reports table containing fields such as:

id
type
item_name
category
color
location
description
report_date
contact
created_at

Where:

type = "lost"

or:

type = "found"

You may use separate tables for lost and found reports if there is a clear
benefit, but avoid unnecessary database complexity.

---

# 10. Database Rules

The application should:

- Automatically create the SQLite database if it does not exist.
- Automatically create required tables if they do not exist.
- Use parameterized SQL queries.
- Handle basic database errors gracefully.
- Avoid storing unnecessary personal information.
- Avoid hardcoding database records into the application.

Database operations should be separated from UI logic where practical.

---

# 11. User Interface

Use Streamlit.

The UI should be:

- Clean
- Simple
- Professional
- Easy to navigate
- Suitable for a college demonstration

Suggested navigation:

🏠 Home
🔴 Report Lost
🟢 Report Found
🔎 Search Reports
🎯 Possible Matches

---

# 12. Home Page

The home page should briefly explain the application.

Example:

FindIt
Campus Lost & Found

Lost something on campus?
Found something that belongs to someone?

FindIt helps connect lost and found reports
using simple Python-based matching.

A small dashboard may show:

Lost Reports: 12
Found Reports: 9
Possible Matches: 4

Do not create an unnecessarily complicated dashboard.

---

# 13. Forms

Forms should include basic validation.

Examples:

- Required fields cannot be empty.
- Dates must be valid.
- Text fields should be trimmed.
- Extremely long input should be handled reasonably.
- Invalid values should produce a clear user-friendly message.

Use Streamlit validation and feedback such as:

st.success()
st.warning()
st.error()
st.info()

where appropriate.

---

# 14. Search

Search should remain simple.

Users should be able to search/filter by:

Item
Category
Location
Type
Date

Do not build Elasticsearch-like functionality.

---

# 15. Match Results UI

Possible matches should be visually clear.

Example:

──────────────────────────────────
Possible Match #1

Black Leather Wallet

📍 Computer Lab
📅 5 October 2026
🎯 Match Score: 87%

Matching factors:
✓ Category
✓ Color
✓ Location
✓ Description
✓ Date

[View Details]
──────────────────────────────────

Use appropriate Streamlit components such as:

- st.metric
- st.info
- st.success
- st.warning
- st.expander
- st.columns

Do not overuse animations or visual effects.

---

# 16. Optional Features

Only add these AFTER the core MVP is complete.

Possible optional features:

- Mark an item as resolved/claimed
- Sort reports by date
- Delete a report
- Show statistics
- Simple Matplotlib visualization
- Match explanation details

Only implement optional features if they remain small and useful.

---

# 17. Features That Are NOT Required

Do not implement the following unless explicitly requested:

- User registration
- Login system
- Password management
- Email verification
- OTP
- Social login
- Admin authentication
- Chat
- Notifications
- Push notifications
- Maps
- Image recognition
- AI-generated descriptions
- Cloud database
- Deployment infrastructure
- Mobile application
- Payment
- Messaging between users

These features are outside the scope of this mini-project.

---

# 18. Error Handling

Handle common errors gracefully.

Examples:

- Database unavailable
- Invalid form input
- Missing required values
- Invalid dates
- No matching reports
- Empty database

The application should not crash because of normal user mistakes.

Show understandable messages instead of raw Python tracebacks whenever
possible.

---

# 19. Code Quality

Write code that a college student can understand and explain.

Follow these principles:

- Meaningful variable names
- Small functions
- Avoid unnecessary classes
- Avoid unnecessary design patterns
- Avoid excessive abstraction
- Avoid duplicated logic
- Keep database logic organized
- Keep matching logic separate
- Keep UI logic readable

Do not optimize prematurely.

Readable code is more important than clever code.

---

# 20. Comments

Use comments when they explain:

- Why something is being done
- How the matching algorithm works
- Important database logic
- Non-obvious implementation decisions

Do not add comments to every line.

Bad:

# Increment i
i += 1

Good:

# Give higher weight to location because lost and found reports
# from the same campus area are more likely to correspond.

---

# 21. Dependencies

Keep requirements.txt minimal.

Only include packages actually used by the application.

At minimum, the project is expected to require:

streamlit

Additional dependencies should only be added when genuinely necessary.

SQLite is part of Python's standard library and should not be installed as
an external dependency.

---

# 22. README

Create a concise but complete README containing:

1. Project title
2. Problem statement
3. Proposed solution
4. Features
5. Technology stack
6. Project structure
7. How the matching system works
8. Installation instructions
9. How to run the application
10. Example screenshots if available
11. Future improvements

Do not make unsupported claims.

---

# 23. Running the Application

The application should run with:

streamlit run app.py

The README should clearly explain this.

---

# 24. Development Workflow

Before making major changes:

1. Inspect the current project structure.
2. Inspect existing files.
3. Understand what has already been implemented.
4. Identify the smallest change needed.
5. Implement the change.
6. Test the affected functionality.
7. Check that the application still starts.
8. Only then move to the next feature.

Do not rewrite working code unnecessarily.

---

# 25. Agent Behavior

When asked to implement a feature:

1. First understand the existing implementation.
2. Reuse existing utilities and functions when appropriate.
3. Make the smallest reasonable change.
4. Avoid introducing new dependencies unless necessary.
5. Test the implementation.
6. Report what was changed.
7. Mention any remaining issues.

Do not silently introduce major architectural changes.

---

# 26. Before Coding

If the project is empty, first create a short implementation plan.

The initial development order should generally be:

1. Project structure
        ↓
2. SQLite database
        ↓
3. Database operations
        ↓
4. Lost item form
        ↓
5. Found item form
        ↓
6. Search/browse
        ↓
7. Matching algorithm
        ↓
8. Match results UI
        ↓
9. Validation/error handling
        ↓
10. UI polishing
        ↓
11. Testing
        ↓
12. README

Do not attempt to build everything at once.

---

# 27. Testing

At minimum, test:

### Database

- Creating a report
- Reading reports
- Searching reports
- Handling empty database

### Forms

- Valid input
- Empty required fields
- Invalid dates

### Matching

Test cases should include:

Exact/similar match
Partial match
Different item
Different location
Different color
Different dates
No matching report

### Example

Input:

Lost:
Black Wallet
Computer Lab
5 Oct

Found:

Black Leather Wallet
Computer Lab
5 Oct

Expected:

High match score

Another:

Lost:
Black Wallet
Computer Lab
5 Oct

Found:
Red Backpack
Canteen
2 Oct

Expected:

Low score / no match

---

# 28. Demo Requirements

The application must be easy to demonstrate live.

The recommended demo flow is:

1. Open FindIt
2. Report a lost item
3. Report a found item with similar information
4. Open Possible Matches
5. Show the automatically calculated match score
6. Explain why the items were considered a match
7. Show that unrelated items receive a low score

The complete demonstration should take only a few minutes.

---

# 29. Academic Presentation

This is a Python Programming PBL mini-project.

The project should clearly demonstrate:

- Python programming
- Functions
- Data structures
- File/database handling
- Exception handling
- Basic application development
- Problem-solving
- Optional data visualization if used

The project should be explainable to a faculty member who has basic Python
knowledge.

Do not make the project dependent on advanced AI concepts.

---

# 30. Mini-Project Constraint

Always keep asking:

"Is this necessary for a small college mini-project?"

If the answer is no, do not add it.

The goal is NOT to build the most advanced Lost & Found system.

The goal is to build a small, functional, polished Python application that
clearly solves a real-world campus problem.

Prefer:

Simple + Working + Explainable

over:

Complex + Over-engineered + Difficult to explain

---

# 31. Definition of Done

The project is considered complete when:

- Application starts successfully
- Lost reports can be created
- Found reports can be created
- Reports are stored in SQLite
- Reports can be searched/viewed
- Lost and found reports can be compared
- Possible matches are displayed
- Match score is understandable
- Basic validation works
- Common errors are handled
- UI is clean enough for demonstration
- README is available
- requirements.txt is available
- Demo flow works from start to finish

Do not continue adding features simply because the application can support
them.

Once the above requirements work reliably, prioritize testing, cleanup, and
presentation quality.

---

# 32. Final Principle

Build a mini-project, not a startup.

Every technical decision should favor:

- Simplicity
- Reliability
- Explainability
- Small scope
- Demonstrability
- Python-first implementation

The finished application should be something a student can confidently
explain line-by-line and demonstrate to a professor.