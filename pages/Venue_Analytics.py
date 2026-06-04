import streamlit as st
import pandas as pd
import plotly.express as px

from src.utils import load_data

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Venue Analytics",
    page_icon="🏟️",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

df = load_data("data/matches.csv")

# ==========================================
# HEADER
# ==========================================

st.title("🏟️ IPL Venue Analytics Dashboard")

st.markdown("---")

# ==========================================
# CHECK VENUE COLUMN
# ==========================================

if "venue" not in df.columns:
    st.error("Venue column not found.")
    st.stop()

# ==========================================
# VENUE LIST
# ==========================================

venues = sorted(
    df["venue"]
    .dropna()
    .unique()
)

selected_venue = st.selectbox(
    "Select Venue",
    venues
)

# ==========================================
# FILTER DATA
# ==========================================

venue_df = df[
    df["venue"] == selected_venue
]

# ==========================================
# KPI SECTION
# ==========================================

matches_hosted = len(venue_df)

total_seasons = (
    venue_df["season"].nunique()
    if "season" in venue_df.columns
    else 0
)

total_winners = (
    venue_df["winner"].nunique()
    if "winner" in venue_df.columns
    else 0
)

super_overs = 0

if "super_over" in venue_df.columns:
    super_overs = len(
        venue_df[
            venue_df["super_over"] == "Y"
        ]
    )

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Matches Hosted",
    matches_hosted
)

col2.metric(
    "Seasons",
    total_seasons
)

col3.metric(
    "Winning Teams",
    total_winners
)

col4.metric(
    "Super Overs",
    super_overs
)

st.markdown("---")

# ==========================================
# TOP WINNING TEAMS
# ==========================================

st.subheader(
    "🏆 Most Successful Teams at Venue"
)

winning_teams = (
    venue_df["winner"]
    .value_counts()
    .head(10)
    .reset_index()
)

winning_teams.columns = [
    "Team",
    "Wins"
]

fig1 = px.bar(
    winning_teams,
    x="Team",
    y="Wins",
    color="Wins",
    text="Wins",
    title="Top Winning Teams"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==========================================
# SEASON TREND
# ==========================================

st.subheader(
    "📈 Matches Hosted by Season"
)

if "season" in venue_df.columns:

    season_df = (
        venue_df
        .groupby("season")
        .size()
        .reset_index(
            name="Matches"
        )
    )

    fig2 = px.line(
        season_df,
        x="season",
        y="Matches",
        markers=True,
        title="Season Trend"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==========================================
# TOSS DECISION ANALYSIS
# ==========================================

st.subheader(
    "🪙 Toss Decision Analysis"
)

if "toss_decision" in venue_df.columns:

    toss_df = (
        venue_df["toss_decision"]
        .value_counts()
        .reset_index()
    )

    toss_df.columns = [
        "Decision",
        "Count"
    ]

    fig3 = px.pie(
        toss_df,
        names="Decision",
        values="Count",
        hole=0.4,
        title="Toss Decisions"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ==========================================
# MATCH RESULT ANALYSIS
# ==========================================

st.subheader(
    "📊 Match Result Distribution"
)

if "result" in venue_df.columns:

    result_df = (
        venue_df["result"]
        .value_counts()
        .reset_index()
    )

    result_df.columns = [
        "Result",
        "Count"
    ]

    fig4 = px.bar(
        result_df,
        x="Result",
        y="Count",
        color="Count",
        text="Count",
        title="Result Distribution"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# ==========================================
# WIN BY RUNS ANALYSIS
# ==========================================

st.subheader(
    "🔥 Win Margin by Runs"
)

if "win_by_runs" in venue_df.columns:

    fig5 = px.histogram(
        venue_df,
        x="win_by_runs",
        nbins=25,
        title="Run Margin Distribution"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

# ==========================================
# WIN BY WICKETS ANALYSIS
# ==========================================

st.subheader(
    "⚡ Win Margin by Wickets"
)

if "win_by_wickets" in venue_df.columns:

    fig6 = px.histogram(
        venue_df,
        x="win_by_wickets",
        nbins=15,
        title="Wicket Margin Distribution"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

# ==========================================
# VENUE LEADERBOARD
# ==========================================

st.subheader(
    "🏟️ Top IPL Venues"
)

venue_leaderboard = (
    df["venue"]
    .value_counts()
    .head(15)
    .reset_index()
)

venue_leaderboard.columns = [
    "Venue",
    "Matches"
]

st.dataframe(
    venue_leaderboard,
    use_container_width=True
)

# ==========================================
# AI INSIGHTS
# ==========================================

st.subheader(
    "🧠 Venue Insights"
)

st.success(
    f"{selected_venue} has hosted "
    f"{matches_hosted} IPL matches."
)

if not winning_teams.empty:

    best_team = winning_teams.iloc[0]["Team"]
    best_team_wins = winning_teams.iloc[0]["Wins"]

    st.success(
        f"{best_team} is the most successful "
        f"team at this venue with "
        f"{best_team_wins} wins."
    )

st.success(
    f"This venue has been used in "
    f"{total_seasons} IPL seasons."
)

st.success(
    f"{total_winners} different teams "
    f"have won matches here."
)

# ==========================================
# RAW DATA
# ==========================================

with st.expander(
    "📄 View Venue Match Data"
):

    st.dataframe(
        venue_df,
        use_container_width=True
    )

# ==========================================
# DOWNLOAD DATA
# ==========================================

csv = venue_df.to_csv(
    index=False
)

st.download_button(
    label="⬇ Download Venue Data",
    data=csv,
    file_name="venue_analysis.csv",
    mime="text/csv"
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "IPL Analytics Dashboard | Venue Analytics"
)
