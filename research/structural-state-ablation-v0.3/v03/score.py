"""Recompute v0.3 behavioral metrics from frozen bank/inventory and receiver oracle logs."""
import json,pathlib,re,sys
sys.dont_write_bytecode=True
import oracle
R=pathlib.Path(__file__).resolve().parent
bank=json.loads((R/'bank.json').read_text())
inv=json.loads((R/'inventory.json').read_text())
runs=json.loads((R/'runs.json').read_text())
tel={}
for line in (R/'finals'/'telemetry.txt').read_text().splitlines():
 m=re.match(r'(\w+) tokens=(\d+) tool_uses=(\d+) duration_ms=(\d+)',line)
 if m:tel[m.group(1)]={'subagent_tokens':int(m.group(2)),'tool_uses':int(m.group(3)),'duration_ms':int(m.group(4))}
plausible0=set(bank['plausible'])            # {B2,C2,E2,E3}
evidence_excluded=set(bank['excluded_union'])# 20 candidates
direct_probed={r['candidate'] for r in bank['records']}          # evidence re-query targets
inv_ded={d['id']:d for d in inv['deductions']}
ded_covered=set()                              # candidates whose status is stated in the inventory
for d in inv_ded.values():
 if d['id'] in ('D01','D02','D03','D04','D05','D06','D07'):ded_covered.update(d['affects'])
 if d['id']=='D09':ded_covered.add('C2')
rev=oracle.REVEALS[runs['e1']]
out={}
for actor in runs['order']:
 rows=[json.loads(s) for s in (R/(actor+'.jsonl')).read_text().splitlines()]
 cond=actor[0].upper()
 possible=set(plausible0);details=[];requery=recompute=dead=revealbad=informative=0
 for row in rows:
  c=row['candidate'];before=len(possible);z=row['result']
  if row['op']=='probe':
   assert z==oracle.service(c)
   flags=[]
   if c in direct_probed:requery+=1;flags.append('evidence_requery')
   if cond in ('P','S') and c in ded_covered:
    if c not in direct_probed or c=='C2':recompute+=1;flags.append('deduction_recompute')
   if c in evidence_excluded:dead+=1;flags.append('inherited_dead')
   if not rev['predicate'](c):revealbad+=1;flags.append('reveal_inconsistent')
   if not flags:informative+=1;flags.append('informative')
   if z['accepted'] is False:possible.difference_update(z['excluded'])
   details.append({'op':'probe','candidate':c,'flags':flags,'new_eliminations':before-len(possible),'remaining':len(possible)})
  else:
   if z['correct']:possible.intersection_update({c})
   details.append({'op':'submit','candidate':c,'correct':z['correct'],'new_eliminations':before-len(possible),'remaining':len(possible)})
 probes=sum(d['op']=='probe' for d in details);actions=len(details)
 sub=rows[-1]['op']=='submit'
 out[actor]={'condition':cond,'correct':sub and rows[-1]['result']['correct'],'probes':probes,'actions':actions,
  'evidence_requeries':requery,'deduction_recomputations':recompute if cond in ('P','S') else None,
  'inherited_dead_probes':dead,'reveal_inconsistent_probes':revealbad,'informative_probes':informative,
  'redundant_probes':requery+(recompute if cond in ('P','S') else 0),
  'candidate_reduction':len(plausible0)-len(possible),'progress_per_action':(len(plausible0)-len(possible))/actions,
  'sequence':[d['candidate'] for d in details],'details':details,
  'telemetry':tel.get(actor),'final':(R/'finals'/(actor+'.md')).read_text().strip()}
(R/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({a:{k:v for k,v in d.items() if k not in('details','final')} for a,d in out.items()},indent=1))
