import streamlit as st
import pandas as pd
import plotly.express as px

from src.utils import (
    load_data,
    dashboard_kpis
)

from src.insights import IPLInsights
from src.report_generator import ReportGenerator

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

df = load_data("data/matches.csv")

if df.empty:
    st.error("Dataset not found!")
    st.stop()

# ==========================================
# REPORT GENERATOR
# ==========================================

report_gen = ReportGenerator(df)

# ==========================================
# HEADER
# ==========================================

st.title("🏏 IPL Analytics Dashboard")

st.markdown("""
Analyze IPL matches, teams, players,
venues and performance trends using
interactive visualizations.
""")

st.markdown("---")

# ==========================================
# KPI SECTION
# ==========================================

kpis = dashboard_kpis(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Matches",
    kpis["Matches"]
)

col2.metric(
    "Teams",
    kpis["Teams"]
)

col3.metric(
    "Venues",
    kpis["Venues"]
)

col4.metric(
    "Seasons",
    kpis["Seasons"]
)

st.markdown("---")

# ==========================================
# TOP WINNING TEAMS
# ==========================================

st.subheader("🏆 Top Winning Teams")

winner_df = (
    df["winner"]
    .value_counts()
    .head(10)
    .reset_index()
)

winner_df.columns = [
    "Team",
    "Wins"
]

fig1 = px.bar(
    winner_df,
    x="Team",
    y="Wins",
    color="Wins",
    text="Wins",
    title="Top IPL Teams"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==========================================
# PLAYER OF MATCH ANALYSIS
# ==========================================

st.subheader("⭐ Top Players")

player_df = (
    df["player_of_match"]
    .value_counts()
    .head(10)
    .reset_index()
)

player_df.columns = [
    "Player",
    "Awards"
]

fig2 = px.bar(
    player_df,
    x="Player",
    y="Awards",
    color="Awards",
    text="Awards",
    title="Player Of Match Leaders"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================
# TOP VENUES
# ==========================================

st.subheader("🏟️ Top Venues")

venue_df = (
    df["venue"]
    .value_counts()
    .head(10)
    .reset_index()
)

venue_df.columns = [
    "Venue",
    "Matches"
]

fig3 = px.bar(
    venue_df,
    x="Venue",
    y="Matches",
    color="Matches",
    text="Matches",
    title="Most Active Venues"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================
# MATCHES PER SEASON
# ==========================================

if "season" in df.columns:

    st.subheader("📈 Season Trend")

    season_df = (
        df.groupby("season")
        .size()
        .reset_index(name="Matches")
    )

    fig4 = px.line(
        season_df,
        x="season",
        y="Matches",
        markers=True,
        title="Matches Per Season"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# ==========================================
# TOSS IMPACT
# ==========================================

if (
    "toss_winner" in df.columns
    and
    "winner" in df.columns
):

    st.subheader("🪙 Toss Impact")

    toss_wins = len(
        df[
            df["toss_winner"]
            ==
            df["winner"]
        ]
    )

    toss_losses = len(df) - toss_wins

    toss_df = pd.DataFrame({

        "Result": [
            "Won Toss & Match",
            "Won Toss Lost Match"
        ],

        "Count": [
            toss_wins,
            toss_losses
        ]

    })

    fig5 = px.pie(
        toss_df,
        names="Result",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

# ==========================================
# INSIGHTS
# ==========================================

st.subheader("🧠 AI Insights")

insights_engine = IPLInsights(df)

insights = (
    insights_engine
    .generate_all_insights()
)

for insight in insights:
    st.success(insight)

# ==========================================
# DOWNLOAD REPORT
# ==========================================

st.markdown("---")
st.subheader("📄 Download Report")

report_text = f"""
IPL ANALYTICS DASHBOARD REPORT

Total Matches : {len(df)}

Top Team :
{df['winner'].mode()[0]}

Top Player :
{df['player_of_match'].mode()[0]}

Top Venue :
{df['venue'].mode()[0]}
"""

st.download_button(
    label="📥 Download Insights Report",
    data=report_text,
    file_name="insights_report.txt",
    mime="text/plain"
)

# ==========================================
# GENERATE REPORTS
# ==========================================

if st.button("📊 Generate All Reports"):

    report_gen.generate_all_reports()

    st.success(
        "Reports Generated Successfully!"
    )

# ==========================================
# RAW DATA
# ==========================================

with st.expander("📄 View Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "IPL Analytics Dashboard | Streamlit | Plotly | Python"
)

