"""FindIt — Campus Lost & Found. Run with: streamlit run app.py"""

from datetime import date

import streamlit as st

import database
from database import add_report, count_reports, get_reports, init_db, search_reports
from icons import badge, icon, icon_text, nav_icon_css, score_badge, type_badge
from matching import MATCH_THRESHOLD, find_matches
from utils import CATEGORIES, clean_text, validate_report

st.set_page_config(page_title="FindIt — Campus Lost & Found")

# Create DB/tables on first run so a fresh clone works immediately.
try:
    init_db()
except Exception as exc:
    st.error("Could not open the database: %s" % exc)
    st.stop()


def report_form(report_type):
    """Shared lost/found form. report_type is 'lost' or 'found'."""
    label = "Lost" if report_type == "lost" else "Found"
    form_icon = "file-plus" if report_type == "lost" else "package"
    st.markdown("### %s" % icon_text(form_icon, "Report %s Item" % label, 22),
                unsafe_allow_html=True)

    with st.form("report_%s" % report_type, clear_on_submit=True):
        item_name = st.text_input("Item name *", placeholder="e.g. Wallet")
        category = st.selectbox("Category *", CATEGORIES)
        color = st.text_input("Color *", placeholder="e.g. Black")
        location = st.text_input(
            "Location *",
            placeholder="Where was it %s?" % ("lost" if report_type == "lost" else "found"),
        )
        report_date = st.date_input(
            "Date %s *" % ("lost" if report_type == "lost" else "found"),
            value=date.today(), max_value=date.today(),
        )
        description = st.text_area("Description", placeholder="Brand, marks, contents...")
        contact = st.text_input("Contact (optional)", placeholder="Email or phone")
        submitted = st.form_submit_button("Submit %s report" % label)

    if not submitted:
        return

    errors = validate_report(item_name, category, color, location, report_date, description)
    if errors:
        for err in errors:
            st.error(err)
        return

    try:
        new_id = add_report(report_type, clean_text(item_name), category,
                            clean_text(color), clean_text(location),
                            clean_text(description), str(report_date), clean_text(contact))
        st.success("%s report #%d saved!" % (label, new_id))
        if report_type == "lost":
            st.info("Go to Possible Matches to see found items similar to yours.")
    except Exception as exc:
        st.error("Could not save the report: %s" % exc)


def show_report_card(rep):
    """One-line summary + expandable details for a report."""
    st.markdown("**#%d — %s**  %s  %s" % (rep["id"], rep["item_name"],
                                          type_badge(rep["type"]),
                                          badge(rep["category"])),
                unsafe_allow_html=True)
    st.markdown("%s  |  %s  |  %s" % (
        icon_text("map-pin", rep["location"], 14),
        icon_text("calendar", rep["report_date"], 14),
        icon_text("droplet", rep["color"], 14)), unsafe_allow_html=True)
    with st.expander("View details"):
        st.write(rep["description"] or "_No description._")
        if rep["contact"]:
            st.markdown(icon_text("phone", "Contact: %s" % rep["contact"], 14),
                        unsafe_allow_html=True)


def page_home():
    st.markdown("# %s" % icon_text("search", "FindIt", 30), unsafe_allow_html=True)
    st.subheader("Campus Lost & Found")
    st.write("Lost something on campus? Found something that belongs to someone?")
    st.write("FindIt connects lost and found reports using simple Python-based matching.")

    try:
        lost_count, found_count = count_reports()
        lost = get_reports("lost")
        found = get_reports("found")
        match_count = sum(len(find_matches(l, found)) for l in lost) if lost and found else 0
    except Exception as exc:
        st.error("Could not load statistics: %s" % exc)
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Lost Reports", lost_count)
    col2.metric("Found Reports", found_count)
    col3.metric("Possible Matches", match_count)

    st.divider()
    st.write("**How it works:** Report a lost or found item, then check "
             "Possible Matches for an automatic match score (60%+ = possible match).")


