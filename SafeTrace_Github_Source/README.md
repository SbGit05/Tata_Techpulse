# SafeTrace HARA — CS2
Functional Safety HARA and Safety Requirement Management Assistant.

**Educational synthetic prototype.** This submission has not received faculty approval, a safety-engineer review, or the submitting student's verification. Signature fields remain blank. Video generation was excluded on request.

## Quick start on Windows
Install Python 3.12 (64 bit). Open PowerShell in this submission folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r Code/requirements.txt
cd Code
..\.venv\Scripts\python.exe app.py
```
Open http://127.0.0.1:5000. No cloud account or API key is needed.

## Local Qwen model
Install Ollama from https://ollama.com/download and run:

```powershell
ollama pull qwen2.5:1.5b-instruct-q4_K_M
ollama list
```
Keep Ollama running. Select **Local Qwen draft with citations** in the interface.
For the exact tested upstream GGUF and import steps, see `Model_Prompts_Config/DEPENDENCIES.md`; the registry pull is an installation convenience and may have a different manifest. Configuration is in `Model_Prompts_Config/config.json`. Record your installed model digest with `python record_model.py` from Code. A model tag may change; compare the digest against the submitted model manifest.
The weights are downloaded separately and are not in the ZIP. Initial Python and model installation require internet. Normal evidence mode and already-installed local model inference do not require external APIs. Failed local-model requests fall back to visibly labelled evidence mode.

## Reproduce evidence
From Code, using the virtual-environment Python:

```powershell
..\.venv\Scripts\python.exe evaluate.py
..\.venv\Scripts\python.exe test_system.py
..\.venv\Scripts\python.exe test_api.py
..\.venv\Scripts\python.exe test_model_protocol.py
..\.venv\Scripts\python.exe evaluate.py --llm
```
On Linux/macOS use `python3 -m venv .venv`, `.venv/bin/python -m pip install -r Code/requirements.txt` and run `.venv/bin/python Code/app.py`.

## What it actually implements
- 12 synthetic event references and 10 original teaching notes.
- TF-IDF word unigram/bigram vectors; FAISS exact inner-product retrieval with top 3 and threshold 0.16.
- Offline cited evidence excerpts, and optional local Qwen generation from retrieved evidence.
- Input validation, controlled S/E/C entry and a versioned **synthetic** candidate risk lookup.
- Prewritten synthetic goal, FSR, TSR and verification drafts; these are reference templates, not model-generated engineering requirements.
- Persistent local SQLite case/review/audit records, CSV traceability export and a heuristic requirement checker.
- A requirement edit invalidates prior review; a missing test blocks STUDENT_REVIEWED.

## Scope limits
No standards text ingestion, certified ASIL logic, production ECU connection, autonomous safety approval, enterprise authentication, PDF/OCR upload, independent expert labels or real-time-saving claim. Local demo isolation is not enterprise RBAC. Citation-ID checks are not claim-level faithfulness assessment. The synthetic ratings and timing limits require independent validation.

## Files
`Synopsis/`: unsigned synopsis and faculty approval form.
`Input_Data/`: original synthetic corpus and provenance.
`Code/`: application, evaluation, tests, launch scripts.
`Model_Prompts_Config/`: model settings, prompt, rules and model inventory.
`Evaluation_Results/`: frozen questions, actual answers, metrics and logs.
`Documentation/`: technical report, screenshots, installation guide, viva guide, form checklist.
`Declarations/`: unsigned declarations and AI disclosure.
`Video/`: recording outline only; no video was generated.

## Required before submission
Read `Documentation/Submission_Checklist.md`, run the application on your laptop, personally review AI-assisted content, complete missing student details and truthful contribution statements, sign the declaration, obtain real faculty approval and upload the folder/video to Drive. Do not label an unsigned synopsis as approved.
Repository target: https://github.com/SbGit05/Tata_Techpulse — the connected account had no push permission when this package was prepared. No repository update is claimed.


Assistant review completed on 11 October 2026; see Documentation/Actual_Contributions_and_Review.md and Evaluation_Results/assistant_output_review.json. Actual contributions are recorded. Student verification remains pending. Local-model Q18 contains incorrect terminology and Q08 is incomplete; automated passing metrics do not represent content accuracy.
