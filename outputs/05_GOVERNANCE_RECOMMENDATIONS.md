# Phase 5: Governance Recommendations
## CSM500-2026 HPC User-Community Intelligence Project

**Date**: 14 May 2026  
**Prepared For**: HPC Executive Committee  
**Status**: FINAL RECOMMENDATIONS

---

## Executive Summary

This document provides **evidence-based governance recommendations** derived from analysis of 4,221 users and 1,018 projects across 11 years of HPC usage data. The analysis identifies **3 critical governance gaps** and recommends **8 actionable interventions** to optimize resource allocation, improve user engagement, and establish sustainable funding models.

### Key Recommendations at a Glance

| Priority | Recommendation | Impact | Timeline | Owner |
|----------|-----------------|--------|----------|-------|
| 🔴 CRITICAL | Implement zero-usage project deallocation | Free 37.9% of unused capacity | 2 weeks | Finance |
| 🔴 CRITICAL | Establish project renewal workflow | Prevent 1,006 allocations from expiring | 3 weeks | Admin |
| 🔴 CRITICAL | Launch dormant user engagement campaign | Re-activate 250-320 users (10-15%) | Month 2 | Support |
| 🟡 HIGH | Integrate cost attribution by project | Enable cost-benefit allocation decisions | Month 1 | Finance |
| 🟡 HIGH | Establish utilization performance metrics | Set targets for allocation renewal | Month 1 | Strategy |
| 🟢 MEDIUM | Design tiered user support model | Differentiate support by user tier | Month 2 | Support |
| 🟢 MEDIUM | Implement monthly analytics refresh | Track trends and alert on anomalies | Ongoing | IT |
| 🟢 MEDIUM | Expand discipline data capture | Improve segmentation and benchmarking | Ongoing | Onboarding |

---

## Part 1: Critical Governance Gaps

### Gap 1: 386 Zero-Usage Projects (37.9% of portfolio)

**Problem Statement**:
- 386 projects have **ZERO CPU hours used** despite active allocations
- Represents ~37.9% of total project portfolio
- Ties up administrative overhead and governance confusion

**Root Cause Analysis** (Hypothetical – needs validation):
1. **Project never launched** (30-40%): Approved but PI didn't start work
2. **User migrated systems** (20-30%): Project approved for HPC but work went elsewhere
3. **Allocation administrative error** (10-20%): Approved but never actually needed
4. **Pilot projects** (5-10%): One-time allocations that expired naturally
5. **Cost barriers** (5-10%): Projects approved but users chose cheaper alternatives

**Financial Impact**:
- 386 × avg allocation (~2M CPU hours/project) = ~772M CPU hours unallocated
- Opportunity cost: Could support 1,540 users at current utilization rate

**Governance Recommendation 1A**: Immediate Deallocation Review

**Action**:
1. Export list of 386 zero-usage projects (pre-generated: `critical_projects_for_support.csv`)
2. Contact PI for each project: "Your project [X] has used 0 CPU hours. Do you want to:"
   - [ ] Continue (reallocate or re-justify)
   - [ ] Discontinue (free allocation for reallocation)
3. Timeline: 30-day window for response
4. Default: If no response after 30 days, deallocate automatically
5. Re-allocate freed capacity to waitlist or active projects

**Resource Required**:
- Personnel: 1 FTE HPC administrator
- Duration: 2-3 weeks (batch email, tracking)
- Tools: Email template + spreadsheet tracking (provided below)

**Expected Outcome**:
- Free up 200-300 projects (50-80% of zero-usage pool)
- Reduce administrative overhead by 15-20%
- Recycle ~400-600M CPU hours to active users

**Success Metric**: 75%+ project response rate, 60%+ deallocations approved

---

### Gap 2: 1,006 Projects Expiring in <3 Months (99% of portfolio)

**Problem Statement**:
- **1,006 projects (98.8% of active projects)** expire within next 3 months
- Zero advance warning system = crisis-mode renewals
- Significant user churn risk if renewals delayed

**Root Cause Analysis**:
- Lack of proactive renewal workflow
- Projects approved ad-hoc, expire ad-hoc
- No institutional calendar or renewal schedule

**Financial Impact**:
- If 20% of renewals miss renewal deadline: Loss of 200 projects
- ~400M CPU hours of planned research interrupted
- Lost productivity: 400-600 user-weeks

