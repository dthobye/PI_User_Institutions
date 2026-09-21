# CSM500 HPC Intelligence Dashboard: How To Run

## Purpose

This project converts anonymized `users.csv` and `projects.csv` extracts into data-quality summaries, user and project indicators, a governance export, and an interactive Plotly dashboard. The Flask application provides a local interface to refresh the outputs and open the dashboard.

## Requirements

- Python 3.8 or later
- `flask`, `pandas`, `numpy`, and `plotly`
- The two input CSV files in this project directory

From the project directory, create and activate an isolated environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

If your institution provides a managed Python environment with the dependencies already installed, use that interpreter instead. On this machine, the Conda `python` interpreter is the working option.

## Run The Complete Pipeline

```bash
python 01_data_profiling.py
python 02_analytics_pipeline.py
python build_dashboard.py
python validate_project.py
```

The commands write refreshed files to `outputs/`. The validation command must end with `Validation passed` before the results are used.

## Run The Flask Application

```bash
python app.py
```

Open `http://127.0.0.1:5000/`. Select **Run Full Data Refresh** to run all three processing stages from the application, then select **Open Dashboard**. `GET /api/status` returns the current output availability and the last refresh result as JSON.

## Generated Outputs

- `data_quality_report.json`: dataset counts, utilisation, and data-quality flags.
- `user_indicators.csv`: user participation, trend, portfolio, and support-priority indicators.
- `project_indicators.csv`: utilisation, activity, user-count, health, and support-priority indicators.
- `critical_projects_for_support.csv`: projects requiring governance attention.
- `INDICATOR_CATALOGUE.md`: definitions and calculation rules.
- `dashboard.html`: self-contained interactive dashboard with five charts.

## Interpretation And Limits

The supplied extract is a historical snapshot evaluated against the fixed reference date `2026-05-14`, which makes the results reproducible. Flags identify records for human review; they must not be treated as automatic renewal, deallocation, or individual-performance decisions. Direct identifiers should not be published with analytical outputs.

## Troubleshooting

- `ModuleNotFoundError`: activate the virtual environment, or use the dependency-complete Python interpreter, then install `requirements.txt`.
- Missing output file: run the three pipeline commands in order.
- Dashboard looks stale: run `build_dashboard.py` after the analytics pipeline.
- Flask refresh fails: read the run log displayed on the home page; the first failed script and its output are shown there.