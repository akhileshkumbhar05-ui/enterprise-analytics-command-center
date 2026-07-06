-- Enterprise Analytics Command Center
-- Step 01: Profile TheLook e-commerce source tables.
-- Run the full script or run sections one by one.

-- 1. Source table row counts.
SELECT 'users' AS source_table, COUNT(*) AS row_count
FROM `bigquery-public-data.thelook_ecommerce.users`
UNION ALL
SELECT 'orders', COUNT(*)
FROM `bigquery-public-data.thelook_ecommerce.orders`
UNION ALL
SELECT 'order_items', COUNT(*)
FROM `bigquery-public-data.thelook_ecommerce.order_items`
UNION ALL
SELECT 'products', COUNT(*)
FROM `bigquery-public-data.thelook_ecommerce.products`
UNION ALL
SELECT 'inventory_items', COUNT(*)
FROM `bigquery-public-data.thelook_ecommerce.inventory_items`
UNION ALL
SELECT 'distribution_centers', COUNT(*)
FROM `bigquery-public-data.thelook_ecommerce.distribution_centers`
UNION ALL
SELECT 'events', COUNT(*)
FROM `bigquery-public-data.thelook_ecommerce.events`
ORDER BY source_table;

-- 2. Source schemas.
SELECT
  table_name,
  ordinal_position,
  column_name,
  data_type,
  is_nullable
FROM `bigquery-public-data.thelook_ecommerce.INFORMATION_SCHEMA.COLUMNS`
ORDER BY table_name, ordinal_position;

-- 3. Order date coverage.
SELECT
  COUNT(*) AS order_count,
  COUNT(DISTINCT user_id) AS customer_count,
  MIN(created_at) AS first_order_at,
  MAX(created_at) AS last_order_at
FROM `bigquery-public-data.thelook_ecommerce.orders`;

-- 4. Order status distribution.
SELECT
  status,
  COUNT(*) AS orders
FROM `bigquery-public-data.thelook_ecommerce.orders`
GROUP BY status
ORDER BY orders DESC;

-- 5. Order item status distribution.
SELECT
  status,
  COUNT(*) AS order_items,
  ROUND(SUM(sale_price), 2) AS gross_sale_price
FROM `bigquery-public-data.thelook_ecommerce.order_items`
GROUP BY status
ORDER BY order_items DESC;

-- 6. Product category and department distribution.
SELECT
  department,
  category,
  COUNT(*) AS products,
  ROUND(AVG(retail_price), 2) AS avg_retail_price,
  ROUND(AVG(cost), 2) AS avg_cost
FROM `bigquery-public-data.thelook_ecommerce.products`
GROUP BY department, category
ORDER BY products DESC;

-- 7. Event type distribution.
SELECT
  event_type,
  COUNT(*) AS events,
  COUNT(DISTINCT session_id) AS sessions,
  COUNT(DISTINCT user_id) AS users
FROM `bigquery-public-data.thelook_ecommerce.events`
GROUP BY event_type
ORDER BY events DESC;

-- 8. Data quality sniff test.
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

