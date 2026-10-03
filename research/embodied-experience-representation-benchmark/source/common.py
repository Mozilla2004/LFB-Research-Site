import csv, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REPS = ('raw', 'summary', 'state_change')
def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path, data):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def csv_write(path, rows, fields):
    with Path(path).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
def jsonl(path):
    return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]
