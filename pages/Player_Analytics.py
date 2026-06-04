import streamlit as st
import pandas as pd
import plotly.express as px

from src.utils import load_data

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Player Analytics",
    page_icon="⭐",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

df = load_data("data/matches.csv")

# ==========================================
# HEADER
# ==========================================

st.title("⭐ IPL Player Analytics Dashboard")

st.markdown("---")

# ==========================================
# CHECK COLUMN
# ==========================================

if "player_of_match" not in df.columns:

    st.error(
        "player_of_match column not found in dataset."
    )

    st.stop()

# ==========================================
# PLAYER LIST
# ==========================================

players = sorted(
    df["player_of_match"]
    .dropna()
    .unique()
)

selected_player = st.selectbox(
    "Select Player",
    players
)

# ==========================================
# PLAYER DATA
# ==========================================

player_df = df[
    df["player_of_match"]
    == selected_player
]

# ==========================================
# KPI SECTION
# ==========================================

total_awards = len(player_df)

total_seasons = (
    player_df["season"].nunique()
    if "season" in player_df.columns
    else 0
)

total_venues = (
    player_df["venue"].nunique()
    if "venue" in player_df.columns
    else 0
)

avg_awards_per_season = round(
    total_awards / total_seasons,
    2
) if total_seasons > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Awards",
    total_awards
)

col2.metric(
    "Seasons",
    total_seasons
)

col3.metric(
    "Venues",
    total_venues
)

col4.metric(
    "Avg/Season",
    avg_awards_per_season
)

st.markdown("---")

# ==========================================
# SEASON PERFORMANCE
# ==========================================

st.subheader(
    "📈 Season-wise Awards"
)

if "season" in player_df.columns:

    season_awards = (
        player_df
        .groupby("season")
        .size()
        .reset_index(
            name="Awards"
        )
    )

    fig1 = px.line(
        season_awards,
        x="season",
        y="Awards",
        markers=True,
        title=f"{selected_player} Performance Trend"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# ==========================================
# VENUE PERFORMANCE
# ==========================================

st.subheader(
    "🏟 Best Venues"
)

venue_stats = (
    player_df["venue"]
    .value_counts()
    .head(10)
    .reset_index()
)

venue_stats.columns = [
    "Venue",
    "Awards"
]

fig2 = px.bar(
    venue_stats,
    x="Venue",
    y="Awards",
    color="Awards",
    text="Awards",
    title="Top Venues"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================
# TOP PLAYERS
# ==========================================

st.subheader(
    "🏆 Top Player of Match Winners"
)

top_players = (
    df["player_of_match"]
    .value_counts()
    .head(15)
    .reset_index()
)

top_players.columns = [
    "Player",
    "Awards"
]

fig3 = px.bar(
    top_players,
    x="Player",
    y="Awards",
    color="Awards",
    text="Awards",
    title="Top Players"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================
# PIE CHART
# ==========================================

st.subheader(
    "🥇 Award Share"
)

top10 = top_players.head(10)

fig4 = px.pie(
    top10,
    names="Player",
    values="Awards",
    hole=0.4
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ==========================================
# YEARLY HEATMAP DATA
# ==========================================

st.subheader(
    "🔥 Award Distribution"
)

if "season" in player_df.columns:

    heatmap_df = (
        player_df
        .groupby("season")
        .size()
        .reset_index(
            name="Awards"
        )
    )

    fig5 = px.bar(
        heatmap_df,
        x="season",
        y="Awards",
        color="Awards",
        title="Awards by Season"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

# ==========================================
# COMPARISON TABLE
# ==========================================

st.subheader(
    "📊 Top 20 Players"
)

leaderboard = (
    df["player_of_match"]
    .value_counts()
    .head(20)
    .reset_index()
)

leaderboard.columns = [
    "Player",
    "Awards"
]

st.dataframe(
    leaderboard,
    use_container_width=True
)

# ==========================================
# AI INSIGHTS
# ==========================================

st.subheader(
    "🧠 Player Insights"
)

rank = (
    leaderboard[
        leaderboard["Player"]
        == selected_player
    ].index
)

if len(rank) > 0:

    player_rank = rank[0] + 1

    st.success(
        f"{selected_player} ranks #{player_rank} "
        f"in IPL Player of the Match awards."
    )

st.success(
    f"{selected_player} has won "
    f"{total_awards} Player of the Match awards."
)

best_venue = (
    venue_stats.iloc[0]["Venue"]
    if not venue_stats.empty
    else "N/A"
)

st.success(
    f"Best venue for {selected_player} "
    f"is {best_venue}."
)

st.success(
    f"{selected_player} appeared in "
    f"{total_seasons} IPL seasons."
)

# ==========================================
# RAW DATA
# ==========================================

with st.expander(
    "📄 View Match Records"
):

    st.dataframe(
        player_df,
        use_container_width=True
    )

# ==========================================
# DOWNLOAD DATA
# ==========================================

csv = player_df.to_csv(
    index=False
)

st.download_button(
    label="⬇ Download Player Data",
    data=csv,
    file_name=f"{selected_player}_player_data.csv",
    mime="text/csv"
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "IPL Analytics Dashboard | Player Analytics"
)
