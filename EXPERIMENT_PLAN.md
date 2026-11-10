# A-MEM reproduction plan

Upstream: https://github.com/WujiangXu/A-mem
Pinned starting commit: f9a173dec325d84fcc97e7828775c7b241c33466

Status: preparation; no measured results yet.

Use the upstream robust memory pipeline with a DeepSeek model verified against the user's account. Record the exact model identifier, endpoint, decoding settings, dataset hash and code commit. The robust pipeline and changed model differ from the original paper; results are a partial reproduction under changed conditions.

Proposed fixed subset: LoCoMo conv-30 (369 turns), selected before observing outcomes because it has the fewest turns. Preserve all conversation history. Select fixed category-stratified questions, excluding category 5 from the primary evaluation because its multiple-choice protocol differs from ordinary QA. Report selection and category counts explicitly.

Baseline retrieval k=10, modification k=5. All other settings identical. Build memory once, reuse identical memory for both arms, repeat QA 3 times per arm. Report mean and sample variance across runs, paired per-question differences, and note that repetitions do not measure memory-construction variability.

Primary metric: upstream token-set F1 (not an interchangeable implementation of official LoCoMo scoring). Secondary: exact match, wall time, API-reported prompt/completion tokens. Separate memory-build cost from QA cost. API failures must be reported, not silently treated as ordinary wrong answers.

First perform a small connectivity and memory-construction pilot to estimate tokens before the full experiment. Never invent outcomes or claim full-paper reproduction from this subset.

Required deliverables: report <=10 pages, reproducible GitHub repository, <=15-minute recorded Zoom presentation link. Draft slides and speaker notes can be prepared, but a real recording and hosted link must still be produced.
