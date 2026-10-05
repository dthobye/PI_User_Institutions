# PI_User_Institutions

Overview
The HPC Intelligence Dashboard converts anonymized users.csv and projects.csv extracts into:
- Data quality summaries
- User and project performance indicators
- Governance reports
- Interactive Plotly dashboards

The application includes a Flask-based web interface for refreshing data and viewing dashboard outputs.

Features
- Automated data profiling and validation
- User participation and trend analysis
- Project utilisation and health indicators
- Governance reporting for critical projects
- Interactive dashboard visualisations
- Flask web interface for data refresh and dashboard access

Requirements
- Python 3.8 or later
- Flask
- Pandas
- NumPy
- Plotly

Project Workflow
  users.csv + projects.csv
            │
            ▼
01_data_profiling.py
            │
            ▼
02_analytics_pipeline.py
            │
            ▼
build_dashboard.py
            │
            ▼
dashboard.html
            │
            ▼
app.py (Flask Web Interface)

Output Files
| File | Description |
|--------|-------------|
| data_quality_report.json | Summary of data profiling results, completeness checks, and quality metrics. |
| user_indicators.csv | User-level KPIs including participation, usage trends, and activity classifications. |
| project_indicators.csv | Project-level KPIs including utilisation, health scores, and lifecycle indicators. |
| critical_projects_for_support.csv | Governance report identifying projects that may require intervention or support. |
| INDICATOR_CATALOGUE.md | Data dictionary describing calculated indicators and metrics. |
| dashboard.html | Interactive Plotly dashboard containing visualisations and KPI summaries. |

Flask Web Interface 
The Flask application provides a lightweight web-based interface that allows users to:
- Execute a full analytics refresh from the browser.
- Monitor pipeline execution status.
- View generated user and project metrics.
- Access the interactive dashboard.
- Retrieve application status through a REST API endpoint.

Important Notes:
- The analysis is based on a historical snapshot with a fixed reference date of 2026-05-14.
- Results are intended to support governance and operational review.
- Generated flags should not be used as automatic decisions for resource allocation, renewals, or personnel evaluation.
- Personally identifiable information should not be published with analytical outputs


