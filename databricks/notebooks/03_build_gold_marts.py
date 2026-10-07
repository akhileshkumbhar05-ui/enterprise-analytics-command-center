# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC # 03 - Build Gold Marts
# MAGIC
# MAGIC Builds dimensional Gold Delta tables for Tableau and business analysis.

# COMMAND ----------

dbutils.widgets.text("catalog", "workspace")
dbutils.widgets.text("silver_schema", "eacc_ecommerce_silver")
dbutils.widgets.text("gold_schema", "eacc_ecommerce_gold")

catalog = dbutils.widgets.get("catalog").strip()
silver_schema = dbutils.widgets.get("silver_schema").strip()
gold_schema = dbutils.widgets.get("gold_schema").strip()

silver = f"`{catalog}`.`{silver_schema}`"
gold = f"`{catalog}`.`{gold_schema}`"

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE TABLE {gold}.dim_date
USING DELTA
AS
WITH bounds AS (
  SELECT
    MIN(order_created_date) AS min_date,
    MAX(order_created_date) AS max_date
  FROM {silver}.stg_orders
),
date_spine AS (
  SELECT EXPLODE(SEQUENCE(min_date, max_date, INTERVAL 1 DAY)) AS date_day
  FROM bounds
)
SELECT
  date_day,
  YEAR(date_day) AS year,
  QUARTER(date_day) AS quarter,
  MONTH(date_day) AS month_number,
  DATE_FORMAT(date_day, 'MMMM') AS month_name,
  DATE_TRUNC('MONTH', date_day) AS month_start_date,
  DATE_TRUNC('QUARTER', date_day) AS quarter_start_date,
  DATE_TRUNC('YEAR', date_day) AS year_start_date,
  WEEKOFYEAR(date_day) AS week_number,
  DAYOFWEEK(date_day) AS day_of_week_number,
  DATE_FORMAT(date_day, 'EEEE') AS day_of_week_name,
  CASE WHEN DAYOFWEEK(date_day) IN (1, 7) THEN TRUE ELSE FALSE END AS is_weekend
FROM date_spine
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {gold}.dim_customer
USING DELTA
AS
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
FROM {silver}.stg_users
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {gold}.dim_product
USING DELTA
AS
SELECT
  p.product_id,
  p.product_name,
  p.brand,
  p.category,
  p.department,
  p.sku,
  p.cost,
  p.retail_price,
  (p.retail_price - p.cost) / NULLIF(p.retail_price, 0) AS list_margin_pct,
  p.distribution_center_id,
  dc.distribution_center_name,
  dc.distribution_center_latitude,
  dc.distribution_center_longitude
FROM {silver}.stg_products p
LEFT JOIN {silver}.stg_distribution_centers dc
  ON p.distribution_center_id = dc.distribution_center_id
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {gold}.fact_order_items
USING DELTA
AS
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
  (oi.sale_price - p.cost) / NULLIF(oi.sale_price, 0) AS gross_margin_pct,
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
FROM {silver}.stg_order_items oi
LEFT JOIN {silver}.stg_orders o
  ON oi.order_id = o.order_id
LEFT JOIN {silver}.stg_products p
  ON oi.product_id = p.product_id
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {gold}.fact_orders
USING DELTA
AS
SELECT
  o.order_id,
  o.customer_id,
  o.order_status,
  o.customer_gender,
  o.order_created_at,
  o.order_created_date,
  DATE_TRUNC('MONTH', o.order_created_date) AS order_month,
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
  SUM(CASE WHEN foi.is_returned THEN 1 ELSE 0 END) AS returned_item_count,
  SUM(CASE WHEN foi.is_cancelled THEN 1 ELSE 0 END) AS cancelled_item_count,
  CASE WHEN LOWER(o.order_status) = 'returned' THEN TRUE ELSE FALSE END AS is_returned_order,
  CASE WHEN LOWER(o.order_status) = 'cancelled' THEN TRUE ELSE FALSE END AS is_cancelled_order
FROM {silver}.stg_orders o
LEFT JOIN {gold}.fact_order_items foi
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
  o.num_of_item
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {gold}.fact_customer_cohorts
USING DELTA
AS
WITH valid_orders AS (
  SELECT
    customer_id,
    order_id,
    order_created_date,
    DATE_TRUNC('MONTH', order_created_date) AS order_month,
    net_revenue_amount
  FROM {gold}.fact_orders
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
    CAST(MONTHS_BETWEEN(vo.order_month, cfo.cohort_month) AS INT) AS months_since_first_purchase,
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
GROUP BY cohort_month, order_month, months_since_first_purchase
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {gold}.fact_sessions
USING DELTA
AS
SELECT
  session_id,
  FIRST(customer_id, TRUE) AS customer_id,
  MIN(event_created_at) AS session_start_at,
  MAX(event_created_at) AS session_end_at,
  TO_DATE(MIN(event_created_at)) AS session_date,
  FIRST(traffic_source, TRUE) AS traffic_source,
  FIRST(browser, TRUE) AS browser,
  COUNT(*) AS event_count,
  SUM(CASE WHEN LOWER(event_type) = 'home' THEN 1 ELSE 0 END) AS home_events,
  SUM(CASE WHEN LOWER(event_type) = 'department' THEN 1 ELSE 0 END) AS department_events,
  SUM(CASE WHEN LOWER(event_type) = 'product' THEN 1 ELSE 0 END) AS product_events,
  SUM(CASE WHEN LOWER(event_type) = 'cart' THEN 1 ELSE 0 END) AS cart_events,
  SUM(CASE WHEN LOWER(event_type) = 'purchase' THEN 1 ELSE 0 END) AS purchase_events,
  SUM(CASE WHEN LOWER(event_type) = 'cancel' THEN 1 ELSE 0 END) AS cancel_events,
  SUM(CASE WHEN LOWER(event_type) = 'purchase' THEN 1 ELSE 0 END) > 0 AS has_purchase_event
FROM {silver}.stg_events
GROUP BY session_id
""")

# COMMAND ----------

gold_tables = [
    "dim_date",
    "dim_customer",
    "dim_product",
    "fact_order_items",
    "fact_orders",
    "fact_customer_cohorts",
    "fact_sessions",
]

row_counts = [(table_name, spark.table(f"{gold}.{table_name}").count()) for table_name in gold_tables]
display(spark.createDataFrame(row_counts, ["gold_table", "row_count"]))