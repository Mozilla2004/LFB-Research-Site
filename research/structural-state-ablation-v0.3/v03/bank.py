import json,pathlib,hashlib,sys
sys.dont_write_bytecode=True
import oracle
R=pathlib.Path(__file__).resolve().parent
rows=[json.loads(s) for s in (R/'explorer.jsonl').read_text().splitlines()]
assert len(rows)==9 and all(r['op']=='probe' for r in rows)
excluded=set()
for r in rows:
 z=r['result']
 assert oracle.service(r['candidate'])==z
 if z['accepted'] is False:excluded.update(z['excluded'])
plausible=[c for c in oracle.ALL if c not in excluded]
assert plausible==['B2','C2','E2','E3'],plausible
records=[{'id':'E%02d'%(i+1),'step':r['step'],'op':'probe','candidate':r['candidate'],'result':r['result']} for i,r in enumerate(rows)]
bank={'description':'Frozen Stage-1 source evidence. One deterministic scripted explorer, nine probes, run once. No LLM exploration, no retries, no Stage-2 information. Probe order fixed in advance: A2,F1,B1,E4,B3,C3,D2,C2,E2.','records':records,'excluded_union':sorted(excluded),'plausible':plausible}
(R/'bank.json').write_text(json.dumps(bank,indent=2)+'\n')
man={'oracle.py':None,'task.md':None,'ground_truth.json':None}
g1=json.loads((R/'manifest_g1.json').read_text())
for n in man:man[n]=g1[n]
for n in ['explorer.jsonl','bank.json']:man[n]=hashlib.sha256((R/n).read_bytes()).hexdigest()
(R/'manifest_g2.json').write_text(json.dumps(man,indent=2)+'\n')
print('excluded:',len(excluded),'plausible:',plausible,'GATE2 FROZEN')
