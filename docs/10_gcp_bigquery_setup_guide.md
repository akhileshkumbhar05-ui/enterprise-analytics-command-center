# GCP and BigQuery Setup Guide

## Goal

Create a Google Cloud project, confirm BigQuery access, and run the first query against the e-commerce public dataset.

## Recommended Setup

For this project, use the Google Cloud free trial with billing enabled and budget alerts.

Why:

- The project is meant to demonstrate deployable cloud skills.
- Later steps may need saved tables, dbt jobs, Power BI connections, and possibly Cloud Storage.
- BigQuery public datasets are hosted by Google; you pay for the queries you run, not for storing the public source data.

If you do not want to add billing yet, BigQuery Sandbox can work for initial exploration, but it has limitations and is less ideal for a portfolio-grade build.

Official docs:

- Create Google Cloud projects: https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects
- BigQuery Sandbox: https://docs.cloud.google.com/bigquery/docs/sandbox
- BigQuery public datasets: https://docs.cloud.google.com/bigquery/public-data

## Step 1: Open Google Cloud Console

Go to:

https://console.cloud.google.com/

Sign in with the Google account you want to use for the project.

## Step 2: Create a New Project

1. Click the project selector in the top navigation bar.
2. Click `New Project`.
3. Use a clear project name:

```text
Enterprise Analytics Command Center
```

4. Choose or edit the project ID. It must be globally unique and cannot be changed later.

Suggested pattern:

```text
eacc-analytics-yourname
```

or

```text
da-ecommerce-command-center
```

If Google says the ID is taken, add initials or numbers.

5. Click `Create`.

## Step 3: Copy Your Project ID

After the project is created:

1. Open the project selector again.
2. Select your new project.
3. Copy the `Project ID`.

Send that ID back into this thread. We will use it in SQL like this:

```sql
`your_project_id.ecom_raw.orders`
```

## Step 4: Enable or Confirm BigQuery

In most new Google Cloud projects, BigQuery is enabled automatically.

To confirm:

1. In the search bar, type `BigQuery`.
2. Open BigQuery.
3. If prompted, click `Enable`.

If you need to enable it manually:

1. Go to `APIs & Services`.
2. Click `Enable APIs and Services`.
3. Search for `BigQuery API`.
4. Click `Enable`.

## Step 5: Set a Budget Alert

This is important even if you have free credits.

1. Search for `Billing`.
2. Open `Budgets & alerts`.
3. Create a budget for the project.
4. Suggested starting budget:

```text
$10 monthly
```

5. Add alerts at:

```text
50%, 90%, 100%
```

## Step 6: Open BigQuery Studio

1. Search for `BigQuery`.
2. Open `BigQuery`.
3. Make sure your project is selected in the Explorer panel.

## Step 7: Find the Public E-commerce Dataset

In BigQuery Explorer:

1. Click `+ Add`.
2. Choose `Star a project by name` or search public datasets.
3. Add this project:

```text
bigquery-public-data
```

4. Expand:

```text
bigquery-public-data
```

5. Look for:

```text
thelook_ecommerce
```

If you cannot find it, use the query directly. BigQuery can still query fully qualified public table names.

## Step 8: Run the First Query

Open a new SQL query tab and run:

```sql
SELECT
  COUNT(*) AS order_count,
  COUNT(DISTINCT user_id) AS customer_count,
  MIN(created_at) AS first_order_date,
  MAX(created_at) AS last_order_date
FROM `bigquery-public-data.thelook_ecommerce.orders`;
```

Expected result:

- One row with order count, customer count, first order date, and last order date.

## Step 9: Run the First Profiling Query

```sql
SELECT
  status,
  COUNT(*) AS orders
FROM `bigquery-public-data.thelook_ecommerce.orders`
GROUP BY status
ORDER BY orders DESC;
```

This confirms the order lifecycle statuses available for dashboard metrics.

## Step 10: Create Our Project Datasets

After the first query works, create these datasets in your project:

- `ecom_raw`
- `ecom_staging`
- `ecom_intermediate`
- `ecom_marts`
- `analytics_quality`

In BigQuery UI:

1. In Explorer, click the three dots next to your project.
2. Click `Create dataset`.
3. Use location `US` unless your project/default setup requires something else.
4. Repeat for each dataset.

## What To Send Me Next

Send:

1. Your Google Cloud `Project ID`.
2. Whether the first query ran successfully.
3. Any error message if it failed.

Then I will create the exact SQL scripts for:

- Dataset creation.
- Raw table/view setup.
- Source profiling.
- First staging models.
- First mart tables for Power BI.

