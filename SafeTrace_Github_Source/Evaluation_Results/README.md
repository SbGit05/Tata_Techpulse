# Actual evaluation evidence
`metrics.json`, `answers.json`, `question_results.csv`, `evaluation_run.log`: final evidence-mode run.
`metrics_llm.json`, `answers_llm.json`, `question_results_llm.csv`, `evaluation_llm_run.log`: final structured Qwen run. In-scope passes require actual model mode; evidence fallback is not counted as a model pass.
`*_initial` and `*_unstructured`: retained development runs before structured generation. Initial metrics counted pipeline fallback correctness; they are not LLM-success metrics. The final run uses the stricter model-mode pass criterion.
`system_tests.log`: 12 real workflow tests.
`api_tests.log`: 9 Flask test-client checks.
`model_protocol_tests.log`: 5 clearly labelled mocked protocol checks; not real inference evidence.
`demonstration_*`: actual automated UI demo case/audit export. The reviewer name Demonstration tester denotes an automated exercise, not the submitting student's genuine verification.
The submitted question set is an authored development smoke test. It was not used to fit the vectorizer or tune the similarity threshold, but observed outputs were used to improve the model prompt and response schema. It is not an untouched benchmark. Citation membership does not establish claim-level faithfulness or safety correctness.


Assistant review completed on 11 October 2026; see Documentation/Actual_Contributions_and_Review.md and Evaluation_Results/assistant_output_review.json. Actual contributions are recorded. Student verification remains pending. Local-model Q18 contains incorrect terminology and Q08 is incomplete; automated passing metrics do not represent content accuracy.
