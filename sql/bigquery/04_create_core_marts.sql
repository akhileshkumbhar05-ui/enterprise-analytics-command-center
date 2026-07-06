-- Enterprise Analytics Command Center
-- Step 04: Create first curated dimensional marts for Power BI.

CREATE OR REPLACE TABLE `enterprise-analytics-cc.ecom_marts.dim_date` AS
WITH bounds AS (
  SELECT
    MIN(order_created_date) AS min_date,
    MAX(order_created_date) AS max_date
  FROM `enterprise-analytics-cc.ecom_staging.stg_orders`
),
date_spine AS (
  SELECT date_day
  FROM bounds,
  UNNEST(GENERATE_DATE_ARRAY(min_date, max_date)) AS date_day
)
SELECT
  date_day,
  EXTRACT(YEAR FROM date_day) AS year,
  EXTRACT(QUARTER FROM date_day) AS quarter,
  EXTRACT(MONTH FROM date_day) AS month_number,
  FORMAT_DATE('%B', date_day) AS month_name,
  DATE_TRUNC(date_day, MONTH) AS month_start_date,
  DATE_TRUNC(date_day, QUARTER) AS quarter_start_date,
  DATE_TRUNC(date_day, YEAR) AS year_start_date,
  EXTRACT(WEEK FROM date_day) AS week_number,
  EXTRACT(DAYOFWEEK FROM date_day) AS day_of_week_number,
  FORMAT_DATE('%A', date_day) AS day_of_week_name,
  CASE WHEN EXTRACT(DAYOFWEEK FROM date_day) IN (1, 7) THEN TRUE ELSE FALSE END AS is_weekend
FROM date_spine;

CREATE OR REPLACE TABLE `enterprise-analytics-cc.ecom_marts.dim_customer` AS
SELECT
  customer_id,
  first_name,
  last_name,
  email,
  age,
  CASE
    WHEN age < 18 THEN 'Under 18'
    WHEN age BETWEEN 18 AND 24 THEN '18-24'
    WHEN age BETWEEN 25 AND 34 THEN '25-34'
    WHEN age BETWEEN 35 AND 44 THEN '35-44'
    WHEN age BETWEEN 45 AND 54 THEN '45-54'
    WHEN age >= 55 THEN '55+'
    ELSE 'Unknown'
  END AS age_band,
  gender,
  country,
  state,
  city,
  postal_code,
  latitude,
  longitude,
  traffic_source,
  customer_created_at,
  customer_created_date
FROM `enterprise-analytics-cc.ecom_staging.stg_users`;

CREATE OR REPLACE TABLE `enterprise-analytics-cc.ecom_marts.dim_product` AS
SELECT
  p.product_id,
  p.product_name,
  p.brand,
  p.category,
  p.department,
  p.sku,
  p.cost,
  p.retail_price,
  SAFE_DIVIDE(p.retail_price - p.cost, p.retail_price) AS list_margin_pct,
  p.distribution_center_id,
  dc.distribution_center_name,
  dc.distribution_center_latitude,
  dc.distribution_center_longitude
FROM `enterprise-analytics-cc.ecom_staging.stg_products` p
LEFT JOIN `enterprise-analytics-cc.ecom_staging.stg_distribution_centers` dc
  ON p.distribution_center_id = dc.distribution_center_id;

CREATE OR REPLACE TABLE `enterprise-analytics-cc.ecom_marts.fact_order_items` AS
SELECT
  oi.order_item_id,
  oi.order_id,
  oi.customer_id,
  oi.product_id,
  oi.inventory_item_id,
  oi.item_status,
  o.order_status,
  oi.order_item_created_at,
  oi.order_item_created_date,
  oi.shipped_at,
  oi.shipped_date,
  oi.delivered_at,
  oi.delivered_date,
  oi.returned_at,
  oi.returned_date,
  oi.sale_price,
  p.cost AS product_cost,
  oi.sale_price - p.cost AS gross_profit_amount,
  SAFE_DIVIDE(oi.sale_price - p.cost, oi.sale_price) AS gross_margin_pct,
  CASE
    WHEN LOWER(oi.item_status) IN ('cancelled', 'returned') THEN 0
    ELSE oi.sale_price
  END AS net_revenue_amount,
  CASE
    WHEN LOWER(oi.item_status) IN ('cancelled', 'returned') THEN 0
    ELSE p.cost
  END AS net_cost_amount,
  CASE WHEN LOWER(oi.item_status) = 'returned' THEN TRUE ELSE FALSE END AS is_returned,
  CASE WHEN LOWER(oi.item_status) = 'cancelled' THEN TRUE ELSE FALSE END AS is_cancelled,
  CASE WHEN oi.shipped_at IS NOT NULL THEN TRUE ELSE FALSE END AS is_shipped,
  CASE WHEN oi.delivered_at IS NOT NULL THEN TRUE ELSE FALSE END AS is_delivered
