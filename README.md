# Enterprise Analytics Command Center

An end-to-end, cloud-first analytics portfolio project designed for Data Analyst, Business Analyst, BI Analyst, and junior Analytics Engineering roles.

## Goal

Build a deployable analytics platform that proves you can:

- Query and model business data with advanced SQL.
- Clean, validate, and automate analysis with Python.
- Design star-schema analytical marts and documented metrics.
- Build executive-ready Power BI dashboards.
- Work with large public datasets in cloud warehouses and lakehouse tools.
- Produce business analyst artifacts: requirements, user stories, process maps, UAT, and stakeholder-ready recommendations.

## Positioning

This is not a single-dashboard project. It is a multi-domain analytics platform with repeatable patterns across:

- E-commerce and product analytics
- Marketing funnel and customer retention
- Finance, banking, and risk
- Healthcare quality and operations
- Logistics and operational performance

## Primary Stack

- Warehouse / source system: BigQuery
- Lakehouse / big data: Databricks + PySpark + Delta-style medallion modeling
- Transformations: dbt
- Quality: dbt tests plus Python validation checks
- BI: Power BI first, Tableau track added for Databricks-connected dashboards
- Documentation: Markdown, metric dictionary, data catalog, BA artifacts
- CI / deployment evidence: GitHub Actions or dbt Cloud jobs

## Core Deliverables

- Cloud warehouse with raw, staging, intermediate, and mart layers
- Domain-specific analytical marts
- Power BI semantic model with DAX measures and documented KPIs
- Executive dashboard suite
- SQL case-study library
- Python notebooks and/or scripts for EDA, data quality, forecasting, and segmentation
- BA portfolio pack
- Resume bullets and interview talking points tied to real artifacts

## Repo Map

- `docs/`: market study, project charter, architecture, dashboard spec, and roadmap
- `data_catalog/`: datasets, source notes, schemas, and data quality expectations
- `sql/`: reusable SQL analyses and interview-grade query examples
- `python/`: cleaning, validation, EDA, and modeling scripts/notebooks
- `dbt/`: dbt project workspace
- `databricks/`: Databricks notebooks, SQL views, and Lakehouse build assets
- `powerbi/`: dashboard specs, screenshots, measure catalog, deployment notes
- `tableau/`: Tableau connection and dashboard plan for Databricks Gold tables
- `ba_artifacts/`: requirements, user stories, process maps, UAT, traceability
- `portfolio/`: final case-study narrative, demo script, resume bullets

## First Build Target

The first vertical slice should be e-commerce and marketing analytics using BigQuery public datasets. It gives the strongest immediate story for junior analyst interviews:

- Revenue and margin trends
- Customer acquisition and repeat purchase behavior
- Product/category performance
- Funnel and cohort analysis
- Returns or fulfillment issues
- Executive recommendations

After the first vertical slice works end to end, the same architecture expands into healthcare, finance, and logistics modules.

## Current Pivot

The active build path is now:

```text
BigQuery public e-commerce source
  -> GCS Parquet export or Databricks BigQuery connector
  -> Databricks Bronze Delta tables
  -> Silver cleaned tables
  -> Gold dimensional marts
  -> Tableau dashboard
```

This preserves the work already completed in BigQuery while adding hands-on practice for the Databricks Certified Data Engineer Associate exam.
