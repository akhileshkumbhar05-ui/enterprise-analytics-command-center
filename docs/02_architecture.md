# Cloud Architecture

## Guiding Principle

Local files should store code, documentation, and portfolio assets. Data processing, warehouse modeling, and BI delivery should happen in cloud tools so the project demonstrates deployable capability.

## Target Architecture

```text
Public datasets / APIs
        |
        v
Cloud landing layer
        |
        v
BigQuery raw datasets --------------+
        |                            |
        v                            v
dbt staging/intermediate/marts    Databricks PySpark lakehouse experiments
        |                            |
        +------------+---------------+
                     |
                     v
Curated analytical marts
                     |
        +------------+------------+
        |                         |
        v                         v
Power BI semantic model        Snowflake replication / marketplace module
        |
        v
Power BI Service dashboard suite
```

## Layers

### Raw

Preserve source shape with minimal changes. Store source load date, source system, and file/table metadata when applicable.

### Staging

Clean names, cast types, standardize dates, handle nulls, deduplicate, and apply basic source-specific validation.

### Intermediate

Business logic that combines staging tables into reusable entities such as orders, customers, sessions, providers, trips, loans, or facilities.

### Marts

Fact and dimension tables designed for Power BI:

- `fact_orders`
- `fact_sessions`
- `fact_customer_cohorts`
- `fact_healthcare_measures`
- `fact_trips`
- `fact_mortgage_applications`
- `dim_customer`
- `dim_product`
- `dim_date`
- `dim_location`
- `dim_provider`
- `dim_institution`

## Tools By Purpose

### BigQuery

Use as the first warehouse because it has strong public datasets and clean Power BI connectivity.

### Snowflake

Use for cross-platform exposure, marketplace/public datasets, and to prove you can work outside one vendor ecosystem.

### Databricks

Use for the big data layer: PySpark transformations, large-scale feature engineering, and medallion architecture evidence.

### dbt

Use for model organization, tests, docs, lineage, and transformation reproducibility.

### Power BI

Use as the main BI layer:

- Import mode for curated marts.
- DirectQuery only where justified.
- Star schema model.
- DAX measure table.
- KPI tooltips.
- Drillthrough pages.
- Row-level security demonstration.
- Refresh/deployment notes.

### GitHub Actions or dbt Cloud

Use for CI evidence:

- SQL lint or dbt parse/build.
- dbt tests.
- Python validation tests.
- Documentation checks.

## Data Quality Controls

Minimum checks:

- Row count by source and load date.
- Primary key uniqueness.
- Foreign key relationship integrity.
- Null checks for required fields.
- Accepted values for status fields.
- Date sanity checks.
- Revenue/fare/amount non-negative checks.
- Reconciliation checks between source totals and mart totals.

## Security and Governance Evidence

- No private or sensitive personal data.
- Public datasets only.
- Data dictionary and metric dictionary.
- Clearly documented assumptions and limitations.
- Power BI row-level security demo, even if using synthetic regions or business units.
- Change log for KPI definitions.

