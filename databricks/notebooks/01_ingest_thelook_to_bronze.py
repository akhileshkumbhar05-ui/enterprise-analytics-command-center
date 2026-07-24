# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Ingest TheLook To Bronze
# MAGIC
# MAGIC Loads TheLook e-commerce source data into Bronze Delta tables.
# MAGIC
# MAGIC Preferred mode: `gcs_parquet`
# MAGIC
# MAGIC Alternative mode: `bigquery`

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

dbutils.widgets.text("catalog", "main")
dbutils.widgets.text("bronze_schema", "eacc_ecommerce_bronze")
dbutils.widgets.dropdown("source_mode", "gcs_parquet", ["gcs_parquet", "bigquery"])
dbutils.widgets.text("gcs_raw_path", "gs://YOUR_GCS_BUCKET_NAME/eacc/thelook")
dbutils.widgets.text("bigquery_billing_project", "enterprise-analytics-cc")

catalog = dbutils.widgets.get("catalog").strip()
bronze_schema = dbutils.widgets.get("bronze_schema").strip()
source_mode = dbutils.widgets.get("source_mode").strip()
gcs_raw_path = dbutils.widgets.get("gcs_raw_path").strip().rstrip("/")
bigquery_billing_project = dbutils.widgets.get("bigquery_billing_project").strip()

source_tables = [
    "users",
    "orders",
    "order_items",
    "products",
    "inventory_items",
    "distribution_centers",
    "events",
]

def target_table(table_name: str) -> str:
    return f"`{catalog}`.`{bronze_schema}`.`raw_{table_name}`"

def read_source_table(table_name: str):
    if source_mode == "gcs_parquet":
        return spark.read.format("parquet").load(f"{gcs_raw_path}/{table_name}/")

    if source_mode == "bigquery":
        return (
            spark.read.format("bigquery")
            .option("parentProject", bigquery_billing_project)
            .option("table", f"bigquery-public-data.thelook_ecommerce.{table_name}")
            .load()
        )

    raise ValueError(f"Unsupported source_mode: {source_mode}")

row_counts = []

for table_name in source_tables:
    df = (
        read_source_table(table_name)
        .withColumn("_ingested_at", current_timestamp())
        .withColumn("_source_system", lit("thelook_ecommerce"))
        .withColumn("_source_table", lit(table_name))
    )

    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(target_table(table_name))
    row_counts.append((table_name, df.count(), target_table(table_name)))

display(spark.createDataFrame(row_counts, ["source_table", "rows_loaded", "bronze_table"]))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Certification Practice Notes
# MAGIC
# MAGIC This notebook supports:
# MAGIC
# MAGIC - Data ingestion and loading.
# MAGIC - Delta Lake table creation.
# MAGIC - Cloud source connectivity.
# MAGIC - Batch ingestion patterns.