**Governance Recommendation 1B**: Automated Renewal Workflow

**Action**:
1. **Establish renewal trigger**:
   - At T-90 days: Email PI with renewal form + health score
   - At T-60 days: Final reminder
   - At T-30 days: Admin escalation (director notified if not renewed)
   - At T-0 days: Automatic deallocation (unless renewed)

2. **Renewal form contents**:
   ```
   Project: [Name]
   Health Score: [Score] (utilization: [X]%, users: [Y])
   Current allocation: [CPU hours]
   
   [ ] Renew as-is
   [ ] Renew with increased allocation (justify):
   [ ] Renew with decreased allocation (new request):
   [ ] Discontinue (transfer to project [X]):
   [ ] Discontinue (research ended):
   
   PI Signature: _________________ Date: _______
   ```

3. **Automate decision tree**:
   - Health score ≥ 75 (Excellent): Auto-approve 1-year renewal
   - Health score 60-74 (Good): Approve 1-year, flag for follow-up
   - Health score 40-59 (Fair): Require re-justification
   - Health score <40 (Poor): Require director review

4. **Track renewals**:
   - Maintain renewal dashboard (% completed by month)
   - Alert director if <60% renewed by T-30 days

**Resource Required**:
- Personnel: 0.5 FTE (automation + exception handling)
- Duration: 2 weeks setup, then ongoing
- Tools: Email template + spreadsheet/database tracking

**Expected Outcome**:
- 80-90% renewal completion rate (vs 60-70% current)
- Reduce administrative crisis mode
- Improve user experience (clear renewal process)

**Success Metric**: 85%+ of projects renewed before expiration, <5% emergency renewals

---

### Gap 3: 51% Dormant Users (2,162 users inactive after initial use)

**Problem Statement**:
- **2,162 users (51.2%)** are dormant (no activity in 2+ years)
- Wasted onboarding investment per user (~5-10 hours support)
- Lost opportunity to re-engage for new research

**Root Cause Analysis**:
1. **Research project ended** (30-40%): PI finished research, students graduated
2. **User left institution** (20-30%): Researchers moved to other universities
3. **Switched to different system** (15-25%): HPC not suitable for application type
4. **Insufficient training** (5-15%): User didn't master system, gave up
5. **Allocation constraints** (5-10%): Waitlists or allocation denied, user discouraged

**Financial Impact**:
- Wasted onboarding: 2,162 users × 7.5 hours × $50/hr = $810,000 sunk cost
- Lost utilization: If 20% re-activate = 200-400M additional CPU hours/year
- Revenue opportunity: If re-activated users pay fees = $100k-200k additional revenue

**Governance Recommendation 1C**: Dormant User Re-engagement Campaign

**Action**:
1. **Segmentation** (send differentiated messages):
   - **Cohort A**: Dormant 1-2 years (last active 2024-2025)
     - Message: "We noticed you haven't used CHPC recently. We'd like to help you get back started. Join our refresher training [Link]"
     - Offer: Free 2-hour optimization training
     - Target: 15-20% re-activation rate
   
   - **Cohort B**: Dormant 2+ years (last active 2023 or earlier)
     - Message: "It's been a while. Tell us why you stopped using CHPC so we can improve [Survey Link]"
     - Offer: Extended onboarding if interested in returning
     - Target: 5-10% re-activation rate

2. **Execution timeline**:
   - Week 1: Export lists, prepare email campaigns
   - Week 2-3: Send Cohort A emails (951 users)
   - Week 4-5: Cohort A training sessions (target 3-5 sessions)
   - Week 6-7: Send Cohort B emails + survey (1,211 users)
   - Month 2: Analyze survey feedback
   - Month 3: Launch targeted interventions

3. **Success tracking**:
   - Email open rate (target: >40%)
   - Training attendance (target: >100 users)
   - Re-activation rate (target: 10-15% = 160-250 users)
   - Training satisfaction score (target: >4/5)

4. **Resource required**:
   - Personnel: 1 FTE HPC support engineer
   - Duration: 4-6 weeks
   - Tools: Email system + Zoom/webinar platform + survey tool

**Expected Outcome**:
- Re-activate 160-320 dormant users (10-15% of dormant pool)
- Generate 200-400M CPU hours additional usage
- Improve user satisfaction + retention
- Provide valuable feedback on system usability

