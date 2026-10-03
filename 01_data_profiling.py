#!/usr/bin/env python3
"""
Phase 1: Data Profiling and Quality Assessment
CSM500-2026 User-Community Intelligence Project

Objective:
- Profile users.csv and projects.csv for completeness, consistency, and usability
- Map user-project relationships
- Document data quality baseline
- Inform indicator design
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# Setup
DATA_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = DATA_DIR / 'outputs'
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("PHASE 1: DATA PROFILING AND QUALITY ASSESSMENT")
print("=" * 80)

# ==============================================================================
# 1. LOAD DATASETS
# ==============================================================================
print("\n[1] Loading datasets...")
try:
    users_df = pd.read_csv(DATA_DIR / 'users.csv')
    projects_df = pd.read_csv(DATA_DIR / 'projects.csv')
    print(f"✓ users.csv loaded: {users_df.shape[0]} rows × {users_df.shape[1]} columns")
    print(f"✓ projects.csv loaded: {projects_df.shape[0]} rows × {projects_df.shape[1]} columns")
except Exception as e:
    print(f"✗ Error loading data: {e}")
    exit(1)

# ==============================================================================
# 2. USERS DATASET PROFILING
# ==============================================================================
print("\n" + "=" * 80)
print("USERS DATASET PROFILING")
print("=" * 80)

print("\n[2a] Users - Data Types and Nullability")
users_info = pd.DataFrame({
    'Column': users_df.columns,
    'Type': users_df.dtypes.astype(str),
    'NonNull': users_df.count(),
    'Null': users_df.isnull().sum(),
    'NullPct': (users_df.isnull().sum() / len(users_df) * 100).round(1)
})
print(users_info.to_string(index=False))

print("\n[2b] Users - Key Statistics")
print(f"Total unique users: {users_df.shape[0]}")
print(f"Unique institutions: {users_df['institution_name'].nunique()}")
print(f"Unique disciplines: {users_df['discipline_name'].nunique()}")
print(f"Unique qualifications: {users_df['qualification'].nunique()}")
print(f"Gender distribution:\n{users_df['gender'].value_counts(dropna=False)}")
print(f"\nEthnicity distribution:\n{users_df['ethnicity'].value_counts(dropna=False)}")

print("\n[2c] Users - Usage Summary (CPU hours)")
usage_cols = [c for c in users_df.columns if 'usage' in c.lower()]
print(f"Total usage (all time): {users_df['total'].sum():,.0f} CPU hours")
print(f"Mean per user: {users_df['total'].mean():,.0f} CPU hours")
print(f"Median per user: {users_df['total'].median():,.0f} CPU hours")
print(f"Max single user: {users_df['total'].max():,.0f} CPU hours")
print(f"\nUsage distribution:")
print(f"  Users with 0 usage: {(users_df['total'] == 0).sum()}")
print(f"  Users with < 1000 CPU hours: {(users_df['total'] < 1000).sum()}")
print(f"  Users with >= 1000 CPU hours: {(users_df['total'] >= 1000).sum()}")

print("\n[2d] Users - Project Portfolio")
users_df['project_count'] = users_df['project_shortnames'].fillna('').apply(
    lambda x: len([p.strip() for p in str(x).split(',') if p.strip()])
)
print(f"Users with project assignments: {(users_df['project_count'] > 0).sum()}")
print(f"Users without project assignments: {(users_df['project_count'] == 0).sum()}")
print(f"Project portfolio size distribution:")
print(users_df['project_count'].value_counts().sort_index().head(10))

# ==============================================================================
# 3. PROJECTS DATASET PROFILING
# ==============================================================================
print("\n" + "=" * 80)
print("PROJECTS DATASET PROFILING")
print("=" * 80)

print("\n[3a] Projects - Data Types and Nullability")
projects_info = pd.DataFrame({
    'Column': projects_df.columns,
    'Type': projects_df.dtypes.astype(str),
    'NonNull': projects_df.count(),
    'Null': projects_df.isnull().sum(),
    'NullPct': (projects_df.isnull().sum() / len(projects_df) * 100).round(1)
})
print(projects_info.to_string(index=False))

print("\n[3b] Projects - Key Statistics")
print(f"Total projects: {projects_df.shape[0]}")
print(f"Duplicate project keys: {projects_df.duplicated(['id', 'shortname']).sum()}")
print(f"Unique disciplines: {projects_df['discipline_name'].nunique()}")
print(f"Unique institutions: {projects_df['institution_name'].nunique()}")
print(f"\nProject status distribution:")
print(projects_df['status'].value_counts())

print("\n[3c] Projects - Allocation vs. Usage")
projects_df['utilization_rate'] = (
    projects_df['used_hours'] / projects_df['cpu_hours'] * 100
).round(1)
print(f"Total CPU hours allocated: {projects_df['cpu_hours'].sum():,.0f}")
print(f"Total CPU hours used: {projects_df['used_hours'].sum():,.0f}")
print(f"Overall utilization: {(projects_df['used_hours'].sum() / projects_df['cpu_hours'].sum() * 100):.1f}%")
print(f"\nUtilization rate statistics:")
print(f"  Mean: {projects_df['utilization_rate'].mean():.1f}%")
print(f"  Median: {projects_df['utilization_rate'].median():.1f}%")
print(f"  Min: {projects_df['utilization_rate'].min():.1f}%")
print(f"  Max: {projects_df['utilization_rate'].max():.1f}%")
print(f"\nProjects by utilization:")
print(f"  >90% utilized: {(projects_df['utilization_rate'] > 90).sum()}")
print(f"  50-90% utilized: {((projects_df['utilization_rate'] >= 50) & (projects_df['utilization_rate'] <= 90)).sum()}")
print(f"  <50% utilized: {(projects_df['utilization_rate'] < 50).sum()}")
print(f"  0% utilized (no usage): {(projects_df['used_hours'] == 0).sum()}")

print("\n[3d] Projects - Timeline")
projects_df['allo_start'] = pd.to_datetime(projects_df['allo_start'], errors='coerce')
projects_df['allo_end'] = pd.to_datetime(projects_df['allo_end'], errors='coerce')
print(f"Earliest allocation start: {projects_df['allo_start'].min()}")
print(f"Latest allocation end: {projects_df['allo_end'].max()}")

# ==============================================================================
# 4. USER-PROJECT MAPPING
# ==============================================================================
print("\n" + "=" * 80)
print("USER-PROJECT MAPPING")
print("=" * 80)

print("\n[4a] Parsing User-Project Relationships...")
user_project_pairs = []
for idx, row in users_df.iterrows():
    user_id = row['user_id']
    projects = row['project_shortnames']
    if pd.notna(projects) and str(projects).strip():
        # Split on comma and strip whitespace
        project_list = [p.strip() for p in str(projects).split(',') if p.strip()]
        for project in project_list:
            user_project_pairs.append({'user_id': user_id, 'project_shortname': project})

user_project_df = pd.DataFrame(user_project_pairs)
print(f"Total user-project relationships: {len(user_project_df)}")
print(f"Unique project shortnames referenced: {user_project_df['project_shortname'].nunique()}")

# Cross-reference with projects dataset
projects_set = set(projects_df['shortname'].unique())
user_refs = set(user_project_df['project_shortname'].unique())
unmapped = user_refs - projects_set
print(f"Unmapped project references (in users but not in projects): {len(unmapped)}")
if unmapped and len(unmapped) <= 20:
    print(f"  Examples: {list(unmapped)[:10]}")

print("\n[4b] Project Reference Coverage")
print(f"Projects with user references: {user_project_df['project_shortname'].nunique()}")
print(f"Projects without user references: {len(projects_set) - user_project_df['project_shortname'].nunique()}")

# ==============================================================================
# 5. DATA QUALITY SUMMARY
# ==============================================================================
print("\n" + "=" * 80)
print("DATA QUALITY SUMMARY")
print("=" * 80)

quality_flags = {
    'Missing Data': {
        'users_no_institution': (users_df['institution_name'].isnull().sum(), users_df.shape[0]),
        'users_no_discipline': (users_df['discipline_name'].isnull().sum(), users_df.shape[0]),
        'projects_no_staff': (projects_df['staff_id'].isnull().sum(), projects_df.shape[0]),
    },
    'Data Consistency': {
        'duplicate_project_keys': (projects_df.duplicated(['id', 'shortname']).sum(), projects_df.shape[0]),
        'zero_allocation_projects': ((projects_df['cpu_hours'] == 0).sum(), projects_df.shape[0]),
        'unmapped_user_projects': (len(unmapped), len(user_refs)),
    },
    'Activity Status': {
        'inactive_users': ((users_df['total'] == 0).sum(), users_df.shape[0]),
        'inactive_projects': ((projects_df['used_hours'] == 0).sum(), projects_df.shape[0]),
    }
}

for category, flags in quality_flags.items():
    print(f"\n{category}:")
    for flag_name, (count, total) in flags.items():
        pct = (count / total * 100) if total > 0 else 0
        print(f"  {flag_name}: {count} / {total} ({pct:.1f}%)")

# ==============================================================================
# 6. EXPORT SUMMARY PROFILES
# ==============================================================================
print("\n" + "=" * 80)
print("EXPORTING SUMMARY PROFILES")
print("=" * 80)

# Users summary
users_summary = users_df.groupby('institution_name').agg({
    'user_id': 'count',
    'total': ['sum', 'mean', 'median'],
    'project_count': 'mean'
}).round(1)
users_summary.columns = ['user_count', 'total_usage', 'mean_usage', 'median_usage', 'avg_projects']
users_summary = users_summary.sort_values('total_usage', ascending=False)
users_summary.to_csv(OUTPUT_DIR / 'users_by_institution.csv')
print(f"✓ Exported: users_by_institution.csv")

# Discipline summary
discipline_summary = users_df.groupby('discipline_name').agg({
    'user_id': 'count',
    'total': ['sum', 'mean'],
    'project_count': 'mean'
}).round(1)
discipline_summary.columns = ['user_count', 'total_usage', 'mean_usage', 'avg_projects']
discipline_summary = discipline_summary.sort_values('total_usage', ascending=False)
discipline_summary.to_csv(OUTPUT_DIR / 'users_by_discipline.csv')
print(f"✓ Exported: users_by_discipline.csv")

# Projects summary
projects_summary = projects_df.groupby('status').agg({
    'id': 'count',
    'cpu_hours': 'sum',
    'used_hours': 'sum',
    'utilization_rate': 'mean'
}).round(1)
projects_summary.columns = ['project_count', 'total_allocated', 'total_used', 'mean_utilization']
projects_summary.to_csv(OUTPUT_DIR / 'projects_by_status.csv')
print(f"✓ Exported: projects_by_status.csv")

# Utilization profile
util_bins = [0, 10, 25, 50, 75, 90, 100, 500]
util_labels = ['0-10%', '10-25%', '25-50%', '50-75%', '75-90%', '90-100%', '>100%']
projects_df['utilization_band'] = pd.cut(projects_df['utilization_rate'], bins=util_bins, labels=util_labels, right=False)
util_profile = projects_df['utilization_band'].value_counts().sort_index()
util_profile.to_csv(OUTPUT_DIR / 'projects_utilization_bands.csv')
print(f"✓ Exported: projects_utilization_bands.csv")

# Data quality report
quality_report = {
    'profiling_date': pd.Timestamp.now().isoformat(),
    'users_count': int(users_df.shape[0]),
    'projects_count': int(projects_df.shape[0]),
    'user_project_relationships': int(len(user_project_df)),
    'total_cpu_allocated': float(projects_df['cpu_hours'].sum()),
    'total_cpu_used': float(projects_df['used_hours'].sum()),
    'overall_utilization_pct': round(projects_df['used_hours'].sum() / projects_df['cpu_hours'].sum() * 100, 1),
    'quality_flags': {k: {kk: int(vv[0]) if isinstance(vv, tuple) else vv for kk, vv in v.items()} for k, v in quality_flags.items()}
}

with open(OUTPUT_DIR / 'data_quality_report.json', 'w') as f:
    json.dump(quality_report, f, indent=2)
print(f"✓ Exported: data_quality_report.json")

print("\n" + "=" * 80)
print("PHASE 1 COMPLETE")
print("=" * 80)
print(f"\nNext steps:")
print(f"  1. Review summary profiles in {OUTPUT_DIR}/")
print(f"  2. Design core indicators (Phase 2)")
print(f"  3. Build analytics pipeline")
