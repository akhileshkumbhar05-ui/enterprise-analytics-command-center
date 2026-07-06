-- Enterprise Analytics Command Center
-- Step 03a: Validate staging views before building marts.

SELECT 'stg_users' AS staging_view, COUNT(*) AS row_count
FROM `enterprise-analytics-cc.ecom_staging.stg_users`
UNION ALL
SELECT 'stg_orders', COUNT(*)
FROM `enterprise-analytics-cc.ecom_staging.stg_orders`
UNION ALL
SELECT 'stg_order_items', COUNT(*)
FROM `enterprise-analytics-cc.ecom_staging.stg_order_items`
UNION ALL
SELECT 'stg_products', COUNT(*)
FROM `enterprise-analytics-cc.ecom_staging.stg_products`
UNION ALL
SELECT 'stg_distribution_centers', COUNT(*)
FROM `enterprise-analytics-cc.ecom_staging.stg_distribution_centers`
UNION ALL
SELECT 'stg_events', COUNT(*)
FROM `enterprise-analytics-cc.ecom_staging.stg_events`
ORDER BY staging_view;

-- Check key uniqueness in staging dimensions/entities.
SELECT
  'stg_users.customer_id' AS key_check,
  COUNT(*) AS row_count,
  COUNT(DISTINCT customer_id) AS distinct_key_count,
  COUNT(*) - COUNT(DISTINCT customer_id) AS duplicate_count
FROM `enterprise-analytics-cc.ecom_staging.stg_users`
UNION ALL
SELECT
  'stg_orders.order_id',
  COUNT(*),
  COUNT(DISTINCT order_id),
  COUNT(*) - COUNT(DISTINCT order_id)
FROM `enterprise-analytics-cc.ecom_staging.stg_orders`
UNION ALL
SELECT
  'stg_order_items.order_item_id',
  COUNT(*),
  COUNT(DISTINCT order_item_id),
  COUNT(*) - COUNT(DISTINCT order_item_id)
FROM `enterprise-analytics-cc.ecom_staging.stg_order_items`
UNION ALL
SELECT
  'stg_products.product_id',
  COUNT(*),
  COUNT(DISTINCT product_id),
  COUNT(*) - COUNT(DISTINCT product_id)
FROM `enterprise-analytics-cc.ecom_staging.stg_products`;

