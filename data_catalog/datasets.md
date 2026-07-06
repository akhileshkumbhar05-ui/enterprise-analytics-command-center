# Dataset Catalog

## Selection Rules

Use datasets that are:

- Publicly accessible.
- Cloud-friendly.
- Large enough to show real analysis challenges.
- Relevant to common junior analyst domains.
- Safe to publish in a portfolio.

## Priority 1: E-commerce and Product Analytics

### TheLook E-commerce

Use case:

- Orders, users, products, inventory, events, logistics, and digital commerce analytics.

Why it is strong:

- Great first MVP.
- Supports revenue, products, cohorts, funnel, returns/fulfillment, and customer segmentation.
- Hosted in BigQuery public datasets.

Reference:

- BigQuery public datasets documentation: https://docs.cloud.google.com/bigquery/public-data
- TheLook public dataset reference: https://console.cloud.google.com/marketplace/product/bigquery-public-data/thelook-ecommerce

### GA4 Sample E-commerce

Use case:

- Event-level product and web analytics.
- Funnel analysis.
- Marketing/product behavior.

Reference:

- https://developers.google.com/analytics/bigquery/web-ecommerce-demo-dataset

## Priority 2: Logistics and Operations

### NYC Taxi / TLC Trip Data

Use case:

- Big data operations analytics.
- Demand by time/location.
- Fare/tip analysis.
- Service efficiency and anomaly detection.

Why it is strong:

- Large enough to discuss big data and query cost/performance.
- Available from NYC TLC and through cloud public dataset ecosystems.

References:

- NYC TLC trip records: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- BigQuery public datasets documentation: https://docs.cloud.google.com/bigquery/public-data

## Priority 3: Healthcare Quality and Operations

### CMS Hospital / Provider Data

Use case:

- Provider quality.
- Hospital comparisons.
- Patient experience.
- Geographic benchmarking.

Why it is strong:

- Healthcare is common in analyst JDs.
- Shows careful metric definition and public-sector data literacy.

References:

- CMS provider hospital datasets: https://data.cms.gov/provider-data/topics/hospitals
- Medicare Care Compare: https://www.medicare.gov/care-compare/

## Priority 4: Finance, Banking, and Risk

### HMDA Mortgage Data

Use case:

- Loan application trends.
- Approval/denial rates.
- Regional analysis.
- Institution and applicant segment analysis.

Why it is strong:

- Banking and financial services JDs often ask for reporting, SQL, data validation, compliance awareness, and clear documentation.

Reference:

- CFPB HMDA data: https://www.consumerfinance.gov/data-research/hmda/

### FDIC Bank Data

Use case:

- Financial institution benchmarking.
- Quarterly financial trends.
- Bank-level metrics.

References:

- FDIC data downloads: https://www.fdic.gov/bank-data-guide/data-downloads
- Snowflake public data listing reference: https://data-docs.snowflake.com/sources/fdic-ffiec

## Priority 5: Company Financials

### SEC Financial Statement Data Sets

Use case:

- Public company reporting.
- Financial metrics.
- Trend and ratio analysis.

Reference:

- https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets

## First Dataset Decision

Start with TheLook e-commerce in BigQuery. Add GA4 sample e-commerce if event-level funnel analysis is needed in the first MVP.

This gives the fastest complete path to:

- SQL analysis.
- dbt modeling.
- Power BI dashboard.
- Python cohort/segmentation.
- BA artifacts.

