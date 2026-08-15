# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Ingest TheLook To Bronze
# MAGIC
# MAGIC Loads TheLook e-commerce source data into Bronze Delta tables.
# MAGIC
# MAGIC Free Edition path:
# MAGIC
# MAGIC 1. Export BigQuery public data to GCS as Parquet.
# MAGIC 2. Temporarily allow public read on the exported sample dataset.
# MAGIC 3. Set `stage_public_gcs_to_volume` to `true` once.
# MAGIC 4. Read from the managed Volume path into Bronze Delta tables.
# MAGIC
# MAGIC Alternative mode: `bigquery`

# COMMAND ----------

import json
import os
import urllib.parse
import urllib.request

from pyspark.sql.functions import current_timestamp, lit

dbutils.widgets.text("catalog", "workspace")
dbutils.widgets.text("bronze_schema", "eacc_ecommerce_bronze")
dbutils.widgets.dropdown("source_mode", "gcs_parquet", ["gcs_parquet", "bigquery"])
dbutils.widgets.text("gcs_raw_path", "/Volumes/workspace/eacc_ecommerce_bronze/raw_files/thelook")
dbutils.widgets.dropdown("stage_public_gcs_to_volume", "false", ["false", "true"])
dbutils.widgets.text("public_gcs_bucket", "eacc-thelook-raw-akhil-20260724")
dbutils.widgets.text("public_gcs_prefix", "eacc/thelook")
dbutils.widgets.text("volume_name", "raw_files")
dbutils.widgets.text("bigquery_billing_project", "enterprise-analytics-cc")

catalog = dbutils.widgets.get("catalog").strip()
bronze_schema = dbutils.widgets.get("bronze_schema").strip()
source_mode = dbutils.widgets.get("source_mode").strip()
gcs_raw_path = dbutils.widgets.get("gcs_raw_path").strip().rstrip("/")
stage_public_gcs_to_volume = dbutils.widgets.get("stage_public_gcs_to_volume").strip().lower() == "true"
public_gcs_bucket = dbutils.widgets.get("public_gcs_bucket").strip()
public_gcs_prefix = dbutils.widgets.get("public_gcs_prefix").strip().strip("/")
volume_name = dbutils.widgets.get("volume_name").strip()
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

# COMMAND ----------

def list_public_gcs_objects(bucket_name: str, prefix: str) -> list[str]:
    encoded_prefix = urllib.parse.quote(prefix, safe="")
    url = f"https://storage.googleapis.com/storage/v1/b/{bucket_name}/o?prefix={encoded_prefix}"

    with urllib.request.urlopen(url) as response:
        payload = json.load(response)

    return [
        item["name"]
        for item in payload.get("items", [])
        if item["name"].endswith(".parquet")
    ]


if stage_public_gcs_to_volume:
    spark.sql(f"CREATE VOLUME IF NOT EXISTS `{catalog}`.`{bronze_schema}`.`{volume_name}`")

    volume_base = f"/Volumes/{catalog}/{bronze_schema}/{volume_name}/thelook"
    download_results = []

    for table_name in source_tables:
        target_dir = f"{volume_base}/{table_name}"
        os.makedirs(target_dir, exist_ok=True)

        objects = list_public_gcs_objects(public_gcs_bucket, f"{public_gcs_prefix}/{table_name}/")

        for object_name in objects:
            file_name = os.path.basename(object_name)
            target_path = f"{target_dir}/{file_name}"
            object_url = f"https://storage.googleapis.com/{public_gcs_bucket}/{urllib.parse.quote(object_name, safe='/')}"
            urllib.request.urlretrieve(object_url, target_path)

        download_results.append((table_name, len(objects), target_dir))

    display(spark.createDataFrame(download_results, ["source_table", "files_downloaded", "volume_path"]))
else:
    print(f"Skipping Volume staging. Reading source files from {gcs_raw_path}.")

# COMMAND ----------

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
