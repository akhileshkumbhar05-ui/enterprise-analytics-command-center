# Phase 5 — Embeddings, AI Search, and Semantic Retrieval

## Objective

Transform the retrieval-ready enterprise knowledge chunks into a
semantic search system using Databricks AI Search.

---

## Embedding Model

Embedding model:

`BGE Large English`

Manual embedding experiments demonstrated that semantically similar
sentences can have high vector similarity even when their wording differs.

---

## Source Table

`workspace.eacc_ecommerce_rag.chunks`

Total chunks:

`95`

The source table uses Change Data Feed to support Delta Sync.

---

## AI Search

Endpoint:

`eacc-rag-search`

Index:

`workspace.eacc_ecommerce_rag.enterprise_knowledge_index`

Index type:

Delta Sync

Pipeline mode:

Triggered

Embedding source:

`chunk_text`

Primary key:

`chunk_id`

---

## Retrieval Strategies Evaluated

Two retrieval strategies were tested:

- ANN semantic retrieval
- Hybrid semantic + lexical retrieval

### ANN Results

Hit@1: 90.00%

Hit@3: 100.00%

MRR: 0.950

### HYBRID Results

Hit@1: 90.00%

Hit@3: 90.00%

MRR: 0.900

---

## Selected Retrieval Configuration

Query Type:

`ANN`

Top K:

`3`

ANN was selected because it achieved complete Hit@3 coverage and a
higher Mean Reciprocal Rank on the evaluation set.

---

## Retrieval Stress Testing

The knowledge corpus intentionally contains similar but distinct policy
thresholds.

The retrieval system successfully distinguished:

- 30-day standard return window
- 14-day damaged-product reporting window
- >10% standard product review threshold
- >18% priority product investigation threshold
- >12% standard category review threshold
- >15% priority category review threshold
- >10% standard cancellation review threshold
- >15% priority cancellation review threshold

This provides evidence that the current semantic-section chunking strategy
preserves important policy distinctions.

---

## Synchronization

The index uses triggered Delta Sync.

When source knowledge changes, the processing pipeline can update the
chunk table and explicitly synchronize the index.

This design supports future incremental enterprise knowledge updates.

---

## Phase Outcome

The project now contains a measured semantic retrieval system rather
than relying on manual document selection or keyword matching.

Current flow:

User Question
    ↓
BGE Query Embedding
    ↓
Databricks AI Search
    ↓
ANN Retrieval
    ↓
Top 3 Relevant Enterprise Chunks

Generation has not yet been added.