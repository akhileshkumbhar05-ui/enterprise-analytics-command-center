# Phase 6 — Retrieval-Augmented Generation

## Objective

Combine Databricks AI Search retrieval with a foundation model to
produce grounded answers from enterprise knowledge.

The RAG pipeline uses the retrieval system developed in Phase 5 and
Gemma 3 12B for generation.

---

## Architecture

User Question
    ↓
Databricks AI Search
    ↓
ANN Top-3 Retrieval
    ↓
Enterprise Context Assembly
    ↓
Gemma 3 12B
    ↓
Structured Grounded Response
    ↓
Application-Rendered Citations

---

## Retrieval Configuration

Query Type:

`ANN`

Top K:

`3`

AI Search Index:

`workspace.eacc_ecommerce_rag.enterprise_knowledge_index`

---

## Generation Model

`system.ai.gemma-3-12b`

The model receives only the enterprise chunks retrieved for the
current question.

---

## Grounding Behavior

The RAG application was designed to:

- answer only from retrieved enterprise evidence,
- abstain when evidence is insufficient,
- avoid using external knowledge for company-specific facts,
- preserve numerical policy thresholds,
- distinguish operational thresholds from customer eligibility rules,
- identify conflicting enterprise evidence,
- apply explicit source-governance rules when supplied.

---

## Structured Output

Generation uses API-enforced structured output.

Possible response states:

- `ANSWERED`
- `INSUFFICIENT_EVIDENCE`
- `CONFLICTING_EVIDENCE`

The model returns source numbers separately from the answer text.

Citation formatting is performed deterministically by application code
rather than relying on free-form LLM citation formatting.

---

## Citation Behavior

Only sources directly supporting an answer are presented as citations.

When evidence is insufficient:

- the system abstains,
- citation list is empty,
- unrelated retrieved chunks are not presented as evidence.

---

## Evaluation

A controlled 10-case RAG evaluation set was executed.

Results:

- Overall Pass Rate: 100%
- Status Accuracy: 100%
- Answer-Content Accuracy: 100%
- Citation Behavior Accuracy: 100%
- Citation-Reference Validity: 100%

These results apply only to the defined evaluation set and should not
be interpreted as universal system accuracy.

---

## Token Usage

Total evaluation tokens:

`8,551`

Average tokens per RAG request:

`855.1`

Token usage includes retrieved context, instructions, and generated
structured responses.

---

## Additional Tests

The pipeline successfully demonstrated:

- 30-day standard return vs. 14-day damaged-product reporting
- product-level 10% / 18% thresholds
- category-level 12% / 15% thresholds
- cancellation 10% / 15% thresholds
- insufficient-evidence abstention
- conflicting-source detection
- source-precedence handling
- grounded multi-source answers

---

## Application Interface

The final knowledge capability is exposed through:

`enterprise_knowledge_search(question)`

The function abstracts:

- semantic retrieval,
- context construction,
- grounded generation,
- structured output,
- citation handling.

This interface can later be exposed as a tool to an AI agent.

---

## Phase Outcome

The project now contains an end-to-end enterprise RAG capability:

Enterprise Documents
    ↓
Semantic Chunks
    ↓
Embeddings
    ↓
AI Search
    ↓
Retrieval
    ↓
Grounded Generation
    ↓
Source Attribution

The RAG system is now ready to become one capability available to the
agentic layer.