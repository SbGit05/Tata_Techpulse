# Model and dependency declaration
Runtime generator: local Ollama, model tag qwen2.5:1.5b-instruct-q4_K_M (Qwen2.5 1.5B Instruct, Q4_K_M quantization). Temperature 0, seed 42, num_ctx 4096, num_predict 140, num_thread 2. Model digest and local runtime status are recorded in model_manifest.json when available. Model weights are not included in the submission archive.

Embedding baseline: scikit-learn TF-IDF word unigrams and bigrams, English stop-word removal and L2 normalization. No pretrained embedding model is used. Dense float32 vectors are indexed with FAISS IndexFlatIP. SQLite is the workflow store. Custom Python orchestration; no LangChain/agent framework.

Internet/external dependencies: first pip installation, Ollama installer and model download need internet. Evidence mode and downloaded local model inference are offline. No remote LLM API, paid key or cloud vector database is configured. The local model HTTP endpoint is 127.0.0.1:11434; it is an external local process dependency. A failed request or failed citation-ID validation returns a disclosed evidence-mode fallback.

Pretrained model attribution: Qwen team, Qwen2.5 model family; see https://ollama.com/library/qwen2.5:1.5b-instruct-q4_K_M and upstream https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct . Check the upstream license before redistributing weights. No pretrained model training or fine-tuning is claimed.

Exact model used during preparation: official upstream Qwen GGUF, downloaded from https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf and imported with the supplied Modelfile under the configured tag. The upstream GGUF SHA-256 is 6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e. Ollama runtime version was 0.40.3. This imported manifest differs from the Ollama registry artifact with the same tag. Compare the recorded manifest digest; do not assume an unpinned registry pull exactly reproduces this tested artifact.

For exact reproduction on Windows, open PowerShell in Model_Prompts_Config, download the official GGUF using Invoke-WebRequest (URL above) with -OutFile qwen2.5-1.5b-instruct-q4_k_m.gguf, verify Get-FileHash -Algorithm SHA256, then run `ollama create qwen2.5:1.5b-instruct-q4_K_M -f Modelfile`. After verifying, keep the large weight file outside the public submission archive. Running create installs the imported artifact under that tag.

Generation now uses Ollama structured output with an answer string and a citations array restricted to the retrieved IDs. Python validates the fields and formats bracketed citations. Schema conformance and citation IDs do not establish semantic correctness. See https://docs.ollama.com/capabilities/structured-outputs .
