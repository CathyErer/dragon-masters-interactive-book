"""Copy the standalone starter into a new directory, never over an existing book."""
import argparse,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--destination',type=Path,required=True);a=p.parse_args()
source=Path(__file__).resolve().parents[1]/'assets/starter'
if a.destination.exists(): raise SystemExit('Destination exists; choose a new directory.')
shutil.copytree(source,a.destination)
print('Created standalone book at '+str(a.destination))
