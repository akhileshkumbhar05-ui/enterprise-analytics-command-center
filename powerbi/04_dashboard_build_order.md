# Dashboard Build Order

## Page 1: Executive Overview

Build this page first.

Visuals:

- KPI cards:
  - Total Net Revenue
  - Orders
  - Customers
  - Average Order Value
  - Net Margin %
  - Data Quality Pass Rate
- Line chart:
  - Axis: `dim_date[month_start_date]`
  - Values: `Total Net Revenue`, `Orders`
- Bar chart:
  - Axis: `dim_product[category]`
  - Values: `Total Net Revenue`
- Table:
  - `dim_product[category]`
  - `Total Net Revenue`
  - `Total Net Profit`
  - `Net Margin %`
  - `Return Rate`

## Page 2: Product Performance

Visuals:

- Category revenue bar chart.
- Product table with revenue, orders, net profit, margin, return rate.
- Department/category slicers.
- Product drillthrough target.

## Page 3: Customer Retention

Visuals:

- Cohort matrix:
  - Rows: `fact_customer_cohorts[cohort_month]`
  - Columns: `fact_customer_cohorts[months_since_first_purchase]`
  - Values: `Cohort Retention %`
- New/active customer trend.
- Cohort revenue trend.

## Page 4: Funnel and Sessions

Visuals:

- Cards:
  - Sessions
  - Product Event Sessions
  - Cart Event Sessions
  - Sessions With Purchase
  - Session Conversion Rate
- Bar chart by traffic source.
- Bar chart by browser.

## Page 5: Data Quality

Visuals:

- Cards:
  - Quality Checks
  - Passed Quality Checks
  - Failed Quality Checks
  - Data Quality Pass Rate
- Table:
  - `check_name`
  - `check_category`
  - `check_value`
  - `check_status`
  - `details`

