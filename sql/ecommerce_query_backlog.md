# E-commerce SQL Query Backlog

## Source Profiling

- Row counts by source table.
- Duplicate primary keys by table.
- Null rates by required field.
- Status value distribution.
- Date range by source table.

## Revenue and Product

- Monthly revenue and orders.
- Revenue by category and product.
- Top 20 products by revenue.
- Products with declining revenue trend.
- Product/category Pareto analysis.

## Customers and Retention

- First purchase date by customer.
- New vs returning customers by month.
- Repeat purchase rate.
- Cohort retention matrix.
- Customer lifetime revenue proxy.

## Funnel and Events

- Event counts by stage.
- Funnel conversion rate by source/channel/device.
- Session-to-purchase lag.
- Product view to cart to purchase drop-off.

## Data Quality and Reconciliation

- Source order total vs mart order total.
- Orphan order items without valid order/customer/product.
- Negative or zero revenue checks.
- Future date checks.
- Missing customer/product/category checks.

## Interview-Grade SQL Patterns To Include

- CTE chain for readable transformation.
- Window function for first purchase and ranking.
- Date spine for complete month reporting.
- Conditional aggregation.
- Percent-of-total analysis.
- Cohort query.
- Reconciliation query.

