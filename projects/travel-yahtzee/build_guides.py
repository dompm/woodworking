"""Regenerate the project guides from their editable Markdown sources."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'lib'))
from guide_pages import write_guide
PAGES={'README.md':'guide.html','ROUTER_TABLE_GUIDE.md':'router-table-guide.html'}
for source,target in PAGES.items():
    print(write_guide(HERE/source,HERE/target,page_links=PAGES,navigation=[
        ('Box build guide','guide.html'),('Optional router table','router-table-guide.html'),('Editable source',source)]))
