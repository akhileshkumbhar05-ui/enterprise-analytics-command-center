-- Enterprise Analytics Command Center
-- Step 00: Create BigQuery datasets for the e-commerce MVP.
-- Run this in BigQuery Studio with project enterprise-analytics-cc selected.

CREATE SCHEMA IF NOT EXISTS `enterprise-analytics-cc.ecom_raw`
OPTIONS (
  location = "US",
  description = "Raw source-aligned views for TheLook e-commerce public data."
);

CREATE SCHEMA IF NOT EXISTS `enterprise-analytics-cc.ecom_staging`
OPTIONS (
  location = "US",
  description = "Cleaned and standardized staging views for e-commerce analytics."
);

CREATE SCHEMA IF NOT EXISTS `enterprise-analytics-cc.ecom_intermediate`
OPTIONS (
  location = "US",
  description = "Reusable intermediate business logic for e-commerce analytics."
);

CREATE SCHEMA IF NOT EXISTS `enterprise-analytics-cc.ecom_marts`
OPTIONS (
  location = "US",
  description = "Curated dimensional marts for Power BI e-commerce reporting."
);

CREATE SCHEMA IF NOT EXISTS `enterprise-analytics-cc.analytics_quality`
OPTIONS (
  location = "US",
  description = "Data quality checks, reconciliation outputs, and monitoring tables."
);

