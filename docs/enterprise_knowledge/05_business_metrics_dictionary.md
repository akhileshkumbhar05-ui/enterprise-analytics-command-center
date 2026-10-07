# Business Metrics Dictionary

## Document Metadata

Document Owner: Analytics and Data Operations  
Document Type: Business Metrics Reference  
Version: 1.0  
Status: Active  
Last Reviewed: October 2026

---

## 1. Purpose

This document defines commonly used business metrics for the Enterprise Analytics Command Center.

The purpose is to ensure that analysts, dashboards, AI systems, and business users interpret important metrics consistently.

Metrics should be calculated using governed data sources whenever possible.

---

## 2. Total Orders

### Definition

Total Orders represents the number of unique orders recorded during the selected reporting period.

### Recommended Calculation

COUNT(DISTINCT order_id)

### Primary Source

workspace.eacc_ecommerce_gold.fact_orders

### Interpretation

Each row in fact_orders represents one order.

Total Orders should therefore normally equal the row count of fact_orders for the selected reporting period.

---

## 3. Gross Revenue

### Definition

Gross Revenue represents the total revenue value associated with orders before cancellation and return adjustments.

### Source Field

gross_revenue_amount

### Recommended Calculation

SUM(gross_revenue_amount)

### Important Note

Gross Revenue may include revenue associated with orders that were later cancelled or returned.

Gross Revenue should therefore not be interpreted as adjusted or retained revenue.

---

## 4. Net Revenue

### Definition

Net Revenue represents revenue after cancellation and return adjustments defined in the Gold-layer analytical model.

### Source Field

net_revenue_amount

### Recommended Calculation

SUM(net_revenue_amount)

### Current Model Behavior

Cancelled and returned orders have:

- net_revenue_amount = 0
- net_cost_amount = 0
- net_profit_amount = 0

Processing, shipped, and complete orders retain their net financial values.

### Important Interpretation Note

Net Revenue should not automatically be described as strictly realized or recognized accounting revenue.

The current analytical definition is:

Gross order revenue after cancellation and return adjustments.

---

## 5. Gross Cost

### Definition

Gross Cost represents the total modeled cost associated with orders before cancellation and return adjustments.

### Source Field

gross_cost_amount

### Recommended Calculation

SUM(gross_cost_amount)

---

## 6. Net Cost

### Definition

Net Cost represents modeled cost after cancellation and return adjustments.

### Source Field

net_cost_amount

### Recommended Calculation

SUM(net_cost_amount)

Cancelled and returned orders currently contribute zero Net Cost.

---

## 7. Gross Profit

### Definition

Gross Profit represents Gross Revenue minus Gross Cost before cancellation and return adjustments.

### Source Field

gross_profit_amount

### Recommended Calculation

SUM(gross_profit_amount)

---

## 8. Net Profit

### Definition

Net Profit represents the analytical profit measure after cancellation and return adjustments.

### Source Field

net_profit_amount

### Recommended Calculation

SUM(net_profit_amount)

Net Profit should be interpreted consistently with the current Net Revenue and Net Cost definitions.

---

## 9. Cancellation Rate

### Definition

Cancellation Rate represents the percentage of orders classified as cancelled.

### Recommended Calculation

Cancelled Orders
divided by
Total Orders
multiplied by 100

### Gold-Layer Indicator

is_cancelled_order

### Example

If:

- Total Orders = 125,082
- Cancelled Orders = 18,856

then:

Cancellation Rate = 15.07%

### Operational Thresholds

According to the Order Cancellation Policy:

- Above 10% monthly cancellation rate → standard operational review
- Above 15% monthly cancellation rate → priority review

These values are operational review thresholds, not desired target rates.

---

## 10. Return Rate

### Definition

Return Rate represents the percentage of orders classified as returned.

### Recommended Calculation

Returned Orders
divided by
Total Orders
multiplied by 100

### Gold-Layer Indicator

is_returned_order

### Example

If:

- Total Orders = 125,082
- Returned Orders = 12,328

then:

Return Rate = 9.86%

### Important Note

Return-rate thresholds depend on the level of analysis.

