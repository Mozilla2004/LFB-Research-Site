# Structural State Ablation v0.3

**Archived pilot with a behavioral null result.** This project compares three research-state handoffs: evidence only (E), evidence plus compiled deductions in prose (P), and the same evidence/deductions organized as structural state (S). Six archived receiver runs produced the same observed sequence. No behavioral advantage was observed in this small experiment.

**结构化状态消融实验：保留无差异结果，检查评测本身。** 本项目展示任务定义、对照设计、信息等价检查、日志回放与结果审阅。它不是结构化交接有效性的证明，也不是已经验证的通用 benchmark。

## Start here

1. Read the [current review and corrections](REVIEW.md). It qualifies claims in the historical report.
2. Inspect the [task](v03/task.md), [E](v03/E.md), [P](v03/P.md), and [S](v03/S.md) handoffs.
3. Run the offline verifier below.
4. Read the [original report](REPORT_v0.3_PHASE1.md) and [recorded metrics](v03/results.json).

## Reproduce the archived checks

Python 3.10+; standard library only. No model account, API key or paid inference is required.

```bash
git clone https://github.com/Mozilla2004/LFB-Research-Site.git
cd LFB-Research-Site/research/structural-state-ablation-v0.3
python3 verify_release.py
```

Expected final line: `PASS: archived gates, replay, submissions, metrics, and source preservation`.

This recomputes scores from archived logs and replays deterministic oracle responses. It **does not** rerun the original model sessions, independently authenticate their provenance, or reproduce model behavior from scratch. The historical report attributes those sessions to GLM-5.3 through a ZCode harness; this release has not independently verified that model attribution.

## Experimental comparison

| Arm | Supplied content | Intended comparison |
|---|---|---|
| E | Nine recorded observations | Evidence-only baseline |
| P | Same observations plus 13 compiled deductions in prose | P vs E: effect of supplying deductions |
| S | Same observations and deductions in operational sections | S vs P: organization, with core content held fixed |

A deployment requirement arrives after the handoffs are frozen. The receiver continues in a deterministic candidate-selection environment. P/S rendering differs in length; this is not an equal-token comparison.

## Observed results

| Arm | Recorded successes | Recorded action sequences | Mean harness tokens |
|---|---:|---|---:|
| E | 2/2 | probe B2, submit C2 (both runs) | 41,438 |
| P | 2/2 | probe B2, submit C2 (both runs) | 45,292 |
| S | 2/2 | probe B2, submit C2 (both runs) | 48,865 |

All six runs have one probe and one submit. These are observations, **not a proof of a two-action optimum**. The original optimality claim is corrected in [REVIEW.md](REVIEW.md). No confidence interval, general superiority claim or cross-domain validation is warranted by two runs per arm on one task/reveal. Harness token totals are not comparable to generated-output-only token counts.

## Files

- `v03/`: unmodified extracted experiment files, logs, handoffs, manifests, scoring code and final responses.
- `REPORT_v0.3_PHASE1.md`: unmodified historical report; consult corrections before citing.
- `verify_release.py`: offline verification wrapper; runs mutating historical scripts only inside a temporary copy, checks submissions against the oracle and compares recomputed metrics.
- `SOURCE_SHA256.json`: hashes of the uploaded archive and every preserved source file.
- `REVIEW.md`: release-time findings, evidence limits and human/AI contribution statement.

## Limits and reuse

This is a synthetic toy environment, with instruction-based file isolation, one selected reveal and no controlled seeds. Logs are compact records rather than full provider-authenticated model transcripts. The publication wrapper is new; the archived experiment is not a new run.

Ground truth and oracle internals are public here for **audit**. A future live evaluation must isolate them from the evaluated agent and protect held-out tasks. Do not give this complete repository to a receiver and call the resulting score a blind evaluation.

Alex Lu / 陆向荣: problem framing, experiment constraints and review, in collaboration with AI systems. AI tools assisted implementation, execution and documentation. This release presents collaborative work, not a claim of unaided software implementation.
