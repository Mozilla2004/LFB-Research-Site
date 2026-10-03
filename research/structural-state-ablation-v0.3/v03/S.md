# Handoff S — Structural State

This structural state contains two blocks: the complete frozen record of what was observed during Stage-1 source exploration, then the complete audited inventory of everything already inferred, organized by operational relationship (evidence -> constraint -> scope -> consequence -> search-space update). Nothing here was obtained by querying the environment during compilation. Every entry is traceable to the cited observations or to the task rules.

## Block 1 — Evidence (what was observed)

E01 — probe A2: REJECTED. Certificate: "family A retired". Stated exclusion scope: A1, A2, A3, A4.
E02 — probe F1: REJECTED. Certificate: "family F retired". Stated exclusion scope: F1, F2, F3, F4.
E03 — probe B1: REJECTED. Certificate: "variant 1 discontinued everywhere". Stated exclusion scope: A1, B1, C1, D1, E1, F1.
E04 — probe E4: REJECTED. Certificate: "variant 4 discontinued everywhere". Stated exclusion scope: A4, B4, C4, D4, E4, F4.
E05 — probe B3: REJECTED. Certificate: "family B unavailable at variants 3 and above". Stated exclusion scope: B3, B4.
E06 — probe C3: REJECTED. Certificate: "variant 3 unavailable in families C and D". Stated exclusion scope: C3, D3.
E07 — probe D2: REJECTED. Certificate: "family D unavailable". Stated exclusion scope: D1, D2, D3, D4.
E08 — probe C2: CONDITIONAL (not rejected, not accepted). Certificate: "C2 availability rule: unavailable while any family-D variant-2 unit is deployable; a probe restates this rule and does not resolve it". Stated exclusion scope: none.
E09 — probe E2: CONDITIONAL (not rejected, not accepted). Certificate: "E2 availability rule: available for batch deployment profiles, unavailable for extended profiles; a probe restates this rule and does not resolve it". Stated exclusion scope: none.

## Block 2 — Structural state (what has already been inferred, and how it organizes the search)


Candidate-space state:
[D08]
  evidence provenance: E01, E02, E03, E04, E05, E06, E07
  depends on: D01, D02, D03, D04, D05, D06, D07
  constraint / basis: enumeration of the 24-candidate space minus the union of the exclusion scopes D01 through D07
  scope: whole candidate space
  consequence: Exactly four candidates are not excluded by any frozen certificate: B2, C2, E2 and E3. Every other candidate is unavailable, so all further work concerns only these four branches.
  validity / confidence: valid, derived
  affected branches: B2, C2, E2, E3
  candidate-space update: candidate space reduced from 24 to 4: {B2, C2, E2, E3}


Failed paths (certain exclusions):
[D01]
  evidence provenance: E01
  depends on: none
  constraint / basis: task rule: a rejection certificate rules out every candidate in its stated scope
  scope: family A: A1, A2, A3, A4
  consequence: A1, A2, A3 and A4 are all unavailable; the entire family A is out of consideration.
  validity / confidence: valid, directly evidenced
  affected branches: A1, A2, A3, A4
  candidate-space update: removes A1, A2, A3, A4 from the 24-candidate space
[D02]
  evidence provenance: E02
  depends on: none
  constraint / basis: task rule: a rejection certificate rules out every candidate in its stated scope
  scope: family F: F1, F2, F3, F4
  consequence: F1, F2, F3 and F4 are all unavailable; the entire family F is out of consideration.
  validity / confidence: valid, directly evidenced
  affected branches: F1, F2, F3, F4
  candidate-space update: removes F1, F2, F3, F4 from the 24-candidate space
[D03]
  evidence provenance: E03
  depends on: none
  constraint / basis: task rule: a rejection certificate rules out every candidate in its stated scope
  scope: variant column 1: A1, B1, C1, D1, E1, F1
  consequence: Every variant-1 candidate is unavailable in all families.
  validity / confidence: valid, directly evidenced
  affected branches: A1, B1, C1, D1, E1, F1
  candidate-space update: removes the variant-1 column (members not already removed by D01/D02: B1, C1, D1, E1)
[D04]
  evidence provenance: E04
  depends on: none
  constraint / basis: task rule: a rejection certificate rules out every candidate in its stated scope
  scope: variant column 4: A4, B4, C4, D4, E4, F4
  consequence: Every variant-4 candidate is unavailable in all families.
  validity / confidence: valid, directly evidenced
  affected branches: A4, B4, C4, D4, E4, F4
  candidate-space update: removes the variant-4 column (members not already removed: B4, C4, D4)
