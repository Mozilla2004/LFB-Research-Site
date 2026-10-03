"""Typed action commitments and explicit synthetic constraint predicates.
No dynamics, robot simulator, learned judge, or physics inference is used.
"""
import copy, json, math, random
from common import ROOT, read

def design(): return read(ROOT/'repairs/action_space/action_candidate_recipes.json')
def specification(case):
    return copy.deepcopy(design()[case['family_id']]['boundary' if case['transfer_level']=='boundary' else 'positive'])
def render_action(action, spec):
    for option in spec['options']:
        if (action['kind'], action['parameters'], action['steps']) == (option['kind'],option['parameters'],option['steps']):
            base=option['text']; break
    else:
        base=f"Commit {action['kind']} with {json.dumps(action['parameters'], sort_keys=True)} and ordered steps {json.dumps(action['steps'])}."
    if action.get('extra_steps'): base+=' Additional steps: '+', '.join(action['extra_steps'])+'.'
    return base

def repair_case(case):
    c=copy.deepcopy(case); spec=specification(c)
    public={k:spec[k] for k in ('facts','effect_fields','rules','model','world')}
    # Versioned field is a shared current-case fact, never representation-specific.
    c['action_constraints']=public
    inherited=c['task_constraints'].split('\nExplicit action-space facts:')[0]
    c['task_constraints']=inherited+'\nExplicit action-space facts: '+public['facts']
    options=copy.deepcopy(spec['options']); random.Random(5100+int(c['family_id'][1:])*10+int(c['case_id'].split('_T')[1])).shuffle(options)
    semantics={}
    for letter,option in zip('ABCD',options):
        action={k:copy.deepcopy(option[k]) for k in ('kind','parameters','steps')}
        action.update(primary_variable=c['diagnosis_options'][0], direction='command_specified_values', extra_steps=[],
                      requires_new_observation=option['kind']=='query_then_place',
                      applies_prior_experience=option==spec['options'][1], resolves_uncertainty=option['kind']=='query_then_place')
        if option['kind']=='cradle': action['primary_variable']='support_mode'
        elif option['kind'] in ('sequence','remove_insert','release_latch'): action['primary_variable']='subgoal_order'
        elif c['transfer_level']=='boundary':
            action['primary_variable']={'F01':'contact_point','F02':'support_mode','F05':'approach_route','F08':'route','F09':'route','F16':'contact_point','F17':'contact_point'}.get(c['family_id'],action['primary_variable'])
        if c['family_id']=='F06':
            action['requires_new_observation']=True
            action['resolves_uncertainty']=all(test_rule(action,r)[0] for r in spec['rules'])
        semantics[letter]=action
    c['action_options']={letter:render_action(a,spec) for letter,a in semantics.items()}
    return c,semantics

def lookup(action,path):
    if path=='derived.start_difference':
        times=action['parameters']['start_times']; return times[1]-times[0]
    value=action
    for key in path.split('.'): value=value[key]
    return value

def test_rule(action,rule):
    try: value=lookup(action,rule['path'])
    except (KeyError,TypeError,IndexError): return False, 'missing '+rule['path']
    expected=rule['value']; op=rule['op']
    if op=='eq': ok=normalize(value,rule['path'])==normalize(expected,rule['path'])
    elif op=='range':
        value=normalize(value,rule['path'])
        ok=isinstance(value,(int,float)) and expected[0]<=value<=expected[1]
    else: raise ValueError('Unknown constraint operator '+op)
    return ok,rule['path']+' '+op+' '+str(expected)

def normalize(value,field=''):
    if isinstance(value,dict): return {k:normalize(v,k) for k,v in sorted(value.items())}
    if isinstance(value,list):
        items=[normalize(v,field) for v in value]
        return sorted(items) if field.endswith('contacts') else items
    if isinstance(value,(int,float)) and not isinstance(value,bool):
        value=float(value)
        if 'angle' in field or 'pose_degrees' in field:
            value=((value+180)%360)-180
        return round(value,8)
    return value

def sequence_result(action,constraints):
    model=constraints['model']; state=copy.deepcopy(constraints['world']); trace=[]; failed=None
    kind=action['kind']; steps=action['steps']
    if kind!='sequence': return False,['requires an ordered operation sequence'],{'trace':[]}
    inserted=False; complete=False
    for step in steps:
        before=copy.deepcopy(state)
        if model=='container_sequence':
            if step=='equalize': state['pressure_equalized']=True
            elif step=='open':
                if not state['pressure_equalized']: failed='opening before pressure equalization'
                else: state['lid_open']=True
            elif step=='close': state['lid_open']=False
            elif step=='insert':
                if not state['lid_open']: failed='insertion against closed lid'
                else: inserted=True
            elif step=='remove': inserted=False
            else: failed='undeclared operation '+step
            state['inserted']=inserted; complete=inserted
        elif model=='two_support_sequence':
            if step=='release_lock': state['locked']=False
            elif step=='synchronized_lift':
                if state['locked']: failed='synchronized lift while locked'
                else: complete=True; state['support']='both'
            elif step=='left_lift': state['support']='left_only'; complete=False
            elif step=='right_lift':
                if state['locked']: failed='right lift while locked'
                else: state['support']='right_only'; complete=False
            else: failed='undeclared operation '+step
        trace.append({'operation':step,'state_before':before,'state_after':copy.deepcopy(state),'violation':failed})
        if failed: break
    return complete and not failed, [failed] if failed else ([] if complete else ['goal remains incomplete']), {'trace':trace,'final_state':state}

