# Databricks and Tableau Pivot Plan

## Decision

Do not abandon the e-commerce project. Transfer it into Databricks.

The business case, KPI logic, and BigQuery source profiling already have value. The next move is to rebuild the same e-commerce analytics pipeline in Databricks using Delta tables, PySpark, Lakehouse modeling, data quality checks, jobs, and Tableau.

## Target Architecture

```text
BigQuery public dataset: thelook_ecommerce
        |
        | Option A: BigQuery -> GCS Parquet export
        | Option B: Databricks BigQuery connector
        v
Databricks Bronze Delta tables
        |
        v
Databricks Silver cleaned tables
        |
        v
Databricks Gold dimensional marts
        |
        v
Databricks SQL Warehouse
        |
        v
Tableau dashboard
```

## Recommended Path

Use Option A first:

1. Export TheLook source tables from BigQuery to GCS as Parquet.
2. Ingest those Parquet files into Databricks Bronze Delta tables.
3. Transform Bronze to Silver with PySpark.
4. Build Gold dimensional marts in Delta.
5. Connect Tableau to Databricks.

Why this path:

- It practices cloud file ingestion.
- It prepares for Auto Loader and Lakeflow concepts.
- It avoids treating Databricks as just another SQL client.
- It gives a cleaner Data Engineer Associate story.

Use Option B later:

- Read directly from BigQuery using Databricks' BigQuery connector.
- This is useful for interoperability, but it practices less of the lakehouse ingestion pattern.

## What Transfers From BigQuery

Already completed:

- Source understanding.
- KPI definitions.
- BigQuery SQL model logic.
- Data quality checks.
- Business analyst artifacts.
- E-commerce dashboard plan.

To rebuild in Databricks:

- Raw views become Bronze Delta tables.
- Staging views become Silver Delta tables.
- BigQuery marts become Gold Delta tables.
- BigQuery quality checks become a Delta quality table.
- Power BI model becomes Tableau data source / workbook.

## Databricks Skills Practiced

- Workspace setup.
- Notebook development.
- PySpark DataFrames.
- Spark SQL.
- Delta Lake managed tables.
- Medallion architecture.
- Data ingestion from cloud storage.
- Batch and incremental ingestion patterns.
- Data quality checks.
- SQL Warehouse consumption.
- Tableau connectivity.
- Job orchestration readiness.
- Unity Catalog naming and access patterns.

## Immediate Next Steps

1. Create a Databricks Free Edition or trial workspace.
2. Create a GCS bucket in the existing Google Cloud project.
3. Run `sql/bigquery/06_export_thelook_to_gcs_parquet.sql` after replacing the bucket placeholder.
4. Import notebooks from `databricks/notebooks/`.
5. Run notebooks in order from `00` through `04`.
6. Run Tableau SQL views from `databricks/sql/05_tableau_views.sql`.
7. Connect Tableau.

## Tool Choice

Use Databricks Free Edition if it supports the needed workspace features for your account. Databricks describes Free Edition as a no-cost workspace for students, educators, hobbyists, and learners, with serverless, quota-limited access for notebooks, SQL, dashboards, and pipelines.

Use a full trial if the BigQuery connector, GCS access, SQL Warehouse, or Tableau integration is limited in Free Edition.

References:

- Databricks Free Edition: https://www.databricks.com/learn/free-edition
- Databricks Free Edition docs: https://docs.databricks.com/aws/en/getting-started/free-edition
- Google guide for connecting Databricks to BigQuery: https://docs.cloud.google.com/bigquery/docs/connect-databricks
- Databricks Tableau connection docs: https://docs.databricks.com/aws/en/partners/bi/tableau
