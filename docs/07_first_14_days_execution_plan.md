# First 14 Days Execution Plan

## Objective

Create the first credible vertical slice:

TheLook/GA4 source data -> BigQuery profiling -> dbt marts -> Power BI dashboard -> BA documentation -> portfolio story.

## Day 1: Cloud and Repo Setup

Tasks:

- Create or confirm Google Cloud account.
- Create BigQuery project.
- Pin `bigquery-public-data` in BigQuery Explorer.
- Confirm access to TheLook e-commerce and GA4 sample e-commerce.
- Create Power BI workspace.
- Create GitHub repo and push this scaffold.

Output:

- Screenshot of BigQuery public dataset access.
- Screenshot of Power BI workspace.
- Repo link.

## Day 2: Source Profiling

Tasks:

- Inspect source tables.
- Identify table grain.
- Count rows per table.
- Check nulls and duplicate keys.
- Document source limitations.

Output:

- `data_catalog/ecommerce_source_notes.md`
- SQL profiling queries in `sql/ecommerce/`

## Day 3: Business Questions and KPI Dictionary

Tasks:

- Finalize stakeholder questions.
- Define KPIs.
- Define metric formulas and grain.
- Create assumptions and exclusions.

Output:

- KPI dictionary.
- Requirements log.
- Problem brief.

## Days 4-5: dbt Staging Layer

Tasks:

- Create dbt project.
- Add BigQuery profile.
- Define sources.
- Build staging models.
- Add tests for uniqueness, nulls, and accepted values.

Output:

- `stg_*` models.
- dbt test results.
- dbt docs generated.

## Days 6-7: dbt Mart Layer

Tasks:

- Build date dimension.
- Build customer dimension.
- Build product dimension.
- Build order/order-item facts.
- Build customer cohort fact.
- Build funnel fact if using GA4/events.

Output:

- Star schema ready for Power BI.
- Model lineage.
- Data quality tests.

## Days 8-10: Power BI MVP

Tasks:

- Connect Power BI to BigQuery marts.
- Build semantic model.
- Create DAX measures.
- Build executive overview, revenue/product, customer retention, funnel, and data quality pages.
- Add slicers, drillthrough, and tooltips.

Output:

- `.pbix` file.
- Dashboard screenshots.
- Measure catalog.

## Days 11-12: Python Analytics

Tasks:

- Pull curated marts into Python.
- Run cohort analysis.
- Run segmentation.
- Run anomaly or forecast analysis.
- Write recommendation memo.

Output:

- Python notebook/script.
- Insight memo.
- Exported supporting charts or result tables.

## Day 13: BA Artifact Completion

Tasks:

- Finish stakeholder map.
- Finish user stories.
- Finish acceptance criteria.
- Finish UAT cases.
- Finish traceability matrix.

Output:

- BA artifact pack.

## Day 14: Portfolio Packaging

Tasks:

- Write final case-study README.
- Add dashboard screenshots.
- Add architecture diagram.
- Draft resume bullets.
- Draft interview talking points.

Output:

- Recruiter-facing MVP case study.
- Interview-ready demo script.

## MVP Acceptance Criteria

- A recruiter can understand the project in 90 seconds.
- A hiring manager can inspect SQL, model design, dashboard screenshots, and documentation.
- You can explain one business recommendation backed by data.
- The dashboard has data quality and metric-definition evidence.
- The project has a clean story for DA, BA, BI, and Analytics Engineering roles.

