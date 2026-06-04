import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime


# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data(filepath):

    try:

        df = pd.read_csv(filepath)

        return df

    except Exception as e:

        st.error(f"Error loading dataset: {e}")

        return pd.DataFrame()


# =====================================================
# CONVERT DATE COLUMN
# =====================================================

def convert_date(df):

    if "date" in df.columns:

        try:

            df["date"] = pd.to_datetime(
                df["date"],
                errors="coerce"
            )

        except:

            pass

    return df


# =====================================================
# FILTER BY SEASON
# =====================================================

def filter_by_season(df, seasons):

    if not seasons:
        return df

    return df[
        df["season"].isin(seasons)
    ]


# =====================================================
# FILTER BY TEAM
# =====================================================

def filter_by_team(df, teams):

    if not teams:
        return df

    return df[
        (df["team1"].isin(teams))
        |
        (df["team2"].isin(teams))
    ]


# =====================================================
# FILTER BY VENUE
# =====================================================

def filter_by_venue(df, venues):

    if not venues:
        return df

    return df[
        df["venue"].isin(venues)
    ]


# =====================================================
# TEAM LIST
# =====================================================

def get_team_list(df):

    teams = set(
        df["team1"].dropna().unique()
    ).union(
        set(
            df["team2"].dropna().unique()
        )
    )

    return sorted(list(teams))


# =====================================================
# VENUE LIST
# =====================================================

def get_venue_list(df):

    if "venue" not in df.columns:
        return []

    return sorted(
        df["venue"].dropna().unique()
    )


# =====================================================
# SEASON LIST
# =====================================================

def get_season_list(df):

    if "season" not in df.columns:
        return []

    return sorted(
        df["season"].dropna().unique()
    )


# =====================================================
# TOTAL MATCHES
# =====================================================

def total_matches(df):

    return len(df)


# =====================================================
# TOTAL TEAMS
# =====================================================

def total_teams(df):

    teams = set(
        df["team1"]
    ).union(
        set(df["team2"])
    )

    return len(teams)


# =====================================================
# TOTAL VENUES
# =====================================================

def total_venues(df):

    if "venue" not in df.columns:
        return 0

    return df["venue"].nunique()


# =====================================================
# TOTAL SEASONS
# =====================================================

def total_seasons(df):

    if "season" not in df.columns:
        return 0

    return df["season"].nunique()


# =====================================================
# TOP TEAM
# =====================================================

def top_team(df):

    if "winner" not in df.columns:
        return "N/A"

    return (
        df["winner"]
        .value_counts()
        .idxmax()
    )


# =====================================================
# TOP PLAYER
# =====================================================

def top_player(df):

    if "player_of_match" not in df.columns:
        return "N/A"

    return (
        df["player_of_match"]
        .value_counts()
        .idxmax()
    )


# =====================================================
# MOST ACTIVE VENUE
# =====================================================

def top_venue(df):

    if "venue" not in df.columns:
        return "N/A"

    return (
        df["venue"]
        .value_counts()
        .idxmax()
    )


# =====================================================
# DASHBOARD KPI
# =====================================================

def dashboard_kpis(df):

    return {

        "Matches":
            total_matches(df),

        "Teams":
            total_teams(df),

        "Venues":
            total_venues(df),

        "Seasons":
            total_seasons(df),

        "Top Team":
            top_team(df),

        "Top Player":
            top_player(df),

        "Top Venue":
            top_venue(df)

    }


# =====================================================
# EXPORT CSV
# =====================================================

def convert_to_csv(df):

    return df.to_csv(
        index=False
    ).encode("utf-8")


# =====================================================
# DOWNLOAD BUTTON
# =====================================================

def create_download_button(df):

    csv = convert_to_csv(df)

    st.download_button(

        label="⬇ Download Data",

        data=csv,

        file_name="ipl_filtered_data.csv",

        mime="text/csv"

    )


# =====================================================
# DATASET SUMMARY
# =====================================================

def dataset_summary(df):

    summary = {

        "Rows":
            df.shape[0],

        "Columns":
            df.shape[1],

        "Missing Values":
            df.isnull().sum().sum(),

        "Duplicates":
            df.duplicated().sum()

    }

    return summary


# =====================================================
# MISSING VALUES REPORT
# =====================================================

def missing_value_report(df):

    report = pd.DataFrame({

        "Column":
            df.columns,

        "Missing Values":
            df.isnull().sum().values

    })

    report = report.sort_values(

        by="Missing Values",

        ascending=False

    )

    return report


# =====================================================
# NUMERIC COLUMN LIST
# =====================================================

def get_numeric_columns(df):

    return list(

        df.select_dtypes(

            include=np.number

        ).columns

    )


# =====================================================
# CATEGORICAL COLUMN LIST
# =====================================================

def get_categorical_columns(df):

    return list(

        df.select_dtypes(

            include="object"

        ).columns

    )


# =====================================================
# SAFE DIVISION
# =====================================================

def safe_divide(a, b):

    if b == 0:

        return 0

    return round(a / b, 2)


# =====================================================
# FORMAT LARGE NUMBERS
# =====================================================

def format_number(number):

    if number >= 1000000:

        return f"{number/1000000:.1f}M"

    elif number >= 1000:

        return f"{number/1000:.1f}K"

    else:

        return str(number)


# =====================================================
# PAGE HEADER
# =====================================================

def page_header(title):

    st.markdown(
        f"# {title}"
    )


# =====================================================
# FOOTER
# =====================================================

def footer():

    st.markdown("---")

    st.caption(
        "IPL Analytics Dashboard | Streamlit | Plotly | Pandas"
    )


# =====================================================
# APP INFO
# =====================================================

def app_info():

    return {

        "Project":
            "IPL Analytics Dashboard",

        "Framework":
            "Streamlit",

        "Visualization":
            "Plotly",

        "Language":
            "Python",

        "Version":
            "1.0"

    }


# =====================================================
# TESTING
# =====================================================

if __name__ == "__main__":

    df = pd.read_csv(
        "data/matches.csv"
    )

    print(dataset_summary(df))

    print(
        dashboard_kpis(df)
    )

    print(
        get_team_list(df)[:5]
    )

    print(
        get_venue_list(df)[:5]
    )