[D05]
  evidence provenance: E05
  depends on: none
  constraint / basis: task rule: a rejection certificate rules out every candidate in its stated scope
  scope: family B at variants 3 and above: B3, B4
  consequence: B3 and B4 are unavailable; this certificate does not cover B1 or B2.
  validity / confidence: valid, directly evidenced
  affected branches: B3, B4
  candidate-space update: removes B3 (B4 is already removed by D04)
[D06]
  evidence provenance: E06
  depends on: none
  constraint / basis: task rule: a rejection certificate rules out every candidate in its stated scope
  scope: variant 3 within families C and D: C3, D3
  consequence: C3 and D3 are unavailable; variant 3 elsewhere is not covered by this certificate.
  validity / confidence: valid, directly evidenced
  affected branches: C3, D3
  candidate-space update: removes C3 and D3
[D07]
  evidence provenance: E07
  depends on: none
  constraint / basis: task rule: a rejection certificate rules out every candidate in its stated scope
  scope: family D: D1, D2, D3, D4
  consequence: The entire family D is unavailable, including D2, the only variant-2 candidate in family D.
  validity / confidence: valid, directly evidenced
  affected branches: D1, D2, D3, D4
  candidate-space update: removes D2 (D1, D3, D4 already removed by D03/D06/D04)


Dependencies (conditional rule, resolved):
[D09]
  evidence provenance: E08
  depends on: D07
  constraint / basis: conditional-rule resolution: the rule's stated terms evaluated against established evidence (no new probe)
  scope: candidate C2
  consequence: C2's rule blocks it only while some family-D variant-2 unit is deployable. By D07 the entire family D is unavailable, so no family-D variant-2 unit is deployable, the blocking condition is false, and C2 is service-compatible. A probe would only restate the rule and cannot confirm this.
  validity / confidence: valid, deduced (not directly observed)
  affected branches: C2
  candidate-space update: C2 is an available member of the remaining four


Conditional status (partial success, unresolved):
[D10]
  evidence provenance: E09
  depends on: none
  constraint / basis: conditional-rule reading: compatibility depends on the deployment profile, which is not part of Stage-1 knowledge
  scope: candidate E2
  consequence: E2 is service-compatible if the eventual deployment profile is batch, and unavailable if the profile is extended. E2's compatibility therefore remains unresolved until the deployment requirement is revealed.
  validity / confidence: conditional, open at handoff
  affected branches: E2
  candidate-space update: E2 remains in the space with a profile-dependent status (partial success)


Open branches (no information):
[D11]
  evidence provenance: E01, E02, E03, E04, E05, E06, E07, E08, E09
  depends on: D08
  constraint / basis: absence of evidence: no frozen observation or rule covers B2 or E3
  scope: candidates B2 and E3
  consequence: B2 and E3 carry no availability information in the frozen evidence: they are neither excluded nor governed by any known rule. Their compatibility is unknown and can only be established during continuation, for example by probing or by the outcome of a submission.
  validity / confidence: open
  affected branches: B2, E3
  candidate-space update: two of the four remaining branches are fully unresolved


Task-level constraint on continuation:
[D12]
  evidence provenance: task rules
  depends on: D08, D09, D10, D11
  constraint / basis: task rules: the deliverable must be both service-compatible and satisfy the deployment requirement; the requirement is revealed only at continuation and exactly one candidate satisfies both
  scope: continuation contract
  consequence: The deliverable cannot be determined from Stage-1 knowledge: it depends on the deployment requirement, which consists of a deployment profile and a family or variant constraint revealed only at continuation time. The residual task is to apply the revealed requirement to the four remaining candidates, resolve the remaining conditionals, and submit the unique candidate that is both service-compatible and requirement-satisfying.
  validity / confidence: valid, meta
  affected branches: B2, C2, E2, E3
  candidate-space update: no candidate can be singled out before the requirement is revealed


Invariants:
[D13]
  evidence provenance: task rules
  depends on: none
  constraint / basis: task rules
  scope: whole task
  consequence: The service policy is fixed throughout exploration and continuation; certificates remain authoritative within their stated scope; conditional rules resolve according to their stated terms; the service may be compatible with several candidates at once.
  validity / confidence: valid, rule-based
  affected branches: ALL
  candidate-space update: no frozen conclusion can be invalidated by later service behavior

