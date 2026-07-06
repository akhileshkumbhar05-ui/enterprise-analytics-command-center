# E-commerce MVP Problem Brief

## Business Context

Leadership at a fictional online retail company receives inconsistent reporting across sales, marketing, product, and operations teams. Revenue reports are manually reconciled, customer retention is not consistently measured, and product/category performance lacks a shared source of truth.

## Problem Statement

The business needs a trusted analytics layer and Power BI dashboard that standardizes KPI definitions, identifies revenue and customer retention drivers, and highlights operational or product-level issues that require action.

## Stakeholders

- Executive sponsor: wants top-line performance and risks.
- Marketing lead: wants acquisition and conversion performance.
- Product/category manager: wants category and SKU performance.
- Operations lead: wants fulfillment, return, or cancellation patterns where available.
- Finance analyst: wants reconciliation and trustworthy KPI definitions.
- BI/data owner: wants maintainable models and documented logic.

## Key Business Questions

- Is revenue growth driven by more customers, higher order value, or repeat purchases?
- Which products and categories are growing, declining, or creating risk?
- Which customer cohorts retain best?
- Where does the funnel lose users?
- Are there data quality issues that could reduce trust in reporting?
- What actions should leadership prioritize next month?

## Success Metrics

- One standardized executive dashboard in Power BI.
- Documented KPI dictionary.
- Source-to-dashboard reconciliation checks.
- Repeat purchase and cohort retention analysis.
- At least three actionable recommendations.

## In Scope

- Revenue, orders, customers, products, categories, events/funnel, cohorts, and data quality.
- BigQuery warehouse modeling.
- dbt transformations and tests.
- Power BI executive dashboard.
- BA requirements and UAT artifacts.

## Out of Scope

- Private customer data.
- Production payment systems.
- Real marketing spend unless a suitable public source exists.
- Full machine learning productization.

## Assumptions

- Public datasets are representative enough for portfolio demonstration.
- Some financial metrics may be proxies if source data lacks true cost or margin fields.
- Funnel analysis depends on event-level source availability.

## Risks

- Synthetic or obfuscated data may limit real-world causal claims.
- Public datasets may not include every operational field.
- Dashboard recommendations must clearly separate observed insight from assumption.

