import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/matches.csv")
    return df

df = load_data()
from src.report_generator import ReportGenerator

report_gen = ReportGenerator(df)

# -----------------------------
# TITLE
# -----------------------------
st.title("🏏 IPL Deep Analytics Dashboard")
st.markdown("---")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

seasons = sorted(df['season'].dropna().unique())

selected_seasons = st.sidebar.multiselect(
    "Select Season",
    seasons,
    default=seasons
)

filtered_df = df[df['season'].isin(selected_seasons)]

teams = sorted(
    list(
        set(filtered_df['team1'].dropna().unique())
        .union(set(filtered_df['team2'].dropna().unique())
    ))
)

selected_teams = st.sidebar.multiselect(
    "Select Team",
    teams,
    default=teams
)

filtered_df = filtered_df[
    (filtered_df['team1'].isin(selected_teams))
    | (filtered_df['team2'].isin(selected_teams))
]

# -----------------------------
# KPI SECTION
# -----------------------------
st.subheader("📊 Executive Summary")

col1, col2, col3, col4 = st.columns(4)

total_matches = len(filtered_df)

total_teams = len(
    set(filtered_df['team1']).union(set(filtered_df['team2']))
)

total_venues = filtered_df['venue'].nunique()

total_seasons = filtered_df['season'].nunique()

col1.metric("Matches", total_matches)
col2.metric("Teams", total_teams)
col3.metric("Venues", total_venues)
col4.metric("Seasons", total_seasons)

st.markdown("---")

# -----------------------------
# TEAM WINS ANALYSIS
# -----------------------------
st.subheader("🏆 Most Successful Teams")

wins = filtered_df['winner'].value_counts().reset_index()

wins.columns = ['Team', 'Wins']

fig = px.bar(
    wins,
    x='Team',
    y='Wins',
    text='Wins',
    title='Team Wins'
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# PIE CHART
# -----------------------------
st.subheader("📈 Win Share")

top10 = wins.head(10)

fig2 = px.pie(
    top10,
    names='Team',
    values='Wins',
    hole=0.4
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# TOSS ANALYSIS
# -----------------------------
st.subheader("🪙 Toss Impact")

if 'toss_winner' in filtered_df.columns:

    toss_win = (
        filtered_df[
            filtered_df['toss_winner']
            == filtered_df['winner']
        ]
        .shape[0]
    )

    toss_loss = total_matches - toss_win

    toss_df = pd.DataFrame({
        "Category": ["Won Match", "Lost Match"],
        "Count": [toss_win, toss_loss]
    })

    fig3 = px.pie(
        toss_df,
        names='Category',
        values='Count',
        title='Toss Winner Match Result'
    )

    st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# VENUE ANALYSIS
# -----------------------------
st.subheader("🏟 Top Venues")

venue_count = (
    filtered_df['venue']
    .value_counts()
    .head(10)
    .reset_index()
)

venue_count.columns = ['Venue', 'Matches']

fig4 = px.bar(
    venue_count,
    x='Matches',
    y='Venue',
    orientation='h',
    text='Matches',
    title='Top 10 Venues'
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# PLAYER OF MATCH
# -----------------------------
if 'player_of_match' in filtered_df.columns:

    st.subheader("⭐ Player of Match Leaders")

    pom = (
        filtered_df['player_of_match']
        .value_counts()
        .head(15)
        .reset_index()
    )

    pom.columns = ['Player', 'Awards']

    fig5 = px.bar(
        pom,
        x='Player',
        y='Awards',
        text='Awards',
        color='Awards'
    )

    st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# WIN MARGIN ANALYSIS
# -----------------------------
if 'win_by_runs' in filtered_df.columns:

    st.subheader("🔥 Win Margin Distribution")

    fig6 = px.histogram(
        filtered_df,
        x='win_by_runs',
        nbins=30,
        title='Win By Runs Distribution'
    )

    st.plotly_chart(fig6, use_container_width=True)

# -----------------------------
# SEASON TREND
# -----------------------------
st.subheader("📅 Matches Per Season")

season_trend = (
    filtered_df.groupby('season')
    .size()
    .reset_index(name='Matches')
)

fig7 = px.line(
    season_trend,
    x='season',
    y='Matches',
    markers=True
)

st.plotly_chart(fig7, use_container_width=True)

# -----------------------------
# INSIGHTS SECTION
# -----------------------------
st.subheader("🧠 AI Generated Insights")

best_team = wins.iloc[0]['Team']
best_team_wins = wins.iloc[0]['Wins']

best_venue = venue_count.iloc[0]['Venue']

st.success(
    f"""
    • Most Successful Team : {best_team}

    • Total Wins : {best_team_wins}

    • Most Active Venue : {best_venue}

    • Total Matches Analysed : {total_matches}

    • Total Seasons Covered : {total_seasons}
    """
)

# -----------------------------
# RAW DATA
# -----------------------------
with st.expander("📄 View Dataset"):
    st.dataframe(filtered_df)

# -----------------------------
# DOWNLOAD CSV
# -----------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_matches.csv",
    mime="text/csv"
)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("IPL Analytics Dashboard | Streamlit + Pandas + Plotly")
