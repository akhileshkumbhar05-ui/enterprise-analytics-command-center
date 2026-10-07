# Phase 1 — Workspace and Data Validation

## Objective

Establish the current state of the Enterprise Analytics Command Center
before beginning Generative AI and AI Agent development.

This phase validated the existing Databricks environment, Unity Catalog
objects, Gold-layer analytical model, and several important data-quality
and business-logic assumptions.

The purpose was not to perform extensive SQL analysis, but to confirm
that the structured enterprise data used in later GenAI and agentic
workflows is reliable and understood.

---

## Environment

Databricks Free Edition

Primary Unity Catalog catalog:

`workspace`

Primary Gold schema:

`workspace.eacc_ecommerce_gold`

Primary Gold fact table:

`workspace.eacc_ecommerce_gold.fact_orders`

---

## Primary Fact Table

`fact_orders`

### Grain

One row per order.

### Important Fields

#### Identifiers

- `order_id`
- `customer_id`

#### Order State

- `order_status`
- `customer_gender`

#### Lifecycle Fields

- `order_created_at`
- `order_created_date`
- `order_month`
- `shipped_at`
- `shipped_date`
- `delivered_at`
- `delivered_date`
- `returned_at`
- `returned_date`

#### Financial Measures

- `gross_revenue_amount`
- `gross_cost_amount`
- `gross_profit_amount`
- `net_revenue_amount`
- `net_cost_amount`
- `net_profit_amount`

#### Operational Measures

- `source_item_count`
- `modeled_item_count`
- `returned_item_count`
- `cancelled_item_count`

#### Flags

- `is_returned_order`
- `is_cancelled_order`

---

## Validated Order Counts

Total orders:

`125,082`

Order status distribution:

- Shipped: `37,714`
- Complete: `31,096`
- Processing: `25,088`
- Cancelled: `18,856`
- Returned: `12,328`

The status counts reconcile to the total number of orders.

---

## Validated Business Metrics

Cancellation Rate:

`15.07%`

Return Rate:

`9.86%`

These metrics were calculated from the Gold-layer fact table and will
later be used in analytics, prompting, RAG, and agentic workflow tests.

---

## Source-to-Model Reconciliation

The following fields were compared:

- `source_item_count`
- `modeled_item_count`

Results:

- Total orders: `125,082`
- Matching orders: `125,082`
- Mismatched orders: `0`
- Item reconciliation rate: `100.00%`

This confirms that item counts represented in the analytical model
match the source-derived item counts for all orders.

---

## Lifecycle Validation

Two initial lifecycle-quality rules were tested.

### Cancelled Orders with Delivery Timestamp

Result:

`0`

No cancelled orders were found with a delivery timestamp.

### Returned Orders Without Delivery Timestamp

Result:

`0`

No returned orders were found without a delivery timestamp.

These checks indicate consistent lifecycle behavior for the tested rules.

---

## Financial Model Behavior

The Gold-layer model distinguishes gross and net financial measures.

### Shipped, Complete, and Processing Orders

These statuses retain:

- gross financial values
- net financial values

### Cancelled and Returned Orders

These statuses retain their gross financial values, but:

- `net_revenue_amount = 0`
- `net_cost_amount = 0`
- `net_profit_amount = 0`

Therefore:

`net_revenue_amount`

should currently be interpreted as revenue after cancellation and return
adjustments.

It should not automatically be described as strictly realized or
recognized accounting revenue.

---

## Data Discovery Activities

This phase included:

- exploring Unity Catalog
- identifying project catalogs and schemas
- inspecting tables and views
- reviewing table metadata
- inspecting Gold-layer columns
- reviewing Delta-table behavior
- validating important business metrics
- performing data-quality checks
- reviewing Query History and query execution information

---

## Relationship to Later GenAI Work

The structured Enterprise Analytics data will later provide the
analytics side of agentic workflows.

Examples:

Structured question:

> What percentage of orders were cancelled?

Source:

`workspace.eacc_ecommerce_gold.fact_orders`

Unstructured question:

> What action should be taken when cancellation rate exceeds the
> operational threshold?

Source:

Enterprise knowledge corpus.

Hybrid question:

> Our cancellation rate is 15.07%. What action is required under
> company policy?

Required capabilities:

- structured enterprise analytics
- unstructured policy retrieval

This structured + unstructured pattern will later be used for RAG,
tool-calling agents, and multi-agent workflows.

---

## Phase Outcome

The Enterprise Analytics Command Center was confirmed to contain a
usable and internally consistent structured-data foundation for later
Generative AI and AI Agent experiments.

No major data-quality issues were identified in the validation checks
performed during this phase.