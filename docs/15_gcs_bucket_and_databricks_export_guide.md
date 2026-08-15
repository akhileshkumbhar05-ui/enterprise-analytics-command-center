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

## Step 4: Stage GCS Files Into A Databricks Managed Volume

In Databricks Free Edition, serverless compute may not have a Google Cloud service account attached. If direct `gs://` reads fail, use the managed Volume staging path in:

```text
databricks/notebooks/01_ingest_thelook_to_bronze.py
```

Use these widgets:

```text
catalog = workspace
source_mode = gcs_parquet
stage_public_gcs_to_volume = true
public_gcs_bucket = YOUR_GCS_BUCKET_NAME
public_gcs_prefix = eacc/thelook
gcs_raw_path = /Volumes/workspace/eacc_ecommerce_bronze/raw_files/thelook
```

Run the staging cell once. Then set `stage_public_gcs_to_volume = false` for future reruns and keep reading from the Volume path.

## Security Notes

- Do not make private/company data public.
- For this project, temporary public-read access is acceptable only because the exported dataset comes from BigQuery public sample data.
- Remove `allUsers` bucket access after the Volume has been populated.
- Do not commit service account JSON keys.
- If Databricks needs permanent GCS access, use Workload Identity Federation, service-account based storage credentials, or workspace-approved credential storage instead of committing keys.

## Cost Notes

- BigQuery exports are usually much cheaper than repeated full table scans.
- Parquet is compact and columnar, which is better for Databricks ingestion.
- Delete unused exported files when finished if storage cost matters.
