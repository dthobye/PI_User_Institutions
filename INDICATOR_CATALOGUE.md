
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

