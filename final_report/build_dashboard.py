#!/usr/bin/env python3
"""
Phase 3: HTML Dashboard Generator (Fixed Version)
CSM500-2026 User-Community Intelligence Project
"""

import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

DATA_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = DATA_DIR / 'outputs'

print("=" * 80)
print("PHASE 3: HTML DASHBOARD GENERATION (V2 - FIXED)")
print("=" * 80)

print("\n[1] Loading indicators...")
user_ind = pd.read_csv(OUTPUT_DIR / 'user_indicators.csv')
proj_ind = pd.read_csv(OUTPUT_DIR / 'project_indicators.csv')

print(f"  ✓ Loaded {len(user_ind):,} user records")
print(f"  ✓ Loaded {len(proj_ind):,} project records")

print("\n[2] Creating visualizations...")

# Chart 1: User Usage Tier (Pie)
user_tier_counts = user_ind['usage_tier'].value_counts().reset_index()
user_tier_counts.columns = ['usage_tier', 'count']
fig1 = go.Figure(data=[go.Pie(
    labels=user_tier_counts['usage_tier'],
    values=user_tier_counts['count'],
    marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
)])
fig1.update_layout(
    title='<b>Users by Usage Tier</b>',
    height=400,
    font=dict(size=12),
    margin=dict(l=0, r=0, t=40, b=0)
)

# Chart 2: User Trend (Bar)
user_trend_counts = user_ind['usage_trend'].value_counts().reset_index()
user_trend_counts.columns = ['usage_trend', 'count']
user_trend_counts = user_trend_counts.sort_values('count', ascending=False)
fig2 = go.Figure(data=[go.Bar(
    x=user_trend_counts['usage_trend'],
    y=user_trend_counts['count'],
    marker=dict(color=user_trend_counts['count'], colorscale='Viridis')
)])
fig2.update_layout(
    title='<b>Users by Trend</b>',
    xaxis_title='Trend',
    yaxis_title='Number of Users',
    height=400,
    font=dict(size=12),
    margin=dict(l=50, r=0, t=40, b=50)
)

# Chart 3: Project Activity (Bar)
status_order = ['Inactive (No Usage)', 'Low Activity', 'Moderate Activity', 'High Activity']
proj_activity_counts = (
    proj_ind['activity_status']
    .value_counts()
    .reindex(status_order, fill_value=0)
    .reset_index()
)
proj_activity_counts.columns = ['activity_status', 'count']
colors = ['#FF6B6B', '#FFA500', '#FFD700', '#90EE90']
fig3 = go.Figure(data=[go.Bar(
    x=proj_activity_counts['activity_status'].tolist(),
    y=proj_activity_counts['count'].tolist(),
    marker=dict(color=colors)
)])
fig3.update_layout(
    title='<b>Projects by Activity Status</b>',
    xaxis_title='Activity Status',
    yaxis_title='Number of Projects',
    height=400,
    font=dict(size=12),
    margin=dict(l=50, r=0, t=40, b=50)
)

# Chart 4: Project Health (Pie)
proj_health_counts = proj_ind['health_category'].value_counts().reset_index()
proj_health_counts.columns = ['health_category', 'count']
health_colors = {
    'Excellent': '#00AA00',
    'Good': '#99DD00',
    'Fair': '#FFAA00',
    'Poor': '#DD0000'
}
colors_list = [health_colors.get(h, '#999999') for h in proj_health_counts['health_category']]
fig4 = go.Figure(data=[go.Pie(
    labels=proj_health_counts['health_category'],
    values=proj_health_counts['count'],
    marker=dict(colors=colors_list)
)])
fig4.update_layout(
    title='<b>Projects by Health Category</b>',
    height=400,
    font=dict(size=12),
    margin=dict(l=0, r=0, t=40, b=0)
)

# Chart 5: Top 15 Institutions (Bar)
inst_summary = user_ind.groupby('institution_name').agg({
    'total_usage_hours': 'sum'
}).reset_index().sort_values('total_usage_hours', ascending=False).head(15)

fig5 = go.Figure(data=[go.Bar(
    y=inst_summary['institution_name'],
    x=inst_summary['total_usage_hours'],
    orientation='h',
    marker=dict(color=inst_summary['total_usage_hours'], colorscale='Blues')
)])
fig5.update_layout(
    title='<b>Top 15 Institutions by CPU Usage</b>',
    xaxis_title='Total CPU Hours',
    yaxis_title='Institution',
    height=450,
    font=dict(size=11),
    margin=dict(l=250, r=0, t=40, b=50)
)

