#!/usr/bin/env python3
"""
Phase 2: Analytics Pipeline and Indicator Generation

This script transforms profiled CHPC user and project data into
actionable analytics indicators that support operational reporting,
decision making, and dashboard visualisation.

Outputs generated in this phase form the analytical foundation for
Phase 3 dashboard development.
"""

import pandas as pd
from pathlib import Path

# Path to the directory containing this script
DATA_DIR = Path(__file__).resolve().parent

# Create destination directory for outputs
OUTPUT_DIR = DATA_DIR / 'outputs'
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("PHASE 2: ANALYTICS PIPELINE AND INDICATOR GENERATION")
print("=" * 80)

# Load the profiled datasets produced during Phase 1.
print("\n[1] Loading and preparing data...")
users_df = pd.read_csv(DATA_DIR / 'users.csv')
projects_df = pd.read_csv(DATA_DIR / 'projects.csv')

# Remove duplicate project allocation records to prevent
# over-counting during indicator calculations.
duplicate_project_rows = projects_df.duplicated(['id', 'shortname']).sum()
if duplicate_project_rows:
    projects_df = projects_df.drop_duplicates(['id', 'shortname']).copy()
    print(f"Removed {duplicate_project_rows} repeated project allocation row(s).")

# Parse dates
projects_df['allo_start'] = pd.to_datetime(projects_df['allo_start'], errors='coerce')
projects_df['allo_end'] = pd.to_datetime(projects_df['allo_end'], errors='coerce')
projects_df['data_created'] = pd.to_datetime(projects_df['data_created'], errors='coerce')

current_date = pd.Timestamp('2026-05-14')  # Today's date in the scenario
print(f"Reference date: {current_date.date()}")

print("\n" + "=" * 80)
print("COMPUTING USER INDICATORS")
print("=" * 80)

user_indicators = users_df[['user_id', 'user_username', 'gender', 'ethnicity', 
                             'qualification', 'institution_name', 'discipline_name']].copy()

# Usage tier classification
def classify_usage_tier(total_hours):
    """Classify user by CPU usage"""
    if total_hours == 0:
        return 'Inactive'
    elif total_hours < 1_000:
        return 'Minimal'
    elif total_hours < 100_000:
        return 'Light'
    elif total_hours < 1_000_000:
        return 'Medium'
    else:
        return 'Heavy'

user_indicators['usage_tier'] = users_df['total'].apply(classify_usage_tier)
user_indicators['total_usage_hours'] = users_df['total']
user_indicators['usage_7day'] = users_df['usage_7_day']

# Calculate usage trend (recent vs historical)
user_indicators['usage_2025_2026'] = users_df['usage_2025_2026']
user_indicators['usage_2024_2025'] = users_df['usage_2024_2025']
user_indicators['usage_2023_2024'] = users_df['usage_2023_2024']
user_indicators['usage_historical_2016_2023'] = (
    users_df['usage_2016_2017'] + users_df['usage_2017_2018'] + users_df['usage_2018_2019'] +
    users_df['usage_2019_2020'] + users_df['usage_2020_2021'] + users_df['usage_2021_2022'] +
    users_df['usage_2022_2023']
)

# Build historical and recent usage metrics to identify
# behavioural trends within the CHPC user community.
def classify_trend(recent, historical):
    """Classify usage trend"""
    if recent == 0 and historical == 0:
        return 'Never Active'
    if recent == 0 and historical > 0:
        return 'Dormant'
    if historical == 0:
        return 'New'
    growth_rate = (recent - historical) / historical
    if growth_rate > 0.5:
        return 'Growing'
    elif growth_rate > -0.2:
        return 'Stable'
    else:
        return 'Declining'

user_indicators['usage_trend'] = user_indicators.apply(
    lambda r: classify_trend(r['usage_2025_2026'], r['usage_historical_2016_2023']),
    axis=1
)

# Project portfolio
users_df['project_count'] = users_df['project_shortnames'].fillna('').apply(
    lambda x: len([p.strip() for p in str(x).split(',') if p.strip()])
)
user_indicators['project_count'] = users_df['project_count']

def classify_portfolio(count):
    if count == 0:
        return 'Unallocated'
    elif count == 1:
        return 'Single Project'
    elif count <= 3:
        return 'Multi-Project (2-3)'
    else:
        return 'Multi-Project (4+)'

user_indicators['portfolio_type'] = users_df['project_count'].apply(classify_portfolio)

