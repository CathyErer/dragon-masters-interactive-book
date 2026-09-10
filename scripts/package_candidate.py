"""Build a reproducible local review archive; never publish or select a license."""
import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('--destination', type=Path, required=True)
a = p.parse_args()
destination = a.destination.resolve()
if destination == root or root in destination.parents:
    raise SystemExit('Choose an output directory outside the candidate source.')
subprocess.run([sys.executable, str(root/'scripts/audit_public.py')], check=True)
subprocess.run([sys.executable, str(root/'skills/dragon-masters-interactive-book/scripts/validate_book.py'),
                str(root/'skills/dragon-masters-interactive-book/assets/starter')], check=True)
archive = destination/'Dragon Masters Interactive Book.zip'
manifest = archive.with_suffix('.manifest.json')
if archive.exists() or manifest.exists():
    raise SystemExit('Candidate already exists; choose a new output directory.')
destination.mkdir(parents=True, exist_ok=True)
members = {}
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for file in sorted(root.rglob('*')):
        if not file.is_file():
            continue
        name = 'Dragon Masters Interactive Book/'+file.relative_to(root).as_posix()
        data = file.read_bytes()
        info = zipfile.ZipInfo(name, (2026, 9, 9, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        z.writestr(info, data)
        members[name] = hashlib.sha256(data).hexdigest()
with zipfile.ZipFile(archive) as z:
    assert set(z.namelist()) == set(members)
    assert z.testzip() is None
    assert all(hashlib.sha256(z.read(n)).hexdigest() == h for n, h in members.items())
report = {'status': 'local-review-candidate-not-published', 'license': 'MIT', 'author': 'CathyErer',
          'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(), 'members': members}
manifest.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'ok': True, 'members': len(members), 'sha256': report['sha256']}))
