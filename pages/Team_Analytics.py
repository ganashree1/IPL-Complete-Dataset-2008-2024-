import streamlit as st
import pandas as pd
import plotly.express as px

from src.utils import load_data
from src.analytics import IPLAnalytics

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Team Analytics",
    page_icon="🏏",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

df = load_data("data/matches.csv")

analytics = IPLAnalytics(df)

# ==========================================
# HEADER
# ==========================================

st.title("🏏 Team Analytics Dashboard")

st.markdown("---")

# ==========================================
# TEAM LIST
# ==========================================

teams = sorted(
    list(
        set(df["team1"].dropna())
        .union(
            set(df["team2"].dropna())
        )
    )
)

selected_team = st.selectbox(
    "Select Team",
    teams
)

# ==========================================
# FILTER TEAM MATCHES
# ==========================================

team_df = df[
    (df["team1"] == selected_team)
    |
    (df["team2"] == selected_team)
]

# ==========================================
# KPI SECTION
# ==========================================

matches_played = len(team_df)

wins = len(
    team_df[
        team_df["winner"] == selected_team
    ]
)

losses = matches_played - wins

win_percentage = round(
    (wins / matches_played) * 100,
    2
) if matches_played > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Matches",
    matches_played
)

col2.metric(
    "Wins",
    wins
)

col3.metric(
    "Losses",
    losses
)

col4.metric(
    "Win %",
    f"{win_percentage}%"
)

st.markdown("---")

# ==========================================
# WINS BY SEASON
# ==========================================

st.subheader(
    "📈 Season-wise Wins"
)

season_wins = (
    team_df[
        team_df["winner"] == selected_team
    ]
    .groupby("season")
    .size()
    .reset_index(
        name="Wins"
    )
)

fig = px.line(
    season_wins,
    x="season",
    y="Wins",
    markers=True,
    title=f"{selected_team} Season Performance"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# WINS BY VENUE
# ==========================================

st.subheader(
    "🏟 Venue Performance"
)

venue_wins = (
    team_df[
        team_df["winner"] == selected_team
    ]["venue"]
    .value_counts()
    .head(10)
    .reset_index()
)

venue_wins.columns = [
    "Venue",
    "Wins"
]

fig2 = px.bar(
    venue_wins,
    x="Venue",
    y="Wins",
    color="Wins",
    text="Wins",
    title="Top Winning Venues"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================
# OPPONENT ANALYSIS
# ==========================================

st.subheader(
    "⚔ Opponent Analysis"
)

opponents = []

for _, row in team_df.iterrows():

    if row["team1"] == selected_team:
        opponents.append(row["team2"])
    else:
        opponents.append(row["team1"])

opponent_df = pd.DataFrame(
    {
        "Opponent": opponents
    }
)

opponent_matches = (
    opponent_df["Opponent"]
    .value_counts()
    .head(10)
    .reset_index()
)

opponent_matches.columns = [
    "Opponent",
    "Matches"
]

fig3 = px.bar(
    opponent_matches,
    x="Opponent",
    y="Matches",
    color="Matches",
    text="Matches",
    title="Most Faced Opponents"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================
# TOSS ANALYSIS
# ==========================================

st.subheader(
    "🪙 Toss Impact"
)

team_toss = team_df[
    team_df["toss_winner"]
    == selected_team
]

won_after_toss = len(
    team_toss[
        team_toss["winner"]
        == selected_team
    ]
)

lost_after_toss = len(team_toss) - won_after_toss

toss_data = pd.DataFrame({

    "Result": [
        "Won Match",
        "Lost Match"
    ],

    "Count": [
        won_after_toss,
        lost_after_toss
    ]

})

fig4 = px.pie(
    toss_data,
    names="Result",
    values="Count",
    hole=0.4,
    title="Performance After Winning Toss"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ==========================================
# WIN TYPE ANALYSIS
# ==========================================

st.subheader(
    "🔥 Win Type Analysis"
)

runs_wins = len(
    team_df[
        (team_df["winner"] == selected_team)
        &
        (team_df["win_by_runs"] > 0)
    ]
)

wicket_wins = len(
    team_df[
        (team_df["winner"] == selected_team)
        &
        (team_df["win_by_wickets"] > 0)
    ]
)

win_type_df = pd.DataFrame({

    "Type": [
        "Runs",
        "Wickets"
    ],

    "Wins": [
        runs_wins,
        wicket_wins
    ]

})

fig5 = px.bar(
    win_type_df,
    x="Type",
    y="Wins",
    color="Wins",
    text="Wins",
    title="Winning Pattern"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ==========================================
# AI INSIGHTS
# ==========================================

st.subheader(
    "🧠 Team Insights"
)

st.success(
    f"{selected_team} has played "
    f"{matches_played} matches."
)

st.success(
    f"{selected_team} won "
    f"{wins} matches."
)

st.success(
    f"Overall win percentage is "
    f"{win_percentage}%."
)

best_venue = (
    venue_wins.iloc[0]["Venue"]
    if not venue_wins.empty
    else "N/A"
)

st.success(
    f"Best venue for "
    f"{selected_team} is "
    f"{best_venue}."
)

# ==========================================
# RAW DATA
# ==========================================

with st.expander(
    "📄 View Team Match Data"
):

    st.dataframe(team_df)

# ==========================================
# DOWNLOAD DATA
# ==========================================

csv = team_df.to_csv(
    index=False
)

st.download_button(
    label="⬇ Download Team Data",
    data=csv,
    file_name=f"{selected_team}_matches.csv",
    mime="text/csv"
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "IPL Analytics Dashboard | Team Analytics"
)
