# Phase 3 — Enterprise Knowledge Corpus

## Objective

Create a realistic enterprise knowledge base that will later be used
for Retrieval-Augmented Generation (RAG), knowledge retrieval,
and agentic workflows.

## Source Documents

The source knowledge corpus is stored at:

`docs/enterprise_knowledge/`

The corpus contains:

1. `01_return_refund_policy.md`
2. `02_shipping_fulfillment_policy.md`
3. `03_order_cancellation_policy.md`
4. `04_product_quality_returns_playbook.md`
5. `05_business_metrics_dictionary.md`
6. `06_customer_service_operations_guide.md`

## Design Goals

The corpus was intentionally designed to contain:

- enterprise policies
- operational procedures
- business metric definitions
- overlapping business concepts
- cross-document relationships
- similar but distinct thresholds
- policy exceptions
- operational escalation rules

These characteristics will allow later testing of:

- document parsing
- structure-aware chunking
- metadata extraction
- semantic retrieval
- cross-document retrieval
- retrieval precision
- grounded generation
- conflicting or similar policy rules
- hybrid structured-data and unstructured-knowledge questions

## Relationship to Enterprise Analytics Data

The corpus complements the structured analytics data already stored
in the Enterprise Analytics Command Center.

Structured data provides operational facts and metrics.

The knowledge corpus provides policies, definitions, thresholds,
procedures, and business interpretation.

Future agentic workflows will combine both sources.