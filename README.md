# A-MEM reproduction with DeepSeek

FTEC5660 individual reproducibility study by XU Nuo.

**Status: complete. 369 memory turns, 30 questions, 180 scored answers.**

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

`results/usage.csv`: published API token usage and timing. `results/study_calls.jsonl` is generated locally during a new run and is not included in the public repository. The analyzer falls back to the published CSV when this local file is absent.

To recompute the published results without API calls, run `python3 experiments/analyze.py` immediately after cloning. This uses only Python's standard library and the included result files.

`results/summary.json` and `results/predictions.csv`: generated only after a complete, duplicate-free run.

## Measured results

| Metric | k=10 | k=5 |
|---|---:|---:|
| Mean F1 (%) | 34.59 | 33.49 |
| Exact match (%) | 12.22 | 11.11 |
| QA input tokens | 1,230,702 | 617,608 |
| Mean QA seconds | 1.85 | 1.71 |

Reducing k lowered QA input tokens by 49.82%, with a 1.10 percentage-point reduction in mean F1. This is descriptive evidence on one conversation, not a significance claim. Category 3 is absent from the selected conversation; the final sample contains ten questions each from categories 1, 2 and 4. The loader reports sample index 1, corresponding to original sample_id conv-30.

Conservative study cost: CNY 6.84, excluding pilots and an interrupted request with no returned usage. See results/summary.json, predictions.csv and usage.csv. Full local API response usage metadata remains available in the original workspace.
