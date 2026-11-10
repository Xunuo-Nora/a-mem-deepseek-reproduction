# Debug diary

- 2026-11-10: Cloned upstream at f9a173dec325d84fcc97e7828775c7b241c33466. Installed isolated Python 3.12 environment and saved requirements-lock.txt.
- DeepSeek account exposes deepseek-flash and deepseek-v4-pro. Connectivity test succeeded (51 tokens). Selected deepseek-flash for pilot; no assumption that older deepseek-chat alias is available.
- NLTK downloader refused the environment's proxy. No bypass was applied. Primary evaluation uses the upstream token-set F1 arithmetic and lowercase exact match, neither requiring NLTK downloads. Extra metrics are outside scope.
- Local all-MiniLM-L6-v2 loaded and produced a 384-dimensional embedding on CPU.
- First 5-note pilot: 13 calls, 5,760 prompt tokens, 6,113 completion tokens, 69.26 seconds. Two memory-evolution operations failed because completions were empty/truncated under the upstream 1,000-token cap with default thinking mode. These are pilot failures, not valid reproduction results.
- Retest changes: thinking disabled, max_tokens=4096, requested temperature=1.0. DeepSeek documentation says Flash non-thinking temperature is fixed at 1.0. Apply settings identically to baseline and intervention; preserve both pilot logs.
- Upstream retrieval k controls initial retrieval and linked-neighbor expansion. Describe the intervention accordingly.
- Upstream loader's image-evidence diagnostic matches suffix IDs rather than complete IDs; do not use its printed image counts as study statistics. Original dataset captions remain included by the upstream parser.
