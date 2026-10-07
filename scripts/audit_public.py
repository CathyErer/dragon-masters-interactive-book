"""Portable publication hygiene check; not a legal or exhaustive security audit."""
from pathlib import Path
import json,re

root=Path(__file__).resolve().parents[1]
allowed={'.md','.py','.js','.cjs','.json','.html','.css','.svg','.wav','.yaml','.yml'}
patterns=[re.compile('/'+'Users/'),re.compile('/private/'+'tmp/'),re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'),re.compile(r'sk-[A-Za-z0-9]{24,}')]
issues=[];files=[]
for p in sorted(root.rglob('*')):
    if '.git' in p.relative_to(root).parts:continue
    if p.is_symlink():issues.append('symlink: '+str(p.relative_to(root)));continue
    if not p.is_file():continue
    rel=p.relative_to(root).as_posix()
    if '__pycache__' in p.parts:issues.append('remove build cache: '+rel);continue
    files.append(rel)
    if p.suffix not in allowed and p.name not in {'LICENSE','.gitattributes','.gitignore'}:issues.append('unreviewed type: '+rel)
    if p.suffix!='.wav':
        text=p.read_text(encoding='utf-8')
        if any(pattern.search(text) for pattern in patterns):issues.append('possible private data: '+rel)
print(json.dumps({'ok':not issues,'files':files,'issues':issues,'boundary':'Heuristic file hygiene only; license, references and publication require human review'},ensure_ascii=False,indent=2))
raise SystemExit(1 if issues else 0)
