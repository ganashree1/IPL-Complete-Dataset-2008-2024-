import streamlit as st
import pandas as pd
import plotly.express as px

from src.utils import load_data

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Match Analytics",
    page_icon="🏏",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

df = load_data("data/matches.csv")

# ==========================================
# HEADER
# ==========================================

st.title("🏏 IPL Match Analytics Dashboard")

st.markdown("---")

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("Filters")

if "season" in df.columns:

    seasons = sorted(
        df["season"]
        .dropna()
        .unique()
    )

    selected_seasons = st.sidebar.multiselect(
        "Select Seasons",
        seasons,
        default=seasons
    )

    filtered_df = df[
        df["season"]
        .isin(selected_seasons)
    ]

else:
    filtered_df = df.copy()

# ==========================================
# KPI SECTION
# ==========================================

total_matches = len(filtered_df)

total_seasons = (
    filtered_df["season"].nunique()
    if "season" in filtered_df.columns
    else 0
)

total_venues = (
    filtered_df["venue"].nunique()
    if "venue" in filtered_df.columns
    else 0
)

super_over_count = 0

if "super_over" in filtered_df.columns:

    super_over_count = len(
        filtered_df[
            filtered_df["super_over"] == "Y"
        ]
    )

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Matches",
    total_matches
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
    "Super Overs",
    super_over_count
)

st.markdown("---")

# ==========================================
# MATCHES PER SEASON
# ==========================================

st.subheader(
    "📈 Matches Per Season"
)

if "season" in filtered_df.columns:

    season_matches = (
        filtered_df
        .groupby("season")
        .size()
        .reset_index(
            name="Matches"
        )
    )

    fig1 = px.line(
        season_matches,
        x="season",
        y="Matches",
        markers=True,
        title="Season Trend"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# ==========================================
# TOSS IMPACT ANALYSIS
# ==========================================

st.subheader(
    "🪙 Toss Impact Analysis"
)

if (
    "toss_winner" in filtered_df.columns
    and
    "winner" in filtered_df.columns
):

    toss_win_match = len(
        filtered_df[
            filtered_df["toss_winner"]
            ==
            filtered_df["winner"]
        ]
    )

    toss_lost_match = (
        total_matches
        -
        toss_win_match
    )

    toss_df = pd.DataFrame({

        "Category": [
            "Won Toss & Match",
            "Won Toss Lost Match"
        ],

        "Count": [
            toss_win_match,
            toss_lost_match
        ]

    })

    fig2 = px.pie(
        toss_df,
        names="Category",
        values="Count",
        hole=0.4,
        title="Toss Influence"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==========================================
# TOSS DECISION
# ==========================================

st.subheader(
    "📌 Toss Decision Preference"
)

if "toss_decision" in filtered_df.columns:

    toss_decision = (
        filtered_df["toss_decision"]
        .value_counts()
        .reset_index()
    )

    toss_decision.columns = [
        "Decision",
        "Count"
    ]

    fig3 = px.bar(
        toss_decision,
        x="Decision",
        y="Count",
        color="Count",
        text="Count",
        title="Toss Decision Analysis"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ==========================================
# WIN BY RUNS
# ==========================================

st.subheader("🔥 Win Margin by Runs")

if "margin" in filtered_df.columns and "margin_type" in filtered_df.columns:

    runs_df = filtered_df[
        filtered_df["margin_type"].str.lower() == "runs"
    ]

    if not runs_df.empty:

        fig4 = px.histogram(
            runs_df,
            x="margin",
            nbins=30,
            title="Runs Margin Distribution"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )
    else:
        st.warning("Run margin data unavailable.")

# ==========================================
# WIN BY WICKETS
# ==========================================

st.subheader("⚡ Win Margin by Wickets")

if "margin" in filtered_df.columns and "margin_type" in filtered_df.columns:

    wickets_df = filtered_df[
        filtered_df["margin_type"].str.lower() == "wickets"
    ]

    if not wickets_df.empty:

        fig5 = px.histogram(
            wickets_df,
            x="margin",
            nbins=15,
            title="Wicket Margin Distribution"
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )
    else:
        st.warning("Wicket margin data unavailable.")
# ==========================================
# RESULT DISTRIBUTION
# ==========================================

st.subheader(
    "📊 Match Result Distribution"
)

if "result" in filtered_df.columns:

    result_df = (
        filtered_df["result"]
        .value_counts()
        .reset_index()
    )

    result_df.columns = [
        "Result",
        "Count"
    ]

    fig6 = px.pie(
        result_df,
        names="Result",
        values="Count",
        hole=0.5,
        title="Result Distribution"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

# ==========================================
# TOP WINNING TEAMS
# ==========================================

st.subheader(
    "🏆 Most Successful Teams"
)

if "winner" in filtered_df.columns:

    winners = (
        filtered_df["winner"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    winners.columns = [
        "Team",
        "Wins"
    ]

    fig7 = px.bar(
        winners,
        x="Team",
        y="Wins",
        color="Wins",
        text="Wins",
        title="Top Winning Teams"
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )

# ==========================================
# SUPER OVER ANALYSIS
# ==========================================

st.subheader(
    "🎯 Super Over Analysis"
)

if "super_over" in filtered_df.columns:

    super_df = (
        filtered_df["super_over"]
        .value_counts()
        .reset_index()
    )

    super_df.columns = [
        "SuperOver",
        "Count"
    ]

    fig8 = px.bar(
        super_df,
        x="SuperOver",
        y="Count",
        color="Count",
        text="Count",
        title="Super Over Frequency"
    )

    st.plotly_chart(
        fig8,
        use_container_width=True
    )

# ==========================================
# SEASON WINNERS
# ==========================================

st.subheader(
    "🏅 Season-wise Match Winners"
)

if (
    "season" in filtered_df.columns
    and
    "winner" in filtered_df.columns
):

    season_winner = (
        filtered_df
        .groupby(
            ["season", "winner"]
        )
        .size()
        .reset_index(
            name="Wins"
        )
    )

    fig9 = px.sunburst(
        season_winner,
        path=["season", "winner"],
        values="Wins",
        title="Season-wise Winner Distribution"
    )

    st.plotly_chart(
        fig9,
        use_container_width=True
    )

# ==========================================
# AI INSIGHTS
# ==========================================

st.subheader(
    "🧠 Match Insights"
)

if "winner" in filtered_df.columns:

    top_team = (
        filtered_df["winner"]
        .value_counts()
        .idxmax()
    )

    top_team_wins = (
        filtered_df["winner"]
        .value_counts()
        .max()
    )

    st.success(
        f"🏆 Most successful team: "
        f"{top_team} ({top_team_wins} wins)"
    )

if (
    "toss_winner" in filtered_df.columns
    and
    "winner" in filtered_df.columns
):

    toss_percent = round(
        (
            toss_win_match
            /
            total_matches
        ) * 100,
        2
    )

    st.success(
        f"🪙 Toss winners won "
        f"{toss_percent}% of matches."
    )

st.success(
    f"🎯 Total Super Over Matches: "
    f"{super_over_count}"
)

st.success(
    f"📅 Seasons Analysed: "
    f"{total_seasons}"
)

# ==========================================
# RAW DATA
# ==========================================

with st.expander(
    "📄 View Match Dataset"
):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# ==========================================
# DOWNLOAD DATA
# ==========================================

csv = filtered_df.to_csv(
    index=False
)

st.download_button(
    label="⬇ Download Match Data",
    data=csv,
    file_name="match_analytics.csv",
    mime="text/csv"
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "IPL Analytics Dashboard | Match Analytics"
)
