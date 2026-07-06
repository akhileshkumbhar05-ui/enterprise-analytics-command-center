-- Enterprise Analytics Command Center
-- Step 01a: Cost-optimized source profiling.
--
-- Use this when you want lightweight profiling before running deeper scans.
-- It uses BigQuery metadata where possible and samples large event data.

-- 1. Metadata-based row counts and table sizes.
-- This is much cheaper than COUNT(*) against every source table.
-- Note: For this public dataset, use the dataset metadata table instead of
-- INFORMATION_SCHEMA.TABLE_STORAGE, which is not available at this path.
SELECT
  table_id AS table_name,
  row_count,
  ROUND(size_bytes / 1024 / 1024, 2) AS size_mb
FROM `bigquery-public-data.thelook_ecommerce.__TABLES__`
WHERE table_id IN (
  'users',
  'orders',
  'order_items',
  'products',
  'inventory_items',
  'distribution_centers',
  'events'
)
ORDER BY table_id;

-- 2. Schema metadata.
-- Metadata queries do not scan the full source tables.
SELECT
  table_name,
  ordinal_position,
  column_name,
  data_type,
  is_nullable
FROM `bigquery-public-data.thelook_ecommerce.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name IN (
  'users',
  'orders',
  'order_items',
  'products',
  'inventory_items',
  'distribution_centers',
  'events'
)
ORDER BY table_name, ordinal_position;

-- 3. Exact order coverage.
-- Small enough to run exactly.
SELECT
  COUNT(*) AS order_count,
  COUNT(DISTINCT user_id) AS customer_count,
  MIN(created_at) AS first_order_at,
  MAX(created_at) AS last_order_at
FROM `bigquery-public-data.thelook_ecommerce.orders`;

-- 4. Exact order status distribution.
-- Small enough to run exactly.
SELECT
  status,
  COUNT(*) AS orders
FROM `bigquery-public-data.thelook_ecommerce.orders`
GROUP BY status
ORDER BY orders DESC;

-- 5. Exact order item status distribution.
-- Moderate scan, but important for revenue definitions.
SELECT
  status,
  COUNT(*) AS order_items,
  ROUND(SUM(sale_price), 2) AS gross_sale_price
FROM `bigquery-public-data.thelook_ecommerce.order_items`
GROUP BY status
ORDER BY order_items DESC;

-- 6. Exact product distribution.
-- Small dimension table.
SELECT
  department,
  category,
  COUNT(*) AS products,
  ROUND(AVG(retail_price), 2) AS avg_retail_price,
  ROUND(AVG(cost), 2) AS avg_cost
FROM `bigquery-public-data.thelook_ecommerce.products`
GROUP BY department, category
ORDER BY products DESC;

-- 7. Sampled event type distribution.
-- Use this for quick exploration. Run the exact event distribution later if needed.
SELECT
  event_type,
  COUNT(*) AS sampled_events,
  COUNT(DISTINCT session_id) AS sampled_sessions,
  COUNT(DISTINCT user_id) AS sampled_users
FROM `bigquery-public-data.thelook_ecommerce.events` TABLESAMPLE SYSTEM (10 PERCENT)
GROUP BY event_type
ORDER BY sampled_events DESC;

-- 8. Lightweight data quality sniff test.
-- This scans only required columns.
SELECT
  'orders_missing_order_id' AS check_name,
  COUNTIF(order_id IS NULL) AS issue_count
FROM `bigquery-public-data.thelook_ecommerce.orders`
UNION ALL
SELECT
  'orders_missing_user_id',
  COUNTIF(user_id IS NULL)
FROM `bigquery-public-data.thelook_ecommerce.orders`
UNION ALL
SELECT
  'order_items_missing_order_id',
  COUNTIF(order_id IS NULL)
FROM `bigquery-public-data.thelook_ecommerce.order_items`
UNION ALL
SELECT
  'order_items_missing_product_id',
  COUNTIF(product_id IS NULL)
FROM `bigquery-public-data.thelook_ecommerce.order_items`
UNION ALL
SELECT
  'order_items_negative_sale_price',
  COUNTIF(sale_price < 0)
FROM `bigquery-public-data.thelook_ecommerce.order_items`;