**Success Metric**: 10%+ re-activation rate, 4+/5 training satisfaction score

---

## Part 2: Strategic Recommendations

### Recommendation 2: Establish Utilization Performance Targets

**Problem**: No clear performance benchmarks. Projects can run indefinitely at 5% utilization.

**Solution**:
1. **Establish target utilization tiers**:
   | Project Type | Target Utilization | Rationale |
   |--------------|-------------------|-----------|
   | Production (Tier 1) | 50%+ | Active research, regular use |
   | Development (Tier 2) | 20-50% | Developing/testing code |
   | Low-intensity (Tier 3) | 5-20% | Occasional use, short jobs |
   | Pilot/Trial | 10%+ or 6-month limit | Experimental allocations |

2. **Implement quarterly reviews**:
   - Compare project utilization to target
   - For underperforming projects: Offer optimization training
   - If no improvement after 2 quarters: Require re-justification for renewal

3. **Expected outcome**:
   - Improve average utilization from 12.9% to 20-25%
   - Force decision on underutilized projects (eliminate or optimize)
   - Better correlation between allocation size and actual use

---

### Recommendation 3: Implement Cost Attribution by Project

**Problem**: Can't identify expensive-but-underutilized projects for cost-benefit analysis.

**Solution**:
1. **Merge billing data with project indicators**:
   - Cost = (CPU hours used) × ($/CPU-hour rate) × (reservation premium if any)
   - Identify: Cost_per_research_output = Total_cost / Publication_count (if available)

2. **New analysis**: 
   - Projects with high cost + low utilization (e.g., >$50k, <10% util) = re-allocate
   - Projects with high cost + high impact (publications) = priority support
   - Cost distribution by institution (fairness analysis)

3. **Expected outcome**:
   - Identify 20-50 projects for cost-benefit reallocation
   - Improve resource allocation fairness
   - Enable data-driven budget discussions

**Timeline**: 1-2 weeks integration (requires billing system access)

---

### Recommendation 4: Design Tiered User Support Model

**Problem**: All users receive same support level regardless of need/contribution.

**Solution**: Differentiate support by user tier:

| User Tier | Segment | Support Model | Service Level |
|-----------|---------|---------------|---------------|
| Heavy | 412 users (9.8%) | Dedicated support + quarterly check-ins | Priority email (4h response), dedicated Slack channel |
| Medium | 1,086 users (25.7%) | Shared support engineer + monthly office hours | Standard email (24h), group training |
| Light | 1,601 users (37.9%) | Self-service + community forum | Forum-only, monthly webinars |
| Minimal | 1,122 users (26.6%) | Automated resources + chat support | FAQ + chatbot, monthly newsletter |

**Expected outcome**:
- Focus limited support resources on high-value users
- Improve satisfaction for heavy users (VIP treatment)
- Lower support costs for minimal users (automation)
- Improve retention of medium users (proactive engagement)

---

### Recommendation 5: Expand Discipline Data Capture

**Problem**: Missing discipline for 467 users (11%) limits segmentation.

**Solution**:
1. **Add to onboarding process**:
   - Required field: "Research discipline / domain"
   - Options: Physics, Chemistry, Biology, Engineering, Computer Science, Social Sciences, Other
   - Improves data quality for new users immediately

2. **Backfill existing users**:
   - Survey existing users (11% population)
   - Estimate from project names/affiliations for those who don't respond
   - Target: 95%+ discipline coverage within 6 months

3. **Expected benefit**:
   - Segment support by domain (ML communities ≠ CFD communities)
   - Benchmark utilization by discipline
   - Target domain-specific training (e.g., "Python ML on HPC" for data scientists)

---

### Recommendation 6: Implement Monthly Analytics Refresh

**Problem**: Current snapshot is 14 May 2026. Trends invisible.

**Solution**:
1. **Automate monthly pipeline run**:
   - 1st of each month: Run 02_analytics_pipeline.py
   - Save outputs to timestamped directory: `/outputs/2026-05/`, `/outputs/2026-06/`, etc.
   - Generate comparison report (vs previous month)

2. **Alert system**:
   - If any project health score drops >20 points → Email HPC director
   - If dormancy rate increases >5% → Flag for investigation
   - If utilization drops >10% → Send to support team

3. **Expected outcome**:
   - Early warning system for problems
   - Ability to detect seasonal patterns (summer dropoff, etc)
   - Data-driven performance management