# Identify users that may require onboarding,
# engagement, training or support interventions.
def flag_user_support_priority(row):
    """Flag users requiring support or attention"""
    flags = []
    if row['usage_tier'] == 'Inactive':
        flags.append('Inactive')
    elif row['usage_tier'] == 'Minimal' and row['usage_trend'] == 'Dormant':
        flags.append('Dormant User')
    if row['project_count'] == 0:
        flags.append('Unallocated')
    if row['usage_7day'] > 0 and row['usage_2025_2026'] == 0 and row['usage_7day'] > row['usage_2025_2026']:
        flags.append('Recently Active')
    return '; '.join(flags) if flags else 'None'

user_indicators['support_priority'] = user_indicators.apply(flag_user_support_priority, axis=1)

print(f"✓ Generated {len(user_indicators)} user indicators")
print(f"\nUser Usage Tiers:")
print(user_indicators['usage_tier'].value_counts().sort_index())
print(f"\nUser Trends:")
print(user_indicators['usage_trend'].value_counts())
print(f"\nUser Portfolio Types:")
print(user_indicators['portfolio_type'].value_counts())

user_indicators.to_csv(OUTPUT_DIR / 'user_indicators.csv', index=False)
print(f"✓ Exported: user_indicators.csv")

print("\n" + "=" * 80)
print("COMPUTING PROJECT INDICATORS")
print("=" * 80)

project_indicators = projects_df[['id', 'shortname', 'fullname', 'status', 'discipline_name',
                                   'institution_name', 'person_gender', 'person_race',
                                   'cpu_hours', 'used_hours', 'data_created', 'allo_start', 'allo_end']].copy()

# Utilization metrics
project_indicators['cpu_allocated'] = projects_df['cpu_hours'].values
project_indicators['cpu_used'] = projects_df['used_hours'].values
project_indicators['utilization_rate_pct'] = (
    (projects_df['used_hours'] / projects_df['cpu_hours'] * 100)
    .round(1)
    .fillna(0)
)

# Utilization band
util_bins = [0, 10, 25, 50, 75, 90, 100, 500]
util_labels = ['0-10%', '10-25%', '25-50%', '50-75%', '75-90%', '90-100%', '>100%']
project_indicators['utilization_band'] = pd.cut(
    project_indicators['utilization_rate_pct'],
    bins=util_bins,
    labels=util_labels,
    right=False
)

# Project age and allocation metrics
project_indicators['project_age_days'] = (current_date - projects_df['data_created']).dt.days
project_indicators['allocation_start'] = projects_df['allo_start']
project_indicators['allocation_end'] = projects_df['allo_end']
project_indicators['allocation_years_remaining'] = (
    (projects_df['allo_end'] - current_date).dt.days / 365
).round(1)

# Activity status
def classify_project_activity(cpu_used, util_rate):
    if cpu_used == 0:
        return 'Inactive (No Usage)'
    elif util_rate < 10:
        return 'Low Activity'
    elif util_rate < 50:
        return 'Moderate Activity'
    else:
        return 'High Activity'

project_indicators['activity_status'] = project_indicators.apply(
    lambda r: classify_project_activity(r['cpu_used'], r['utilization_rate_pct']),
    axis=1
)

# User count
project_shortnames = set(projects_df['shortname'].unique())
user_projects = {}
for idx, row in users_df.iterrows():
    projects = row['project_shortnames']
    if pd.notna(projects) and str(projects).strip():
        project_list = [p.strip() for p in str(projects).split(',') if p.strip()]
        for proj in project_list:
            if proj not in user_projects:
                user_projects[proj] = 0
            user_projects[proj] += 1

project_indicators['user_count'] = projects_df['shortname'].map(
    lambda x: user_projects.get(x, 0)
)

# Support priority flags
def flag_project_support_priority(row):
    """Flag projects requiring governance or support attention"""
    flags = []
    
    if row['cpu_used'] == 0:
        flags.append('No Usage')
    elif row['utilization_rate_pct'] < 5:
        flags.append('Critical Underutilization')
    elif row['utilization_rate_pct'] < 25:
        flags.append('Significant Underutilization')
    
    if row['allocation_years_remaining'] < 0.25:  # Less than 3 months
        flags.append('Expiring Soon')
    
    if row['user_count'] == 0:
        flags.append('No Users Assigned')
    elif row['user_count'] == 1 and row['cpu_allocated'] > 100_000:
        flags.append('Single User - Large Allocation')
    
    # High-value underutilized
    if row['cpu_allocated'] > 500_000 and row['utilization_rate_pct'] < 20:
        flags.append('Large Allocation Underutilized')
    
    return '; '.join(flags) if flags else 'None'

project_indicators['support_priority'] = project_indicators.apply(
    flag_project_support_priority, axis=1
)

