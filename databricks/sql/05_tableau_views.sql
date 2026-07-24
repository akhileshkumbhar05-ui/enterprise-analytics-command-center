-- Enterprise Analytics Command Center
-- Tableau-facing Databricks SQL views.
--
-- Replace catalog/schema names if you used different widget values.

USE CATALOG main;
USE SCHEMA eacc_ecommerce_gold;

CREATE OR REPLACE VIEW vw_executive_monthly AS
SELECT
  order_month,
  COUNT(DISTINCT order_id) AS orders,
  COUNT(DISTINCT customer_id) AS customers,
  ROUND(SUM(net_revenue_amount), 2) AS net_revenue,
  ROUND(SUM(net_profit_amount), 2) AS net_profit,
  ROUND(SUM(net_profit_amount) / NULLIF(SUM(net_revenue_amount), 0), 4) AS net_margin_pct,
  ROUND(SUM(net_revenue_amount) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS average_order_value,
  SUM(returned_item_count) AS returned_items,
  SUM(cancelled_item_count) AS cancelled_items
FROM fact_orders
GROUP BY order_month;

CREATE OR REPLACE VIEW vw_product_performance AS
SELECT
  p.department,
  p.category,
  p.brand,
  p.product_id,
  p.product_name,
  COUNT(DISTINCT oi.order_id) AS orders,
  COUNT(*) AS order_items,
  ROUND(SUM(oi.net_revenue_amount), 2) AS net_revenue,
  ROUND(SUM(oi.net_revenue_amount - oi.net_cost_amount), 2) AS net_profit,
  ROUND(SUM(oi.net_revenue_amount - oi.net_cost_amount) / NULLIF(SUM(oi.net_revenue_amount), 0), 4) AS net_margin_pct,
  ROUND(SUM(CASE WHEN oi.is_returned THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 4) AS return_rate
FROM fact_order_items oi
LEFT JOIN dim_product p
  ON oi.product_id = p.product_id
GROUP BY
  p.department,
  p.category,
  p.brand,
  p.product_id,
  p.product_name;

CREATE OR REPLACE VIEW vw_sessions_by_source AS
SELECT
  session_date,
  traffic_source,
  browser,
  COUNT(DISTINCT session_id) AS sessions,
  SUM(product_events) AS product_events,
  SUM(cart_events) AS cart_events,
  SUM(purchase_events) AS purchase_events,
  ROUND(SUM(CASE WHEN has_purchase_event THEN 1 ELSE 0 END) / NULLIF(COUNT(DISTINCT session_id), 0), 4) AS session_conversion_rate
FROM fact_sessions
GROUP BY session_date, traffic_source, browser;

CREATE OR REPLACE VIEW vw_cohort_retention AS
WITH cohort_sizes AS (
  SELECT
    cohort_month,
    active_customers AS cohort_size
  FROM fact_customer_cohorts
  WHERE months_since_first_purchase = 0
)
SELECT
  c.cohort_month,
  c.order_month,
  c.months_since_first_purchase,
  c.active_customers,
  s.cohort_size,
  ROUND(c.active_customers / NULLIF(s.cohort_size, 0), 4) AS retention_rate,
  c.orders,
  c.net_revenue_amount
FROM fact_customer_cohorts c
LEFT JOIN cohort_sizes s
  ON c.cohort_month = s.cohort_month;
