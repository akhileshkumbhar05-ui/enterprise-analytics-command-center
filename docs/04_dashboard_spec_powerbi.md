# Power BI Dashboard Specification

## Dashboard Name

Enterprise Analytics Command Center

## Design Standard

The dashboard should feel like a real internal executive analytics product:

- Dense but readable.
- Business-first labels.
- Clear KPI definitions.
- No decorative clutter.
- Consistent page navigation.
- Metric cards only for decision-critical KPIs.
- Tables where executives need comparison.
- Trend charts where timing matters.
- Tooltips for definitions and caveats.

## Page 1: Executive Overview

Purpose:
Give leadership one screen for performance, risks, and recommended actions.

KPIs:

- Revenue
- Orders / transactions
- Active customers or users
- Average order value
- Gross margin proxy, if available
- Conversion rate, if event data is available
- Repeat purchase rate
- Return/refund rate, if available
- Data quality score

Visuals:

- KPI cards with period-over-period change.
- Revenue trend.
- Customer/order trend.
- Top categories/products.
- Region or channel performance.
- "Action queue" table with top opportunities and risks.

## Page 2: Revenue and Product Performance

Questions:

- Which categories drive revenue?
- Which products have high volume but weak margin?
- Which products are growing or declining?
- Where are returns or fulfillment issues concentrated?

Visuals:

- Category revenue matrix.
- Product Pareto chart.
- Monthly trend by category.
- Product-level table with conditional formatting.
- Drillthrough to product detail.

## Page 3: Customer Retention and Cohorts

Questions:

- Are customers coming back?
- Which acquisition cohorts retain better?
- What customer segments need action?

KPIs:

- New customers
- Returning customers
- Repeat purchase rate
- Cohort month retention
- Customer lifetime revenue proxy

Visuals:

- Cohort heatmap.
- New vs returning customer trend.
- Segment comparison.
- Top customer behavior indicators.

## Page 4: Funnel and Marketing/Product Behavior

Questions:

- Where do users drop off?
- Which channels or campaigns produce better conversion?
- Which device/traffic segments perform differently?

Visuals:

- Funnel from session to product view to cart to purchase.
- Conversion rate by channel.
- Sessions and revenue by device.
- Campaign/source comparison.
- Event-level behavior table.

## Page 5: Operations / Logistics

Questions:

- Where are delays, costs, or service bottlenecks?
- Which locations or time windows create operational pressure?

Visuals:

- Demand by hour/day.
- Location map or region matrix.
- Delay or service-level trend.
- Operational anomaly table.

## Page 6: Healthcare or Finance Domain View

This page changes by domain:

Healthcare:

- Provider quality score.
- Readmission or measure trend.
- Regional performance.
- Hospital type comparison.

Finance:

- Approval/denial trend.
- Risk or loan segment comparison.
- Institution/region performance.
- Fairness or disparity view where appropriate.

## Page 7: Data Quality and Metric Dictionary

Purpose:
Show maturity beyond pretty dashboards.

Visuals:

- Data freshness.
- Row count checks.
- Failed validation checks.
- Missing values by field.
- Duplicate key count.
- Metric dictionary table.
- Known limitations.

## Measure Catalog Requirements

Create a dedicated Power BI measure table. Each measure should have:

- Business name.
- DAX expression.
- Description.
- Grain.
- Filters/context assumptions.
- Owner or source.

Example measures:

- Total Revenue
- Orders
- Customers
- Average Order Value
- Repeat Customer Rate
- Conversion Rate
- Return Rate
- Revenue YoY %
- Revenue MoM %
- Data Quality Pass Rate

