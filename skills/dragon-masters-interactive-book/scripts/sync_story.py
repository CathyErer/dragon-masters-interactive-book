"""Create the no-fetch browser data file from editable JSON."""
import argparse,json
from pathlib import Path
def sync(root):
    data=json.loads((root/'story.json').read_text(encoding='utf-8'))
    (root/'story.js').write_text('window.BOOK = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();sync(a.directory)
