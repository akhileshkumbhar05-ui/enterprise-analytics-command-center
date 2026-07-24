# BigQuery SQL Run Order

Project ID:

```text
enterprise-analytics-cc
```

Run these scripts in BigQuery Studio in order:

1. `00_create_datasets.sql`
2. `01_source_profiling.sql`
   - Optional cheaper variant: `01a_source_profiling_cost_optimized.sql`
3. `02_create_raw_views.sql`
4. `03_create_staging_views.sql`
   - Optional validation: `03a_validate_staging_views.sql`
5. `04_create_core_marts.sql`
   - Optional validation: `04a_validate_core_marts.sql`
6. `05_quality_checks.sql`
7. `06_export_thelook_to_gcs_parquet.sql`
   - Use this only after creating a GCS bucket and replacing `YOUR_GCS_BUCKET_NAME`.

After each script succeeds, save a screenshot or note the row counts. These become portfolio evidence.

## Why Views First?

The public e-commerce data already lives in BigQuery. Raw and staging views keep cost low while giving us clean project-owned layers. The curated mart tables are materialized because Power BI performs better against modeled tables than against deeply nested query chains.

## Cost Notes

`01_source_profiling.sql` is intentionally thorough. It scans source columns to get exact profiling outputs.

`01a_source_profiling_cost_optimized.sql` is a cheaper alternative. It uses metadata row counts/table sizes where possible and samples the large events table for fast exploration.

In BigQuery, always check the message above the results pane before running a query. It tells you how much data the query will process.

## BigQuery Source

Core source dataset:

```text
bigquery-public-data.thelook_ecommerce
```

Main source tables:

- `users`
- `orders`
- `order_items`
- `products`
- `inventory_items`
- `distribution_centers`
- `events`

## Databricks Export Step

`06_export_thelook_to_gcs_parquet.sql` exports the same TheLook source tables to cloud storage so Databricks can ingest them into Bronze Delta tables.
