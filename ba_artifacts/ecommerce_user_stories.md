# E-commerce User Stories and Acceptance Criteria

## US-001: Executive Performance Overview

As an executive sponsor, I want to see revenue, orders, customers, average order value, and repeat purchase rate in one view, so that I can understand business performance without reconciling multiple reports.

Acceptance criteria:

- KPI cards show selected-period values.
- KPI cards show prior-period comparison.
- Date filter changes all visuals.
- Revenue and order totals reconcile to curated mart totals.

## US-002: Product Performance Drillthrough

As a product manager, I want to rank categories and products by revenue, order volume, and growth, so that I can identify where to invest or investigate.

Acceptance criteria:

- Category visual ranks categories by revenue.
- Product table includes revenue, orders, AOV, and growth.
- User can drill into product details.
- Filters preserve context across relevant visuals.

## US-003: Customer Retention

As a marketing lead, I want cohort retention by first purchase month, so that I can understand whether acquired customers continue buying.

Acceptance criteria:

- Cohort heatmap displays retention by cohort and months since first purchase.
- New and returning customer trend is visible.
- Repeat purchase rate is documented.
- Known limitations are listed.

## US-004: Funnel Performance

As a marketing lead, I want to see event funnel drop-off, so that I can identify where customers leave before purchase.

Acceptance criteria:

- Funnel stages are clearly defined.
- Conversion rate is calculated consistently.
- Funnel can be filtered by source/channel/device if available.
- Stage definitions are included in metric dictionary.

## US-005: Data Quality Trust

As a finance analyst, I want data freshness, row counts, failed validation checks, and KPI definitions, so that I can trust the dashboard for recurring reporting.

Acceptance criteria:

- Data quality page includes source freshness.
- Data quality page includes failed checks.
- Metric dictionary includes formula and grain.
- Reconciliation check results are visible or documented.