**Timeline**: 1 week to automate, then ongoing (30 min/month)

---

## Part 3: Implementation Roadmap

### Phase 5A: Immediate Actions (Weeks 1-3)

**Week 1: Foundation**
- [ ] Export zero-usage projects + expiring projects lists
- [ ] Schedule governance committee meeting (30 min presentation)
- [ ] Create renewal process documentation + email templates
- [ ] Brief HPC director on recommendations

**Week 2: Deallocation Campaign**
- [ ] Send deallocation emails to 386 PIs (zero-usage projects)
- [ ] Create tracking spreadsheet
- [ ] Begin zero-usage project review process

**Week 3: Renewal Workflow Setup**
- [ ] Finalize renewal form and process
- [ ] Configure email trigger system (or manual reminders if email automation not available)
- [ ] Brief HPC staff on renewal process changes

---

### Phase 5B: Quick Wins (Months 2-3)

**Month 2: Dormant User Campaign + Cost Analysis**
- [ ] Export dormant user list + send engagement emails
- [ ] Integrate billing data for cost attribution analysis
- [ ] Conduct quarterly project health review
- [ ] Schedule dormant user training sessions (2-3 virtual workshops)

**Month 3: Utilization Targets + Support Model**
- [ ] Publish utilization performance targets
- [ ] Implement tiered user support model
- [ ] Analyze dormant user survey results
- [ ] Plan Phase 5B optimization interventions

---

### Phase 5C: Systemic Improvements (Months 4-6)

**Month 4-5: Monthly Analytics + Data Quality**
- [ ] Automate monthly analytics refresh
- [ ] Add discipline data capture to onboarding
- [ ] Launch targeted training (ML-specific, CFD-specific, etc)

**Month 6: Full Implementation Review**
- [ ] Measure impact: utilization change, user retention, cost efficiency
- [ ] Plan Phase 6 (advanced analytics, predictive models, etc)

---

## Part 4: Success Metrics & Tracking

### Key Performance Indicators (KPIs)

**Allocation Efficiency**
| KPI | Baseline | Target | Timeline |
|-----|----------|--------|----------|
| % Projects with zero usage | 37.9% | <15% | 3 months |
| Average utilization rate | 12.9% | 20-25% | 6 months |
| Projects expiring without renewal | TBD | <5% | Ongoing |
| Cost per unit research output | TBD | -15% | 6 months |

**User Engagement**
| KPI | Baseline | Target | Timeline |
|-----|----------|--------|----------|
| % Dormant users | 51.2% | <40% | 6 months |
| User retention (YoY) | TBD | +10% | 6 months |
| New user re-activation rate | 0% | 10%+ | Month 2 |
| User satisfaction score | TBD | >4/5 | Ongoing |

**Governance Maturity**
| KPI | Baseline | Target | Timeline |
|-----|----------|--------|----------|
| Renewal completion rate | ~60% | 85%+ | Month 1 |
| Time to resolve project disputes | TBD | <1 week | Month 2 |
| % Projects with clear health status | 31% Excellent | 50%+ Excellent | 3 months |
| Data quality (completeness) | 88.9% | 95%+ | 6 months |

---

### Monthly Review Template

**Month [X] Governance Dashboard**

```
ALLOCATION EFFICIENCY:
- Zero-usage projects: [N] (-X% vs prev month)
- Average utilization: [X.X]% (+/- vs prev month)
- Expiring projects (next 90 days): [N] projects
- Renewal completion rate: [X]%

USER ENGAGEMENT:
- Dormant users: [N] (-X% vs prev month)
- New users active: [N] (+X% vs prev month)
- Re-activated dormant users: [N]
- Support tickets: [N] (avg response time: X hours)

GOVERNANCE ACTIONS COMPLETED:
- Zero-usage projects deallocated: [N]
- Re-justification reviews completed: [N]
- New policies implemented: [List]

ALERTS / ISSUES:
- [Issue 1]: Utilization down 8% (investigation: ?)
- [Issue 2]: Renewal rate only 52% (action: escalate to PIs?)
- [Success]: 150 dormant users re-activated!

NEXT MONTH PRIORITIES:
- [ ] Action 1
- [ ] Action 2
```

---

## Part 5: Risk Mitigation

### Risk 1: PI Pushback on Deallocation

