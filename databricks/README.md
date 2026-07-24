# Databricks Workspace

This folder contains Databricks notebook source files and SQL assets for rebuilding the e-commerce analytics project as a Lakehouse pipeline.

## Run Order

1. `notebooks/00_workspace_setup.py`
2. `notebooks/01_ingest_thelook_to_bronze.py`
   - Optional certification-focused version: `notebooks/01a_ingest_thelook_with_autoloader.py`
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
BigQuery -> GCS Parquet -> Databricks Bronze
```

Alternative path:

```text
BigQuery connector -> Databricks Bronze
```

The GCS Parquet path practices ingestion and Lakehouse patterns more directly, which is better for Data Engineer Associate preparation.
