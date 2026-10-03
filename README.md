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
Input datasets: users.csv and projects.csv

Running the Data Pipeline
Execute the processing steps in the following order:
- python 01_data_profiling.py
- python 02_analytics_pipeline.py
- python build_dashboard.py
- python validate_project.py

- Output Files
Insert Table

Important Notes:
- The analysis is based on a historical snapshot with a fixed reference date of 2026-05-14.
- Results are intended to support governance and operational review.
- Generated flags should not be used as automatic decisions for resource allocation, renewals, or personnel evaluation.
- Personally identifiable information should not be published with analytical outputs


