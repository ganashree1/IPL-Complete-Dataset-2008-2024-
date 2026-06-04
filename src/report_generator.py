import os

os.makedirs("reports/generated_reports", exist_ok=True)

report_path = "reports/generated_reports/insights_report.txt"

with open(report_path, "w", encoding="utf-8") as file:
    file.write("""
IPL ANALYTICS DASHBOARD REPORT
=============================

Generated Date : 2026-06-04

This report contains Team Analysis,
Player Analysis, Venue Analysis,
Toss Analysis and Match Insights.
""")

print("Report Generated Successfully")
