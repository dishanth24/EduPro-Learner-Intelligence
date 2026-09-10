import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from pathlib import Path

# ============================================================
# EduPro Learner Intelligence
# Complete Streamlit Dashboard
# ============================================================

st.set_page_config(
    page_title="EduPro Learner Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# DESIGN TOKENS
# ------------------------------------------------------------
# Palette: deep ink-navy (structure/authority) + a growth-teal
# accent (progress/learning) + a warm amber accent (achievement,
# ratings). Fraunces carries the "EduPro" headers with a bookish,
# studious character; Inter carries the data and UI.

INK = "#16233F"
INK_SOFT = "#3E4C6E"
TEAL = "#1F8A70"
TEAL_SOFT = "#E4F3EF"
AMBER = "#E2914F"
AMBER_SOFT = "#FCEEDF"
BG = "#F5F6F4"
SURFACE = "#FFFFFF"
BORDER = "#E3E6E4"
MUTED = "#6B7280"

CHART_PALETTE = [TEAL, AMBER, INK_SOFT, "#7FB8A8", "#C77B3F", "#9AA5C0"]

CUSTOM_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stMarkdown, .stText {{
    font-family: 'Inter', sans-serif;
    color: {INK};
}}

.stApp {{
    background-color: {BG};
}}

h1, h2, h3 {{
    font-family: 'Fraunces', serif;
    color: {INK};
    letter-spacing: -0.01em;
}}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {{
    background-color: {INK};
}}
[data-testid="stSidebar"] * {{
    color: #E9ECF3 !important;
}}
[data-testid="stSidebar"] h1 {{
    font-family: 'Fraunces', serif;
    font-weight: 600;
}}
[data-testid="stSidebar"] hr {{
    border-color: rgba(255,255,255,0.12);
}}
[data-testid="stSidebar"] .stRadio > label {{
    font-family: 'Fraunces', serif;
}}
[data-testid="stSidebar"] div[role="radiogroup"] label {{
    background-color: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 8px 12px;
    margin-bottom: 6px;
    transition: background-color 0.15s ease;
}}
[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
    background-color: rgba(31,138,112,0.35);
}}
[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {{
    background-color: {TEAL};
    border-color: {TEAL};
}}

/* ---------- Hero banner ---------- */
.edu-hero {{
    background: linear-gradient(120deg, {INK} 0%, #1F2E52 55%, {TEAL} 130%);
    border-radius: 14px;
    padding: 32px 36px;
    margin-bottom: 28px;
    color: #F4F6F5;
}}
.edu-hero h1 {{
    color: #FFFFFF;
    font-size: 2.1rem;
    margin: 0 0 6px 0;
}}
.edu-hero p {{
    color: #CBD6E8;
    font-size: 1.02rem;
    margin: 0;
}}

/* ---------- Section headers ---------- */
.edu-section {{
    display: flex;
    align-items: baseline;
    gap: 10px;
    margin: 6px 0 14px 0;
    border-bottom: 2px solid {BORDER};
    padding-bottom: 8px;
}}
.edu-section .bar {{
    width: 5px;
    height: 1.3rem;
    background-color: {TEAL};
    border-radius: 3px;
    display: inline-block;
}}
.edu-section h3 {{
    margin: 0;
    font-size: 1.25rem;
}}
.edu-section span.sub {{
    color: {MUTED};
    font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
}}

/* ---------- KPI cards ---------- */
.edu-card {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-left: 4px solid {TEAL};
    border-radius: 10px;
    padding: 16px 18px;
    height: 100%;
}}
.edu-card.amber {{ border-left-color: {AMBER}; }}
.edu-card.ink {{ border-left-color: {INK_SOFT}; }}
.edu-card .label {{
    font-size: 0.82rem;
    color: {MUTED};
    margin-bottom: 6px;
}}
.edu-card .value {{
    font-family: 'Fraunces', serif;
    font-size: 1.7rem;
    font-weight: 600;
    color: {INK};
    line-height: 1.1;
}}
.edu-card .note {{
    font-size: 0.78rem;
    color: {TEAL};
    margin-top: 4px;
}}

/* ---------- Info tiles ---------- */
.edu-tile {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 18px 20px;
    height: 100%;
}}
.edu-tile .tile-title {{
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 1.05rem;
    margin-bottom: 6px;
    color: {INK};
}}
.edu-tile .tile-body {{
    color: {INK_SOFT};
    font-size: 0.92rem;
    line-height: 1.45;
}}

