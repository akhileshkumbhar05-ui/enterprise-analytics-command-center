# Databricks notebook source
# MAGIC %md
# MAGIC # 00 - Workspace Setup
# MAGIC
# MAGIC Create the schemas used by the e-commerce Lakehouse pipeline.

# COMMAND ----------

dbutils.widgets.text("catalog", "main")
dbutils.widgets.text("bronze_schema", "eacc_ecommerce_bronze")
dbutils.widgets.text("silver_schema", "eacc_ecommerce_silver")
dbutils.widgets.text("gold_schema", "eacc_ecommerce_gold")
dbutils.widgets.text("quality_schema", "eacc_quality")

catalog = dbutils.widgets.get("catalog").strip()
schemas = [
    dbutils.widgets.get("bronze_schema").strip(),
    dbutils.widgets.get("silver_schema").strip(),
    dbutils.widgets.get("gold_schema").strip(),
    dbutils.widgets.get("quality_schema").strip(),
]

for schema in schemas:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{catalog}`.`{schema}`")

display(spark.createDataFrame([(catalog, schema) for schema in schemas], ["catalog", "schema_created"]))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Naming
# MAGIC
# MAGIC - Bronze tables: `raw_<source_table>`
# MAGIC - Silver tables: `stg_<business_entity>`
# MAGIC - Gold tables: `dim_*`, `fact_*`
# MAGIC - Quality tables: validation and reconciliation outputs
