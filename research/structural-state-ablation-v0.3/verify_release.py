"""Audit preserved artifacts without mutating them or invoking a model."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest = json.loads((ROOT / 'SOURCE_SHA256.json').read_text())['files']
    for name, expected in manifest.items():
        require(digest(ROOT / name) == expected, 'Source hash mismatch: ' + name)
    before = {name: digest(ROOT / name) for name in manifest}
    with tempfile.TemporaryDirectory(prefix='ablation-v03-') as folder:
        scratch = Path(folder) / 'v03'
        shutil.copytree(ROOT / 'v03', scratch)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        for script in ('verify.py', 'score.py'):
            run = subprocess.run([sys.executable, str(scratch / script)], capture_output=True, text=True, env=env)
            require(run.returncode == 0, script + ': ' + run.stdout + run.stderr)
            print(script + ': PASS')
        for gate in scratch.glob('manifest_g*.json'):
            require(gate.read_bytes() == (ROOT / 'v03' / gate.name).read_bytes(), 'Gate changed: ' + gate.name)
        expected_results = json.loads((ROOT / 'v03/results.json').read_text())
        require(json.loads((scratch / 'results.json').read_text()) == expected_results, 'Recomputed metrics differ')
        spec = importlib.util.spec_from_file_location('archived_oracle', scratch / 'oracle.py')
        oracle = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(oracle)
        runs = json.loads((scratch / 'runs.json').read_text())
        for actor in runs['order']:
            rows = [json.loads(line) for line in (scratch / (actor + '.jsonl')).read_text().splitlines()]
            submits = [row for row in rows if row['op'] == 'submit']
            require(len(submits) == 1 and rows[-1]['op'] == 'submit', actor + ': submission shape')
            reveal = oracle.REVEALS[runs[actor]]
            row = submits[0]
            correct = bool(oracle.compatible(row['candidate'], reveal['profile']) and reveal['predicate'](row['candidate']))
            require(row['result'] == {'correct': correct, 'reveal': runs[actor]}, actor + ': submit mismatch')
        actor = runs['order'][0]
        require(runs[actor] == 'V2', 'Direct-submit check expects V2')
        (scratch / (actor + '.jsonl')).unlink()
        direct = subprocess.run([sys.executable, str(scratch / 'oracle.py'), actor, 'submit', 'C2'], capture_output=True, text=True, env=env)
        require(direct.returncode == 0 and json.loads(direct.stdout)['result']['correct'], 'Direct C2 submit check failed')
        print('One-action direct C2 submit under V2: accepted (see REVIEW.md)')
    require(before == {name: digest(ROOT / name) for name in manifest}, 'Source files changed')
    print('PASS: archived gates, replay, submissions, metrics, and source preservation')

if __name__ == '__main__':
    main()
