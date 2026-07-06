# Power BI BigQuery Connection Guide

## Goal

Connect Power BI Desktop to the curated BigQuery marts in:

```text
enterprise-analytics-cc.ecom_marts
```

and the data quality table in:

```text
enterprise-analytics-cc.analytics_quality
```

## Official Reference

Microsoft Google BigQuery connector documentation:

https://learn.microsoft.com/en-us/power-query/connectors/google-bigquery

## Recommended Mode

Use `Import` mode for the first portfolio dashboard.

Why:

- The e-commerce mart tables are small enough for import.
- Dashboard interactions will be fast.
- DAX modeling is easier.
- It avoids unnecessary BigQuery query costs during every report interaction.

Use `DirectQuery` later only if we intentionally want to demonstrate live warehouse querying.

## Step 1: Open Power BI Desktop

Open Power BI Desktop.

## Step 2: Get Data

Go to:

```text
Home > Get data > More
```

Search for:

```text
Google BigQuery
```

Choose the standard `Google BigQuery` connector.

## Step 3: Connect

If Power BI asks for a billing/project ID, use:

```text
enterprise-analytics-cc
```

Choose:

```text
Import
```

Sign in with the same Google account you used for BigQuery.

## Step 4: Select Tables

Load only curated tables, not raw or staging views.

From `ecom_marts`, select:

- `dim_date`
- `dim_customer`
- `dim_product`
- `fact_order_items`
- `fact_orders`
- `fact_customer_cohorts`
- `fact_sessions`

From `analytics_quality`, select:

- `ecommerce_quality_checks`

Do not load:

- `ecom_raw`
- `ecom_staging`
- `ecom_intermediate`

## Step 5: Transform Data

Click `Transform Data` before loading if Power BI offers the option.

In Power Query:

- Confirm ID columns are whole number or text consistently.
- Confirm date columns are date type.
- Confirm timestamp columns are date/time type.
- Confirm revenue/cost/profit columns are decimal number or fixed decimal number.
- Rename tables if needed to clean display names.

Then click:

```text
Close & Apply
```

## Step 6: Model View

After loading, go to Model view and create/check relationships from:

- `dim_date`
- `dim_customer`
- `dim_product`

to the fact tables.

Use the relationship guide:

```text
powerbi/02_model_relationships.md
```

## Step 7: Create Measure Table

In Power BI:

1. Go to `Home`.
2. Click `Enter data`.
3. Create one blank column called `MeasureTable`.
4. Add one row with value `Measures`.
5. Name the table:

```text
_Measures
```

6. Hide the `MeasureTable` column after creating your first measure.

Then create DAX measures from:

```text
powerbi/03_dax_measure_starter_pack.md
```

## Troubleshooting

### Access Denied / jobs.create Error

If Power BI says your user lacks `bigquery.jobs.create`, enter this as the Billing Project ID:

```text
enterprise-analytics-cc
```

Also confirm that you are signed in with the Google account that created the project.

### Missing Tables

Refresh the BigQuery Explorer and confirm that the tables exist in:

```text
enterprise-analytics-cc.ecom_marts
```

If they exist in BigQuery but not Power BI, reconnect or refresh the Navigator.