# Create a composite health indicator that combines
# utilisation, engagement and allocation status into a
# single governance metric ranging from 0 to 100.
def compute_health_score(row):
    """
    Health score integrating utilization, user engagement, and activity.
    Higher is better.
    """
    score = 50  # Baseline
    
    # Utilization component (0-40 points)
    util_pct = row['utilization_rate_pct']
    if util_pct >= 80:
        score += 40
    elif util_pct >= 50:
        score += 30
    elif util_pct >= 20:
        score += 15
    elif util_pct > 0:
        score += 5
    else:
        score -= 30  # Penalty for zero usage
    
    # User engagement component (0-30 points)
    if row['user_count'] >= 10:
        score += 30
    elif row['user_count'] >= 5:
        score += 20
    elif row['user_count'] >= 2:
        score += 10
    elif row['user_count'] == 1:
        score += 5
    else:
        score -= 20  # Penalty for no users
    
    # Status component (0-20 points)
    if row['allocation_years_remaining'] > 1:
        score += 10
    if row['activity_status'] == 'High Activity':
        score += 10
    
    return max(0, min(100, score))  

project_indicators['health_score'] = project_indicators.apply(
    compute_health_score, axis=1
)

# Convert numeric health scores into qualitative categories.
def categorize_health(score):
    if score >= 75:
        return 'Excellent'
    elif score >= 60:
        return 'Good'
    elif score >= 40:
        return 'Fair'
    else:
        return 'Poor'

project_indicators['health_category'] = project_indicators['health_score'].apply(categorize_health)

print(f"✓ Generated {len(project_indicators)} project indicators")
print(f"\nProject Activity Status:")
print(project_indicators['activity_status'].value_counts())
print(f"\nProject Health Categories:")
print(project_indicators['health_category'].value_counts())
print(f"\nProject Support Priorities:")
priority_summary = project_indicators['support_priority'].apply(
    lambda x: [p.strip() for p in x.split(';')]
).explode().value_counts().head(10)
print(priority_summary)

project_indicators.to_csv(OUTPUT_DIR / 'project_indicators.csv', index=False)
print(f"✓ Exported: project_indicators.csv")

print("\n" + "=" * 80)
print("GENERATING SUMMARY DASHBOARDS")
print("=" * 80)

# User summary by institution
user_summary_inst = user_indicators.groupby('institution_name').agg({
    'user_id': 'count',
    'total_usage_hours': ['sum', 'mean'],
    'usage_tier': lambda x: (x == 'Heavy').sum(),
    'usage_trend': lambda x: (x == 'Growing').sum(),
    'support_priority': lambda x: (x != 'None').sum()
}).round(0)
user_summary_inst.columns = ['user_count', 'total_usage', 'avg_usage', 'heavy_users', 'growing_users', 'needs_support']
user_summary_inst = user_summary_inst.sort_values('total_usage', ascending=False)
user_summary_inst.to_csv(OUTPUT_DIR / 'user_summary_by_institution.csv')
print(f"✓ Exported: user_summary_by_institution.csv")

# Project summary by discipline
project_summary_disc = project_indicators.groupby('discipline_name').agg({
    'id': 'count',
    'cpu_allocated': 'sum',
    'cpu_used': 'sum',
    'health_score': 'mean',
    'support_priority': lambda x: (x != 'None').sum()
}).round(1)
project_summary_disc.columns = ['project_count', 'total_allocated', 'total_used', 'avg_health', 'support_needed']
project_summary_disc['utilization_pct'] = (
    (project_summary_disc['total_used'] / project_summary_disc['total_allocated'] * 100)
    .round(1)
)
project_summary_disc = project_summary_disc.sort_values('total_allocated', ascending=False)
project_summary_disc.to_csv(OUTPUT_DIR / 'project_summary_by_discipline.csv')
print(f"✓ Exported: project_summary_by_discipline.csv")

# Critical support priorities 
critical_projects = project_indicators[
    project_indicators['support_priority'] != 'None'
].sort_values('health_score').head(20)
critical_projects[['shortname', 'fullname', 'health_score', 'health_category', 
                    'utilization_rate_pct', 'user_count', 'support_priority']].to_csv(
    OUTPUT_DIR / 'critical_projects_for_support.csv', index=False
)
print(f"✓ Exported: critical_projects_for_support.csv")
print("\n" + "=" * 80)
print("GENERATING INDICATOR CATALOGUE")
print("=" * 80)

