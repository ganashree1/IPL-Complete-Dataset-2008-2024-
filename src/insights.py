import pandas as pd
import numpy as np


class IPLInsights:

    def __init__(self, df):
        self.df = df.copy()

    # =====================================================
    # MOST SUCCESSFUL TEAM
    # =====================================================

    def most_successful_team(self):

        winner_counts = self.df["winner"].value_counts()

        team = winner_counts.idxmax()
        wins = winner_counts.max()

        return (
            f"🏆 {team} is the most successful team "
            f"with {wins} victories."
        )

    # =====================================================
    # TOP PLAYER
    # =====================================================

    def top_player(self):

        if "player_of_match" not in self.df.columns:
            return "Player award data unavailable."

        awards = (
            self.df["player_of_match"]
            .value_counts()
        )

        player = awards.idxmax()
        count = awards.max()

        return (
            f"⭐ {player} has won "
            f"{count} Player of the Match awards."
        )

    # =====================================================
    # MOST ACTIVE VENUE
    # =====================================================

    def most_active_venue(self):

        venue_counts = (
            self.df["venue"]
            .value_counts()
        )

        venue = venue_counts.idxmax()
        matches = venue_counts.max()

        return (
            f"🏟️ {venue} hosted "
            f"{matches} IPL matches."
        )

    # =====================================================
    # TOSS IMPACT
    # =====================================================

    def toss_impact(self):

        toss_match = self.df[
            self.df["toss_winner"]
            ==
            self.df["winner"]
        ]

        percentage = round(
            (
                len(toss_match)
                /
                len(self.df)
            ) * 100,
            2
        )

        return (
            f"🪙 Toss winners also won the match "
            f"{percentage}% of the time."
        )

    # =====================================================
    # MOST POPULAR TOSS DECISION
    # =====================================================

    def toss_decision(self):

        if "toss_decision" not in self.df.columns:
            return "Toss decision data unavailable."

        decision = (
            self.df["toss_decision"]
            .value_counts()
            .idxmax()
        )

        count = (
            self.df["toss_decision"]
            .value_counts()
            .max()
        )

        return (
            f"📌 Teams preferred to "
            f"'{decision}' after winning the toss "
            f"{count} times."
        )

    # =====================================================
    # BIGGEST RUN WIN
    # =====================================================

    def highest_run_margin(self):

        if "win_by_runs" not in self.df.columns:
            return "Run margin data unavailable."

        row = self.df.loc[
            self.df["win_by_runs"].idxmax()
        ]

        return (
            f"🔥 Biggest win by runs was "
            f"{row['win_by_runs']} runs by "
            f"{row['winner']}."
        )

    # =====================================================
    # BIGGEST WICKET WIN
    # =====================================================

    def highest_wicket_margin(self):

        if "win_by_wickets" not in self.df.columns:
            return "Wicket margin data unavailable."

        row = self.df.loc[
            self.df["win_by_wickets"].idxmax()
        ]

        return (
            f"⚡ Biggest win by wickets was "
            f"{row['win_by_wickets']} wickets by "
            f"{row['winner']}."
        )

    # =====================================================
    # SUPER OVER ANALYSIS
    # =====================================================

    def super_over_analysis(self):

        if "super_over" not in self.df.columns:
            return "Super over data unavailable."

        count = len(
            self.df[
                self.df["super_over"] == "Y"
            ]
        )

        return (
            f"🎯 IPL witnessed "
            f"{count} Super Over matches."
        )

    # =====================================================
    # SEASON WITH MOST MATCHES
    # =====================================================

    def busiest_season(self):

        if "season" not in self.df.columns:
            return "Season data unavailable."

        season_matches = (
            self.df.groupby("season")
            .size()
        )

        season = season_matches.idxmax()
        matches = season_matches.max()

        return (
            f"📅 Season {season} had the highest "
            f"number of matches ({matches})."
        )

    # =====================================================
    # TEAM WITH BEST WIN RATE
    # =====================================================

    def best_win_rate_team(self):

        team1 = self.df["team1"].value_counts()
        team2 = self.df["team2"].value_counts()

        matches = team1.add(
            team2,
            fill_value=0
        )

        wins = self.df["winner"].value_counts()

        stats = pd.DataFrame({

            "Matches": matches,
            "Wins": wins

        }).fillna(0)

        stats["WinRate"] = round(
            (
                stats["Wins"]
                /
                stats["Matches"]
            ) * 100,
            2
        )

        stats = stats[
            stats["Matches"] >= 20
        ]

        team = stats["WinRate"].idxmax()
        rate = stats["WinRate"].max()

        return (
            f"📈 {team} has the best win rate "
            f"of {rate}%."
        )

    # =====================================================
    # MATCH RESULT DISTRIBUTION
    # =====================================================

    def result_distribution(self):

        if "result" not in self.df.columns:
            return "Result data unavailable."

        result = (
            self.df["result"]
            .value_counts()
            .idxmax()
        )

        count = (
            self.df["result"]
            .value_counts()
            .max()
        )

        return (
            f"📊 Most common match result "
            f"is '{result}' with {count} matches."
        )

    # =====================================================
    # GENERATE ALL INSIGHTS
    # =====================================================

    def generate_all_insights(self):

        insights = [

            self.most_successful_team(),

            self.top_player(),

            self.most_active_venue(),

            self.toss_impact(),

            self.toss_decision(),

            self.highest_run_margin(),

            self.highest_wicket_margin(),

            self.super_over_analysis(),

            self.busiest_season(),

            self.best_win_rate_team(),

            self.result_distribution()

        ]

        return insights

    # =====================================================
    # DASHBOARD SUMMARY
    # =====================================================

    def dashboard_summary(self):

        summary = {

            "Most Successful Team":
                self.most_successful_team(),

            "Top Player":
                self.top_player(),

            "Top Venue":
                self.most_active_venue(),

            "Toss Insight":
                self.toss_impact(),

            "Super Over Insight":
                self.super_over_analysis()

        }

        return summary


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    df = pd.read_csv(
        "data/matches.csv"
    )

    insights = IPLInsights(df)

    all_insights = (
        insights.generate_all_insights()
    )

    print("\nIPL INSIGHTS\n")

    for item in all_insights:
        print(item)
