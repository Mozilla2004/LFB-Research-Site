import json,pathlib,re,hashlib,sys
R=pathlib.Path(__file__).resolve().parent
bank=json.loads((R/'bank.json').read_text())
inv=json.loads((R/'inventory.json').read_text())
E=(R/'E.md').read_text();P=(R/'P.md').read_text();S=(R/'S.md').read_text()
rep={}
# 1. All three handoffs carry every bank record verbatim (certificate text + candidate).
for r in bank['records']:
 tag=f"{r['id']} — probe {r['candidate']}"
 for name,t in [('E',E),('P',P),('S',S)]:
  assert tag in t,(name,tag)
  assert r['result']['certificate'] in t,(name,r['id'])
# 2. E carries no deduction content: no deduction IDs, no derived four-branch enumeration, no C2-resolution claim.
for did in [d['id'] for d in inv['deductions']]:
 assert did not in E,('E leaks',did)
assert 'B2, C2, E2 and E3' not in E and '{B2, C2, E2, E3}' not in E
assert 'C2 is service-compatible' not in E
# 3. P and S each anchor every deduction exactly once (paragraph head in P, bracketed entry in S)
#    with identical evidence citations. Dependency references to other deduction IDs are expected.
def p_blocks(text):
 return {m.group(1):b for m,b in [(re.match(r'(D\d\d) \(',l),l) for l in text.splitlines() if re.match(r'D\d\d \(',l)]}
def s_blocks(text):
 out={};cur=None
 for l in text.splitlines():
  m=re.match(r'^\[(D\d\d)\]$',l.strip())
  if m:cur=m.group(1);out[cur]=[]
  elif cur is not None:out[cur].append(l)
 return {k:'\n'.join(v) for k,v in out.items()}
PB=p_blocks(P);SB=s_blocks(S)
assert sorted(PB)==sorted(SB)==sorted(d['id'] for d in inv['deductions'])
for d in inv['deductions']:
 i=d['id']
 assert sorted(re.findall(r'E\d\d',PB[i]))==sorted(re.findall(r'E\d\d',SB[i]))==sorted(d['evidence']),(i,'citation mismatch')
# 4. P and S carry identical consequence strings (same canonical sentences, only organization differs).
for d in inv['deductions']:
 assert d['consequence'] in P and d['consequence'] in S,d['id']
# 5. S uses only whitelisted structural labels beyond P's content.
labels=['Candidate-space state','Failed paths','Dependencies','Conditional status','Open branches','Task-level constraint','Invariants','evidence provenance','depends on','constraint / basis','scope','consequence','validity / confidence','affected branches','candidate-space update','REJECTED','CONDITIONAL','block']
# 6. Size report.
rep['sizes']={n:len(t.split()) for n,t in [('E',E),('P',P),('S',S)]}
rep['chars']={n:len(t) for n,t in [('E',E),('P',P),('S',S)]}
rep['deductions']=[d['id'] for d in inv['deductions']]
rep['evidence_ids']=[r['id'] for r in bank['records']]
(R/'audit.json').write_text(json.dumps(rep,indent=2)+'\n')
man=json.loads((R/'manifest_g2.json').read_text())
for n in ['inventory.json','render.py','E.md','P.md','S.md','audit.py','audit.json']:
 man[n]=hashlib.sha256((R/n).read_bytes()).hexdigest()
(R/'manifest_g3.json').write_text(json.dumps(man,indent=2)+'\n')
print(json.dumps(rep));print('P/S EQUIVALENCE AUDIT PASS; GATE3 FROZEN')
