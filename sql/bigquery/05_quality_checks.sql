-- Enterprise Analytics Command Center
-- Step 05: Create e-commerce quality checks for portfolio evidence.

CREATE OR REPLACE TABLE `enterprise-analytics-cc.analytics_quality.ecommerce_quality_checks` AS
WITH checks AS (
  SELECT
    'raw_users_has_rows' AS check_name,
    'row_count' AS check_category,
    COUNT(*) AS check_value,
    1 AS expected_minimum,
    COUNT(*) >= 1 AS passed,
    'Raw users view should contain rows.' AS details
  FROM `enterprise-analytics-cc.ecom_raw.users`

  UNION ALL

  SELECT
    'raw_orders_has_rows',
    'row_count',
    COUNT(*),
    1,
    COUNT(*) >= 1,
    'Raw orders view should contain rows.'
  FROM `enterprise-analytics-cc.ecom_raw.orders`

  UNION ALL

  SELECT
    'orders_unique_order_id',
    'primary_key',
    COUNT(*) - COUNT(DISTINCT order_id),
    0,
    COUNT(*) - COUNT(DISTINCT order_id) = 0,
    'Orders should have unique order_id values.'
  FROM `enterprise-analytics-cc.ecom_staging.stg_orders`

  UNION ALL

  SELECT
    'order_items_unique_order_item_id',
    'primary_key',
    COUNT(*) - COUNT(DISTINCT order_item_id),
    0,
    COUNT(*) - COUNT(DISTINCT order_item_id) = 0,
    'Order items should have unique order_item_id values.'
  FROM `enterprise-analytics-cc.ecom_staging.stg_order_items`

  UNION ALL

  SELECT
    'products_unique_product_id',
    'primary_key',
    COUNT(*) - COUNT(DISTINCT product_id),
    0,
    COUNT(*) - COUNT(DISTINCT product_id) = 0,
    'Products should have unique product_id values.'
  FROM `enterprise-analytics-cc.ecom_staging.stg_products`

  UNION ALL

  SELECT
    'order_items_missing_order_id',
    'not_null',
    COUNTIF(order_id IS NULL),
    0,
    COUNTIF(order_id IS NULL) = 0,
    'Order items should not have missing order_id values.'
  FROM `enterprise-analytics-cc.ecom_staging.stg_order_items`

  UNION ALL

  SELECT
    'order_items_missing_product_id',
    'not_null',
    COUNTIF(product_id IS NULL),
    0,
    COUNTIF(product_id IS NULL) = 0,
    'Order items should not have missing product_id values.'
  FROM `enterprise-analytics-cc.ecom_staging.stg_order_items`

  UNION ALL

  SELECT
    'order_items_negative_sale_price',
    'accepted_range',
    COUNTIF(sale_price < 0),
    0,
    COUNTIF(sale_price < 0) = 0,
    'Sale price should not be negative.'
  FROM `enterprise-analytics-cc.ecom_staging.stg_order_items`

  UNION ALL

  SELECT
    'orphan_order_items_without_order',
    'relationship',
    COUNTIF(o.order_id IS NULL),
    0,
    COUNTIF(o.order_id IS NULL) = 0,
    'Every order item should map to a valid order.'
  FROM `enterprise-analytics-cc.ecom_staging.stg_order_items` oi
  LEFT JOIN `enterprise-analytics-cc.ecom_staging.stg_orders` o
    ON oi.order_id = o.order_id

  UNION ALL

  SELECT
    'orphan_order_items_without_product',
    'relationship',
    COUNTIF(p.product_id IS NULL),
    0,
    COUNTIF(p.product_id IS NULL) = 0,
    'Every order item should map to a valid product.'
  FROM `enterprise-analytics-cc.ecom_staging.stg_order_items` oi
  LEFT JOIN `enterprise-analytics-cc.ecom_staging.stg_products` p
    ON oi.product_id = p.product_id

  UNION ALL

  SELECT
    'source_to_mart_order_item_revenue_reconciliation',
    'reconciliation',
    CAST(ROUND(ABS(source_totals.source_revenue - mart_totals.mart_revenue), 0) AS INT64),
    1,
    ABS(source_totals.source_revenue - mart_totals.mart_revenue) < 1,
    'Gross order item sale_price should reconcile between staging and mart.'
  FROM (
    SELECT SUM(sale_price) AS source_revenue
    FROM `enterprise-analytics-cc.ecom_staging.stg_order_items`
  ) source_totals
  CROSS JOIN (
    SELECT SUM(sale_price) AS mart_revenue
    FROM `enterprise-analytics-cc.ecom_marts.fact_order_items`
  ) mart_totals
)
SELECT
  CURRENT_TIMESTAMP() AS check_run_at,
  check_name,
  check_category,
  check_value,
  expected_minimum,
  CASE WHEN passed THEN 'PASS' ELSE 'FAIL' END AS check_status,
  details
FROM checks;

-- Review failed checks.
SELECT *
FROM `enterprise-analytics-cc.analytics_quality.ecommerce_quality_checks`
ORDER BY check_status, check_category, check_name;

