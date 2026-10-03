import json,pathlib,hashlib,sys
sys.dont_write_bytecode=True
import oracle
R=pathlib.Path(__file__).resolve().parent
gt={}
for rid,rev in oracle.REVEALS.items():
 hits=[c for c in oracle.ALL if oracle.compatible(c,rev['profile']) and rev['predicate'](c)]
 assert len(hits)==1,(rid,hits)
 gt[rid]={'answer':hits[0],'profile':rev['profile'],'constraint_text':rev['constraint_text']}
(R/'ground_truth.json').write_text(json.dumps(gt,indent=2)+'\n')
print(json.dumps(gt))
man={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['oracle.py','task.md','ground_truth.json']}
(R/'manifest_g1.json').write_text(json.dumps(man,indent=2)+'\n')
print('GATE1 FROZEN')
