# GCS Bucket and Databricks Export Guide

## Goal

Create a Google Cloud Storage bucket and export the TheLook e-commerce source tables as Parquet files for Databricks ingestion.

## Why This Exists

The BigQuery work created a clean source understanding and analytics marts. The Databricks build should practice Lakehouse ingestion, so the preferred path is:

```text
BigQuery source tables -> GCS Parquet files -> Databricks Bronze Delta tables
```

This is better Data Engineer Associate practice than only connecting Databricks directly to BigQuery.

## Step 1: Create A GCS Bucket

In Google Cloud Console:

1. Search for `Cloud Storage`.
2. Open `Buckets`.
3. Click `Create`.
4. Use a globally unique bucket name.

Suggested pattern:

```text
enterprise-analytics-cc-ecommerce-raw-ak
```

5. Location type:

```text
Multi-region
```

6. Location:

```text
US
```

7. Storage class:

```text
Standard
```

8. Keep public access prevention enabled.
9. Create the bucket.

## Step 2: Update The Export Script

Open:

```text
sql/bigquery/06_export_thelook_to_gcs_parquet.sql
```

Replace:

```text
YOUR_GCS_BUCKET_NAME
```

with your actual bucket name.

Example:

```text
enterprise-analytics-cc-ecommerce-raw-ak
```

## Step 3: Run The Export Script In BigQuery

Run the updated script in BigQuery Studio.

Expected folders in the bucket:

- `eacc/thelook/users/`
- `eacc/thelook/orders/`
- `eacc/thelook/order_items/`
- `eacc/thelook/products/`
- `eacc/thelook/inventory_items/`
- `eacc/thelook/distribution_centers/`
- `eacc/thelook/events/`

Each folder should contain Parquet files.

## Step 4: Use The GCS Path In Databricks

In the Databricks notebook widgets, set:

```text
gcs_raw_path = gs://YOUR_GCS_BUCKET_NAME/eacc/thelook
```

Example:

```text
gcs_raw_path = gs://enterprise-analytics-cc-ecommerce-raw-ak/eacc/thelook
```

## Security Notes

- Do not make the bucket public.
- Do not commit service account JSON keys.
- If Databricks needs service account credentials, store them in Databricks secrets or workspace-approved credential storage.

## Cost Notes

- BigQuery exports are usually much cheaper than repeated full table scans.
- Parquet is compact and columnar, which is better for Databricks ingestion.
- Delete unused exported files when finished if storage cost matters.
