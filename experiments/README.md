# Reproduction workspace

Status: pilot validation. No final research claim yet.

All commands run from the repository root. Python 3.12 was used.

1. Create a virtual environment: `python3 -m venv .venv`
2. Install: `.venv/bin/pip install --cache-dir .cache/pip -r requirements-lock.txt`
3. Create `.env` locally with `OPENAI_API_KEY` and `OPENAI_BASE_URL=https://api.deepseek.com`. Never commit it.
4. `.venv/bin/python experiments/check_api.py`
5. `.venv/bin/python experiments/prepare_models.py` (NLTK resources optional for the primary metric; embedding download required).
6. `.venv/bin/python experiments/pilot.py`
7. After confirming budget and a clean pilot: `.venv/bin/python experiments/run_study.py`

The study uses the author's robust memory construction/evolution/retrieval code and category-specific answer prompts. The custom runner restricts the dataset and metrics, logs API token usage, and supports resume. It does not use an LLM judge. Both arms use the same DeepSeek model and decoding settings. Only retrieval k differs.

Results are written under results/. Memory checkpoint is local under .cache/. Restarts must use the same code/config/data. Never load a checkpoint from an untrusted source. The fixed-memory QA repetitions do not estimate full-pipeline variability.
