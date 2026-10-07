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
        if not file.is_file() or '.git' in file.relative_to(root).parts:
            continue
        name = 'Dragon Masters Interactive Book/'+file.relative_to(root).as_posix()
        data = file.read_bytes()
        info = zipfile.ZipInfo(name, (2026, 10, 7, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        z.writestr(info, data)
        members[name] = hashlib.sha256(data).hexdigest()
with zipfile.ZipFile(archive) as z:
    assert set(z.namelist()) == set(members)
    assert z.testzip() is None
    assert all(hashlib.sha256(z.read(n)).hexdigest() == h for n, h in members.items())
report = {'version': '0.3.0', 'status': 'local-package-verified-publication-tracked-separately', 'license': 'MIT', 'author': 'CathyErer',
          'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(), 'members': members}
manifest.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'ok': True, 'members': len(members), 'sha256': report['sha256']}))

# Direct-install artifact: the skill folder is the archive root.
skill_root=root/'skills/dragon-masters-interactive-book'
install=destination/'dragon-masters-interactive-book.skill'
with zipfile.ZipFile(install,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for file in sorted(skill_root.rglob('*')):
        if file.is_file():
            info=zipfile.ZipInfo('dragon-masters-interactive-book/'+file.relative_to(skill_root).as_posix(),(2026,10,7,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,file.read_bytes())
with zipfile.ZipFile(install) as z:
    assert z.testzip() is None
    assert all(z.read('dragon-masters-interactive-book/'+p.relative_to(skill_root).as_posix())==p.read_bytes() for p in skill_root.rglob('*') if p.is_file())
report['installPackage']={'name':install.name,'sha256':hashlib.sha256(install.read_bytes()).hexdigest()}
manifest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'installPackage':install.name,'sha256':report['installPackage']['sha256']}))
