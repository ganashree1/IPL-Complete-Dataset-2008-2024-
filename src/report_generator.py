
import os

class ReportGenerator:

    def __init__(self, df):
        self.df = df

    def generate_all_reports(self):

        os.makedirs(
            "reports/generated_reports",
            exist_ok=True
        )

        report_path = (
            "reports/generated_reports/"
            "insights_report.txt"
        )

        with open(
            report_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "IPL ANALYTICS DASHBOARD REPORT\n"
            )

            file.write(
                "=============================\n\n"
            )

            file.write(
                f"Total Matches : {len(self.df)}\n\n"
            )

            if "winner" in self.df.columns:
                file.write(
                    f"Top Team : "
                    f"{self.df['winner'].mode()[0]}\n"
                )

        return report_path
