# Handoff E — Flat Evidence

This handoff contains the complete frozen record of what was observed during Stage-1 source exploration of the compatibility service: every probe that was made and the service's original answer to it, in exploration order. The evidence below is the relevant known state of the environment. No derived conclusions are included in this handoff; anything not stated below has not been observed.

## Observations (what was observed)

E01 — probe A2: REJECTED. Certificate: "family A retired". Stated exclusion scope: A1, A2, A3, A4.
E02 — probe F1: REJECTED. Certificate: "family F retired". Stated exclusion scope: F1, F2, F3, F4.
E03 — probe B1: REJECTED. Certificate: "variant 1 discontinued everywhere". Stated exclusion scope: A1, B1, C1, D1, E1, F1.
E04 — probe E4: REJECTED. Certificate: "variant 4 discontinued everywhere". Stated exclusion scope: A4, B4, C4, D4, E4, F4.
E05 — probe B3: REJECTED. Certificate: "family B unavailable at variants 3 and above". Stated exclusion scope: B3, B4.
E06 — probe C3: REJECTED. Certificate: "variant 3 unavailable in families C and D". Stated exclusion scope: C3, D3.
E07 — probe D2: REJECTED. Certificate: "family D unavailable". Stated exclusion scope: D1, D2, D3, D4.
E08 — probe C2: CONDITIONAL (not rejected, not accepted). Certificate: "C2 availability rule: unavailable while any family-D variant-2 unit is deployable; a probe restates this rule and does not resolve it". Stated exclusion scope: none.
E09 — probe E2: CONDITIONAL (not rejected, not accepted). Certificate: "E2 availability rule: available for batch deployment profiles, unavailable for extended profiles; a probe restates this rule and does not resolve it". Stated exclusion scope: none.
