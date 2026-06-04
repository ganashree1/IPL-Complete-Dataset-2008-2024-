import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class IPLVisualizations:

    def __init__(self):
        pass

    # ============================================
    # TEAM WINS BAR CHART
    # ============================================

    def team_wins_chart(self, wins_df):

        fig = px.bar(
            wins_df,
            x="Team",
            y="Wins",
            color="Wins",
            text="Wins",
            title="Most Successful IPL Teams"
        )

        fig.update_layout(
            xaxis_title="Teams",
            yaxis_title="Wins",
            template="plotly_dark"
        )

        return fig

    # ============================================
    # TEAM WIN PERCENTAGE
    # ============================================

    def win_percentage_chart(self, win_df):

        fig = px.bar(
            win_df,
            x="Team",
            y="Win Percentage",
            color="Win Percentage",
            text="Win Percentage",
            title="Team Win Percentage"
        )

        fig.update_layout(
            template="plotly_dark"
        )

        return fig

    # ============================================
    # PIE CHART
    # ============================================

    def win_share_chart(self, wins_df):

        fig = px.pie(
            wins_df.head(10),
            names="Team",
            values="Wins",
            hole=0.4,
            title="Top Teams Win Share"
        )

        return fig

    # ============================================
    # TOP PLAYERS
    # ============================================

    def player_awards_chart(self, player_df):

        fig = px.bar(
            player_df,
            x="Player",
            y="Awards",
            color="Awards",
            text="Awards",
            title="Player Of Match Leaders"
        )

        fig.update_layout(
            template="plotly_dark"
        )

        return fig

    # ============================================
    # VENUE ANALYSIS
    # ============================================

    def venue_chart(self, venue_df):

        fig = px.bar(
            venue_df,
            x="Matches",
            y="Venue",
            orientation="h",
            text="Matches",
            title="Top IPL Venues"
        )

        fig.update_layout(
            template="plotly_dark"
        )

        return fig

    # ============================================
    # MATCHES PER SEASON
    # ============================================

    def season_trend_chart(self, season_df):

        fig = px.line(
            season_df,
            x="season",
            y="Matches",
            markers=True,
            title="IPL Matches Per Season"
        )

        fig.update_layout(
            template="plotly_dark"
        )

        return fig

    # ============================================
    # TOSS IMPACT
    # ============================================

    def toss_analysis_chart(self, toss_df):

        fig = px.pie(
            toss_df,
            names="Result",
            values="Count",
            title="Toss Impact Analysis"
        )

        return fig

    # ============================================
    # WIN BY RUNS HISTOGRAM
    # ============================================

    def win_margin_runs_chart(self, df):

        fig = px.histogram(
            df,
            x="win_by_runs",
            nbins=30,
            title="Win Margin By Runs"
        )

        fig.update_layout(
            template="plotly_dark"
        )

        return fig

    # ============================================
    # WIN BY WICKETS HISTOGRAM
    # ============================================

    def win_margin_wickets_chart(self, df):

        fig = px.histogram(
            df,
            x="win_by_wickets",
            nbins=20,
            title="Win Margin By Wickets"
        )

        fig.update_layout(
            template="plotly_dark"
        )

        return fig

    # ============================================
    # SUPER OVER CHART
    # ============================================

    def super_over_chart(self, super_count):

        chart_df = pd.DataFrame({

            "Type": [
                "Super Over"
            ],

            "Count": [
                super_count
            ]

        })

        fig = px.bar(
            chart_df,
            x="Type",
            y="Count",
            text="Count",
            title="Super Over Matches"
        )

        return fig

    # ============================================
    # TEAM VS TEAM HEATMAP
    # ============================================

    def team_heatmap(self, df):

        heatmap_df = pd.crosstab(
            df["team1"],
            df["team2"]
        )

        fig = px.imshow(
            heatmap_df,
            text_auto=False,
            aspect="auto",
            title="Team Matchup Heatmap"
        )

        return fig

    # ============================================
    # SCATTER PLOT
    # ============================================

    def scatter_runs_vs_wickets(self, df):

        fig = px.scatter(
            df,
            x="win_by_runs",
            y="win_by_wickets",
            title="Runs vs Wickets Margin"
        )

        return fig

    # ============================================
    # TREEMAP
    # ============================================

    def treemap_teams(self, wins_df):

        fig = px.treemap(
            wins_df,
            path=["Team"],
            values="Wins",
            title="IPL Teams Treemap"
        )

        return fig

    # ============================================
    # SUNBURST
    # ============================================

    def sunburst_teams(self, df):

        sun_df = df.groupby(
            ["season", "winner"]
        ).size().reset_index(
            name="Wins"
        )

        fig = px.sunburst(
            sun_df,
            path=["season", "winner"],
            values="Wins",
            title="Season Wise Winners"
        )

        return fig

    # ============================================
    # DONUT CHART
    # ============================================

    def donut_chart(self, df):

        result_df = df["result"].value_counts()

        chart_df = pd.DataFrame({

            "Result": result_df.index,
            "Count": result_df.values

        })

        fig = px.pie(
            chart_df,
            names="Result",
            values="Count",
            hole=0.5,
            title="Match Result Distribution"
        )

        return fig

    # ============================================
    # GAUGE CHART
    # ============================================

    def win_percentage_gauge(
            self,
            percentage
    ):

        fig = go.Figure(

            go.Indicator(

                mode="gauge+number",

                value=percentage,

                title={
                    "text":
                    "Win Percentage"
                },

                gauge={
                    "axis": {
                        "range":
                        [0, 100]
                    }
                }

            )

        )

        return fig

    # ============================================
    # KPI CARD FIGURE
    # ============================================

    def kpi_card(
            self,
            title,
            value
    ):

        fig = go.Figure()

        fig.add_trace(

            go.Indicator(

                mode="number",

                value=value,

                title={
                    "text": title
                }

            )

        )

        return fig
