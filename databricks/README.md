# Databricks Workspace

This folder contains Databricks notebook source files and SQL assets for rebuilding the e-commerce analytics project as a Lakehouse pipeline.

## Run Order

1. `notebooks/00_workspace_setup.py`
2. `notebooks/01_ingest_thelook_to_bronze.py`
   - In Databricks Free Edition, set `stage_public_gcs_to_volume` to `true` once to copy exported public GCS Parquet files into the managed Volume.
   - After the Volume is populated, keep `source_mode = gcs_parquet` and `gcs_raw_path = /Volumes/workspace/eacc_ecommerce_bronze/raw_files/thelook`.
   - Optional certification-focused version: `notebooks/01a_ingest_thelook_with_autoloader.py`.
3. `notebooks/02_transform_bronze_to_silver.py`
4. `notebooks/03_build_gold_marts.py`
5. `notebooks/04_quality_checks.py`
6. `sql/05_tableau_views.sql`

## Target Layers

- Bronze: source-aligned Delta tables.
- Silver: cleaned and standardized Delta tables.
- Gold: dimensional marts for Tableau.

## Source Options

Preferred first path:

```text
BigQuery -> GCS Parquet -> Databricks managed Volume -> Bronze Delta
```

Alternative path:

```text
BigQuery connector -> Databricks Bronze
```

The GCS Parquet path practices ingestion and Lakehouse patterns more directly, which is better for Data Engineer Associate preparation.

## Free Edition Notes

- Use the `workspace` catalog unless your workspace shows a different catalog.
- Serverless compute does not support direct `spark.sparkContext` Hadoop configuration, so the project uses Databricks managed Volumes instead of notebook-level GCS connector settings.
- The temporary public-read bucket approach is only for exported public sample data. Remove `allUsers` access from the GCS bucket after staging files into the managed Volume.
