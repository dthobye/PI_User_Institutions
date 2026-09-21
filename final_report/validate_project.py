#!/usr/bin/env python3
"""Validate the generated CSM500 project outputs."""

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


required_files = [
    "data_quality_report.json",
    "user_indicators.csv",
    "project_indicators.csv",
    "critical_projects_for_support.csv",
    "INDICATOR_CATALOGUE.md",
    "dashboard.html",
]
for filename in required_files:
    require((OUTPUT_DIR / filename).is_file(), f"Missing output: {filename}")

users = pd.read_csv(OUTPUT_DIR / "user_indicators.csv")
projects = pd.read_csv(OUTPUT_DIR / "project_indicators.csv")

require(len(users) == 4221, f"Expected 4,221 user indicators, found {len(users):,}")
require(len(projects) == 1016, f"Expected 1,016 deduplicated project indicators, found {len(projects):,}")
require(users["user_id"].is_unique, "User IDs are not unique")
require(projects["shortname"].is_unique, "Project shortnames are not unique")
require(users["usage_tier"].notna().all(), "Missing user usage tiers")
require(users["usage_trend"].notna().all(), "Missing user usage trends")
require(projects["health_score"].between(0, 100).all(), "Health scores fall outside 0-100")
require((projects["utilization_rate_pct"] >= 0).all(), "Negative utilization detected")

dashboard = (OUTPUT_DIR / "dashboard.html").read_text(encoding="utf-8")
for chart_number in range(1, 6):
    require(f'id="chart{chart_number}"' in dashboard, f"Dashboard chart {chart_number} is missing")
require("{TOTAL_USERS}" not in dashboard, "Dashboard metric placeholders remain")

print("Validation passed")
print(f"Users: {len(users):,}; projects: {len(projects):,}; dashboard charts: 5")