# Reference target

Source: Xu et al., A-Mem: Agentic Memory for LLM Agents, arXiv:2502.12110v1 (17 February 2025), https://arxiv.org/html/2502.12110v1

Table 1, A-Mem with GPT-4o-mini, F1 (%): single-hop 27.02; multi-hop 45.85; temporal 12.14; open-domain 44.65; adversarial 50.03. Reported average answering token length: 2,520.

Our target is a restricted reproduction of the memory-backed QA capability, with measured category F1, followed by a retrieval-k intervention. These reference numbers are contextual, not matched-condition baselines: our model, robust prompts, data subset, and decoding settings differ. Category 5 is excluded. The intervention compares k=10 and k=5; the paper's Figure 3 studies k=10,20,30,40,50, so our intervention is an extension rather than an exact recreation of that figure.

Map LoCoMo categories using dataset documentation before labeling plots. Report answer-call input tokens separately from the complete keyword-generation plus answer pipeline if comparing token lengths.