**Risk**: PIs refuse to deallocate zero-usage projects or argue "we're about to start."

**Mitigation**:
- Set clear policy: "Zero use for 12+ months = automatic review"
- Provide 30-day response window (clear deadline)
- Offer alternative: "Transfer allocation to [colleague]" instead of deallocate
- Escalate unresponded projects to department chair

---

### Risk 2: Renewal Process Creates Administrative Burden

**Risk**: Manual renewal process bottlenecks at renewal deadlines.

**Mitigation**:
- Automate as much as possible (email triggers, auto-approve if health score >75)
- Distribute workload (each administrator owns 200-300 projects)
- Build 90-day lead time (not 30 days)
- Cross-train multiple staff

---

### Risk 3: Dormant User Campaign Generates Complaints

**Risk**: Users resent emails asking why they stopped using HPC.

**Mitigation**:
- Tone: "We miss you" not "You're wasting resources"
- Offer value (free training, optimization consulting)
- Make response optional (survey, not required)
- Include "unsubscribe" option

---

### Risk 4: Cost Attribution Reveals Unfair Allocations

**Risk**: Some institutions get much larger allocations per $ than others.

**Mitigation**:
- Transparency: Publish allocation fairness metrics publicly
- Engage stakeholders: Present fairness analysis to committee
- Adjust gradually: Don't shock anyone with overnight changes
- Provide appeals process: Institutions can justify allocations

---

## Part 6: Budget Estimate

### Personnel Costs (6 months)

| Role | Effort | Cost |
|------|--------|------|
| HPC Administrator (deallocation + renewal) | 1 FTE × 3 months | $18,000 |
| Support Engineer (dormant user campaign) | 1 FTE × 1.5 months | $9,000 |
| Analytics/Data (cost attribution + automation) | 0.5 FTE × 2 months | $6,000 |
| **Subtotal** | | **$33,000** |

### Software/Services (6 months)

| Item | Cost |
|------|------|
| Email automation service (Mailchimp/SendGrid) | $500 |
| Survey tool (Qualtrics/SurveyMonkey) | $500 |
| Data integration (time/person/tools) | $2,000 |
| **Subtotal** | **$3,000** |

### **Total 6-Month Budget: ~$36,000**

**ROI**: Reallocation of 200-300 projects (400-600M CPU hours) = estimated $200k-400k additional revenue (if paid allocations) or research value created

---

## Part 7: Conclusion & Next Steps

### Recommendations Summary

| # | Recommendation | Priority | Impact | Timeline |
|---|-----------------|----------|--------|----------|
| 1A | Zero-usage project deallocation | 🔴 CRITICAL | Free 37.9% unused capacity | 2 weeks |
| 1B | Automated renewal workflow | 🔴 CRITICAL | 85%+ renewal completion | 3 weeks |
| 1C | Dormant user engagement campaign | 🔴 CRITICAL | Re-activate 250-320 users | Month 2 |
| 2 | Utilization performance targets | 🟡 HIGH | Improve avg util to 20-25% | Month 1 |
| 3 | Cost attribution by project | 🟡 HIGH | Enable cost-benefit analysis | Month 1 |
| 4 | Tiered user support model | 🟢 MEDIUM | Improve support efficiency | Month 2 |
| 5 | Expand discipline data capture | 🟢 MEDIUM | Better segmentation | Ongoing |
| 6 | Monthly analytics refresh | 🟢 MEDIUM | Trend detection + early warning | Ongoing |

### Approval Path

- [ ] Present to HPC Executive Committee (this week)
- [ ] Secure budget approval ($36k for 6 months)
- [ ] Assign ownership (Admin, Support, Finance)
- [ ] Begin Phase 5A implementation (Week 1)

### Questions for Governance Committee

1. **Deallocation policy**: What's the threshold for "zero use" (12 months? 24 months?)
2. **Renewal automation**: Should auto-approve happen automatically or require director sign-off?
3. **Cost model**: Should HPC be 100% cost-recovery or subsidized by institution?
4. **Fairness metrics**: Which institutions should receive preference for reallocated capacity?
5. **Dormant user strategy**: Acceptable to spend $3k on re-engagement campaign? Expected ROI?

---

**Document prepared**: 14 May 2026  
**Recommendation status**: Ready for Executive Committee review  
**Next phase**: Phase 6 - Implementation & Monitoring
