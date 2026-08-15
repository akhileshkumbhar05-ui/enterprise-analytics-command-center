# Databricks notebook source
# MAGIC %md
# MAGIC # 01a - Ingest TheLook With Auto Loader
# MAGIC
# MAGIC Optional certification-focused ingestion notebook.
# MAGIC
# MAGIC This uses Auto Loader with `cloudFiles` and `availableNow` to process existing Parquet files from cloud storage into Bronze Delta tables.

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

dbutils.widgets.text("catalog", "workspace")
dbutils.widgets.text("bronze_schema", "eacc_ecommerce_bronze")
dbutils.widgets.text("gcs_raw_path", "gs://YOUR_GCS_BUCKET_NAME/eacc/thelook")
dbutils.widgets.text("checkpoint_base_path", "/tmp/eacc/checkpoints/thelook")

catalog = dbutils.widgets.get("catalog").strip()
bronze_schema = dbutils.widgets.get("bronze_schema").strip()
gcs_raw_path = dbutils.widgets.get("gcs_raw_path").strip().rstrip("/")
checkpoint_base_path = dbutils.widgets.get("checkpoint_base_path").strip().rstrip("/")

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

# COMMAND ----------

queries = []

for table_name in source_tables:
    source_path = f"{gcs_raw_path}/{table_name}/"
    checkpoint_path = f"{checkpoint_base_path}/{table_name}"

    stream_df = (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "parquet")
        .load(source_path)
        .withColumn("_ingested_at", current_timestamp())
        .withColumn("_source_system", lit("thelook_ecommerce"))
        .withColumn("_source_table", lit(table_name))
    )

    query = (
        stream_df.writeStream.format("delta")
        .option("checkpointLocation", checkpoint_path)
        .trigger(availableNow=True)
        .toTable(target_table(table_name))
    )
    queries.append((table_name, query))

for table_name, query in queries:
    query.awaitTermination()

# COMMAND ----------

row_counts = []
for table_name in source_tables:
    row_counts.append((table_name, spark.table(target_table(table_name)).count(), target_table(table_name)))

display(spark.createDataFrame(row_counts, ["source_table", "rows_loaded", "bronze_table"]))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Production Note
# MAGIC
# MAGIC `/tmp` is acceptable for learning but not for production checkpoints. In a real workspace, use a Unity Catalog volume or approved cloud storage path for checkpointing.
