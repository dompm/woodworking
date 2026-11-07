"""Regenerate the collection's existing build guides with shared presentation."""
from pathlib import Path
import subprocess
import sys

from guide_pages import write_guide

ROOT=Path(__file__).resolve().parent.parent
for preset in ('winerack','documents'):
    subprocess.run([sys.executable,str(ROOT/'lib/guide.py'),preset],check=True)
for project,source in (('bedside-table','BUILD.md'),('salt-boxes','README.md')):
    folder=ROOT/'projects'/project
    print(write_guide(folder/source,folder/'guide.html',navigation=[
        ('Project','README.md'),('Editable guide',source)]))
subprocess.run([sys.executable,str(ROOT/'projects/travel-yahtzee/build_guides.py')],check=True)
