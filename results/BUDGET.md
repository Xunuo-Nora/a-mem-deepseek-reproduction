# Budget estimate, 2026-11-10

Official CNY pricing: https://api-docs.deepseek.com/zh-cn/quick_start/pricing/
Flash peak per million tokens: input cache miss CNY 2; input cache hit CNY 0.04; output CNY 8. Off-peak half price.

Successful five-note pilot: 7,108 input + 1,379 output = CNY 0.025248 at peak, ignoring discounts. Linear extrapolation to 369 notes = CNY 1.8633. This is NOT a reliable final estimate: mature memories have longer linked context.

Planning scenarios (not measured forecasts): memory construction 1-3M input / 0.1-0.3M output = CNY 2.8-8.4; QA 0.5-2M input / 0.01-0.05M output = CNY 1.08-4.4. Combined CNY 3.88-12.8 before retries. Reserve up to CNY 18, within user-reported CNY 22 balance.

Guard conservatively charges all logged tokens at peak cache-miss rates and reserves the next call using UTF-8 bytes plus overhead and full output cap. Stops rather than silently reducing experiment scope. Actual account billing remains authoritative; other simultaneous account usage is not included.
