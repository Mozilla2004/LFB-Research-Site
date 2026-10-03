import json,pathlib,hashlib,sys
sys.dont_write_bytecode=True
import oracle
R=pathlib.Path(__file__).resolve().parent
# 1. All four freeze-gate manifests still match the files they froze.
for g in ['manifest_g1.json','manifest_g2.json','manifest_g3.json','manifest_g4.json']:
 for name,digest in json.loads((R/g).read_text()).items():
  assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest,(g,name)
# 2. Ground truth still unique per reveal and matches oracle brute force.
gt=json.loads((R/'ground_truth.json').read_text())
for rid,rev in oracle.REVEALS.items():
 hits=[c for c in oracle.ALL if oracle.compatible(c,rev['profile']) and rev['predicate'](c)]
 assert hits==[gt[rid]['answer']],(rid,hits)
# 3. Every recorded probe result replays identically through the fixed service.
for f in ['explorer.jsonl','e1.jsonl','e2.jsonl','p1.jsonl','p2.jsonl','s1.jsonl','s2.jsonl']:
 for line in (R/f).read_text().splitlines():
  row=json.loads(line)
  if row['op']=='probe':assert oracle.service(row['candidate'])==row['result'],(f,row['step'])
# 4. Bank integrity: 9 records, 20 excluded, 4 plausible; evidence IDs stable.
bank=json.loads((R/'bank.json').read_text())
assert len(bank['records'])==9 and len(bank['excluded_union'])==20 and bank['plausible']==['B2','C2','E2','E3']
assert [r['id'] for r in bank['records']]==['E%02d'%i for i in range(1,10)]
# 5. P/S equivalence audit re-runs clean (re-derive, compare to frozen audit.json).
import audit
print('PASS: 4 freeze gates; unique ground truth per reveal; all recorded oracle results replay; bank integrity; P/S audit.')
