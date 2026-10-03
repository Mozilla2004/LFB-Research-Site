# Release review 2026-10-04

## Scope

This review accompanies the preserved `Structural State Ablation03.zip` source. Original experiment files and the original report remain byte-identical. New documentation takes precedence over the historical report where it explicitly corrects a claim.

## Findings

1. **Historical two-action optimality claim is not supported.** E07 excludes family D; E08 says C2 is unavailable while a family-D variant-2 unit is deployable. Thus C2's compatibility can be inferred without probing B2. Under V2, C2 meets the profile and family constraint. `task.md` also promises a unique qualifying candidate, and the oracle CLI allows submit without a preceding probe. A direct correct submit of C2 is therefore available in one action. All six archived receivers used two actions; that observation remains valid, but the report's claim that all hit a necessary two-action floor must not be repeated. A follow-up would need to examine why all receivers made the extra probe.
2. **The behavioral null remains a descriptive result.** P/E and S/P show no observed difference in six archived runs. This does not establish equivalent capabilities, an optimal floor, or a general law about handoff utility. The report's strong-receiver stopping rationale and break-even generalizations inherit limits from this small design.
3. **The historical verifier mutates files.** `verify.py` imports `audit.py`, which writes `audit.json` and re-freezes `manifest_g3.json`. The new wrapper checks preserved file hashes first and runs these scripts in a disposable copy, then confirms the frozen gate still matches. It does not silently repair the source.
4. **Submit records need independent checking.** Historical `verify.py` replays probes but does not recompute every submit. The wrapper checks each recorded submission against `compatible` and the selected reveal predicate before scoring.
5. **An audit comment exceeds the implementation.** `audit.py` declares a whitelist of structural labels but does not enforce it. Its content/citation assertions are useful checks, not a proof that all possible semantic differences have been excluded.
6. **Provenance limits remain.** Manifests detect changes relative to supplied hashes; they do not establish trusted timestamps, external preregistration or model-provider provenance. The offline checks use supplied logs and final responses. There is no claim of freshly rerunning six live model sessions.

## Human and AI contribution

陆向荣 / Alex Lu supplied the research direction, constraints and review decisions in collaboration with AI. AI-assisted tools produced experimental code, execution artifacts and documentation. The 2026-10-04 publication work added this review, a reproducibility wrapper and an index. It did not regenerate or improve the recorded model results.

## Verification scope

The release wrapper verifies archived hashes, freeze gates, oracle probe replay, P/S audit assertions, submit correctness and exact recomputation of `results.json`, while preserving source files. It also checks that the public CLI permits a direct C2 submit under V2 in a temporary copy. These checks establish local artifact consistency, not full experimental validity or historical authenticity.