FROM `enterprise-analytics-cc.ecom_staging.stg_order_items` oi
LEFT JOIN `enterprise-analytics-cc.ecom_staging.stg_orders` o
  ON oi.order_id = o.order_id
LEFT JOIN `enterprise-analytics-cc.ecom_staging.stg_products` p
  ON oi.product_id = p.product_id;

CREATE OR REPLACE TABLE `enterprise-analytics-cc.ecom_marts.fact_orders` AS
SELECT
  o.order_id,
  o.customer_id,
  o.order_status,
  o.customer_gender,
  o.order_created_at,
  o.order_created_date,
  DATE_TRUNC(o.order_created_date, MONTH) AS order_month,
  o.shipped_at,
  o.shipped_date,
  o.delivered_at,
  o.delivered_date,
  o.returned_at,
  o.returned_date,
  o.num_of_item AS source_item_count,
  COUNT(foi.order_item_id) AS modeled_item_count,
  ROUND(SUM(foi.sale_price), 2) AS gross_revenue_amount,
  ROUND(SUM(foi.product_cost), 2) AS gross_cost_amount,
  ROUND(SUM(foi.gross_profit_amount), 2) AS gross_profit_amount,
  ROUND(SUM(foi.net_revenue_amount), 2) AS net_revenue_amount,
  ROUND(SUM(foi.net_cost_amount), 2) AS net_cost_amount,
  ROUND(SUM(foi.net_revenue_amount - foi.net_cost_amount), 2) AS net_profit_amount,
  COUNTIF(foi.is_returned) AS returned_item_count,
  COUNTIF(foi.is_cancelled) AS cancelled_item_count,
  CASE WHEN LOWER(o.order_status) = 'returned' THEN TRUE ELSE FALSE END AS is_returned_order,
  CASE WHEN LOWER(o.order_status) = 'cancelled' THEN TRUE ELSE FALSE END AS is_cancelled_order
FROM `enterprise-analytics-cc.ecom_staging.stg_orders` o
LEFT JOIN `enterprise-analytics-cc.ecom_marts.fact_order_items` foi
  ON o.order_id = foi.order_id
GROUP BY
  o.order_id,
  o.customer_id,
  o.order_status,
  o.customer_gender,
  o.order_created_at,
  o.order_created_date,
  o.shipped_at,
  o.shipped_date,
  o.delivered_at,
  o.delivered_date,
  o.returned_at,
  o.returned_date,
  o.num_of_item;

CREATE OR REPLACE TABLE `enterprise-analytics-cc.ecom_marts.fact_customer_cohorts` AS
WITH valid_orders AS (
  SELECT
    customer_id,
    order_id,
    order_created_date,
    DATE_TRUNC(order_created_date, MONTH) AS order_month,
    net_revenue_amount
  FROM `enterprise-analytics-cc.ecom_marts.fact_orders`
  WHERE net_revenue_amount > 0
),
customer_first_order AS (
  SELECT
    customer_id,
    MIN(order_month) AS cohort_month
  FROM valid_orders
  GROUP BY customer_id
),
cohort_activity AS (
  SELECT
    cfo.cohort_month,
    vo.order_month,
    DATE_DIFF(vo.order_month, cfo.cohort_month, MONTH) AS months_since_first_purchase,
    vo.customer_id,
    vo.order_id,
    vo.net_revenue_amount
  FROM valid_orders vo
  INNER JOIN customer_first_order cfo
    ON vo.customer_id = cfo.customer_id
)
SELECT
  cohort_month,
  order_month,
  months_since_first_purchase,
  COUNT(DISTINCT customer_id) AS active_customers,
  COUNT(DISTINCT order_id) AS orders,
  ROUND(SUM(net_revenue_amount), 2) AS net_revenue_amount
FROM cohort_activity
GROUP BY cohort_month, order_month, months_since_first_purchase;

CREATE OR REPLACE TABLE `enterprise-analytics-cc.ecom_marts.fact_sessions` AS
SELECT
  session_id,
  ANY_VALUE(customer_id) AS customer_id,
  MIN(event_created_at) AS session_start_at,
  MAX(event_created_at) AS session_end_at,
  DATE(MIN(event_created_at)) AS session_date,
  ANY_VALUE(traffic_source) AS traffic_source,
  ANY_VALUE(browser) AS browser,
  COUNT(*) AS event_count,
  COUNTIF(LOWER(event_type) = 'home') AS home_events,
  COUNTIF(LOWER(event_type) = 'department') AS department_events,
  COUNTIF(LOWER(event_type) = 'product') AS product_events,
  COUNTIF(LOWER(event_type) = 'cart') AS cart_events,
  COUNTIF(LOWER(event_type) = 'purchase') AS purchase_events,
  COUNTIF(LOWER(event_type) = 'cancel') AS cancel_events,
  COUNTIF(LOWER(event_type) = 'purchase') > 0 AS has_purchase_event
FROM `enterprise-analytics-cc.ecom_staging.stg_events`
GROUP BY session_id;

