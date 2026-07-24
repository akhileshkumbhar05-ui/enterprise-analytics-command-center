# Databricks Data Engineer Associate Certification Alignment

## Current Official Exam Snapshot

As of July 2026, Databricks lists the Data Engineer Associate exam as:

- Proctored certification.
- 45 scored multiple-choice questions.
- 90 minutes.
- Registration fee: `USD 200`.
- No formal prerequisites.
- Recommended: hands-on experience performing the exam-guide data engineering tasks.
- Validity: 2 years.

Current official exam domains:

| Domain | Weight |
|---|---:|
| Databricks Intelligence Platform | 6% |
| Data Ingestion and Loading | 21% |
| Data Transformation and Modeling | 22% |
| Working with Lakeflow Jobs | 16% |
| Implementing CI/CD | 10% |
| Troubleshooting, Monitoring, and Optimization | 10% |
| Governance and Security | 15% |

Official source:

https://www.databricks.com/learn/certification/data-engineer-associate

## How This Project Maps To The Exam

### Databricks Intelligence Platform

Project evidence:

- Workspace, catalog, schema, SQL Warehouse, notebooks.
- Clear separation of Bronze, Silver, and Gold layers.

Artifacts:

- `databricks/notebooks/00_workspace_setup.py`
- `docs/12_databricks_tableau_pivot_plan.md`

### Data Ingestion and Loading

Project evidence:

- Export source data from BigQuery to GCS Parquet.
- Load files into Bronze Delta tables.
- Optional direct BigQuery connector ingestion.
- Prep for Auto Loader patterns.

Artifacts:

- `sql/bigquery/06_export_thelook_to_gcs_parquet.sql`
- `databricks/notebooks/01_ingest_thelook_to_bronze.py`

### Data Transformation and Modeling

Project evidence:

- Bronze to Silver cleaning.
- Silver to Gold dimensional marts.
- Fact/dimension design.
- Product, customer, order, cohort, session models.

Artifacts:

- `databricks/notebooks/02_transform_bronze_to_silver.py`
- `databricks/notebooks/03_build_gold_marts.py`

### Working With Lakeflow Jobs

Project evidence to add:

- Create a job with tasks:
  - ingest bronze
  - transform silver
  - build gold
  - run quality checks
  - refresh Tableau views

Artifact to add later:

- `databricks/jobs/ecommerce_lakehouse_job.yml`

### Implementing CI/CD

Project evidence to add:

- Databricks Asset Bundle or Git-backed repo integration.
- Bundle validation.
- Environment-specific variables.

Artifact to add later:

- `databricks/bundle/databricks.yml`

### Troubleshooting, Monitoring, and Optimization

Project evidence:

- Quality table.
- Row counts and relationship checks.
- Later: optimize, z-order, vacuum, and analyze notes.

Artifacts:

- `databricks/notebooks/04_quality_checks.py`

### Governance and Security

Project evidence to add:

- Unity Catalog naming.
- Least-privilege notes.
- No committed secrets.
- Service account/key handling outside the repo.
- Tableau OAuth or token-auth notes.

Artifacts:

- `.gitignore`
- `tableau/01_databricks_connection_guide.md`

## Study Strategy

Use the project as the study spine:

1. Learn the concept.
2. Implement it in this e-commerce pipeline.
3. Document the artifact.
4. Convert it into a resume bullet and interview story.

This keeps certification study from becoming passive video watching.
