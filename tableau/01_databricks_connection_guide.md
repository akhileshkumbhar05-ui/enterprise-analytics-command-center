# Tableau Databricks Connection Guide

## Goal

Connect Tableau Desktop or Tableau Cloud to Databricks Gold tables/views.

## Preferred Data Source

Use the Tableau-facing views from:

```text
main.eacc_ecommerce_gold
```

Views:

- `vw_executive_monthly`
- `vw_product_performance`
- `vw_sessions_by_source`
- `vw_cohort_retention`

## Databricks Setup

In Databricks:

1. Create or start a SQL Warehouse.
2. Open the SQL Warehouse connection details.
3. Copy:
   - Server Hostname
   - HTTP Path
4. Confirm the catalog and schema:

```text
main.eacc_ecommerce_gold
```

## Tableau Desktop Connection

In Tableau Desktop:

1. Open Tableau.
2. Select `Connect > To a Server > Databricks`.
3. Enter:
   - Server Hostname
   - HTTP Path
4. Use OAuth if available.
5. If using token auth, generate a Databricks personal access token and use it as the password.
6. Select the catalog and schema.
7. Connect to the Tableau views.

## Tableau Cloud Option

Databricks supports Partner Connect and "Explore in Tableau Cloud" flows for Unity Catalog data. If available in your workspace, this is the fastest way to move from a Databricks schema/table to a Tableau Cloud workbook.

## Official References

- Databricks Tableau docs: https://docs.databricks.com/aws/en/partners/bi/tableau
- Tableau Databricks connector help: https://help.tableau.com/current/pro/desktop/en-us/examples_databricks.htm
