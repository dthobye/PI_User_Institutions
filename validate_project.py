#!/usr/bin/env python3
"""
PHASE 4: OUTPUT VALIDATION
 
This script verifies that all project deliverables generated during the previous
phases exist, contain valid data, and meet expected quality criteria.
 
This validation step acts as a quality assurance control to ensure
that the analytical pipeline has executed successfully and that
dashboard outputs are ready for reporting and assessment.
"""

from pathlib import Path
import pandas as pd

# Path to the directory containing this script
# OUTPUT_DIR contains all artefacts generated in previous phases.
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"

# Simplifies assertions by raising a clear error message whenever
# a validation rule fails.
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

# Ensure all expected dashboard visualisations exist and that
# template placeholders have been successfully replaced with
# actual metric values.
dashboard = (OUTPUT_DIR / "dashboard.html").read_text(encoding="utf-8")
for chart_number in range(1, 6):
    require(f'id="chart{chart_number}"' in dashboard, f"Dashboard chart {chart_number} is missing")
require("{TOTAL_USERS}" not in dashboard, "Dashboard metric placeholders remain")

print("Validation passed")
print(f"Users: {len(users):,}; projects: {len(projects):,}; dashboard charts: 5")
