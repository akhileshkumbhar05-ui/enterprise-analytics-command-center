# Project Charter

## Project Name

Enterprise Analytics Command Center

## Business Scenario

A multi-business operating group wants a unified analytics capability across retail, marketing, finance, healthcare, and logistics operations. Leadership has inconsistent reports, manual spreadsheet reconciliation, unclear KPI definitions, and limited trust in dashboards.

The project creates a cloud analytics platform that centralizes public datasets, standardizes KPI logic, validates data quality, and delivers Power BI dashboards with clear recommendations for different stakeholder groups.

## Target Roles

- Data Analyst: SQL analysis, Python EDA, KPI investigation, recommendations.
- BI Analyst: Power BI semantic model, DAX, dashboard suite, refresh/deployment.
- Business Analyst: requirements, stakeholder questions, user stories, UAT, process documentation.
- Junior Analytics Engineer: dbt models, tests, documentation, star schemas, lineage.

## Domain Modules

### 1. E-commerce and Marketing

Primary first build. Shows revenue, conversion, customer retention, product performance, campaign/event analysis, returns, and customer behavior.

Candidate story:
"I built a cloud analytics mart for an e-commerce business and created executive dashboards that identify revenue drivers, repeat purchase gaps, and product opportunities."

### 2. Finance, Banking, and Risk

Uses public mortgage, bank, or financial institution data. Shows approval rates, risk segmentation, fairness considerations, institution performance, and regional trends.

Candidate story:
"I analyzed financial and risk data to identify portfolio trends, reporting gaps, and decision-support metrics."

### 3. Healthcare Quality and Operations

Uses CMS hospital or provider datasets. Shows provider quality, patient experience, readmission/measure trends, geographic variation, and operational benchmarking.

Candidate story:
"I built healthcare quality reporting that compares provider performance and highlights improvement opportunities."

### 4. Logistics and Operations

Uses large transportation data such as NYC TLC trips or flight delay datasets. Shows demand patterns, utilization, peak periods, service delays, geospatial patterns, and operational efficiency.

Candidate story:
"I worked with large operational datasets in BigQuery/PySpark and built dashboards for capacity planning and performance monitoring."

### 5. Product Analytics / SaaS Behavior

Uses event data from GA4 sample e-commerce or TheLook events. Shows funnel performance, user behavior, cohort retention, and feature/event engagement.

Candidate story:
"I turned event-level data into funnel and cohort insights that support product and marketing decisions."

## Success Criteria

- At least one end-to-end deployed Power BI report connected to a cloud warehouse.
- At least three complete domain case studies.
- At least one big-data case using BigQuery and/or Databricks with millions of rows.
- dbt project with staging and mart models, tests, and documentation.
- Data quality checks that catch realistic issues.
- BA artifact pack with requirements, user stories, acceptance criteria, UAT, and traceability.
- Final portfolio page or README that recruiters can understand in 90 seconds.
- Resume bullets backed by screenshots, queries, docs, and deployed dashboard evidence.

## MVP Definition

The MVP is one complete vertical slice:

E-commerce source data -> BigQuery raw/staging -> dbt marts -> Power BI model -> dashboard -> written recommendations -> BA requirements/UAT evidence.

Once MVP is complete, domain expansion becomes repeatable instead of chaotic.