/* ---------- Badge / pill ---------- */
.edu-pill {{
    display: inline-block;
    background-color: {TEAL_SOFT};
    color: {TEAL};
    border-radius: 999px;
    padding: 5px 14px;
    font-size: 0.88rem;
    font-weight: 600;
    margin-bottom: 4px;
}}

/* ---------- Streamlit widgets ---------- */
div[data-testid="stMetric"] {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 12px 14px;
}}
[data-testid="stMetricLabel"] {{
    color: {MUTED};
}}
[data-testid="stMetricValue"] {{
    color: {INK};
    font-family: 'Fraunces', serif;
}}

.stButton > button, .stDownloadButton > button {{
    background-color: {INK};
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.1rem;
    font-weight: 500;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{
    background-color: {TEAL};
    color: #FFFFFF;
}}

div[data-baseweb="select"] > div {{
    border-radius: 8px;
    border-color: {BORDER};
}}

[data-testid="stDataFrame"] {{
    border: 1px solid {BORDER};
    border-radius: 10px;
    overflow: hidden;
}}

hr {{
    border-color: {BORDER};
}}

.stAlert {{
    border-radius: 10px;
}}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def altair_theme():
    return {
        "config": {
            "background": SURFACE,
            "title": {"font": "Fraunces", "fontSize": 14, "color": INK},
            "axis": {
                "labelFont": "Inter",
                "titleFont": "Inter",
                "labelColor": MUTED,
                "titleColor": INK_SOFT,
                "gridColor": BORDER,
                "domainColor": BORDER,
            },
            "legend": {"labelFont": "Inter", "titleFont": "Inter"},
            "range": {"category": CHART_PALETTE, "heatmap": [TEAL_SOFT, TEAL]},
        }
    }


alt.themes.register("edupro", altair_theme)
alt.themes.enable("edupro")


def section_header(title, subtitle=None):
    sub_html = f'<span class="sub">{subtitle}</span>' if subtitle else ""
    st.markdown(
        f'<div class="edu-section"><span class="bar"></span>'
        f'<h3>{title}</h3>{sub_html}</div>',
        unsafe_allow_html=True,
    )


def kpi_card(label, value, note=None, tone="teal"):
    tone_class = "" if tone == "teal" else f" {tone}"
    note_html = f'<div class="note">{note}</div>' if note else ""
    st.markdown(
        f'<div class="edu-card{tone_class}">'
        f'<div class="label">{label}</div>'
        f'<div class="value">{value}</div>{note_html}</div>',
        unsafe_allow_html=True,
    )


def info_tile(title, body):
    st.markdown(
        f'<div class="edu-tile"><div class="tile-title">{title}</div>'
        f'<div class="tile-body">{body}</div></div>',
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# APP CONSTANTS
# ------------------------------------------------------------

DATA_FILES = {
    "learner_profiles": "learner_profiles.csv",
    "all_recommendations": "all_recommendations.csv",
    "cluster_engagement": "cluster_engagement.csv",
    "segment_recommendations": "segment_recommendations.csv",
    "top_recommended_courses": "top_recommended_courses.csv",
}

PAGES = [
    "🏠 Overview",
    "👤 Learner Explorer",
    "🧩 Segments",
    "🤖 Recommendations",
    "📊 Analytics",
]


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def money(value):
    try:
        return f"${float(value):,.2f}"
    except (TypeError, ValueError):
        return "$0.00"


def number(value, decimals=0):
    try:
        return f"{float(value):,.{decimals}f}"
    except (TypeError, ValueError):
        return "0"


def existing_columns(df, columns):
    return [c for c in columns if c in df.columns]


def clean_table(df):
    result = df.copy()
    for col in result.columns:
        if pd.api.types.is_float_dtype(result[col]):
            result[col] = result[col].round(2)
    return result


# ------------------------------------------------------------
# DATA LOADING
# ------------------------------------------------------------

@st.cache_data
def load_data():
    base = Path(__file__).resolve().parent
    loaded = {}

    for key, filename in DATA_FILES.items():
        path = base / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing file: {filename}")
        loaded[key] = pd.read_csv(path)

    return loaded


try:
    data = load_data()

    learner_profiles = data["learner_profiles"]
    all_recommendations = data["all_recommendations"]
    cluster_engagement = data["cluster_engagement"]
    segment_recommendations = data["segment_recommendations"]
    top_recommended_courses = data["top_recommended_courses"]

except Exception as error:
    st.error("EduPro could not load the project data.")
    st.write(str(error))
    st.info("Keep app.py and all five CSV files in the same project folder.")
    st.stop()


# ------------------------------------------------------------
# NORMALIZE IMPORTANT COLUMNS
# ------------------------------------------------------------

if "UserID" in learner_profiles.columns:
    learner_profiles["UserID"] = learner_profiles["UserID"].astype(str)

if "UserID" in all_recommendations.columns:
    all_recommendations["UserID"] = all_recommendations["UserID"].astype(str)

numeric_columns = [
    "Age",
    "TotalCoursesEnrolled",
    "EnrollmentFrequency",
    "AverageSpending",
    "AverageCourseRating",
    "CategoryDiversity",
    "LearningDepthIndex",
    "TotalSpending",
]

for column in numeric_columns:
    if column in learner_profiles.columns:
        learner_profiles[column] = pd.to_numeric(learner_profiles[column], errors="coerce")

for column in ["CourseRating", "Score", "RecommendationRank"]:
    if column in all_recommendations.columns:
        all_recommendations[column] = pd.to_numeric(all_recommendations[column], errors="coerce")


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

with st.sidebar:
    st.markdown("# 🎓 EduPro")
    st.caption("Learner Intelligence Platform")

    st.divider()
    st.markdown("**Navigation**")

    page = st.radio(
        "Select page",
        PAGES,
        label_visibility="collapsed",
        key="main_page",
    )

    st.divider()
    st.markdown("**Dashboard Status**")
    st.success("● Data Connected")

    course_count = (
        all_recommendations["CourseID"].nunique()
        if "CourseID" in all_recommendations.columns
        else 0
    )
    segment_count = (
        learner_profiles["SegmentName"].nunique()
        if "SegmentName" in learner_profiles.columns
        else 0
    )

    st.caption(f"👥 {len(learner_profiles):,} learners")
    st.caption(f"📚 {course_count:,} courses")
    st.caption(f"🧩 {segment_count:,} segments")
    st.caption(f"🎯 {len(all_recommendations):,} recommendations")

    st.divider()
    st.caption("EduPro Learner Intelligence")
    st.caption("Student segmentation & personalization")


# ------------------------------------------------------------
# HERO
# ------------------------------------------------------------

st.markdown(
    """
    <div class="edu-hero">
        <h1>🎓 EduPro Learner Intelligence</h1>
        <p>Student segmentation and personalized course recommendation system</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# OVERVIEW
# ============================================================

if page == "🏠 Overview":

    section_header("Platform Overview", "A high-level view of learner behavior, segmentation and recommendations")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Total Learners", f"{len(learner_profiles):,}", tone="teal")
    with k2:
        kpi_card("Learner Segments", f"{segment_count:,}", tone="amber")
    with k3:
        kpi_card("Courses", f"{course_count:,}", tone="ink")
    with k4:
        kpi_card("Recommendations", f"{len(all_recommendations):,}", tone="teal")

    st.write("")
    section_header("What this dashboard provides")

    info1, info2, info3 = st.columns(3)
    with info1:
        info_tile(
            "👤 Learner Explorer",
            "Inspect individual learner profiles, preferences, engagement, spending and assigned segments.",
        )
    with info2:
        info_tile(
            "🧩 Learner Segmentation",
            "Understand segment sizes, learner characteristics and engagement patterns.",
        )
    with info3:
        info_tile(
            "🤖 Personalized Recommendations",
            "Explore ranked course recommendations using learner preferences and recommendation scores.",
        )

    st.write("")
    section_header("Segment Distribution")

    if "SegmentName" in learner_profiles.columns:
        segment_summary = (
            learner_profiles["SegmentName"]
            .value_counts()
            .rename_axis("Segment")
            .reset_index(name="Learners")
        )

        left, right = st.columns([1.4, 1])

        with left:
            chart = (
                alt.Chart(segment_summary)
                .mark_bar(cornerRadiusEnd=4, size=28)
                .encode(
                    x=alt.X("Learners:Q", title="Learners"),
                    y=alt.Y("Segment:N", sort="-x", title=None),
                    color=alt.Color("Segment:N", legend=None, scale=alt.Scale(range=CHART_PALETTE)),
                    tooltip=["Segment", "Learners"],
                )
                .properties(height=280)
            )
            st.altair_chart(chart, use_container_width=True)

        with right:
            segment_summary["Share (%)"] = (
                segment_summary["Learners"] / len(learner_profiles) * 100
            ).round(2)
            st.dataframe(segment_summary, use_container_width=True, hide_index=True)

    st.write("")
    section_header("Top Recommended Courses")

    if not top_recommended_courses.empty:
        st.dataframe(clean_table(top_recommended_courses.head(10)), use_container_width=True, hide_index=True)
    elif not all_recommendations.empty:
        top_display = (
            all_recommendations
            .groupby(["CourseName", "CourseCategory", "CourseLevel"], dropna=False)
            .agg(
                Recommendations=("UserID", "count"),
                AverageScore=("Score", "mean"),
                AverageRating=("CourseRating", "mean"),
            )
            .reset_index()
            .sort_values("Recommendations", ascending=False)
            .head(10)
        )
        top_display["AverageScore"] = top_display["AverageScore"].round(3)
        top_display["AverageRating"] = top_display["AverageRating"].round(2)
        st.dataframe(top_display, use_container_width=True, hide_index=True)

    st.write("")
    section_header("Learner Dataset Preview")

    st.dataframe(clean_table(learner_profiles.head(10)), use_container_width=True, hide_index=True)

    csv_data = learner_profiles.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Learner Data",
        data=csv_data,
        file_name="edupro_learner_profiles.csv",
        mime="text/csv",
    )


# ============================================================
# LEARNER EXPLORER
# ============================================================

elif page == "👤 Learner Explorer":

    section_header("Learner Explorer", "Explore an individual learner's profile, behavior, segment and recommendations")

    if "UserID" not in learner_profiles.columns:
        st.error("UserID column is missing from learner_profiles.csv")
        st.stop()

    users = learner_profiles["UserID"].dropna().astype(str).sort_values().unique().tolist()

    if not users:
        st.warning("No learners are available.")
        st.stop()

    selected_user = st.selectbox("🔎 Select Learner", users, key="explorer_user")

    learner_rows = learner_profiles[learner_profiles["UserID"] == selected_user]

    if learner_rows.empty:
        st.warning("Selected learner could not be found.")
        st.stop()

    learner = learner_rows.iloc[0]
    segment_name = learner.get("SegmentName", "Not assigned")

    st.markdown(f'<span class="edu-pill">🧩 {segment_name}</span>', unsafe_allow_html=True)

    st.write("")
    section_header("Learner Snapshot")

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        kpi_card("Courses Enrolled", number(learner.get("TotalCoursesEnrolled", 0)), tone="teal")
    with s2:
        kpi_card("Total Spending", money(learner.get("TotalSpending", 0)), tone="amber")
    with s3:
        kpi_card("Avg Course Rating", number(learner.get("AverageCourseRating", 0), 2), tone="ink")
    with s4:
        kpi_card("Categories Explored", number(learner.get("CategoryDiversity", 0)), tone="teal")

    st.write("")
    section_header("Learner Profile")

    profile_col1, profile_col2 = st.columns(2)

    with profile_col1:
        st.markdown("**Demographics**")
        profile_data = pd.DataFrame({
            "Attribute": ["User ID", "Age", "Gender", "Segment"],
            "Value": [
                learner.get("UserID", "N/A"),
                learner.get("Age", "N/A"),
                learner.get("Gender", "N/A"),
                learner.get("SegmentName", "N/A"),
            ],
        })
        st.dataframe(profile_data, use_container_width=True, hide_index=True)

    with profile_col2:
        st.markdown("**Learning Preferences**")
        preference_data = pd.DataFrame({
            "Attribute": ["Preferred Category", "Preferred Level", "Courses Enrolled", "Enrollment Frequency"],
            "Value": [
                learner.get("PreferredCategory", "N/A"),
                learner.get("PreferredLevel", "N/A"),
                number(learner.get("TotalCoursesEnrolled", 0)),
                number(learner.get("EnrollmentFrequency", 0), 2),
            ],
        })
        st.dataframe(preference_data, use_container_width=True, hide_index=True)

    st.write("")
    section_header("Behavioral Profile")

    b1, b2, b3 = st.columns(3)
    with b1:
        kpi_card("Average Spending", money(learner.get("AverageSpending", 0)), tone="teal")
    with b2:
        kpi_card("Average Rating", number(learner.get("AverageCourseRating", 0), 2), tone="amber")
    with b3:
        kpi_card("Category Diversity", number(learner.get("CategoryDiversity", 0)), tone="ink")

    b4, b5 = st.columns(2)
    with b4:
        kpi_card("Learning Depth Index", number(learner.get("LearningDepthIndex", 0), 2), tone="teal")
    with b5:
        kpi_card("Total Spending", money(learner.get("TotalSpending", 0)), tone="amber")

    st.write("")
    section_header("Personalized Recommendations")

    learner_recs = all_recommendations[all_recommendations["UserID"] == selected_user].copy()

    if learner_recs.empty:
        st.info("No personalized recommendations are available for this learner.")
    else:
        if "RecommendationRank" in learner_recs.columns:
            learner_recs = learner_recs.sort_values("RecommendationRank")
        elif "Score" in learner_recs.columns:
            learner_recs = learner_recs.sort_values("Score", ascending=False)

        learner_recs = learner_recs.head(5)

        display_cols = existing_columns(
            learner_recs,
            ["RecommendationRank", "CourseName", "CourseCategory", "CourseLevel", "CourseRating", "Score"],
        )

        learner_display = learner_recs[display_cols].copy()
        rename_map = {
            "RecommendationRank": "Rank",
            "CourseName": "Course",
            "CourseCategory": "Category",
            "CourseLevel": "Level",
            "CourseRating": "Rating",
            "Score": "Match Score",
        }
        learner_display = learner_display.rename(columns=rename_map)

        st.dataframe(clean_table(learner_display), use_container_width=True, hide_index=True)


# ============================================================
# SEGMENTS
# ============================================================

elif page == "🧩 Segments":

    section_header("Learner Segments", "Explore learner groups created by the segmentation process")

    if "SegmentName" not in learner_profiles.columns:
        st.error("SegmentName column is missing from learner_profiles.csv")
        st.stop()

    segment_summary = learner_profiles.groupby("SegmentName").size().reset_index(name="Learners")
    segment_summary["Share (%)"] = (segment_summary["Learners"] / len(learner_profiles) * 100).round(2)
    segment_summary = segment_summary.sort_values("Learners", ascending=False)

    q1, q2, q3 = st.columns(3)
    with q1:
        kpi_card("Total Segments", f"{len(segment_summary)}", tone="teal")
    with q2:
        largest_segment = segment_summary.iloc[0]["SegmentName"] if not segment_summary.empty else "N/A"
        kpi_card("Largest Segment", largest_segment, tone="amber")
    with q3:
        largest_size = int(segment_summary.iloc[0]["Learners"]) if not segment_summary.empty else 0
        kpi_card("Largest Segment Size", f"{largest_size:,}", tone="ink")

    st.write("")
    section_header("Segment Distribution")

    left, right = st.columns([1.3, 1])
    with left:
        chart = (
            alt.Chart(segment_summary)
            .mark_bar(cornerRadiusEnd=4, size=28)
            .encode(
                x=alt.X("Learners:Q", title="Learners"),
                y=alt.Y("SegmentName:N", sort="-x", title=None),
                color=alt.Color("SegmentName:N", legend=None, scale=alt.Scale(range=CHART_PALETTE)),
                tooltip=["SegmentName", "Learners", "Share (%)"],
            )
            .properties(height=300)
        )
        st.altair_chart(chart, use_container_width=True)
    with right:
        st.dataframe(segment_summary, use_container_width=True, hide_index=True)

    st.write("")
    selected_segment = st.selectbox("🔎 Explore a segment", segment_summary["SegmentName"].tolist(), key="segment_selector")

    segment_learners = learner_profiles[learner_profiles["SegmentName"] == selected_segment].copy()

    section_header(selected_segment)

    seg1, seg2, seg3, seg4 = st.columns(4)
    with seg1:
        kpi_card("Learners", f"{len(segment_learners):,}", tone="teal")
    with seg2:
        avg_age = segment_learners["Age"].mean() if "Age" in segment_learners.columns else 0
        kpi_card("Avg Age", number(avg_age, 1), tone="amber")
    with seg3:
        avg_spending = segment_learners["AverageSpending"].mean() if "AverageSpending" in segment_learners.columns else 0
        kpi_card("Avg Spending", money(avg_spending), tone="ink")
    with seg4:
        avg_rating = segment_learners["AverageCourseRating"].mean() if "AverageCourseRating" in segment_learners.columns else 0
        kpi_card("Avg Rating", number(avg_rating, 2), tone="teal")

    st.write("")
    section_header("Segment Characteristics")

    characteristic_columns = existing_columns(
        segment_learners,
        [
            "Age", "TotalCoursesEnrolled", "EnrollmentFrequency", "AverageSpending",
            "AverageCourseRating", "CategoryDiversity", "LearningDepthIndex", "TotalSpending",
        ],
    )

    if characteristic_columns:
        characteristics = segment_learners[characteristic_columns].mean(numeric_only=True).reset_index()
        characteristics.columns = ["Metric", "Average Value"]
        characteristics["Average Value"] = characteristics["Average Value"].round(2)
        st.dataframe(characteristics, use_container_width=True, hide_index=True)

    if "PreferredCategory" in segment_learners.columns:
        st.write("")
        section_header("Preferred Categories")

        category_counts = (
            segment_learners["PreferredCategory"]
            .value_counts()
            .rename_axis("Category")
            .reset_index(name="Learners")
        )
        chart = (
            alt.Chart(category_counts)
            .mark_bar(cornerRadiusEnd=4)
            .encode(
                x=alt.X("Category:N", sort="-y", title=None),
                y=alt.Y("Learners:Q"),
                color=alt.value(TEAL),
                tooltip=["Category", "Learners"],
            )
            .properties(height=280)
        )
        st.altair_chart(chart, use_container_width=True)

    if not cluster_engagement.empty:
        st.write("")
        section_header("Cluster Engagement")
        st.dataframe(clean_table(cluster_engagement), use_container_width=True, hide_index=True)

    if not segment_recommendations.empty:
        st.write("")
        section_header("Segment-Level Recommendations")

        segment_rec_display = segment_recommendations.copy()
        possible_segment_columns = [c for c in segment_rec_display.columns if "segment" in c.lower()]

        if possible_segment_columns:
            segment_col = possible_segment_columns[0]
            matching = segment_rec_display[segment_rec_display[segment_col].astype(str) == str(selected_segment)]
            if not matching.empty:
                st.dataframe(clean_table(matching), use_container_width=True, hide_index=True)
            else:
                st.dataframe(clean_table(segment_rec_display), use_container_width=True, hide_index=True)
        else:
            st.dataframe(clean_table(segment_rec_display), use_container_width=True, hide_index=True)


# ============================================================
# RECOMMENDATIONS
# ============================================================

elif page == "🤖 Recommendations":

    section_header("Personalized Recommendations", "Filter and explore the highest-scoring courses for any learner")

    if all_recommendations.empty:
        st.warning("No recommendation data is available.")
        st.stop()

    users = (
        all_recommendations["UserID"].dropna().astype(str).sort_values().unique().tolist()
        if "UserID" in all_recommendations.columns
        else []
    )

    if not users:
        st.warning("No recommendation learners are available.")
        st.stop()

    r1, r2 = st.columns([1.2, 2])
    with r1:
        recommendation_user = st.selectbox("👤 Select learner", users, key="recommendation_user")
    with r2:
        search_course = st.text_input("🔎 Search course", placeholder="Type a course name...", key="recommendation_search")

    recs = all_recommendations[all_recommendations["UserID"] == recommendation_user].copy()

    levels = ["All"] + sorted(recs["CourseLevel"].dropna().astype(str).unique().tolist()) if "CourseLevel" in recs.columns else ["All"]
    categories = ["All"] + sorted(recs["CourseCategory"].dropna().astype(str).unique().tolist()) if "CourseCategory" in recs.columns else ["All"]

    f1, f2, f3 = st.columns(3)
    with f1:
        count = st.selectbox("📚 Courses to show", [5, 10, 15, 20], index=0, key="recommendation_count_page")
    with f2:
        level_filter = st.selectbox("🎓 Filter by level", levels, key="recommendation_level_page")
    with f3:
        category_filter = st.selectbox("🧩 Filter by category", categories, key="recommendation_category_page")

    filtered = recs.copy()

    if level_filter != "All" and "CourseLevel" in filtered.columns:
        filtered = filtered[filtered["CourseLevel"].astype(str) == level_filter]

    if category_filter != "All" and "CourseCategory" in filtered.columns:
        filtered = filtered[filtered["CourseCategory"].astype(str) == category_filter]

    if search_course and "CourseName" in filtered.columns:
        filtered = filtered[filtered["CourseName"].astype(str).str.contains(search_course, case=False, na=False)]

    if "Score" in filtered.columns:
        filtered = filtered.sort_values("Score", ascending=False)
    elif "RecommendationRank" in filtered.columns:
        filtered = filtered.sort_values("RecommendationRank")

    filtered = filtered.head(count)

    st.write("")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        kpi_card("Recommendations", f"{len(filtered)}", tone="teal")
    with p2:
        avg_score = filtered["Score"].mean() if not filtered.empty and "Score" in filtered.columns else 0
        kpi_card("Avg Match Score", number(avg_score, 2), tone="amber")
    with p3:
        avg_rating = filtered["CourseRating"].mean() if not filtered.empty and "CourseRating" in filtered.columns else 0
        kpi_card("Avg Course Rating", number(avg_rating, 2), tone="ink")
    with p4:
        best_score = filtered["Score"].max() if not filtered.empty and "Score" in filtered.columns else 0
        kpi_card("Best Match", number(best_score, 3), tone="teal")

    st.write("")

    if filtered.empty:
        st.info("No recommendations match the selected filters.")
    else:
        section_header("Recommended Courses")

        for position, (_, rec) in enumerate(filtered.iterrows(), start=1):
            course_name = rec.get("CourseName", "Course")
            category = rec.get("CourseCategory", "N/A")
            level = rec.get("CourseLevel", "N/A")
            rating = rec.get("CourseRating", 0)
            score = rec.get("Score", 0)
            rank = rec.get("RecommendationRank", position)

            with st.container(border=True):
                card1, card2, card3 = st.columns([0.7, 3.5, 1.3])
                with card1:
                    st.markdown(
                        f'<div style="font-family:\'Fraunces\',serif;font-size:1.4rem;'
                        f'font-weight:600;color:{TEAL};">#{int(rank)}</div>',
                        unsafe_allow_html=True,
                    )
                with card2:
                    st.markdown(f"##### {course_name}")
                    st.caption(f"🧩 {category}   •   🎓 {level}   •   ⭐ {number(rating, 2)}")
                with card3:
                    kpi_card("Match Score", number(score, 3), tone="amber")

    st.write("")
    section_header("Recommendation Data")

    table_columns = existing_columns(
        filtered,
        ["RecommendationRank", "CourseName", "CourseCategory", "CourseLevel", "CourseRating", "Score"],
    )

    if table_columns:
        recommendation_table = filtered[table_columns].copy()
        recommendation_table = recommendation_table.rename(
            columns={
                "RecommendationRank": "Rank",
                "CourseName": "Course",
                "CourseCategory": "Category",
                "CourseLevel": "Level",
                "CourseRating": "Rating",
                "Score": "Match Score",
            }
        )
        st.dataframe(clean_table(recommendation_table), use_container_width=True, hide_index=True)

        download_data = recommendation_table.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Recommendations",
            data=download_data,
            file_name=f"edupro_recommendations_{recommendation_user}.csv",
            mime="text/csv",
        )


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📊 Analytics":

    section_header("Learner Analytics", "Use interactive filters and charts to understand learner behavior")

    filtered_learners = learner_profiles.copy()

    a1, a2, a3 = st.columns(3)

    with a1:
        if "Gender" in learner_profiles.columns:
            gender_options = ["All"] + sorted(learner_profiles["Gender"].dropna().astype(str).unique().tolist())
            gender_filter = st.selectbox("👤 Gender", gender_options, key="analytics_gender")
            if gender_filter != "All":
                filtered_learners = filtered_learners[filtered_learners["Gender"].astype(str) == gender_filter]

    with a2:
        if "PreferredLevel" in learner_profiles.columns:
            level_options = ["All"] + sorted(learner_profiles["PreferredLevel"].dropna().astype(str).unique().tolist())
            preferred_level = st.selectbox("🎓 Preferred Level", level_options, key="analytics_level")
            if preferred_level != "All":
                filtered_learners = filtered_learners[filtered_learners["PreferredLevel"].astype(str) == preferred_level]

    with a3:
        if "PreferredCategory" in learner_profiles.columns:
            category_options = ["All"] + sorted(learner_profiles["PreferredCategory"].dropna().astype(str).unique().tolist())
            preferred_category = st.selectbox("🧩 Preferred Category", category_options, key="analytics_category")
            if preferred_category != "All":
                filtered_learners = filtered_learners[filtered_learners["PreferredCategory"].astype(str) == preferred_category]

    st.write("")
    an1, an2, an3, an4 = st.columns(4)
    with an1:
        kpi_card("Learners in View", f"{len(filtered_learners):,}", tone="teal")
    with an2:
        avg_spend = filtered_learners["AverageSpending"].mean() if "AverageSpending" in filtered_learners.columns else 0
        kpi_card("Avg Spending", money(avg_spend), tone="amber")
    with an3:
        avg_rating = filtered_learners["AverageCourseRating"].mean() if "AverageCourseRating" in filtered_learners.columns else 0
        kpi_card("Avg Rating", number(avg_rating, 2), tone="ink")
    with an4:
        avg_courses = filtered_learners["TotalCoursesEnrolled"].mean() if "TotalCoursesEnrolled" in filtered_learners.columns else 0
        kpi_card("Avg Courses Enrolled", number(avg_courses, 2), tone="teal")

    if "Age" in filtered_learners.columns:
        st.write("")
        section_header("Age Distribution")
        age_data = filtered_learners["Age"].dropna().round().astype(int).value_counts().sort_index().reset_index()
        age_data.columns = ["Age", "Learners"]
        chart = (
            alt.Chart(age_data)
            .mark_bar(color=TEAL, cornerRadiusEnd=3)
            .encode(x=alt.X("Age:O", title="Age"), y=alt.Y("Learners:Q"), tooltip=["Age", "Learners"])
            .properties(height=260)
        )
        st.altair_chart(chart, use_container_width=True)

    if "SegmentName" in filtered_learners.columns and "AverageSpending" in filtered_learners.columns:
        st.write("")
        section_header("Average Spending by Segment")
        spending_segment = (
            filtered_learners.groupby("SegmentName")["AverageSpending"].mean().sort_values(ascending=False).reset_index()
        )
        chart = (
            alt.Chart(spending_segment)
            .mark_bar(cornerRadiusEnd=4)
            .encode(
                x=alt.X("SegmentName:N", sort="-y", title=None),
                y=alt.Y("AverageSpending:Q", title="Avg Spending"),
                color=alt.Color("SegmentName:N", legend=None, scale=alt.Scale(range=CHART_PALETTE)),
                tooltip=["SegmentName", "AverageSpending"],
            )
            .properties(height=280)
        )
        st.altair_chart(chart, use_container_width=True)

    if "TotalCoursesEnrolled" in filtered_learners.columns:
        st.write("")
        section_header("Course Enrollment Distribution")
        enrollment_data = (
            filtered_learners["TotalCoursesEnrolled"].dropna().round().astype(int).value_counts().sort_index().reset_index()
        )
        enrollment_data.columns = ["Courses Enrolled", "Learners"]
        chart = (
            alt.Chart(enrollment_data)
            .mark_bar(color=AMBER, cornerRadiusEnd=3)
            .encode(x=alt.X("Courses Enrolled:O"), y=alt.Y("Learners:Q"), tooltip=["Courses Enrolled", "Learners"])
            .properties(height=260)
        )
        st.altair_chart(chart, use_container_width=True)

    if "PreferredCategory" in filtered_learners.columns:
        st.write("")
        section_header("Preferred Category Distribution")
        category_data = filtered_learners["PreferredCategory"].value_counts().head(15).reset_index()
        category_data.columns = ["Category", "Learners"]
        chart = (
            alt.Chart(category_data)
            .mark_bar(cornerRadiusEnd=4)
            .encode(
                x=alt.X("Category:N", sort="-y", title=None),
                y=alt.Y("Learners:Q"),
                color=alt.Color("Category:N", legend=None, scale=alt.Scale(range=CHART_PALETTE)),
                tooltip=["Category", "Learners"],
            )
            .properties(height=280)
        )
        st.altair_chart(chart, use_container_width=True)

    if {"AverageSpending", "AverageCourseRating"}.issubset(filtered_learners.columns):
        st.write("")
        section_header("Spending vs Course Rating")
        scatter_data = filtered_learners[["AverageSpending", "AverageCourseRating"]].dropna()
        if not scatter_data.empty:
            chart = (
                alt.Chart(scatter_data)
                .mark_circle(size=70, opacity=0.65, color=TEAL)
                .encode(
                    x=alt.X("AverageSpending:Q", title="Average Spending"),
                    y=alt.Y("AverageCourseRating:Q", title="Average Course Rating"),
                    tooltip=["AverageSpending", "AverageCourseRating"],
                )
                .properties(height=300)
            )
            st.altair_chart(chart, use_container_width=True)

    numeric_data = filtered_learners.select_dtypes(include=np.number)

    if numeric_data.shape[1] >= 2:
        st.write("")
        section_header("Learner Metric Correlations")
        correlation = numeric_data.corr().round(2)
        st.dataframe(
        correlation.round(2),
        use_container_width=True,
    )

    st.write("")
    section_header("Data Quality")

    quality1, quality2, quality3 = st.columns(3)

    total_cells = learner_profiles.shape[0] * learner_profiles.shape[1]
    missing_cells = int(learner_profiles.isna().sum().sum())
    duplicate_rows = int(learner_profiles.duplicated().sum())

    with quality1:
        kpi_card("Total Cells", f"{total_cells:,}", tone="teal")
    with quality2:
        kpi_card("Missing Values", f"{missing_cells:,}", tone="amber")
    with quality3:
        kpi_card("Duplicate Rows", f"{duplicate_rows:,}", tone="ink")

    st.write("")
    analytics_download = filtered_learners.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Current Analytics View",
        data=analytics_download,
        file_name="edupro_analytics_view.csv",
        mime="text/csv",
    )


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.divider()
st.caption("🎓 EduPro Learner Intelligence • Student Segmentation & Personalized Course Recommendation System")
