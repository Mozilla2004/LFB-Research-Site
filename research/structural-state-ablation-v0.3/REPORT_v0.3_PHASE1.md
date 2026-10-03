# REPORT v0.3 PHASE 1 — Capability Transfer (E → P → S)

**Result: behavioral null at the optimal-action floor.** All six ordinary GLM-5.3 receivers (E×2, P×2, S×2) continued correctly from the frozen Stage-1 state under the revealed Stage-2 requirement, and every run executed the identical optimal two-action sequence: one informative probe (B2, the single genuinely unknown branch) and one correct submit (C2). Zero evidence re-queries, zero deduction re-computations, zero dead-region probes, zero reveal-inconsistent probes in every condition. Computation transfer (P vs E) and structural organization (S vs P) produced no observable behavioral difference; the only measurable difference was receiver token totals, which were **lowest for E** because the compiled handoffs are larger to ingest — and token differences alone never support the hypothesis. Phase 1 stops here; a Strong Receiver phase is **not justified** on this data (no ordinary-receiver gap exists that a stronger receiver could shrink; the environment's action floor was reached by everyone).

All artifacts: [v03](v03/). Reproduce scoring without any model calls: `python3 v03/score.py`, `python3 v03/verify.py`.

---

## 1. Inheritance map: KEEP / ADAPT / RETIRE

### KEEP (reused, unchanged in kind)
- **SHA-256 manifest freezing at multiple gates** (v0.1 `freeze.py`, v0.2 `manifest.json`) → `v03/manifest_g1…g4.json`: environment, evidence bank, deduction inventory + handoffs, reveal + run config frozen in that order.
- **Verify-by-replay + brute-force ground truth** (v0.1 `verify.py`) → `v03/verify.py`: every recorded probe result replays identically through the fixed service; per-reveal answers re-derived by enumeration.
- **Metrics recomputed only from frozen artifacts** (v0.1 `score.py`, v0.2 `finish.py`) → `v03/score.py`.
- **Deterministic rendering from one canonical JSON + mechanical equivalence audit** (v0.2 `setup.py`: B/C carried identical atoms) → `v03/render.py` + `v03/audit.py`, lifted from atoms to deductions.
- **Dead-branch / known-failure rediscovery / progress-per-action metric definitions** (v0.2 protocol) → retained and refined (see §10).
- **Scripted deterministic explorer to conserve quota** (v0.2 §3) → kept: one scripted pass, nine probes, no LLM exploration.
- **Run discipline**: fresh sessions per run, identical prompt template / action limits / stopping rules across conditions, instruction-based file isolation, predeclared directional criteria, "token savings alone are insufficient", negative results are valid (v0.2 protocol) → all kept.

### ADAPT (kept, modified for v0.3)
- **Task semantics** (`v03/oracle.py`): the v0.2 opaque-candidate probe/certificate service gains conditional availability rules (a probe restates a rule and cannot resolve it), pair-scoped certificates, a service compatible with several candidates, and submit evaluated against a **deployment requirement** (was: single accepted candidate whose acceptance certificate excluded all alternatives).
- **Handoff set**: v0.2's information-equivalent B/C pair → **E** (evidence only) / **P** (evidence + complete deduction inventory as prose) / **S** (same content in operational schema), realizing the E→P→S causal chain.
- **Two-stage structure**: Stage-1 freeze → Stage-2 requirement reveal, new.
- **Receiver runtime**: Codex/gpt-6-astra session logs → ZCode GLM-5.3 Agent-tool subagents with harness telemetry (`subagent_tokens`, `tool_uses`, `duration_ms`).
- **Metrics**: added *evidence re-query* and *deduction re-computation* as observable-only categories, union-counted with (not added to) dead-region metrics.

### RETIRE (not reused, with reason)
- **v0.1 near-complete handoff** — three forced assignments from completion leaves no residual search (v0.1 lesson).
- **v0.2 B/C information-equivalence design** — reduced the question to explicit categorization vs. implicit structure already recoverable from prose (v0.2 lesson); replaced by the E→P→S causal design in which Structural State is *allowed* to carry valid derived cognition absent from E.
- **v0.2 "exactly one accepted candidate" + acceptance-carries-uniqueness probe semantics** — incompatible with re-solving under a newly revealed requirement and with transfer ≠ retrieval.
- **v0.2 flat-atom condition** — v0.3's E must deliberately *lack* the compiled deductions, so flat evidence is no longer atom-equivalent to the structured conditions.
- **Codex session-log token extraction** — that harness is gone; replaced by Agent-tool telemetry.

## 2. Lessons inherited and how v0.3 honors them
- **v0.1 (handoff too close to completion):** v0.3 freezes Stage 1 with four open branches and a deliverable that is *undeterminable* at handoff time (D12); the receiver must inherit → interpret → choose → continue searching → verify. Every run performed a genuine new probe.
- **v0.2 (flat and structural made information-equivalent):** v0.3 separates the effects. E carries only observations; P adds the complete audited deduction inventory; S carries exactly the same inventory organized operationally. P/S equivalence is enforced mechanically (§7), and S adds no deduction absent from P.

## 3. v0.3 task and modifications from the prior framework
Environment: candidates A1–F4 in a fixed opaque compatibility service. Probes return authoritative rejection certificates with explicit exclusion scopes (family / variant-column / pair / single) or **conditional availability rules that a probe cannot resolve**. The service may be compatible with several candidates. The deliverable is the unique candidate that is both service-compatible and satisfies a **deployment requirement** (profile ∈ {batch, extended} + a public family/variant constraint) that is revealed only after the handoff is frozen. The full set of four possible reveals (V1–V4) is fixed inside the oracle from Gate 1, so the environment never changes — only information arrives.

Decision on reuse (per spec §3): the v0.2 framework was retained (candidates, families/variants, certificates, oracle CLI pattern, action limits, scoring pipeline) and only the task logic that v0.3 requires was replaced — conditional rules, multi-compatibility, reveal-gated submission, and the two-stage freeze discipline. Nothing unrelated was introduced.

## 4. Stage-1 Source Evidence (frozen, Gate 2)
One scripted explorer, nine probes, run once, order fixed in advance: `A2, F1, B1, E4, B3, C3, D2, C2, E2`. Stable Evidence IDs E01–E09; every record carries the original certificate verbatim:

| ID | probe | result |
|---|---|---|
| E01 | A2 | REJECTED — "family A retired" (scope A1–A4) |
| E02 | F1 | REJECTED — "family F retired" (scope F1–F4) |
| E03 | B1 | REJECTED — "variant 1 discontinued everywhere" (scope all \*1) |
| E04 | E4 | REJECTED — "variant 4 discontinued everywhere" (scope all \*4) |
| E05 | B3 | REJECTED — "family B unavailable at variants 3 and above" (scope B3, B4) |
| E06 | C3 | REJECTED — "variant 3 unavailable in families C and D" (scope C3, D3) |
| E07 | D2 | REJECTED — "family D unavailable" (scope D1–D4) |
| E08 | C2 | CONDITIONAL — "unavailable while any family-D variant-2 unit is deployable; a probe restates this rule and does not resolve it" |
| E09 | E2 | CONDITIONAL — "available for batch deployment profiles, unavailable for extended profiles; a probe restates this rule…" |

Union of scopes excludes 20 of 24 candidates. **Plausible set: {B2, C2, E2, E3} — four meaningful branches** (unknown / deducible-conditional / profile-conditional / unknown). No Stage-2 information entered the bank. The bank was hashed (Gate 2) before any handoff existed.

## 5. Canonical Deduction Inventory (frozen, Gate 3)
Authored only from `bank.json` + `task.md`; zero environment queries during compilation (recorded in inventory metadata). Each entry carries: Deduction ID, supporting Evidence IDs, basis/rule, scope, consequence, validity status, affected branches, dependencies, candidate-space note. Thirteen deductions, D01–D13:

- **D01–D07** (each ← one of E01–E07): the seven exclusion consequences, e.g. D07: family D entirely unavailable, including D2, the only variant-2 candidate in family D.
- **D08** (← E01–E07, builds on D01–D07): candidate space = exactly {B2, C2, E2, E3}.
- **D09** (← E08, builds on D07): **dependency resolution** — C2 is blocked only while some family-D variant-2 unit is deployable; by D07 none is, so C2 is service-compatible; a probe would only restate the rule. *This is the crown-jewel compiled cognition: valid, auditable, and not directly observed.*
- **D10** (← E09): E2 compatible iff the deployment profile is batch (open at handoff).
- **D11** (← D08, absence of evidence): B2 and E3 are fully unresolved open branches.
- **D12** (task rules + D08–D11): the deliverable is undeterminable at handoff; it depends on the requirement revealed only at continuation.
- **D13** (task rules): invariants — fixed policy, certificate authority, conditional-rule semantics, multi-compatibility.

Frozen and hashed before any receiver ran. This inventory is the single canonical source for both P and S.

## 6. E / P / S handoffs (deterministically rendered)
All three contain the identical evidence block of §4 verbatim.

- **E — Flat Evidence** (267 words / 1,734 chars): the nine observations in exploration order, competently formatted, with an explicit statement that no derived conclusions are included. E answers *what was observed*. Not degraded, no omissions of observations.
- **P — Compiled Prose** (1,224 words / 7,748 chars): the same evidence plus the complete inventory D01–D13 as ordered prose paragraphs with inline citations ("D09 (from E08; building on D07). …"). E answers + what has already been inferred.
- **S — Structural State** (1,363 words / 9,317 chars): the same evidence plus the same deductions under operational headings — Candidate-space state / Failed paths / Dependencies / Conditional status / Open branches / Task-level constraint / Invariants — each entry carrying evidence provenance, basis, scope, consequence, validity, affected branches, candidate-space update (evidence → constraint → scope → consequence → search-space update). S adds **no** substantive deduction absent from P.

Renderers are deterministic (`render.py`); no model authored P or S.

## 7. P/S equivalence audit (mechanical, `audit.py`)
- Every deduction D01–D13 appears exactly once as an anchor in P and once in S (bracketed entry), with **identical evidence-citation sets** per deduction.
- The **consequence sentences are byte-identical** across P and S; only organization differs.
- All three handoffs contain every bank record and certificate verbatim.
- E contains **no** deduction ID, no four-branch enumeration, no C2-resolution claim (asserted).
- S's overhead over P: +11.4% words, +20.2% chars — headings and field labels only.
Re-run inside `verify.py`; passes on every invocation.

## 8. Stage-2 perturbation (frozen, Gate 4)
Constructed **only after** Gates 1–3. Hidden ground truth fixed at Gate 1: V1→E3, V2→C2, V3→E2, V4→C2 (each verified unique by enumeration). Selection criterion, documented in `runs.json` and applied after Gate 3, condition-independent: choose the reveal whose answer is the **deduced-conditional** candidate with residual probe uncertainty — i.e. maximal diagnostic value for both E→P and P→S. That is **V2**: profile = **batch**, constraint = **family ∈ {A, B, C, D}** (answer C2). V1/V3 would have made the answer retrievable from an open/conditional branch without the dependency resolution. All six receivers received the identical reveal (`reveal.md`), hashed at Gate 4. No completed solution was inferable during compilation: the answer is a function of the reveal, which did not exist for the compiler.

Why V2 forces re-solving: requirement ∩ plausible set = {B2, C2}; B2's status is unknown to everyone (genuine new probe required); C2's compatibility is exactly deduction D09 (or, for E, a two-step chain the receiver must perform itself). Transfer ≠ retrieval held: no handoff contains the answer.

## 9. Six GLM-5.3 runs
Fresh Agent-tool subagent sessions of the ordinary harness model (GLM-5.3; no strong-receiver/Astra condition, no capability modification). Identical task access, tools, limits (≤6 probes, exactly 1 submit, ≤100-word final), stopping rules, and prompt template — differing only in the assigned handoff file. Instruction-based file isolation (inherited limitation). Launch order balanced: **p1, e1, s1, e2, p2, s2** (each condition once per half). No pilot runs; the six launches above are all runs that were started, and none was discarded.

| Run | Condition | Sequence | Correct | Probes | Actions | Harness telemetry |
|---|---|---|---|---:|---:|---|
| p1 | P | B2 → submit C2 | Yes | 1 | 2 | 46,373 tok · 5 tools · 145 s |
| e1 | E | B2 → submit C2 | Yes | 1 | 2 | 41,246 tok · 5 tools · 29 s |
| s1 | S | B2 → submit C2 | Yes | 1 | 2 | 46,236 tok · 5 tools · 28 s |
| e2 | E | B2 → submit C2 | Yes | 1 | 2 | 41,630 tok · 5 tools · 32 s |
| p2 | P | B2 → submit C2 | Yes | 1 | 2 | 44,211 tok · 5 tools · 43 s |
| s2 | S | B2 → submit C2 | Yes | 1 | 2 | 49,494 tok · 5 tools · 58 s |

All six final messages (in [finals/](v03/finals/)) correctly credit inherited information and describe applying the reveal themselves. Qualitative note: s2 reported "re-derived C2's availability" internally despite D09 being supplied — per protocol, internal reconstruction is unobservable and is not counted as re-computation; it is quoted only as color.

## 10. Behavioral metrics
Definitions (observable behavior only): *evidence re-query* = probe of a candidate whose exact Stage-1 probe result is in the assigned handoff (all conditions); *deduction re-computation* = externally re-establishing a status explicitly supplied in the handoff (defined for P/S; for E such probes are necessary derivation, not redundancy); *redundant probes* = union of the two, so dead-region metrics are not double-counted with them; *dead-region* = probes inside frozen exclusion scopes; *reveal-inconsistent* = probes violating the public V2 constraint; *progress* = eliminations of the four-branch handoff set (correct submit resolves the answer, mirroring v0.2 accounting).

| Metric | E (e1,e2) | P (p1,p2) | S (s1,s2) |
|---|---:|---:|---:|
| Verified success | 2/2 | 2/2 | 2/2 |
| Actions to verified success | 2, 2 | 2, 2 | 2, 2 |
| Environment probes | 1, 1 | 1, 1 | 1, 1 |
| Evidence re-queries | 0, 0 | 0, 0 | 0, 0 |
| Deduction re-computations | n/a (E has none supplied) | 0, 0 | 0, 0 |
| Redundant probes (union) | 0, 0 | 0, 0 | 0, 0 |
| Dead-region probes / fraction | 0 (0.0) | 0 (0.0) | 0 (0.0) |
| Known-failure rediscovery (inherited metric) | 0 | 0 | 0 |
| Reveal-inconsistent probes | 0, 0 | 0, 0 | 0, 0 |
| Informative probes | 1, 1 | 1, 1 | 1, 1 |
| Candidate reduction / progress per action | 3 / 1.50 | 3 / 1.50 | 3 / 1.50 |
| Receiver tokens (harness, mean) | **41,438** | 45,292 | 48,865 |

Token figures are harness-reported whole-subagent totals (input-dominated cumulative counts), not generated-output-only telemetry as in v0.1/v0.2; they largely track handoff ingestion size (E < P < S) and are reported for completeness only. Per the predeclared rule, token differences cannot support any hypothesis.

**Optimality note:** two actions is the deterministic optimum for this environment under V2 — {B2, C2} cannot be distinguished without either probing B2 or gambling on a 50% submit. Every receiver, in every condition, hit the floor with zero variance.

## 11. Cost accounting
Recorded separately, as required:

1. **Stage-1 source exploration:** 9 scripted oracle calls; zero LLM tokens (deterministic explorer, v0.2 quota-conservation pattern).
2. **Deduction compilation:** coordinator-authored inventory (13 entries); LLM cost not metered by this harness (limitation); zero environment queries (asserted).
3. **Handoff rendering / validation:** deterministic scripts (`render.py`, `audit.py`); zero LLM cost; repeated validation is free.
4. **Receiver continuation:** table in §9 (per-run tokens/tools/duration).

- **Receiver-only continuation cost:** E 41,438 · P 45,292 · S 48,865 mean tokens; 1 probe + 1 submit everywhere.
- **Single-use end-to-end cost:** receiver cost + compilation. Compilation is unmeasured but strictly positive (authored artifact); observed per-receiver savings from compiling are **zero actions, zero redundant probes, and negative token savings** (P and S cost ~9% and ~15% *more* receiver tokens than E, from ingestion size).
- **Break-even reuse count:** with zero per-use behavioral saving and negative per-use token saving, no finite number of future receiver uses amortizes the compilation cost. Under Phase-1 conditions the answer is **never** — not because compilation is expensive, but because it bought nothing observable here.

No single success-per-dollar score was computed, per protocol.

## 12. P vs E — Computation Transfer: **not supported (behaviorally)**
Both E receivers internally reconstructed everything P supplies: the 20-candidate exclusion union, the four-branch space, and the D09 dependency chain (their finals explicitly describe resolving C2's rule from E07 + E08). Action sequences, probe choices, redundancy, dead-region expenditure, and progress-per-action were identical to P — and identical to the environment's optimal floor. The predeclared criterion (consistent behavioral advantage in both pairs without correctness loss) is not met; the observed token advantage runs the *wrong way* for the hypothesis and is excluded by rule. Negative result, reported as such.

## 13. S vs P — Structural Organization: **not supported**
Same content, same citations, same consequences; only organization differed. Behavior was identical in both pairs (1 probe, 1 submit, 0 redundant). S's larger rendering cost slightly more receiver tokens. Explicit operational structure did not make the same compiled cognition observably easier to consume for this receiver on this task.

## 14. S vs E — Total Structural Handoff Effect: **not supported**
The complete Structural State package (evidence + compiled deductions + operational schema) did not improve continuation over flat evidence on any behavioral measure; both hit the optimal floor, and S cost ~15% more receiver tokens than E. The single most informative observation is that **ordinary GLM-5.3 re-derives cheap, short deduction chains internally and flawlessly**: when the residual computation is this inexpensive for the receiver, transferring it in the handoff cannot show up in observable behavior — it can only add ingestion cost.

## 15. Which previous components proved reusable
Everything in the KEEP column of §1 was reused and worked without modification in kind: gate-hashed freezing, replay verification with brute-forced ground truth, deterministic rendering plus mechanical equivalence auditing, metrics recomputation from frozen artifacts only, the scripted explorer, and the run/protocol discipline (fresh sessions, identical limits, balanced order, predeclared criteria, no hidden pilots, no discarded runs). The v0.2 oracle CLI/action-log pattern carried over cleanly. What did *not* transfer usefully was the v0.2 B/C comparison design — exactly the retirement v0.2's own report recommended. One operational substitution was forced by the harness change (Codex session telemetry → Agent-tool telemetry), which degrades token metrics from generated-only to whole-session totals; this is disclosed wherever tokens are cited. Disclosure: Gate 1 was re-frozen once *before* Stage-1 exploration completed (explorer probe-cap bug, `oracle.py` line-level fix; no receiver or handoff existed yet); `audit.py` re-freezes Gate 3 idempotently on each verification run.

## 16. Strong Receiver gate: **not justified**
The future strong-receiver phase asks whether E→P or P→S benefits *shrink* as receiver capability rises. A shrinkage design presupposes a nonzero ordinary-receiver benefit to shrink. Phase 1 observed none — not because a benefit was washed out by variance, but because the ordinary receiver already performed at the environment's deterministic optimum with zero redundancy in all three conditions. A stronger receiver cannot do better than the floor already achieved, so the question would be unanswerable in this environment. If this line continues, the prerequisite is a **harder continuation environment** (deeper dependency chains, more open branches, costlier re-derivation) in which ordinary receivers demonstrably deviate from optimal — not a stronger receiver on this one. Per protocol, Phase 2 is not run.

---

**Phase 1 is complete and stopped. No v0.4 was started.**

### Limitations (inherited + new)
n = 2 per condition; no seed control; instruction-based file isolation on a shared filesystem; one task, one reveal; token telemetry is whole-session rather than generated-only; scripted (not experienced) Stage-1 exploration; coordinator-authored compilation of a deliberately short deduction chain. A behavioral null under these conditions does not establish that compiled or structural handoffs never help — it establishes that they do not help *this* receiver on *this* residual computation, and it identifies the design condition under which no handoff can help: when internal re-derivation is cheaper than ingestion.
