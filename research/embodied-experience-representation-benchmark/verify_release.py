"""Offline public-score verification. No network, provider records or API calls."""
import collections
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'source'))
from aggregate import metrics, paired_ci
from action_space import evaluate

def read(path): return json.loads(path.read_text())
def lines(path): return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]
def require(ok,message):
    if not ok: raise RuntimeError(message)

def main():
    manifest=read(ROOT/'SOURCE_SHA256.json')
    for name,digest in manifest['files'].items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,'Public file hash differs: '+name)
    cases={x['case_id']:x for x in read(ROOT/'data/cases.json')}
    oracle={x['case_id']:x for x in read(ROOT/'data/oracle.json')}
    answers=lines(ROOT/'data/answers.jsonl')
    keys={(x['case_id'],x['representation'],x['repeat']) for x in answers}
    require(len(answers)==len(keys)==900,'Duplicate or missing answer slots')
    require(keys=={(cid,rep,n) for cid in cases for rep in ['raw','summary','state_change'] for n in range(3)},'Plan coverage differs')
    rows=[]
    for i,x in enumerate(answers):
        c=cases[x['case_id']];o=oracle[x['case_id']];a=x['answers'];valid=x['case_id']!='F11_T5' and o['valid']
        rows.append(dict(x,run_id=str(i),family_id=c['family_id'],transfer_level=c['transfer_level'],case_valid=valid,scientifically_scoreable=valid,
            attempted=True,attempt=1,api_complete=True,provider_complete=True,response_valid=True,parse_status='valid',
            action_correct=a['Q2']==o['correct_next_action'] if valid else None,
            diagnosis_correct=a['Q1']==o['correct_failure_variable'] if valid else None,
            judgment_correct=a['Q3']==o['transfer_label'] if valid else None,
            boundary_refusal_correct=a['Q3']=='NO' if valid and c['transfer_level']=='boundary' else None,
            false_transfer=a['Q3'] in ['YES','PARTIAL'] if valid and c['transfer_level']=='boundary' else None))
    # Execution flags above describe the extracted admitted-answer set, not an independent transport audit.
    require(sum(x['case_valid'] for x in rows)==891,'Invalid-case denominator differs')
    for rep in ['raw','summary','state_change']:
        group=[x for x in rows if x['representation']==rep];m=metrics(group)
        require(m['primary_correct']==m['primary_n']==120,'Primary result differs')
        near=[x for x in group if x['transfer_level']=='near' and x['case_valid']]
        judgment=[x for x in group if x['case_valid']]
        print(rep,'primary',m['primary_correct'],'/',m['primary_n'],'near',sum(x['action_correct'] for x in near),'/',len(near),'Q3',sum(x['judgment_correct'] for x in judgment),'/',len(judgment))
        confusion=collections.Counter((oracle[x['case_id']]['transfer_label'],x['answers']['Q3']) for x in group if x['case_valid'])
        print(' Q3:',dict(confusion))
    for left,right in [('state_change','summary'),('state_change','raw'),('summary','raw')]:
        print(left+'-'+right,paired_ci(rows,left,right))
    sem={}
    for x in lines(ROOT/'data/action_semantics.jsonl'):sem.setdefault(x['case_id'],{})[x['candidate_id']]=x['action_semantics']
    correct=0
    for cid,c in cases.items():
        if c['transfer_level'] in ['medium','far']:
            compatible=[k for k,a in sem[cid].items() if evaluate(a,c['action_constraints'])['compatible']]
            correct+=compatible==[oracle[cid]['correct_next_action']]
    first=sum(c['diagnosis_options'][0]==oracle[cid]['correct_failure_variable'] for cid,c in cases.items())
    print('Diagnostic structured-current-only solver:',correct,'/40; not an LLM baseline')
    print('Diagnostic Q1 first-choice oracle matches:',first,'/100')
    require(correct==40 and first==89,'Review diagnostic differs')
    print('PASS: public-score extract and review diagnostics verified offline')

if __name__=='__main__':main()
