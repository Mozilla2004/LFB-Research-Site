Find the deliverable configuration among candidates A1 through F4 (six families A-F, four variants 1-4) in a fixed opaque compatibility service. Hidden service policies cannot be inferred from candidate names.

Querying a candidate (a probe) returns one of:
1. An authoritative rejection certificate naming every excluded candidate in its stated scope. Scopes can cover a whole family, a whole variant column across all families, a pair of candidates, or a single candidate. A certificate rules out every candidate in its stated scope, not merely the candidate probed.
2. A conditional availability rule. A probe restates the rule and does NOT resolve it: whether the candidate is compatible must be established from the rule's stated terms, the other service evidence, and the deployment requirement. Submitting is the only external check of a conditional candidate.

The service policy is fixed throughout exploration and continuation; certificates are authoritative within their stated scope. The service may be compatible with several candidates at once.

The final deliverable is the unique candidate that is BOTH service-compatible AND satisfies the deployment requirement. The deployment requirement consists of a deployment profile (batch or extended) and a family/variant constraint. It is revealed only at continuation time; it is not part of prior exploration, and prior exploration did not know it.

Exactly one candidate satisfies both conditions under the revealed requirement. Do not assume that an untested candidate is compatible merely because no known certificate excludes it.