print("  ✓ Chart 1: User Usage Tier (Pie)")
print("  ✓ Chart 2: User Trend (Bar)")
print("  ✓ Chart 3: Project Activity (Bar)")
print("  ✓ Chart 4: Project Health (Pie)")
print("  ✓ Chart 5: Top Institutions (Bar)")

# Convert to HTML div
print("\n[3] Converting charts to HTML...")
chart1_html = fig1.to_html(full_html=False, include_plotlyjs=True, div_id='chart1')
chart2_html = fig2.to_html(full_html=False, include_plotlyjs=False, div_id='chart2')
chart3_html = fig3.to_html(full_html=False, include_plotlyjs=False, div_id='chart3')
chart4_html = fig4.to_html(full_html=False, include_plotlyjs=False, div_id='chart4')
chart5_html = fig5.to_html(full_html=False, include_plotlyjs=False, div_id='chart5')

total_users = len(user_ind)
total_projects = len(proj_ind)
total_cpu_used = proj_ind['cpu_used'].sum()
total_cpu_allocated = proj_ind['cpu_allocated'].sum()
overall_utilization = (total_cpu_used / total_cpu_allocated * 100) if total_cpu_allocated else 0
zero_usage_projects = (proj_ind['activity_status'] == 'Inactive (No Usage)').sum()
expiring_projects = (proj_ind['allocation_years_remaining'] < 0.25).sum()
dormant_users = (user_ind['usage_trend'] == 'Dormant').sum()
heavy_users = (user_ind['usage_tier'] == 'Heavy').sum()
projects_without_users = (proj_ind['user_count'] == 0).sum()

