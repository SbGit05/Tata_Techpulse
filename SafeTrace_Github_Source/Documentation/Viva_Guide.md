# Viva guide
Read the implementation and explain these points in your own words.

1. Problem: HARA knowledge and safety requirements are dispersed; this prototype organizes a synthetic example library with source evidence and explicit review.
2. Hazard versus event: a hazard becomes a hazardous event when combined with an operating situation. Show H01 for highway braking loss.
3. Ratings: the user supplies S, E, C and a rationale. Exposure refers to the operating situation. No rating is scientifically inferred here.
4. Retrieval: original event/teaching-note sections become TF-IDF vectors. FAISS IndexFlatIP ranks normalized vectors using inner product, equivalent to cosine similarity. This is lexical retrieval, not pretrained semantic embeddings.
5. Why retrieval: the response can show the exact reference and version. The model receives only the top three sufficiently similar passages.
6. Evidence mode: concatenates cited passages; it uses no generative model. Local model mode: Qwen through local Ollama, temperature 0, seed 42, context 4096, output budget 140 tokens. The model returns JSON with answer and citations, constrained to retrieved source IDs. Python checks fields and formats bracketed citations; invalid responses fall back to evidence mode.
7. Faithfulness: citation IDs may be valid while a claim is wrong. Human checking is still necessary; no expert faithfulness score is claimed.
8. Risk tool: the configured lookup is an educational synthetic rule table. Its status is NOT_EXPERT_APPROVED; candidate classes cannot establish ISO compliance.
9. Drafts: goal, FSR, TSR and test are copied from the selected synthetic reference. The application does not claim to invent complete safety requirements from arbitrary vehicle input.
10. Traceability: hazard → goal → FSR → TSR → test. Completeness is structural. Removing the test gives 80%; marking student reviewed is blocked. Changing an FSR resets prior review.
11. Storage: SQLite holds cases and audit events. Parameterized statements are used. The database is local and not tamper-proof or enterprise authenticated.
12. Evaluation: show actual questions/answers/metrics and test logs. Explain the synthetic set size and that retrieval-hit and citation-ID validity are not real-world safety accuracy.
13. Dependencies: internet is needed for first installation/model download; local runtime does not use a cloud API. Weights are not bundled. Explain a visible fallback if Qwen is unavailable.
14. Limitations: no expert-approved rules, no production vehicle validation, no enterprise access control, no PDF ingestion, no verified time-saving claim.
15. Contributions: explain only the work you personally reviewed, changed or tested. AI assistance was substantial and must be disclosed.
