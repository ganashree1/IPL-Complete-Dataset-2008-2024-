import pandas as pd
import numpy as np


class IPLPreprocessor:

    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    # ---------------------------------------------------
    # LOAD DATA
    # ---------------------------------------------------
    def load_data(self):
        self.df = pd.read_csv(self.filepath)
        return self.df

    # ---------------------------------------------------
    # BASIC INFO
    # ---------------------------------------------------
    def dataset_info(self):

        info = {
            "Rows": self.df.shape[0],
            "Columns": self.df.shape[1],
            "Missing Values": self.df.isnull().sum().sum(),
            "Duplicate Rows": self.df.duplicated().sum()
        }

        return info

    # ---------------------------------------------------
    # REMOVE DUPLICATES
    # ---------------------------------------------------
    def remove_duplicates(self):

        before = len(self.df)

        self.df.drop_duplicates(inplace=True)

        after = len(self.df)

        print(f"Removed {before-after} duplicate rows")

        return self.df

    # ---------------------------------------------------
    # HANDLE MISSING VALUES
    # ---------------------------------------------------
    def handle_missing_values(self):

        object_cols = self.df.select_dtypes(
            include="object"
        ).columns

        for col in object_cols:
            self.df[col].fillna("Unknown", inplace=True)

        numeric_cols = self.df.select_dtypes(
            include=np.number
        ).columns

        for col in numeric_cols:
            self.df[col].fillna(
                self.df[col].median(),
                inplace=True
            )

        return self.df

    # ---------------------------------------------------
    # STANDARDIZE TEAM NAMES
    # ---------------------------------------------------
    def standardize_teams(self):

        replacements = {

            "Delhi Daredevils":
                "Delhi Capitals",

            "Kings XI Punjab":
                "Punjab Kings",

            "Rising Pune Supergiant":
                "Rising Pune Supergiants"

        }

        team_columns = [
            "team1",
            "team2",
            "winner",
            "toss_winner"
        ]

        for col in team_columns:

            if col in self.df.columns:

                self.df[col] = self.df[col].replace(
                    replacements
                )

        return self.df

    # ---------------------------------------------------
    # CREATE SEASON COLUMN
    # ---------------------------------------------------
    def create_season_column(self):

        if "date" in self.df.columns:

            self.df["date"] = pd.to_datetime(
                self.df["date"],
                errors="coerce"
            )

            self.df["year"] = self.df["date"].dt.year

        return self.df

    # ---------------------------------------------------
    # TOSS IMPACT FEATURE
    # ---------------------------------------------------
    def toss_impact_feature(self):

        if (
            "toss_winner" in self.df.columns and
            "winner" in self.df.columns
        ):

            self.df["toss_match_win"] = np.where(
                self.df["toss_winner"]
                == self.df["winner"],
                1,
                0
            )

        return self.df

    # ---------------------------------------------------
    # WIN TYPE FEATURE
    # ---------------------------------------------------
    def create_win_type(self):

        if (
            "win_by_runs" in self.df.columns and
            "win_by_wickets" in self.df.columns
        ):

            conditions = [
                self.df["win_by_runs"] > 0,
                self.df["win_by_wickets"] > 0
            ]

            choices = [
                "Runs",
                "Wickets"
            ]

            self.df["win_type"] = np.select(
                conditions,
                choices,
                default="Tie"
            )

        return self.df

    # ---------------------------------------------------
    # MATCH NUMBER
    # ---------------------------------------------------
    def create_match_id(self):

        self.df["match_id"] = range(
            1,
            len(self.df) + 1
        )

        return self.df

    # ---------------------------------------------------
    # FEATURE ENGINEERING
    # ---------------------------------------------------
    def feature_engineering(self):

        self.create_match_id()

        self.create_season_column()

        self.toss_impact_feature()

        self.create_win_type()

        return self.df

    # ---------------------------------------------------
    # TEAM LIST
    # ---------------------------------------------------
    def get_all_teams(self):

        teams = set(
            self.df["team1"].dropna().unique()
        ).union(
            set(
                self.df["team2"].dropna().unique()
            )
        )

        return sorted(list(teams))

    # ---------------------------------------------------
    # VENUE LIST
    # ---------------------------------------------------
    def get_all_venues(self):

        if "venue" in self.df.columns:
            return sorted(
                self.df["venue"].dropna().unique()
            )

        return []

    # ---------------------------------------------------
    # KPI SUMMARY
    # ---------------------------------------------------
    def generate_kpis(self):

        kpis = {}

        kpis["Total Matches"] = len(self.df)

        if "season" in self.df.columns:
            kpis["Total Seasons"] = \
                self.df["season"].nunique()

        if "venue" in self.df.columns:
            kpis["Total Venues"] = \
                self.df["venue"].nunique()

        teams = set(
            self.df["team1"]
        ).union(
            set(self.df["team2"])
        )

        kpis["Total Teams"] = len(teams)

        if "winner" in self.df.columns:

            kpis["Most Successful Team"] = \
                self.df["winner"].mode()[0]

        if "player_of_match" in self.df.columns:

            kpis["Top Player"] = \
                self.df["player_of_match"].mode()[0]

        return kpis

    # ---------------------------------------------------
    # FULL PIPELINE
    # ---------------------------------------------------
    def preprocess(self):

        self.load_data()

        self.remove_duplicates()

        self.handle_missing_values()

        self.standardize_teams()

        self.feature_engineering()

        return self.df


# -------------------------------------------------------
# MAIN TESTING
# -------------------------------------------------------
if __name__ == "__main__":

    processor = IPLPreprocessor(
        "data/matches.csv"
    )

    df = processor.preprocess()

    print("\nDataset Shape:")
    print(df.shape)

    print("\nDataset Info:")
    print(processor.dataset_info())

    print("\nKPIs:")
    print(processor.generate_kpis())

    print("\nTop 5 Rows:")
    print(df.head())