# Build final HTML
html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HPC User-Community Intelligence Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            background: white;
            padding: 40px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        h1 {
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #7f8c8d;
            font-size: 1.1em;
            margin-bottom: 30px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 25px;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        
        .metric-label {
            font-size: 0.9em;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        
        .metric-value {
            font-size: 2.2em;
            font-weight: bold;
        }
        
        .insights-box {
            background: #e8f4f8;
            border-left: 5px solid #3498db;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        
        .insights-box h3 {
            color: #2980b9;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .insights-box ul {
            list-style: none;
        }
        
        .insights-box li {
            padding: 10px 0;
            color: #2c3e50;
            font-size: 0.95em;
            border-bottom: 1px solid #d0e8f0;
        }
        
        .insights-box li:last-child {
            border-bottom: none;
        }
        
        .insights-box li:before {
            content: "→ ";
            color: #3498db;
            font-weight: bold;
            margin-right: 10px;
        }
        
        .section-title {
            font-size: 1.8em;
            color: white;
            margin: 40px 0 25px 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .charts-grid.full {
            grid-template-columns: 1fr;
        }
        
        .chart-box {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .chart-box h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        
        .plotly-div {
            width: 100%;
            height: 100%;
        }
        
        footer {
            background: rgba(255,255,255,0.9);
            padding: 25px;
            text-align: center;
            border-radius: 10px;
            color: #7f8c8d;
            margin-top: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        footer p {
            margin: 8px 0;
            font-size: 0.95em;
        }
        
        @media (max-width: 1200px) {
            .charts-grid {
                grid-template-columns: 1fr;
            }
            
            h1 {
                font-size: 2em;
            }
        }
        
        @media (max-width: 768px) {
            header {
                padding: 25px;
            }
            
            .metrics-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            h1 {
                font-size: 1.5em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎯 HPC User-Community Intelligence Dashboard</h1>
            <p class="subtitle">Comprehensive analysis of user engagement and programme health</p>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Total Users</div>
                    <div class="metric-value">{TOTAL_USERS:,}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Total Projects</div>
                    <div class="metric-value">{TOTAL_PROJECTS:,}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">CPU Usage</div>
                    <div class="metric-value">{TOTAL_CPU_USED:,.0f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Overall Utilization</div>
                    <div class="metric-value">{OVERALL_UTILIZATION:.1f}%</div>
                </div>
            </div>
        </header>
        
        <div class="insights-box">
            <h3>📊 Critical Findings & Governance Priorities</h3>
            <ul>
                <li><strong>{ZERO_USAGE_PROJECTS:,} projects ({ZERO_USAGE_PCT:.1f}%)</strong> have zero CPU usage and need governance review</li>
                <li><strong>{EXPIRING_PROJECTS:,} projects ({EXPIRING_PROJECTS_PCT:.1f}%)</strong> are within three months of allocation end</li>
                <li><strong>{DORMANT_USERS:,} users ({DORMANT_USERS_PCT:.1f}%)</strong> are dormant after earlier activity</li>
                <li><strong>{HEAVY_USERS:,} heavy users ({HEAVY_USERS_PCT:.1f}%)</strong> form a priority engagement segment</li>
                <li><strong>{PROJECTS_WITHOUT_USERS:,} projects ({PROJECTS_WITHOUT_USERS_PCT:.1f}%)</strong> have no mapped users</li>
            </ul>
        </div>
        
        <div class="section-title">👥 User Community Analysis</div>
        <div class="charts-grid">
            <div class="chart-box">
                <h3>Users by Usage Tier</h3>
                {CHART1}
            </div>
            <div class="chart-box">
                <h3>Users by Engagement Trend</h3>
                {CHART2}
            </div>
        </div>
        
        <div class="section-title">🔬 Projects & Programmes Analysis</div>
        <div class="charts-grid">
            <div class="chart-box">
                <h3>Projects by Activity Status</h3>
                {CHART3}
            </div>
            <div class="chart-box">
                <h3>Projects by Health Category</h3>
                {CHART4}
            </div>
        </div>
        
        <div class="section-title">🏛️ Top Contributors</div>
        <div class="charts-grid full">
            <div class="chart-box">
                <h3>Top 15 Institutions by CPU Usage</h3>
                {CHART5}
            </div>
        </div>
        
        <footer>
            <p><strong>CSM500-2026 HPC User-Community Intelligence Project</strong></p>
            <p>Data as of 14 May 2026 | Anonymized institutional analysis</p>
            <p>For governance and strategic planning purposes only</p>
        </footer>
    </div>
</body>
</html>"""

# Replace placeholders with actual charts
final_html = html_template.replace('{CHART1}', chart1_html)
final_html = final_html.replace('{CHART2}', chart2_html)
final_html = final_html.replace('{CHART3}', chart3_html)
final_html = final_html.replace('{CHART4}', chart4_html)
final_html = final_html.replace('{CHART5}', chart5_html)
dashboard_metrics = {
    'TOTAL_USERS': f'{total_users:,}',
    'TOTAL_PROJECTS': f'{total_projects:,}',
    'TOTAL_CPU_USED': f'{total_cpu_used:,.0f}',
    'OVERALL_UTILIZATION': f'{overall_utilization:.1f}',
    'ZERO_USAGE_PROJECTS': f'{zero_usage_projects:,}',
    'ZERO_USAGE_PCT': f'{zero_usage_projects / total_projects * 100 if total_projects else 0:.1f}',
    'EXPIRING_PROJECTS': f'{expiring_projects:,}',
    'EXPIRING_PROJECTS_PCT': f'{expiring_projects / total_projects * 100 if total_projects else 0:.1f}',
    'DORMANT_USERS': f'{dormant_users:,}',
    'DORMANT_USERS_PCT': f'{dormant_users / total_users * 100 if total_users else 0:.1f}',
    'HEAVY_USERS': f'{heavy_users:,}',
    'HEAVY_USERS_PCT': f'{heavy_users / total_users * 100 if total_users else 0:.1f}',
    'PROJECTS_WITHOUT_USERS': f'{projects_without_users:,}',
    'PROJECTS_WITHOUT_USERS_PCT': f'{projects_without_users / total_projects * 100 if total_projects else 0:.1f}',
}
for key, value in dashboard_metrics.items():
    final_html = final_html.replace(f'{{{key}}}', value)

# Write to file
dashboard_path = OUTPUT_DIR / 'dashboard.html'
with open(dashboard_path, 'w') as f:
    f.write(final_html)

print(f"\n✓ Dashboard created: {dashboard_path}")
print(f"  File size: {dashboard_path.stat().st_size / 1024:.1f} KB")
print(f"\n[4] View dashboard:")
print(f"  Command: open {dashboard_path}")
print(f"  Or open in web browser: file://{dashboard_path}")
print(f"\n✓ Phase 3 complete!")