indicator_doc = """
# INDICATOR CATALOGUE
User-Community Intelligence Project

## USER INDICATORS

### Usage Tier Classification
Classifies users by total CPU hours consumed across all time:
- **Inactive**: 0 CPU hours
- **Minimal**: 1 - 999 CPU hours
- **Light**: 1,000 - 99,999 CPU hours
- **Medium**: 100,000 - 999,999 CPU hours
- **Heavy**: 1,000,000+ CPU hours

### Usage Trend
Describes pattern of usage change over recent period (2025-2026) vs. historical (2016-2023):
- **Growing**: >50% increase in recent usage
- **Stable**: Usage within -20% to +50% of historical
- **Declining**: >20% decrease from historical
- **Dormant**: No recent usage after historical usage
- **New**: No historical usage (newly active)
- **Never Active**: No usage in any period

### Portfolio Type
Classification of user's project involvement:
- **Unallocated**: No projects assigned
- **Single Project**: Assigned to one project
- **Multi-Project (2-3)**: Two or three projects
- **Multi-Project (4+)**: Four or more projects

### User Support Priority Flags
Flags indicating users who may require onboarding, support, or engagement:
- **Inactive**: No usage in system
- **Dormant User**: Long period of inactivity after initial use
- **Unallocated**: No projects assigned
- **Recently Active**: Activity within last 7 days

---

## PROJECT INDICATORS

### Utilization Rate (%)
Percentage of allocated CPU hours actually used:
Formula: (cpu_used / cpu_allocated) * 100
Range: 0-500% (may exceed 100% if project extends allocations)

### Utilization Band
Grouping of projects by utilization rate:
- 0-10%, 10-25%, 25-50%, 50-75%, 75-90%, 90-100%, >100%

### Activity Status
Classification of current project activity level:
- **Inactive (No Usage)**: Zero CPU hours used
- **Low Activity**: <10% utilization
- **Moderate Activity**: 10-50% utilization
- **High Activity**: >50% utilization

### User Count
Number of unique users assigned to the project

### Health Score (0-100)
Composite metric integrating:
- Utilization rate (0-40 points): higher usage = higher score
- User engagement (0-30 points): more users = higher score
- Project status (0-20 points): remaining allocation time + activity level

Scoring formula weights active engagement and utilization.

### Health Category
Interpretation of health score:
- **Excellent**: 75-100 (well-utilized, engaged users, long runway)
- **Good**: 60-74 (solid utilization and engagement)
- **Fair**: 40-59 (moderate activity but improvement needed)
- **Poor**: 0-39 (low utilization, limited users, or imminent expiry)

### Project Support Priority Flags
Flags indicating governance or support needs:
- **No Usage**: Zero CPU hours used to date
- **Critical Underutilization**: <5% utilization rate
- **Significant Underutilization**: 5-25% utilization
- **Expiring Soon**: <3 months until allocation end date
- **No Users Assigned**: Zero users allocated to project
- **Single User - Large Allocation**: One user with >100K CPU hours
- **Large Allocation Underutilized**: >500K CPU hours allocated but <20% utilization

---

## SUMMARY METRICS

### User Summary by Institution
- **user_count**: Number of unique users
- **total_usage**: Total CPU hours consumed
- **avg_usage**: Average CPU hours per user
- **heavy_users**: Count of users in "Heavy" tier
- **growing_users**: Count of users with "Growing" trend
- **needs_support**: Count of users flagged for support

### Project Summary by Discipline
- **project_count**: Number of projects
- **total_allocated**: Total CPU hours allocated
- **total_used**: Total CPU hours used
- **utilization_pct**: Overall utilization rate for discipline
- **avg_health**: Average health score for discipline projects
- **support_needed**: Count of projects flagged for support

---

## DATA QUALITY NOTES
- Missing discipline_name in users: 11.1% (467 of 4,221)
- Missing qualification in users: 6.1% (257 of 4,221)
- Missing staff_id in projects: 9.4% (96 of 1,018)
- Unmapped user-project references: 0 (perfect match)
- Overall data completeness: >88% in all key fields

"""

with open(OUTPUT_DIR / 'INDICATOR_CATALOGUE.md', 'w') as f:
    f.write(indicator_doc)
print(f"✓ Exported: INDICATOR_CATALOGUE.md")

print("\n" + "=" * 80)
print("PHASE 2 COMPLETE")
print("=" * 80)
print(f"\nOutputs generated:")
print(f"  - user_indicators.csv ({len(user_indicators)} records)")
print(f"  - project_indicators.csv ({len(project_indicators)} records)")
print(f"  - user_summary_by_institution.csv")
print(f"  - project_summary_by_discipline.csv")
print(f"  - critical_projects_for_support.csv")
print(f"  - INDICATOR_CATALOGUE.md")

print(f"\nNext steps:")
print(f"  1. Review indicator outputs")
print(f"  2. Build dashboard prototype (Phase 3)")
print(f"  3. Start the Flask app")
