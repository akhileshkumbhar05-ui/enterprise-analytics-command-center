# Databricks notebook source
# MAGIC %md
# MAGIC # 02 - Transform Bronze To Silver
# MAGIC
# MAGIC Cleans and standardizes the Bronze source tables into Silver Delta tables.

# COMMAND ----------

from pyspark.sql.functions import col, to_date

dbutils.widgets.text("catalog", "main")
dbutils.widgets.text("bronze_schema", "eacc_ecommerce_bronze")
dbutils.widgets.text("silver_schema", "eacc_ecommerce_silver")

catalog = dbutils.widgets.get("catalog").strip()
bronze_schema = dbutils.widgets.get("bronze_schema").strip()
silver_schema = dbutils.widgets.get("silver_schema").strip()

def bronze(table_name: str) -> str:
    return f"`{catalog}`.`{bronze_schema}`.`raw_{table_name}`"

def silver(table_name: str) -> str:
    return f"`{catalog}`.`{silver_schema}`.`{table_name}`"

def write_silver(df, table_name: str):
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(silver(table_name))

# COMMAND ----------

stg_users = (
    spark.table(bronze("users"))
    .select(
        col("id").alias("customer_id"),
        "first_name",
        "last_name",
        "email",
        "age",
        "gender",
        "country",
        "state",
        "city",
        "postal_code",
        "latitude",
        "longitude",
        "traffic_source",
        col("created_at").alias("customer_created_at"),
        to_date("created_at").alias("customer_created_date"),
    )
)
write_silver(stg_users, "stg_users")

stg_orders = (
    spark.table(bronze("orders"))
    .select(
        "order_id",
        col("user_id").alias("customer_id"),
        col("status").alias("order_status"),
        col("gender").alias("customer_gender"),
        col("created_at").alias("order_created_at"),
        to_date("created_at").alias("order_created_date"),
        "returned_at",
        to_date("returned_at").alias("returned_date"),
        "shipped_at",
        to_date("shipped_at").alias("shipped_date"),
        "delivered_at",
        to_date("delivered_at").alias("delivered_date"),
        "num_of_item",
    )
)
write_silver(stg_orders, "stg_orders")

stg_order_items = (
    spark.table(bronze("order_items"))
    .select(
        col("id").alias("order_item_id"),
        "order_id",
        col("user_id").alias("customer_id"),
        "product_id",
        "inventory_item_id",
        col("status").alias("item_status"),
        col("created_at").alias("order_item_created_at"),
        to_date("created_at").alias("order_item_created_date"),
        "shipped_at",
        to_date("shipped_at").alias("shipped_date"),
        "delivered_at",
        to_date("delivered_at").alias("delivered_date"),
        "returned_at",
        to_date("returned_at").alias("returned_date"),
        "sale_price",
    )
)
write_silver(stg_order_items, "stg_order_items")

stg_products = (
    spark.table(bronze("products"))
    .select(
        col("id").alias("product_id"),
        col("name").alias("product_name"),
        "brand",
        "category",
        "department",
        "sku",
        "cost",
        "retail_price",
        "distribution_center_id",
    )
)
write_silver(stg_products, "stg_products")

stg_distribution_centers = (
    spark.table(bronze("distribution_centers"))
    .select(
        col("id").alias("distribution_center_id"),
        col("name").alias("distribution_center_name"),
        col("latitude").alias("distribution_center_latitude"),
        col("longitude").alias("distribution_center_longitude"),
    )
)
write_silver(stg_distribution_centers, "stg_distribution_centers")

stg_events = (
    spark.table(bronze("events"))
    .select(
        col("id").alias("event_id"),
        col("user_id").alias("customer_id"),
        "session_id",
        "sequence_number",
        col("created_at").alias("event_created_at"),
        to_date("created_at").alias("event_created_date"),
        "ip_address",
        "city",
        "state",
        "postal_code",
        "browser",
        "traffic_source",
        "uri",
        "event_type",
    )
)
write_silver(stg_events, "stg_events")

# COMMAND ----------

row_counts = []
for table_name in [
    "stg_users",
    "stg_orders",
    "stg_order_items",
    "stg_products",
    "stg_distribution_centers",
    "stg_events",
]:
    row_counts.append((table_name, spark.table(silver(table_name)).count()))

display(spark.createDataFrame(row_counts, ["silver_table", "row_count"]))
