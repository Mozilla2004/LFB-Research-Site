import argparse, random, statistics
from pathlib import Path
from common import REPS, read, write, csv_write

def ratio(rows,key): return sum(bool(r[key]) for r in rows)/len(rows) if rows else None
def terminal_rows(rows):
    groups={}
    for r in rows: groups.setdefault(r['run_id'],[]).append(r)
    result=[]
    for attempts in groups.values():
        attempts=sorted(attempts,key=lambda r:r.get('attempt') or 0)
        complete=[r for r in attempts if r.get('api_complete',r.get('api_status')=='success')]
        if len(complete)>1: raise ValueError('Non-API retry or multiple completed responses; selection prohibited')
        selected=dict(complete[0] if complete else attempts[-1])
        selected['attempted']=any(r.get('attempted',True) for r in attempts)
        selected['attempts_n']=sum(r.get('attempted',True) for r in attempts)
        result.append(selected)
    return result

def metrics(rows):
    rows=terminal_rows(rows)
    eligible=[r for r in rows if r['case_valid']]
    served=[r for r in eligible if r.get('scientifically_scoreable') is True]
    primary=[r for r in served if r['transfer_level'] in ('medium','far')]
    near=[r for r in served if r['transfer_level']=='near']; boundary=[r for r in served if r['transfer_level']=='boundary']
    planned_primary=[r for r in eligible if r['transfer_level'] in ('medium','far')]
    planned_boundary=[r for r in eligible if r['transfer_level']=='boundary']
    planned=len(rows)
    api=sum(r.get('api_complete',False) is True for r in rows)
    provider=sum(r.get('provider_complete',False) is True for r in rows)
    parsed=sum(r.get('response_valid',False) is True and r.get('parse_status')=='valid' and r.get('api_complete',False) is True for r in rows)
    def avg(key):
        values=[r[key] for r in rows if r.get(key) is not None]
        return statistics.mean(values) if values else None
    return {'planned_n':planned,'attempted_n':sum(r['attempted'] for r in rows),
        'attempts_n':sum(r['attempts_n'] for r in rows),'api_complete_n':api,'provider_complete_n':provider,
        'parse_valid_n':parsed,'scientifically_scoreable_n':len(served),
        'scientifically_correct_n':sum(r['action_correct'] is True for r in served),
        'execution_coverage':api/planned if planned else None,'response_coverage':parsed/planned if planned else None,
        'scientific_accuracy':ratio(served,'action_correct'),
        'conditions':planned,'case_invalid':planned-len(eligible),
        'api_failed':sum(r.get('failure_type')=='api_failure' for r in rows),
        'provider_completion_failed':sum(r.get('failure_type')=='provider_completion_failure' for r in rows),
        'malformed':sum(r.get('failure_type')=='parse_format_failure' for r in rows),
        'primary_planned_n':len(planned_primary),'primary_n':len(primary),'primary_correct':sum(r['action_correct'] is True for r in primary),
        'transfer_action_accuracy':ratio(primary,'action_correct'),
        'primary_coverage':len(primary)/len(planned_primary) if planned_primary else None,
        'near_transfer_accuracy':ratio(near,'action_correct'),'failure_diagnosis_accuracy':ratio(served,'diagnosis_correct'),
        'boundary_refusal_accuracy':ratio(boundary,'boundary_refusal_correct'),'transfer_judgment_accuracy':ratio(served,'judgment_correct'),
        'false_transfer_rate':ratio(boundary,'false_transfer'),'boundary_n':len(boundary),
        'boundary_response_coverage':len(boundary)/len(planned_boundary) if planned_boundary else None,
        'diagnostic_U':ratio(primary,'action_correct')-0.5*ratio(boundary,'false_transfer') if primary and boundary else None,
        'input_tokens_mean':avg('input_tokens'),'output_tokens_mean':avg('output_tokens'),'latency_seconds_mean':avg('latency_seconds')}

def paired_ci(rows,left,right):
    # Family is the resampling unit; repeats are averaged inside each family.
    groups={}
    for r in terminal_rows(rows):
        if r.get('scientifically_scoreable') is True and r['transfer_level'] in ('medium','far'):
            key=(r['family_id'],r['case_id'],r['repeat']); groups.setdefault(key,{})[r['representation']]=int(r['action_correct'])
    by_family={}
    for key,g in groups.items():
        if left in g and right in g: by_family.setdefault(key[0],[]).append(g[left]-g[right])
    means=[statistics.mean(v) for v in by_family.values()]
    if not means: return {'families':0,'difference':None,'ci95':None}
    rng=random.Random(20261002); samples=sorted(statistics.mean(rng.choices(means,k=len(means))) for _ in range(5000))
    return {'families':len(means),'difference':statistics.mean(means),'ci95':[samples[124],samples[4874]],'paired_conditions':sum(map(len,by_family.values()))}

def aggregate(out):
    scored=read(out/'scored/scores.json'); mapping={r['run_id']:r for r in read(out/'BLIND_MAPPING.json')}
    rows=[dict(r,**{k:mapping[r['run_id']][k] for k in ('representation','repeat','track','control')}) for r in scored]
    present={r['run_id'] for r in rows}
    from common import ROOT
    import csv
    with (ROOT/'INVALID_CASES.csv').open() as f: invalid={r['case_id'] for r in csv.DictReader(f)}
    invalid.update(read(ROOT/'reports/semantic_match_report.json')['excluded_cases'])
    for rid,m in mapping.items():
        if rid in present: continue
        case=read(ROOT/f'data/canonical/{m["case_id"]}.json')
        rows.append(dict(m,family_id=case['family_id'],transfer_level=case['transfer_level'],case_valid=m['case_id'] not in invalid,
                         attempted=False,api_complete=False,provider_complete=False,response_valid=False,scientifically_scoreable=False,
                         api_status='not_attempted',parse_status='not_attempted',action_correct=None))
    reps=sorted({r['representation'] for r in rows})
    result={'overall':metrics(rows),'evidence_kind':read(out/'RUN_CONFIG.json')['evidence_kind'],'groups':{rep:metrics([r for r in rows if r['representation']==rep]) for rep in reps},
        'per_family':{f:{rep:metrics([r for r in rows if r['representation']==rep and r['family_id']==f]) for rep in reps} for f in sorted({r['family_id'] for r in rows})},
        'paired_primary_differences':{a+'-'+b:paired_ci(rows,a,b) for a,b in [('state_change','summary'),('state_change','raw'),('summary','raw')]}}
    write(out/'tables/aggregate.json',result)
    csv_write(out/'tables/metrics.csv',[dict(representation=k,**v) for k,v in result['groups'].items()],['representation']+list(next(iter(result['groups'].values())).keys()))
    return result
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('run_directory'); aggregate(Path(ap.parse_args().run_directory))