def evaluate(action,constraints):
    # Compatibility is derived from explicit public constraints, not from the oracle ID or a candidate label.
    model=constraints['model']; reasons=[]; compatible=False
    if model=='predicates':
        results=[test_rule(action,r) for r in constraints['rules']]
        kind_rule=any(r['path']=='kind' for r in constraints['rules'])
        compatible=all(ok for ok,_ in results) and (kind_rule or action['kind']=='set')
        reasons=[reason for ok,reason in results if not ok]
        if not kind_rule and action['kind']!='set': reasons.append('command kind is not set')
        observed={'parameters':normalize(action['parameters'])}
    elif model=='support_force':
        force=action['parameters'].get('force_units'); world=constraints['world']
        if isinstance(force,(int,float)):
            if action['kind']=='set': compatible=world['direct_min']<=force<=world['shell_max']
            elif action['kind']=='cradle': compatible=0<=force<=world['cradle_max']
        reasons=[] if compatible else ['direct retention and shell limit cannot both be satisfied, or cradle contact exceeds its limit']
        observed={'mode':action['kind'],'contact_force':force}
    elif model in ('container_sequence','two_support_sequence'):
        compatible,reasons,observed=sequence_result(action,constraints)
    elif model=='preference':
        w=constraints['world']
        compatible=(action['kind']=='place' and action['parameters'].get('location')==w['current_preference']) if w['preference_known'] else action['kind']=='query_then_place'
        reasons=[] if compatible else ['does not satisfy current-user preference resolution and placement requirements']
        observed={'decision':action['kind'],'location':action['parameters'].get('location'),'current_preference_resolved':action['kind']=='query_then_place' or w['preference_known']}
    else: raise ValueError('Undeclared constraint model '+model)
    # Extra actions have no assumed cost. An unconstrained observation cannot turn an otherwise valid plan wrong.
    return {'compatible':compatible,'violations':reasons,'observed_behavior':observed}

def behavior_key(action,constraints):
    if constraints['model'] in ('container_sequence','two_support_sequence'):
        # An unexecuted suffix after the first violation cannot create behavioral distinctness.
        return normalize(evaluate(action,constraints)['observed_behavior'])
    params={k:normalize(action['parameters'].get(k),k) for k in constraints['effect_fields'] if k in action['parameters']}
    if 'start_times' in params:
        params['start_times']=round(params['start_times'][1]-params['start_times'][0],8)
    return {'kind':action['kind'],'task_parameters':params}

def assumption_issues(action,constraints):
    issues=[]; known_kinds={'set','cradle','sequence','place','refuse','query_then_place','remove_insert','release_latch'}
    if action['kind'] not in known_kinds: issues.append('unknown command kind')
    if set(action['parameters'])-set(constraints['effect_fields']): issues.append('parameter without an explicit task-relevant constraint')
    if not all(k in action['parameters'] for k in constraints['effect_fields']) and action['kind'] not in ('refuse','query_then_place','remove_insert','release_latch'):
        issues.append('missing declared task parameter')
    models={'container_sequence':{'equalize','open','close','insert','remove'},'two_support_sequence':{'release_lock','synchronized_lift','left_lift','right_lift'}}
    if action['steps'] and constraints['model'] not in models: issues.append('steps without an explicit operation model')
    if constraints['model'] in models and set(action['steps'])-models[constraints['model']]: issues.append('unmodeled step consequence')
    if action.get('extra_steps'):
        issues.append('extra step has no declared cost, violation, or goal consequence')
    return issues


def schema_issues(action):
    required={'kind','parameters','steps','primary_variable','direction','extra_steps','requires_new_observation','applies_prior_experience','resolves_uncertainty'}
    if set(action)!=required: return ['semantic schema fields missing or extra']
    problems=[]
    for k in ('kind','primary_variable','direction'):
        if not isinstance(action[k],str) or not action[k]: problems.append(k+' is not nonempty text')
    if not isinstance(action['parameters'],dict): problems.append('parameters is not an object')
    for k in ('steps','extra_steps'):
        if not isinstance(action[k],list) or not all(isinstance(x,str) for x in action[k]): problems.append(k+' is not a text list')
    for k in ('requires_new_observation','applies_prior_experience','resolves_uncertainty'):
        if not isinstance(action[k],bool): problems.append(k+' is not boolean')
    return problems
