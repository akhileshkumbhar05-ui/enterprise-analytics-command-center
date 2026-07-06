# E-commerce Ingestion Runbook

## Goal

Build the first e-commerce analytics vertical slice using cloud-hosted public data.

## First Source Choice

Use TheLook e-commerce in BigQuery as the core transactional source.

Likely source tables:

- `bigquery-public-data.thelook_ecommerce.users`
- `bigquery-public-data.thelook_ecommerce.orders`
- `bigquery-public-data.thelook_ecommerce.order_items`
- `bigquery-public-data.thelook_ecommerce.products`
- `bigquery-public-data.thelook_ecommerce.inventory_items`
- `bigquery-public-data.thelook_ecommerce.distribution_centers`
- `bigquery-public-data.thelook_ecommerce.events`

Use GA4 sample e-commerce as the event/funnel source if TheLook events are not enough.

Likely GA4 source:

- `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`

Official references:

- BigQuery public datasets: https://docs.cloud.google.com/bigquery/public-data
- GA4 sample e-commerce: https://developers.google.com/analytics/bigquery/web-ecommerce-demo-dataset

## Ingestion Pattern 1: Query Public Data In Place

This is the MVP approach.

The public tables already live in BigQuery. We do not need to download files first. We query them directly and create our own tables/views in our project.

Example pattern:

```sql
CREATE OR REPLACE TABLE `your_project.ecom_raw.orders` AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.orders`;
```

Why this is good:

- Fastest path to analysis.
- No local data storage.
- Cloud-native.
- Easy to document.

## Ingestion Pattern 2: Create Staging Views

For lighter cost and faster iteration, staging can start as views:

```sql
CREATE OR REPLACE VIEW `your_project.ecom_staging.stg_orders` AS
SELECT
  order_id,
  user_id,
  status,
  created_at,
  returned_at,
  shipped_at,
  delivered_at,
  num_of_item
FROM `bigquery-public-data.thelook_ecommerce.orders`;
```

Later, dbt will manage this more cleanly.

## Ingestion Pattern 3: External Files or APIs

Use this for later domain modules, not the first e-commerce MVP.

Pattern:

1. Put raw files in Google Cloud Storage.
2. Load into BigQuery raw tables or create external tables.
3. Transform with dbt.
4. Connect Power BI to curated marts.

Example sources:

- CSV from CMS hospital data.
- HMDA or FDIC data downloads.
- SEC financial statement zip files.
- NYC TLC parquet files.

## Ingestion Pattern 4: Databricks Lakehouse

Use this for big data/logistics or event-stream style modules.

Pattern:

1. Raw files land in cloud object storage.
2. Databricks Auto Loader ingests files into bronze tables.
3. PySpark cleans data into silver tables.
4. Gold tables feed analysis and dashboards.

This proves PySpark and big-data ingestion, but it should come after the BigQuery MVP.

## Ingestion Pattern 5: Snowflake Marketplace

Use this for a Snowflake-specific module.

Pattern:

1. Find a free or public Snowflake Marketplace listing.
2. Add/listing access to your Snowflake account.
3. Query the shared database directly.
4. Build finance/economic/domain marts.
5. Either dashboard directly or compare with the BigQuery approach.

## First BigQuery Setup

Create these datasets in your project:

- `ecom_raw`
- `ecom_staging`
- `ecom_intermediate`
- `ecom_marts`
- `analytics_quality`

Suggested location:

- Use `US` multi-region if the public datasets are available there.

## First SQL Checks

Run these before modeling:

```sql
SELECT 'users' AS table_name, COUNT(*) AS row_count
FROM `bigquery-public-data.thelook_ecommerce.users`
UNION ALL
SELECT 'orders', COUNT(*)
FROM `bigquery-public-data.thelook_ecommerce.orders`
UNION ALL
SELECT 'order_items', COUNT(*)
FROM `bigquery-public-data.thelook_ecommerce.order_items`
UNION ALL
SELECT 'products', COUNT(*)
FROM `bigquery-public-data.thelook_ecommerce.products`
UNION ALL
SELECT 'events', COUNT(*)
FROM `bigquery-public-data.thelook_ecommerce.events`;
```

```sql
SELECT
  status,
  COUNT(*) AS orders
FROM `bigquery-public-data.thelook_ecommerce.orders`
GROUP BY status
ORDER BY orders DESC;
```

```sql
SELECT
  MIN(created_at) AS first_order_date,
  MAX(created_at) AS last_order_date,
  COUNT(DISTINCT order_id) AS orders,
  COUNT(DISTINCT user_id) AS customers
FROM `bigquery-public-data.thelook_ecommerce.orders`;
```

## First Modeling Target

Create these curated objects:

- `dim_date`
- `dim_customer`
- `dim_product`
- `fact_orders`
- `fact_order_items`
- `fact_customer_cohorts`
- `fact_events` or `fact_funnel_events`

## First Dashboard Target

Power BI pages:

1. Executive Overview
2. Revenue and Product Performance
3. Customer Retention
4. Funnel and Marketing Behavior
5. Data Quality and Metric Dictionary

