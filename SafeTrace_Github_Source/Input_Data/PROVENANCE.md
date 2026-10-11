# Synthetic data provenance
22 original chunks: 12 authored hazard references and 10 teaching notes, created for this educational implementation on 11 October 2026 with ChatGPT/Codex assistance. No actual vehicle data, personal information, approved HARA history or copied standards clauses are included. All example ratings, timing limits, goals and test criteria are synthetic and unvalidated.

`hazards.json` is the structured reference library. `knowledge.json` is the searchable corpus. Each record carries a stable ID, project CS2, version 1.0 and SYNTHETIC_REFERENCE status. A reference ID is a citation to a local dataset section, not a page in ISO 26262.

One chunk is one complete event or one note; chunk text ranges from short paragraphs to a full event/goal/FSR/TSR/test chain. No sliding window is required for this small authored JSON corpus. TF-IDF lowercases, removes English stop words and creates unigram/bigram features. Test expected-source labels appear only in `Evaluation_Results/questions.json` and are not indexed.

The supplied Automotive Engineering AI case-study document was used as a planning reference (CS2, pages 8–11). Its confidentiality/internal-use markings are respected; it is not redistributed, uploaded to a public repository or embedded in the retriever. The public ISO overview is cited for general scope only; no licensed standard content is reproduced.
