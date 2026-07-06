# Business Analyst Artifact Plan

## Purpose

Many junior candidates list SQL and Power BI. Fewer can show how a business request becomes a validated dashboard and decision. These artifacts create that proof.

## Artifact 1: Problem Brief

Must include:

- Business context.
- Stakeholders.
- Current pain points.
- Decisions the dashboard should support.
- Success metrics.
- Out of scope.
- Risks and assumptions.

Example problem:

"Leadership receives inconsistent revenue and retention reports from multiple teams. They need a trusted executive dashboard that standardizes KPI definitions, identifies customer retention issues, and highlights revenue opportunities by product and channel."

## Artifact 2: Stakeholder Map

Stakeholders:

- Executive sponsor
- Sales/marketing lead
- Operations lead
- Finance analyst
- Data engineering partner
- BI owner
- Compliance or governance reviewer, where applicable

For each stakeholder:

- Decision they need to make.
- Metrics they care about.
- Questions they will ask.
- Risk if requirements are missed.

## Artifact 3: Requirements Log

Columns:

- Requirement ID
- Stakeholder
- Business question
- Metric/KPI
- Data source
- Priority
- Acceptance criteria
- Status
- Notes

## Artifact 4: User Stories

Format:

As a `[stakeholder]`, I want `[capability]`, so that `[business outcome]`.

Examples:

- As an executive sponsor, I want to see revenue, orders, margin proxy, and repeat purchase rate by month, so that I can identify whether growth is driven by more customers or better monetization.
- As a marketing lead, I want conversion rate by source and device, so that I can prioritize campaigns with better purchase intent.
- As an operations lead, I want to see late fulfillment or operational bottlenecks by region and time period, so that I can target process improvements.
- As a finance analyst, I want KPI definitions and reconciliation checks, so that dashboard numbers can be trusted during monthly reporting.

## Artifact 5: Acceptance Criteria

Good acceptance criteria are testable.

Examples:

- Revenue must match the source order total within the documented tolerance.
- The dashboard must allow filtering by date, category, region, and customer segment.
- KPI cards must show current period value and period-over-period change.
- Users must be able to drill from category to product detail.
- The data quality page must show freshness and failed validation checks.

## Artifact 6: UAT Test Cases

Test case fields:

- Test ID
- User story
- Steps
- Expected result
- Actual result
- Pass/fail
- Defect notes

Example:

- Filter the dashboard to Q4.
- Confirm revenue, orders, and average order value update.
- Drill into top category.
- Confirm product table is filtered to selected category.

## Artifact 7: Traceability Matrix

Columns:

- Business objective
- Requirement ID
- KPI/metric
- Data model table
- Dashboard visual
- UAT test
- Status

## Artifact 8: Change Impact Note

Use this to show BA maturity:

- What changes if the metric definition changes?
- Which dashboards are affected?
- Which stakeholders need to approve?
- Which tests must be rerun?
- What is the rollout plan?