def page_search():
    st.markdown("### %s" % icon_text("search", "Search Reports", 22),
                unsafe_allow_html=True)
    keyword = st.text_input("Item name", placeholder="e.g. wallet")
    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox("Category", ["All"] + CATEGORIES)
    with col2:
        report_type = st.selectbox("Type", ["All", "lost", "found"])
    with col3:
        location = st.text_input("Location", placeholder="e.g. lab")

    try:
        results = search_reports(keyword, category, location, report_type)
    except Exception as exc:
        st.error("Search failed: %s" % exc)
        return

    if not results:
        st.info("No reports found. Try different filters or report the item first.")
        return
    st.write("Found **%d** report(s):" % len(results))
    for rep in results:
        show_report_card(rep)


def page_matches():
    st.markdown("### %s" % icon_text("target", "Possible Matches", 22),
                unsafe_allow_html=True)
    st.caption("A found item scoring >= %d%% against a lost item is shown as a match." % MATCH_THRESHOLD)

    try:
        lost_reports = get_reports("lost")
        found_reports = get_reports("found")
    except Exception as exc:
        st.error("Could not load reports: %s" % exc)
        return

    if not lost_reports:
        st.info("No lost reports yet. Report a lost item first.")
        return
    if not found_reports:
        st.info("No found reports yet. There is nothing to match against.")
        return

    options = {"#%d — %s (%s)" % (r["id"], r["item_name"], r["report_date"]): r["id"]
               for r in lost_reports}
    choice = st.selectbox("Choose a lost item:", list(options.keys()))
    lost = next(r for r in lost_reports if r["id"] == options[choice])

    matches = find_matches(lost, found_reports)
    if not matches:
        st.warning("No possible matches (score >= %d%%) for this item yet." % MATCH_THRESHOLD)
        return

    st.success("%d possible match(es) found!" % len(matches))
    for i, m in enumerate(matches, 1):
        rep = m["report"]
        st.divider()
        st.markdown("#### Possible Match #%d — %s  %s" % (i, rep["item_name"],
                                                          score_badge(m["score"])),
                    unsafe_allow_html=True)
        st.markdown("%s &nbsp;&nbsp; %s &nbsp;&nbsp; %s" % (
            icon_text("map-pin", rep["location"], 14),
            icon_text("calendar", rep["report_date"], 14),
            icon_text("droplet", rep["color"], 14)), unsafe_allow_html=True)
        st.write("**Matching factors:**")
        for reason in m["reasons"]:
            st.markdown(icon_text("check", reason, 14, "#15803d"),
                        unsafe_allow_html=True)
        with st.expander("View found-item details"):
            st.write(rep["description"] or "_No description._")
            st.caption("Category: %s | Reported: %s" % (rep["category"], rep["report_date"]))
            if rep["contact"]:
                st.markdown(icon_text("phone", "Contact: %s" % rep["contact"], 14),
                            unsafe_allow_html=True)


# Sidebar navigation (single-file app, no pages/ folder).
st.sidebar.markdown("### %s" % icon_text("search", "FindIt", 22),
                    unsafe_allow_html=True)
st.sidebar.caption("Campus Lost & Found")
# Icons beside each nav item (same SVG set as the rest of the UI).
# Native radio keeps its layout, spacing and active-state styling.
st.sidebar.markdown(nav_icon_css(["home", "file-plus", "package", "search", "target"]),
                    unsafe_allow_html=True)
page = st.sidebar.radio("Navigate",
                        ["Home", "Report Lost", "Report Found",
                         "Search Reports", "Possible Matches"])
st.sidebar.caption("Match threshold: >= %d%%" % MATCH_THRESHOLD)

if page == "Home":
    page_home()
elif page == "Report Lost":
    report_form("lost")
elif page == "Report Found":
    report_form("found")
elif page == "Search Reports":
    page_search()
else:
    page_matches()
