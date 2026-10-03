# Embodied Experience Representation Benchmark

**Reviewed snapshot: v0.1.6 + a public scoring extract of the archived 900-call Kimi Track M run.**

This synthetic, text-only pilot compares three information-matched renderings of experience. All arms scored **120/120 on the primary action metric**. The historical stopping decision is retained. This does not establish that raw robot trajectories are sufficient or that state-change representations have no value.

## 中文导读

项目已执行一轮 900 次调用，不再只是设计方案。它展示事实匹配、冻结输入、分层分母、盲评分和负结果保留。当前主要局限是任务对源经验的依赖尚未建立、主指标已饱和。适合作为**评测设计与审计作品**，不宜当作真机迁移能力或“轨迹充分”的验证。

[中文审阅与后续最小验证建议](REVIEW.md)

## Verify the public scoring extract

Python 3.10+; standard library only. From a clone of this repository:

```bash
cd research/embodied-experience-representation-benchmark
python3 verify_release.py
```

This checks public file hashes, 900 answer slots, scoring denominators, primary/secondary results, the original family-bootstrap calculation, and the review diagnostics. No network or API calls. It **does not** verify transport, re-run a model, or authenticate historical remote execution.

## Recorded result

| Measure | Raw-style A | Plain-prose B | State-change C |
|---|---:|---:|---:|
| Primary T3/T4 Q2 | 120/120 | 120/120 | 120/120 |
| Near T1/T2 Q2 | 118/120 | 116/120 | 112/120 |
| All-valid-case Q3 | 182/297 | 183/297 | 183/297 |
| Valid boundary refusal | 57/57 | 57/57 | 57/57 |

20 families × 5 cases × 3 representations × 3 repeats = 900 records. Nine F11_T5 conditions are retained but excluded under the original invalid-case rule; 891 remain. The primary contains 40 distinct cases, not 120 independent cases per arm. The original record identifies Kimi-K2.5 through a SiliconFlow INT4 route, thinking disabled; endpoint variant was constrained rather than echoed.

## What is actually varied

Track M shares the same 12 canonical sentences across all three arms, including changed-variable, correction and applicability/exclusion annotations. Raw is already annotated text. Summary joins the sentences into prose. State-Change adds headings and changes ordering. This primarily tests organization of explicit information, not raw sensor experience versus extracted knowledge. Track P and four mechanism controls were not executed in the supplied full run.

## Review findings

- On the full private source package, frozen hashes and all 917 original run-manifest entries matched; parser/scorer/aggregate artifacts replayed byte-identically, and all 119 original tests passed with historical dependencies present.
- Those full-package checks are reviewer observations. The public extract supports the narrower score verification described above.
- Structured current-case constraints plus authored candidate semantics recover 40/40 primary answers without the source experience. This is not an LLM no-experience baseline or an independent natural-language solver.
- The first Q1 option matches 89/100 case oracles, exposing a strong position baseline.
- Most Q3 errors are PARTIAL→YES. All 20 families retain the same option-text set across T1–T4 despite scenario changes. Far-transfer labels do not establish increased adaptation difficulty.

## Public data scope

- `data/`: synthetic cases, source experiences, three renderings, authored action semantics, public oracles and 900 anonymous Q1–Q3 answer records.
- `source/`: selected unchanged scoring/constraint modules and original design/preregistration/invalid-case documents.
- `SOURCE_SHA256.json`: public-file digests and the source-upload digest.
- `verify_release.py`: public scoring and diagnostic checks.
- `REVIEW.md`: current interpretation; it qualifies the historical H0/Stop language.

No API envelopes, request headers, provider metadata, account-resource records, remote generation identifiers or Q4 free text are included. The original complete package remains with its owner. Publication is a selected scoring extract, not the original experiment bundle; no original result or threshold was changed.

All cases/oracles are public audit material and should not be treated as secret test data for a future blind run.

## Contributions

Alex Lu / 陆向荣: research framing, experimental constraints and review decisions in collaboration with AI. AI assisted implementation, execution and documentation. This describes collaborative work, not unaided engineering or independent domain-expert validation.
