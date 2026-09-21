# CSM500 Project Instructions

## What Is Included

- `01_data_profiling.py`: profiles input completeness, allocation usage, and user-project mapping.
- `02_analytics_pipeline.py`: computes reproducible user and project governance indicators.
- `build_dashboard.py`: builds an offline-capable HTML dashboard from the indicator files.
- `app.py`: Flask interface with home, refresh, dashboard, and JSON status routes.
- `validate_project.py`: automated post-run verification.

## Standard Operating Procedure

1. Place the approved anonymized `users.csv` and `projects.csv` files in the project root.
2. Install the dependencies listed in `requirements.txt`.
3. Run the pipeline and `python validate_project.py` as described in [HOW_TO.md](HOW_TO.md).
4. Start the application with `python app.py` for the local user interface.
5. Retain the generated `outputs/` folder with the source extract version and run date for auditability.

## Flask Routes

| Method | Route | Function |
|---|---|---|
| `GET` | `/` | Displays the local control page and last refresh log. |
| `POST` | `/run-refresh` | Runs profiling, indicator generation, and dashboard creation. |
| `GET` | `/dashboard` | Serves the current dashboard HTML file. |
| `GET` | `/api/status` | Returns output metrics and the last refresh result as JSON. |

## Data Protection

Use only anonymized extracts. Do not add names, email addresses, or other direct identifiers to the dashboard or exported governance reports. Limit access to source files and use indicators to support human judgement, not automated punitive decisions.

## Evidence For The Final Report

The final report is [Assessment3_CSM500_Submission.md](Assessment3_CSM500_Submission.md). Its technical claims should be supported by the scripts, the generated outputs, and a successful `validate_project.py` run. The professor feedback requiring a substantial Flask client-server artefact is traced in [PROFESSOR_FEEDBACK_CHANGELOG.md](PROFESSOR_FEEDBACK_CHANGELOG.md).