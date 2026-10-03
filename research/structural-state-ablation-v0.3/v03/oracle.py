import json,pathlib,sys
R=pathlib.Path(__file__).resolve().parent
ALL=[f'{f}{v}' for f in 'ABCDEF' for v in '1234']
def column(v):return [x for x in ALL if x[1]==v]
def fam(f):return [x for x in ALL if x[0]==f]
def service(c):
 f,v=c[0],c[1]
 if f in 'AF':return {'accepted':False,'excluded':fam(f),'certificate':'family '+f+' retired'}
 if v=='1':return {'accepted':False,'excluded':column('1'),'certificate':'variant 1 discontinued everywhere'}
 if v=='4':return {'accepted':False,'excluded':column('4'),'certificate':'variant 4 discontinued everywhere'}
 if f=='B' and v=='3':return {'accepted':False,'excluded':['B3','B4'],'certificate':'family B unavailable at variants 3 and above'}
 if f=='C' and v=='3':return {'accepted':False,'excluded':['C3','D3'],'certificate':'variant 3 unavailable in families C and D'}
 if f=='D':return {'accepted':False,'excluded':fam('D'),'certificate':'family D unavailable'}
 if f=='B' and v=='2':return {'accepted':False,'excluded':['B2'],'certificate':'candidate B2 unavailable: incompatible with current hardware revision'}
 if f=='C' and v=='2':return {'accepted':None,'excluded':[],'status':'conditional','certificate':'C2 availability rule: unavailable while any family-D variant-2 unit is deployable; a probe restates this rule and does not resolve it'}
 if f=='E' and v=='2':return {'accepted':None,'excluded':[],'status':'conditional','certificate':'E2 availability rule: available for batch deployment profiles, unavailable for extended profiles; a probe restates this rule and does not resolve it'}
 if f=='E' and v=='3':return {'accepted':None,'excluded':[],'status':'conditional','certificate':'E3 availability rule: available for extended deployment profiles, unavailable for batch profiles; a probe restates this rule and does not resolve it'}
 raise AssertionError(c)
def d2_deployable():return service('D2')['accepted'] is True
def compatible(c,profile):
 z=service(c)
 if z['accepted'] is False:return False
 if c=='C2':return not d2_deployable()
 if c=='E2':return profile=='batch'
 if c=='E3':return profile=='extended'
 return True
REVEALS={
 'V1':{'id':'V1','profile':'extended','constraint_text':'the variant number must be odd','predicate':lambda c:c[1] in '13'},
 'V2':{'id':'V2','profile':'batch','constraint_text':'the family must be one of A, B, C, or D','predicate':lambda c:c[0] in 'ABCD'},
 'V3':{'id':'V3','profile':'batch','constraint_text':'the variant number must be even and the family must be E or F','predicate':lambda c:c[1] in '24' and c[0] in 'EF'},
 'V4':{'id':'V4','profile':'extended','constraint_text':'the variant number must be even and the family must be C or D','predicate':lambda c:c[1] in '24' and c[0] in 'CD'}}
ACTORS=['explorer','e1','e2','p1','p2','s1','s2']
if __name__=='__main__':
 actor,op,c=sys.argv[1:4]
 assert actor in ACTORS and op in ['probe','submit'] and c in ALL
 p=R/(actor+'.jsonl');rows=[json.loads(s) for s in p.read_text().splitlines()] if p.exists() else []
 assert not any(x['op']=='submit' for x in rows)
 cap=12 if actor=='explorer' else 6
 assert op=='submit' or sum(x['op']=='probe' for x in rows)<cap
 if op=='probe':result=service(c)
 else:
  rv=json.loads((R/'runs.json').read_text())[actor];rev=REVEALS[rv]
  result={'correct':bool(compatible(c,rev['profile']) and rev['predicate'](c)),'reveal':rv}
 row={'step':len(rows)+1,'op':op,'candidate':c,'result':result}
 with p.open('a') as f:f.write(json.dumps(row)+'\n')
 print(json.dumps(row))
