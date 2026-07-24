# Databricks notebook source
# MAGIC %md
# MAGIC # 04 - Quality Checks
# MAGIC
# MAGIC Creates a quality check table for the Databricks e-commerce Lakehouse.

# COMMAND ----------

dbutils.widgets.text("catalog", "main")
dbutils.widgets.text("bronze_schema", "eacc_ecommerce_bronze")
dbutils.widgets.text("silver_schema", "eacc_ecommerce_silver")
dbutils.widgets.text("gold_schema", "eacc_ecommerce_gold")
dbutils.widgets.text("quality_schema", "eacc_quality")

catalog = dbutils.widgets.get("catalog").strip()
bronze_schema = dbutils.widgets.get("bronze_schema").strip()
silver_schema = dbutils.widgets.get("silver_schema").strip()
gold_schema = dbutils.widgets.get("gold_schema").strip()
quality_schema = dbutils.widgets.get("quality_schema").strip()

bronze = f"`{catalog}`.`{bronze_schema}`"
silver = f"`{catalog}`.`{silver_schema}`"
quality = f"`{catalog}`.`{quality_schema}`"

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE TABLE {quality}.ecommerce_quality_checks
USING DELTA
AS
WITH checks AS (
  SELECT
    'raw_users_has_rows' AS check_name,
    'row_count' AS check_category,
    COUNT(*) AS check_value,
    1 AS expected_minimum,
    COUNT(*) >= 1 AS passed,
    'Raw users table should contain rows.' AS details
  FROM {bronze}.raw_users

  UNION ALL

  SELECT
    'raw_orders_has_rows',
    'row_count',
    COUNT(*),
    1,
    COUNT(*) >= 1,
    'Raw orders table should contain rows.'
  FROM {bronze}.raw_orders

  UNION ALL

  SELECT
    'orders_unique_order_id',
    'primary_key',
    COUNT(*) - COUNT(DISTINCT order_id),
    0,
    COUNT(*) - COUNT(DISTINCT order_id) = 0,
    'Orders should have unique order_id values.'
  FROM {silver}.stg_orders

  UNION ALL

  SELECT
    'order_items_unique_order_item_id',
    'primary_key',
    COUNT(*) - COUNT(DISTINCT order_item_id),
    0,
    COUNT(*) - COUNT(DISTINCT order_item_id) = 0,
    'Order items should have unique order_item_id values.'
  FROM {silver}.stg_order_items

  UNION ALL

  SELECT
    'products_unique_product_id',
    'primary_key',
    COUNT(*) - COUNT(DISTINCT product_id),
    0,
    COUNT(*) - COUNT(DISTINCT product_id) = 0,
    'Products should have unique product_id values.'
  FROM {silver}.stg_products

  UNION ALL

  SELECT
    'order_items_missing_order_id',
    'not_null',
    SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END),
    0,
    SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) = 0,
    'Order items should not have missing order_id values.'
  FROM {silver}.stg_order_items

  UNION ALL

  SELECT
    'order_items_missing_product_id',
    'not_null',
    SUM(CASE WHEN product_id IS NULL THEN 1 ELSE 0 END),
    0,
    SUM(CASE WHEN product_id IS NULL THEN 1 ELSE 0 END) = 0,
    'Order items should not have missing product_id values.'
  FROM {silver}.stg_order_items

  UNION ALL

  SELECT
    'order_items_negative_sale_price',
    'accepted_range',
    SUM(CASE WHEN sale_price < 0 THEN 1 ELSE 0 END),
    0,
    SUM(CASE WHEN sale_price < 0 THEN 1 ELSE 0 END) = 0,
    'Sale price should not be negative.'
  FROM {silver}.stg_order_items

  UNION ALL

  SELECT
    'orphan_order_items_without_order',
    'relationship',
    SUM(CASE WHEN o.order_id IS NULL THEN 1 ELSE 0 END),
    0,
    SUM(CASE WHEN o.order_id IS NULL THEN 1 ELSE 0 END) = 0,
    'Every order item should map to a valid order.'
  FROM {silver}.stg_order_items oi
  LEFT JOIN {silver}.stg_orders o
    ON oi.order_id = o.order_id

  UNION ALL

  SELECT
    'orphan_order_items_without_product',
    'relationship',
    SUM(CASE WHEN p.product_id IS NULL THEN 1 ELSE 0 END),
    0,
    SUM(CASE WHEN p.product_id IS NULL THEN 1 ELSE 0 END) = 0,
    'Every order item should map to a valid product.'
  FROM {silver}.stg_order_items oi
  LEFT JOIN {silver}.stg_products p
    ON oi.product_id = p.product_id
)
SELECT
  CURRENT_TIMESTAMP() AS check_run_at,
  check_name,
  check_category,
  check_value,
  expected_minimum,
  CASE WHEN passed THEN 'PASS' ELSE 'FAIL' END AS check_status,
  details
FROM checks
""")

display(spark.table(f"{quality}.ecommerce_quality_checks").orderBy("check_status", "check_category", "check_name"))
