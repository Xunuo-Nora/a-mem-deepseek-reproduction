# A-MEM reproduction with DeepSeek

FTEC5660 individual reproducibility study by XU Nuo.

**Status: experiment in progress. No final results yet.**

This repository runs the author's A-MEM memory pipeline on one full LoCoMo conversation, then compares retrieval k=10 and k=5 with three QA repetitions per arm. It is a partial reproduction under a different model and evaluation subset, not a claim to match the full paper.

## Provenance

Author repository: https://github.com/WujiangXu/A-mem

Imported snapshot: `f9a173dec325d84fcc97e7828775c7b241c33466`. Original source is retained under its MIT license. See UPSTREAM_README.md. Import and reproduction changes have separate commits.

Paper: https://arxiv.org/abs/2502.12110

## Install and run

Use Python 3.12. Tested on macOS Apple Silicon with CPU embedding inference.

```bash
python3 -m venv .venv
.venv/bin/pip install --cache-dir .cache/pip -r requirements-lock.txt
.venv/bin/python experiments/download_data.py
```

Create `.env` locally:

```dotenv
OPENAI_API_KEY=YOUR_DEEPSEEK_API_KEY
OPENAI_BASE_URL=https://api.deepseek.com
```

Never commit credentials. Then run:

```bash
.venv/bin/python experiments/check_api.py
.venv/bin/python experiments/prepare_models.py
.venv/bin/python experiments/pilot.py
.venv/bin/python experiments/run_study.py
.venv/bin/python experiments/analyze.py
```

The embedding model is downloaded into `.cache/`. NLTK resources are optional for the study's F1/EM metrics. The study stops before a conservative estimated CNY 18 budget is exceeded. Cached memory supports restarting the same configuration. Do not reuse checkpoints across changed code, data or model settings. Model availability is account-specific; confirm the model written to results/connectivity.json before running.

## Design

One complete conversation, conv-30 (369 turns), chosen by minimum length before observing results. Seed-42 stratified question sampling from categories 1-4, up to ten per category. Category 5 excluded. Same memory and model configuration across arms: deepseek-flash, thinking disabled, temperature 1.0, output cap 4096. Retrieval k also changes linked-neighbor expansion. Repetitions measure QA variability conditional on one memory construction.

Metrics: upstream token-set F1, lowercase exact match, wall time and API tokens. This F1 is not necessarily identical to official LoCoMo scoring. No LLM judge. See EXPERIMENT_PLAN.md and DEBUG_DIARY.md for limitations and compatibility changes.

## Outputs

`results/manifest.json`: exact question indices and configuration.

`results/predictions.jsonl`: per-question outputs and scores.

`results/study_calls.jsonl`: API token usage and timing.

`results/summary.json` and `results/predictions.csv`: generated only after a complete, duplicate-free run.
