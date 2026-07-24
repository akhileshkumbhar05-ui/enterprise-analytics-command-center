-- Enterprise Analytics Command Center
-- Step 06: Export TheLook source tables to GCS as Parquet for Databricks ingestion.
--
-- Before running:
-- 1. Create a GCS bucket in the same Google Cloud project.
-- 2. Replace YOUR_GCS_BUCKET_NAME with your actual bucket name.
-- 3. Confirm the bucket location is compatible with BigQuery US multi-region exports.
--
-- Example URI pattern:
-- gs://YOUR_GCS_BUCKET_NAME/eacc/thelook/users/*.parquet

EXPORT DATA OPTIONS (
  uri = 'gs://YOUR_GCS_BUCKET_NAME/eacc/thelook/users/*.parquet',
  format = 'PARQUET',
  overwrite = true
) AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.users`;

EXPORT DATA OPTIONS (
  uri = 'gs://YOUR_GCS_BUCKET_NAME/eacc/thelook/orders/*.parquet',
  format = 'PARQUET',
  overwrite = true
) AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.orders`;

EXPORT DATA OPTIONS (
  uri = 'gs://YOUR_GCS_BUCKET_NAME/eacc/thelook/order_items/*.parquet',
  format = 'PARQUET',
  overwrite = true
) AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.order_items`;

EXPORT DATA OPTIONS (
  uri = 'gs://YOUR_GCS_BUCKET_NAME/eacc/thelook/products/*.parquet',
  format = 'PARQUET',
  overwrite = true
) AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.products`;

EXPORT DATA OPTIONS (
  uri = 'gs://YOUR_GCS_BUCKET_NAME/eacc/thelook/inventory_items/*.parquet',
  format = 'PARQUET',
  overwrite = true
) AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.inventory_items`;

EXPORT DATA OPTIONS (
  uri = 'gs://YOUR_GCS_BUCKET_NAME/eacc/thelook/distribution_centers/*.parquet',
  format = 'PARQUET',
  overwrite = true
) AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.distribution_centers`;

EXPORT DATA OPTIONS (
  uri = 'gs://YOUR_GCS_BUCKET_NAME/eacc/thelook/events/*.parquet',
  format = 'PARQUET',
  overwrite = true
) AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.events`;