Product-level and category-level thresholds are different.

---

## 11. Product Return Rate

### Definition

Product Return Rate measures return activity for an individual product.

### Conceptual Calculation

Returned units for the product
divided by
eligible units sold for the product
multiplied by 100

### Operational Thresholds

According to the Product Quality and Returns Playbook:

- Above 10% → standard product review
- Above 18% → priority product investigation

---

## 12. Category Return Rate

### Definition

Category Return Rate measures return activity across all products belonging to a product category.

### Conceptual Calculation

Returned units or orders in the category
divided by
eligible units or orders in the category
multiplied by 100

The numerator and denominator must use the same business grain.

### Operational Thresholds

According to enterprise policy:

- Above 12% → standard category review
- Above 15% → priority category review

Product-level thresholds should not be substituted for category-level thresholds.

---

## 13. Returned Item Count

### Definition

Returned Item Count represents the number of modeled order items associated with returned activity.

### Source Field

returned_item_count

### Important Note

Returned Item Count and Returned Order Count are different metrics.

One returned order may contain multiple returned items.

---

## 14. Cancelled Item Count

### Definition

Cancelled Item Count represents the number of modeled order items associated with cancelled orders.

### Source Field

cancelled_item_count

Cancelled Item Count should not be confused with the number of cancelled orders.

---

## 15. Source Item Count

### Definition

Source Item Count represents the number of order items observed in the source data for an order.

### Source Field

source_item_count

This field supports reconciliation between source data and the analytical model.

---

## 16. Modeled Item Count

### Definition

Modeled Item Count represents the number of order items represented by the analytical transformation process.

### Source Field

modeled_item_count

---

## 17. Item Reconciliation Rate

### Definition

Item Reconciliation Rate measures how consistently modeled item counts match source item counts.

### Conceptual Calculation

Orders where source_item_count = modeled_item_count
divided by
Total Orders
multiplied by 100

### Current Validated Result

The current Enterprise Analytics dataset has:

- 125,082 total orders
- 125,082 orders with matching source and modeled item counts
- Item Reconciliation Rate = 100%

---

## 18. Order Status

### Definition

Order Status represents the current or terminal operational state assigned to an order.

Common statuses include:

- Processing
- Shipped
- Complete
- Cancelled
- Returned

Statuses should not automatically be treated as interchangeable business events.

For example:

- Cancelled represents cancellation activity.
- Returned represents post-order return activity.
- Processing does not necessarily represent completed fulfillment.

---

## 19. Order Month

### Definition

Order Month is a reporting attribute derived from the order creation date.

### Source Field

order_month

It is used for monthly trend analysis and period-based aggregations.

Consumers should verify the stored format and datatype before assuming whether the year is included in the field representation.

---

## 20. Average Order Value

### Definition

Average Order Value measures the average revenue associated with an order.

The exact revenue measure must be stated.

### Gross AOV

Gross Revenue
divided by
Total Orders

### Net AOV

Net Revenue
divided by
the appropriate eligible order denominator

Analysts should explicitly state whether Gross Revenue or Net Revenue is used.

---

## 21. Metric Grain

Every metric should be evaluated at an appropriate grain.

Examples include:

- order level,
- item level,
- product level,
- category level,
- customer level,
- monthly level.

Metrics with different grains should not be combined without validating the relationship between their numerators and denominators.

---

## 22. Metric Governance Rules

When using metrics:

- use governed Gold-layer sources when available,
- document the numerator and denominator,
- document filters and exclusions,
- distinguish gross from net financial metrics,
- distinguish order counts from item counts,
- distinguish product thresholds from category thresholds,
- do not treat operational thresholds as business targets,
- do not infer causality from aggregate metrics alone.

---

## 23. Important Interpretation Notes

A metric definition and a business target are not the same thing.

A metric threshold and a customer policy are not the same thing.

A return rate of 12% has different implications depending on whether it refers to:

- an individual product,
- a product category,
- the enterprise overall.

Similarly, Gross Revenue and Net Revenue represent different stages of financial adjustment and should not be used interchangeably.