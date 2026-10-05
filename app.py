from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# Flask components used to build the web interface and API endpoints.
from flask import Flask, jsonify, redirect, render_template_string, request, send_from_directory, url_for

# Define application directories.
BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"

app = Flask(__name__)

LAST_RUN = {
    "ok": None,
    "steps": [],
}

# HTML template for the web interface.
# Provides controls for running the analytics pipeline,
# viewing summary metrics, and opening the dashboard.
INDEX_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>HPC Intelligence Flask App</title>
  <style>
    body { font-family: Helvetica, Arial, sans-serif; margin: 24px; background: #f4f7fb; color: #111827; }
    h1 { margin-bottom: 8px; }
    .muted { color: #4b5563; margin-bottom: 20px; }
    .actions { display: flex; gap: 12px; margin-bottom: 18px; flex-wrap: wrap; }
    button, a.btn {
      border: 0;
      padding: 10px 14px;
      border-radius: 8px;
      text-decoration: none;
      font-size: 14px;
      cursor: pointer;
      background: #0f766e;
      color: #fff;
      display: inline-block;
    }
    .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-bottom: 18px; }
    .card { background: #fff; border-radius: 10px; padding: 14px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08); }
    .status-ok { color: #166534; font-weight: 700; }
    .status-bad { color: #991b1b; font-weight: 700; }
    pre {
      background: #111827;
      color: #e5e7eb;
      border-radius: 8px;
      padding: 10px;
      overflow-x: auto;
      max-height: 220px;
      white-space: pre-wrap;
    }
  </style>
</head>
<body>
  <h1>HPC User-Community Intelligence App</h1>
  <p class="muted">Simple Flask client-server UI for running analytics and viewing the dashboard.</p>

  <div class="actions">
    <form method="post" action="{{ url_for('run_refresh') }}">
      <button type="submit">Run Full Data Refresh</button>
    </form>
    <a class="btn" href="{{ url_for('dashboard') }}" target="_blank" rel="noopener">Open Dashboard</a>
  </div>

  <div class="cards">
    <div class="card">
      <h3>Users</h3>
      <div>{{ metrics.users }}</div>
    </div>
    <div class="card">
      <h3>Projects</h3>
      <div>{{ metrics.projects }}</div>
    </div>
    <div class="card">
      <h3>Dashboard</h3>
      <div>{{ "Available" if metrics.dashboard_exists else "Not generated" }}</div>
    </div>
  </div>

  {% if last_run.ok is not none %}
    <h2>Last Run</h2>
    <p class="{{ 'status-ok' if last_run.ok else 'status-bad' }}">
      {{ 'Success' if last_run.ok else 'Failed' }}
    </p>
    {% for step in last_run.steps %}
      <h3>{{ step.script }}</h3>
      <pre>{{ step.output }}</pre>
    {% endfor %}
  {% endif %}
</body>
</html>
"""


def count_rows(csv_path: Path) -> int | None:
    if not csv_path.exists():
        return None

    with csv_path.open("r", encoding="utf-8") as fh:
        # Subtract header row for row count.
        return max(sum(1 for _ in fh) - 1, 0)


def collect_metrics() -> dict[str, object]:
    return {
        "users": count_rows(OUTPUTS_DIR / "user_indicators.csv") or "N/A",
        "projects": count_rows(OUTPUTS_DIR / "project_indicators.csv") or "N/A",
        "dashboard_exists": (OUTPUTS_DIR / "dashboard.html").exists(),
    }


def run_pipeline_scripts() -> dict[str, object]:
    scripts = [
        "01_data_profiling.py",
        "02_analytics_pipeline.py",
        "build_dashboard.py",
    ]

    steps: list[dict[str, str]] = []
    ok = True


    for script in scripts:
        # Execute each pipeline stage using the current Python interpreter.
        command = [sys.executable, script]
        result = subprocess.run(
            command,
            cwd=BASE_DIR,
            text=True,
            capture_output=True,
            check=False,
        )
        output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
        steps.append({"script": script, "output": output.strip() or "No output."})

        if result.returncode != 0:
            ok = False
            break

    return {"ok": ok, "steps": steps}


@app.get("/")
def home() -> str:
    return render_template_string(INDEX_TEMPLATE, metrics=collect_metrics(), last_run=LAST_RUN)


@app.post("/run-refresh")
def run_refresh():
    LAST_RUN.update(run_pipeline_scripts())
    return redirect(url_for("home"))


@app.get("/dashboard")
def dashboard():
    return send_from_directory(OUTPUTS_DIR, "dashboard.html")


@app.get("/api/status")
def api_status():
    return jsonify(
        {
            "metrics": collect_metrics(),
            "last_run_ok": LAST_RUN["ok"],
        }
    )


if __name__ == "__main__":
    # Start the Flask development server.
    app.run(debug=True)