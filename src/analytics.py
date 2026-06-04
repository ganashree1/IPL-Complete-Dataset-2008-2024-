import pandas as pd
import numpy as np


class IPLAnalytics:

    def __init__(self, df):
        self.df = df.copy()

    # =====================================================
    # OVERALL KPIs
    # =====================================================

    def get_total_matches(self):
        return len(self.df)

    def get_total_seasons(self):

        if 'season' in self.df.columns:
            return self.df['season'].nunique()

        return 0

    def get_total_venues(self):

        if 'venue' in self.df.columns:
            return self.df['venue'].nunique()

        return 0

    def get_total_teams(self):

        teams = set(
            self.df['team1'].dropna().unique()
        ).union(
            set(
                self.df['team2'].dropna().unique()
            )
        )

        return len(teams)

    # =====================================================
    # TEAM ANALYTICS
    # =====================================================

    def team_wins(self):

        return (
            self.df['winner']
            .value_counts()
            .reset_index()
            .rename(
                columns={
                    'index': 'Team',
                    'winner': 'Wins'
                }
            )
        )

    def most_successful_team(self):

        return self.df['winner'].value_counts().idxmax()

    def most_successful_team_wins(self):

        return self.df['winner'].value_counts().max()

    def matches_played_by_team(self):

        team1 = self.df['team1'].value_counts()

        team2 = self.df['team2'].value_counts()

        matches = team1.add(
            team2,
            fill_value=0
        )

        result = matches.sort_values(
            ascending=False
        ).reset_index()

        result.columns = [
            'Team',
            'Matches Played'
        ]

        return result

    def win_percentage(self):

        matches = self.matches_played_by_team()

        wins = (
            self.df['winner']
            .value_counts()
            .reset_index()
        )

        wins.columns = [
            'Team',
            'Wins'
        ]

        merged = matches.merge(
            wins,
            on='Team',
            how='left'
        )

        merged['Wins'] = merged['Wins'].fillna(0)

        merged['Win Percentage'] = round(
            (
                merged['Wins']
                /
                merged['Matches Played']
            ) * 100,
            2
        )

        return merged.sort_values(
            'Win Percentage',
            ascending=False
        )

    # =====================================================
    # TOSS ANALYTICS
    # =====================================================

    def toss_analysis(self):

        toss_match_win = self.df[
            self.df['toss_winner']
            ==
            self.df['winner']
        ]

        toss_match_loss = self.df[
            self.df['toss_winner']
            !=
            self.df['winner']
        ]

        return pd.DataFrame({

            "Result": [
                "Won Toss & Match",
                "Won Toss Lost Match"
            ],

            "Count": [
                len(toss_match_win),
                len(toss_match_loss)
            ]
        })

    def toss_decision_analysis(self):

        if 'toss_decision' not in self.df.columns:
            return pd.DataFrame()

        return (
            self.df['toss_decision']
            .value_counts()
            .reset_index()
            .rename(
                columns={
                    'index': 'Decision',
                    'toss_decision': 'Count'
                }
            )
        )

    # =====================================================
    # PLAYER ANALYTICS
    # =====================================================

    def player_of_match_leaders(
            self,
            top_n=15
    ):

        if 'player_of_match' not in self.df.columns:
            return pd.DataFrame()

        result = (
            self.df['player_of_match']
            .value_counts()
            .head(top_n)
            .reset_index()
        )

        result.columns = [
            'Player',
            'Awards'
        ]

        return result

    def top_player(self):

        if 'player_of_match' not in self.df.columns:
            return None

        return (
            self.df['player_of_match']
            .mode()[0]
        )

    # =====================================================
    # VENUE ANALYTICS
    # =====================================================

    def top_venues(
            self,
            top_n=10
    ):

        if 'venue' not in self.df.columns:
            return pd.DataFrame()

        result = (
            self.df['venue']
            .value_counts()
            .head(top_n)
            .reset_index()
        )

        result.columns = [
            'Venue',
            'Matches'
        ]

        return result

    def venue_wise_matches(self):

        return (
            self.df['venue']
            .value_counts()
            .reset_index()
            .rename(
                columns={
                    'index': 'Venue',
                    'venue': 'Matches'
                }
            )
        )

    # =====================================================
    # SEASON ANALYTICS
    # =====================================================

    def matches_per_season(self):

        if 'season' not in self.df.columns:
            return pd.DataFrame()

        return (
            self.df
            .groupby('season')
            .size()
            .reset_index(
                name='Matches'
            )
        )

    def season_winner_count(self):

        if (
                'season' not in self.df.columns
                or
                'winner' not in self.df.columns
        ):
            return pd.DataFrame()

        return (
            self.df
            .groupby(
                ['season', 'winner']
            )
            .size()
            .reset_index(
                name='Wins'
            )
        )

    # =====================================================
    # WIN MARGIN ANALYSIS
    # =====================================================

    def win_by_runs_analysis(self):

        if 'win_by_runs' not in self.df.columns:
            return pd.DataFrame()

        return self.df[
            self.df['win_by_runs'] > 0
        ][['winner', 'win_by_runs']]

    def win_by_wickets_analysis(self):

        if 'win_by_wickets' not in self.df.columns:
            return pd.DataFrame()

        return self.df[
            self.df['win_by_wickets'] > 0
        ][['winner', 'win_by_wickets']]

    def highest_run_margin(self):

        if 'win_by_runs' not in self.df.columns:
            return None

        return self.df[
            self.df['win_by_runs']
            ==
            self.df['win_by_runs'].max()
        ]

    def highest_wicket_margin(self):

        if 'win_by_wickets' not in self.df.columns:
            return None

        return self.df[
            self.df['win_by_wickets']
            ==
            self.df['win_by_wickets'].max()
        ]

    # =====================================================
    # SUPER OVER ANALYSIS
    # =====================================================

    def super_over_matches(self):

        if 'super_over' not in self.df.columns:
            return pd.DataFrame()

        return self.df[
            self.df['super_over'] == 'Y'
        ]

    def super_over_count(self):

        if 'super_over' not in self.df.columns:
            return 0

        return len(
            self.df[
                self.df['super_over'] == 'Y'
            ]
        )

    # =====================================================
    # HOME ADVANTAGE
    # =====================================================

    def home_team_wins(self):

        if (
                'team1' not in self.df.columns
                or
                'winner' not in self.df.columns
        ):
            return pd.DataFrame()

        return self.df[
            self.df['team1']
            ==
            self.df['winner']
        ]

    # =====================================================
    # INSIGHTS
    # =====================================================

    def generate_insights(self):

        insights = []

        insights.append(
            f"Most successful team: "
            f"{self.most_successful_team()}"
        )

        insights.append(
            f"Highest wins: "
            f"{self.most_successful_team_wins()}"
        )

        insights.append(
            f"Top player: "
            f"{self.top_player()}"
        )

        insights.append(
            f"Super Over Matches: "
            f"{self.super_over_count()}"
        )

        return insights

    # =====================================================
    # DASHBOARD SUMMARY
    # =====================================================

    def dashboard_summary(self):

        summary = {

            "Matches":
                self.get_total_matches(),

            "Teams":
                self.get_total_teams(),

            "Venues":
                self.get_total_venues(),

            "Seasons":
                self.get_total_seasons(),

            "Top Team":
                self.most_successful_team(),

            "Top Player":
                self.top_player(),

            "Super Overs":
                self.super_over_count()

        }

        return summary


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    df = pd.read_csv(
        "data/matches.csv"
    )

    analytics = IPLAnalytics(df)

    print("\nDashboard Summary")
    print(
        analytics.dashboard_summary()
    )

    print("\nTop Teams")
    print(
        analytics.team_wins().head()
    )

    print("\nTop Players")
    print(
        analytics.player_of_match_leaders()
    )

    print("\nInsights")
    print(
        analytics.generate_insights()
    )
