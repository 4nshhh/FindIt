"""Shared helpers: constants, text cleaning and form validation."""

from datetime import date

# Fixed dropdown choices keep reports consistent for matching.
CATEGORIES = [
    "Electronics",
    "Personal",
    "Clothing",
    "Books/Stationery",
    "ID/Cards",
    "Keys",
    "Bags",
    "Bag",
    "Bottle",
    "Other",
]

# Keep inputs reasonable so one bad form can't flood the database.
MAX_TEXT_LEN = 200
MAX_DESC_LEN = 500


def clean_text(value):
    """Trim whitespace; return empty string for None."""
    if value is None:
        return ""
    return str(value).strip()


def validate_report(item_name, category, color, location, report_date, description):
    """Check a lost/found form. Returns a list of error messages (empty = valid)."""
    errors = []

    item_name = clean_text(item_name)
    color = clean_text(color)
    location = clean_text(location)
    description = clean_text(description)

    if not item_name:
        errors.append("Item name is required.")
    elif len(item_name) > MAX_TEXT_LEN:
        errors.append("Item name is too long (max %d characters)." % MAX_TEXT_LEN)

    if clean_text(category) not in CATEGORIES:
        errors.append("Please choose a valid category.")

    if not color:
        errors.append("Color is required.")
    elif len(color) > MAX_TEXT_LEN:
        errors.append("Color is too long (max %d characters)." % MAX_TEXT_LEN)

    if not location:
        errors.append("Location is required.")
    elif len(location) > MAX_TEXT_LEN:
        errors.append("Location is too long (max %d characters)." % MAX_TEXT_LEN)

    if report_date is None:
        errors.append("Please choose a valid date.")
    elif report_date > date.today():
        errors.append("Date cannot be in the future.")

    if len(description) > MAX_DESC_LEN:
        errors.append("Description is too long (max %d characters)." % MAX_DESC_LEN)

    return errors
