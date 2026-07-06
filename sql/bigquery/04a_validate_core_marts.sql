-- Enterprise Analytics Command Center
-- Step 04a: Validate core mart tables after materialization.

-- 1. Mart row counts.
SELECT 'dim_date' AS mart_table, COUNT(*) AS row_count
FROM `enterprise-analytics-cc.ecom_marts.dim_date`
UNION ALL
SELECT 'dim_customer', COUNT(*)
FROM `enterprise-analytics-cc.ecom_marts.dim_customer`
UNION ALL
SELECT 'dim_product', COUNT(*)
FROM `enterprise-analytics-cc.ecom_marts.dim_product`
UNION ALL
SELECT 'fact_order_items', COUNT(*)
FROM `enterprise-analytics-cc.ecom_marts.fact_order_items`
UNION ALL
SELECT 'fact_orders', COUNT(*)
FROM `enterprise-analytics-cc.ecom_marts.fact_orders`
UNION ALL
SELECT 'fact_customer_cohorts', COUNT(*)
FROM `enterprise-analytics-cc.ecom_marts.fact_customer_cohorts`
UNION ALL
SELECT 'fact_sessions', COUNT(*)
FROM `enterprise-analytics-cc.ecom_marts.fact_sessions`
ORDER BY mart_table;

-- 2. Fact/dimension relationship checks.
SELECT
  'fact_orders_without_customer' AS check_name,
  COUNTIF(c.customer_id IS NULL) AS issue_count
FROM `enterprise-analytics-cc.ecom_marts.fact_orders` o
LEFT JOIN `enterprise-analytics-cc.ecom_marts.dim_customer` c
  ON o.customer_id = c.customer_id
UNION ALL
SELECT
  'fact_order_items_without_order',
  COUNTIF(o.order_id IS NULL)
FROM `enterprise-analytics-cc.ecom_marts.fact_order_items` oi
LEFT JOIN `enterprise-analytics-cc.ecom_marts.fact_orders` o
  ON oi.order_id = o.order_id
UNION ALL
SELECT
  'fact_order_items_without_product',
  COUNTIF(p.product_id IS NULL)
FROM `enterprise-analytics-cc.ecom_marts.fact_order_items` oi
LEFT JOIN `enterprise-analytics-cc.ecom_marts.dim_product` p
  ON oi.product_id = p.product_id;

-- 3. Executive KPI preview.
SELECT
  COUNT(DISTINCT order_id) AS orders,
  COUNT(DISTINCT customer_id) AS customers,
  ROUND(SUM(gross_revenue_amount), 2) AS gross_revenue,
  ROUND(SUM(net_revenue_amount), 2) AS net_revenue,
  ROUND(SUM(net_profit_amount), 2) AS net_profit,
  ROUND(SAFE_DIVIDE(SUM(net_profit_amount), SUM(net_revenue_amount)), 4) AS net_margin_pct,
  COUNTIF(is_returned_order) AS returned_orders,
  COUNTIF(is_cancelled_order) AS cancelled_orders
FROM `enterprise-analytics-cc.ecom_marts.fact_orders`;

-- 4. Monthly revenue preview for the first Power BI trend visual.
SELECT
  order_month,
  COUNT(DISTINCT order_id) AS orders,
  COUNT(DISTINCT customer_id) AS customers,
  ROUND(SUM(net_revenue_amount), 2) AS net_revenue,
  ROUND(SUM(net_profit_amount), 2) AS net_profit
FROM `enterprise-analytics-cc.ecom_marts.fact_orders`
GROUP BY order_month
ORDER BY order_month;

