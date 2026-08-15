# Tableau Dashboard Plan

## Dashboard Name

E-Commerce Executive Dashboard

## Data Source

Databricks SQL views:

- `vw_executive_monthly`
- `vw_product_performance`
- `vw_sessions_by_source`
- `vw_cohort_retention`

## Current Build Evidence

The first dashboard version has been saved and captured here:

![E-commerce executive dashboard](screenshots/ecommerce_executive_dashboard.png)

Current version includes:

- Executive KPI cards for revenue, profit, orders, customers, and average order value.
- Monthly revenue trend.
- Product revenue by category split by department.

## Sheet 1: Executive Trend

Data:

- `vw_executive_monthly`

Visuals:

- Net revenue by month.
- Orders by month.
- Net margin by month.
- Average order value by month.

## Sheet 2: Product Performance

Data:

- `vw_product_performance`

Visuals:

- Category revenue bar chart.
- Product profitability table.
- Return rate by category.
- Top products by net revenue.

## Sheet 3: Funnel and Sessions

Data:

- `vw_sessions_by_source`

Visuals:

- Sessions by traffic source.
- Conversion rate by browser/source.
- Product/cart/purchase event trend.

## Sheet 4: Cohort Retention

Data:

- `vw_cohort_retention`

Visuals:

- Cohort heatmap.
- Retention curve.
- Cohort revenue table.

## Dashboard Requirements

- Use filters for date, department, category, traffic source, and browser.
- Use clear business labels.
- Include a dashboard note that source data is synthetic public e-commerce data.
- Keep Tableau calculations minimal; push reusable logic into Databricks SQL views.
