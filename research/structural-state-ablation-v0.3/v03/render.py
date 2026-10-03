import json,pathlib
R=pathlib.Path(__file__).resolve().parent
bank=json.loads((R/'bank.json').read_text())
inv=json.loads((R/'inventory.json').read_text())
D={d['id']:d for d in inv['deductions']}
def evidence_block():
 lines=[]
 for r in bank['records']:
  z=r['result']
  if z['accepted'] is False:
   lines.append(f"{r['id']} — probe {r['candidate']}: REJECTED. Certificate: \"{z['certificate']}\". Stated exclusion scope: {', '.join(z['excluded'])}.")
  else:
   lines.append(f"{r['id']} — probe {r['candidate']}: CONDITIONAL (not rejected, not accepted). Certificate: \"{z['certificate']}\". Stated exclusion scope: none.")
 return '\n'.join(lines)
def cite(ev,dep):
 parts=[]
 if ev:parts.append('from '+' and '.join(ev))
 if dep:parts.append('building on '+' and '.join(dep))
 return '; '.join(parts)
# ---- E: flat evidence only ----
E=f"""# Handoff E — Flat Evidence

This handoff contains the complete frozen record of what was observed during Stage-1 source exploration of the compatibility service: every probe that was made and the service's original answer to it, in exploration order. The evidence below is the relevant known state of the environment. No derived conclusions are included in this handoff; anything not stated below has not been observed.

## Observations (what was observed)

{evidence_block()}
"""
# ---- P: evidence + complete deduction inventory as prose ----
paras=[]
for d in inv['deductions']:
 c=cite(d['evidence'],d['depends_on'])
 head=f"{d['id']} ({c})." if c else f"{d['id']} (from the shared task rules)."
 paras.append(f"{head} {d['consequence']} Basis: {d['basis']}. Scope: {d['scope']}. Status: {d['status']}. Effect on the candidate space: {d['candidate_space_note']}.")
P=f"""# Handoff P — Compiled Prose

This handoff contains two parts: first, the complete frozen record of what was observed during Stage-1 source exploration of the compatibility service; second, the complete audited inventory of everything that has already been inferred from that evidence and the shared task rules. Nothing here was obtained by querying the environment during compilation. Every deduction below is traceable to the cited observations or to the task rules.

## Part 1 — Observations (what was observed)

{evidence_block()}

## Part 2 — Compiled deductions (what has already been inferred)

{chr(10).join(paras)}
"""
# ---- S: same evidence + same deductions as explicit structural state ----
sections=[
 ('Candidate-space state',['D08']),
 ('Failed paths (certain exclusions)',['D01','D02','D03','D04','D05','D06','D07']),
 ('Dependencies (conditional rule, resolved)',['D09']),
 ('Conditional status (partial success, unresolved)',['D10']),
 ('Open branches (no information)',['D11']),
 ('Task-level constraint on continuation',['D12']),
 ('Invariants',['D13'])]
body=[]
for title,ids in sections:
 entries=[]
 for i in ids:
  d=D[i]
  entries.append('\n'.join([
   f"[{i}]",
   f"  evidence provenance: {', '.join(d['evidence']) if d['evidence'] else 'task rules'}",
   f"  depends on: {', '.join(d['depends_on']) if d['depends_on'] else 'none'}",
   f"  constraint / basis: {d['basis']}",
   f"  scope: {d['scope']}",
   f"  consequence: {d['consequence']}",
   f"  validity / confidence: {d['status']}",
   f"  affected branches: {', '.join(d['affects'])}",
   f"  candidate-space update: {d['candidate_space_note']}"]))
 body.append(title+':\n'+'\n'.join(entries))
S=f"""# Handoff S — Structural State

This structural state contains two blocks: the complete frozen record of what was observed during Stage-1 source exploration, then the complete audited inventory of everything already inferred, organized by operational relationship (evidence -> constraint -> scope -> consequence -> search-space update). Nothing here was obtained by querying the environment during compilation. Every entry is traceable to the cited observations or to the task rules.

## Block 1 — Evidence (what was observed)

{evidence_block()}

## Block 2 — Structural state (what has already been inferred, and how it organizes the search)

{chr(10).join(chr(10)+b+chr(10) for b in body)}
"""
for n,t in [('E.md',E),('P.md',P),('S.md',S)]:(R/n).write_text(t)
print({n:len(t.split()) for n,t in [('E.md',E),('P.md',P),('S.md',S)]},'words')
print({n:len(t) for n,t in [('E.md',E),('P.md',P),('S.md',S)]},'chars')
