"""Build a portable static site from the project catalog and existing guide pages."""
from html import escape
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import urlsplit
import zipfile
import xml.etree.ElementTree as ET

from PIL import Image, ImageOps

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=HERE/'dist'
DATA=json.loads((HERE/'projects.json').read_text())
PROJECTS=DATA['projects']
ASSETS={}

def href(path,base):return os.path.relpath(path,base).replace(os.sep,'/')

def asset(source):
    source=source.resolve()
    if source in ASSETS:return ASSETS[source]
    relative=source.relative_to(ROOT/'projects')
    slug=relative.parts[0]
    name='-'.join(relative.parts[1:]).replace('.','-')
    folder=OUT/'assets'/slug;folder.mkdir(parents=True,exist_ok=True)
    if source.suffix=='.svg':
        target=folder/(name+'.svg');shutil.copy2(source,target)
        box=ET.parse(source).getroot().attrib.get('viewBox','0 0 1000 650').split()
        data={'large':target,'small':target,'width':round(float(box[2])),'height':round(float(box[3]))}
    else:
        image=ImageOps.exif_transpose(Image.open(source)).convert('RGB')
        sizes={}
        for width in (800,1600):
            copy=image.copy();copy.thumbnail((width,2400),Image.Resampling.LANCZOS)
            target=folder/f'{name}-{copy.width}.webp'
            copy.save(target,'WEBP',quality=88,method=5)
            sizes[width]=(target,copy.width,copy.height)
        data={'large':sizes[1600][0],'small':sizes[800][0],'small_width':sizes[800][1],'width':sizes[1600][1],'height':sizes[1600][2]}
    ASSETS[source]=data
    return data

def image(project,file,base,alt,*,eager=False):
    info=asset(ROOT/'projects'/project['slug']/file)
    large=href(info['large'],base);small=href(info['small'],base)
    srcset=f' srcset="{small} {info["small_width"]}w, {large} {info["width"]}w" sizes="(max-width: 700px) 100vw, 60vw"' if small!=large else ''
    return f'<img src="{large}"{srcset} alt="{escape(alt)}" width="{info["width"]}" height="{info["height"]}" loading="{"eager" if eager else "lazy"}" decoding="async">'

def header(base,active='projects'):
    return f'''<header class="site-header"><a class="wordmark" href="{href(OUT/'index.html',base)}">Woodworking</a><nav aria-label="Main navigation"><a {'aria-current="page"' if active=='projects' else ''} href="{href(OUT/'index.html',base)}">Projects</a><a {'aria-current="page"' if active=='guides' else ''} href="{href(OUT/'guides/index.html',base)}">Guides</a><a href="{DATA['repository']}">GitHub <span aria-hidden="true">↗</span></a></nav></header>'''

def page(title,description,body,base,*,active='projects',route=''):
    css=href(OUT/'assets/site.css',base);js=href(OUT/'assets/site.js',base)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} · Woodworking</title><meta name="description" content="{escape(description)}"><link rel="canonical" href="{DATA['url']}/{route}"><link rel="stylesheet" href="{css}"><script src="{js}" defer></script></head><body><a class="skip" href="#main">Skip to content</a>{header(base,active)}<main id="main">{body}</main><footer class="site-footer"><span>Woodworking</span><a href="{DATA['repository']}">Project files on GitHub ↗</a></footer><dialog class="viewer" aria-label="Image viewer"><div class="viewer-bar"><button type="button" data-prev aria-label="Previous image">←</button><p data-caption aria-live="polite"></p><button type="button" data-next aria-label="Next image">→</button><button type="button" data-close>Close ×</button></div><div data-viewer-image></div></dialog></body></html>'''

def model_bundle(project):
    target=OUT/'downloads'/f'{project["slug"]}-models.zip';target.parent.mkdir(exist_ok=True)
    paths=list((ROOT/'lib').glob('*.scad'))+list((ROOT/'projects'/project['slug']).glob('*.scad'))
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as bundle:
        for source in paths:bundle.write(source,source.relative_to(ROOT))
        bundle.writestr('README.txt','OpenSCAD model sources. Keep the folder structure so includes resolve.\n'+('For the document unit, open lib/casework.scad and set PIECE="documents".\n' if project['slug']=='document-unit' else ''))
    return target

def copy_guides(project):
    source=ROOT/'projects'/project['slug'];folder=OUT/'guides'/project['slug']
    if not project['guides']:return
    folder.mkdir(parents=True,exist_ok=True)
    for note in source.glob('*.md'):shutil.copy2(note,folder/note.name)
    for guide in project['guides']:
        original=source/guide['file']
        text=original.read_text()
        def rewrite(match):
            prefix,url,quote=match.groups();parsed=urlsplit(url)
            if parsed.scheme or not parsed.path:return match[0]
            path=source/parsed.path
            if path.suffix.lower() in ('.png','.jpg','.jpeg','.svg'):
                url=href(asset(path)['large'],folder)
            return prefix+url+quote
        text=re.sub(r'''(\b(?:src|href)\s*=\s*["'])([^"']+)(["'])''',rewrite,text)
        nav=f'<nav aria-label="Project" style="max-width:960px;margin:24px auto 0;padding:0 28px"><a href="../../projects/{project["slug"]}/index.html">← {escape(project["title"])}</a><a href="../index.html">All guides</a></nav>'
        text=text.replace('<body>','<body>'+nav,1)
        (folder/guide['file']).write_text(text)

def project_page(project):
    folder=OUT/'projects'/project['slug'];folder.mkdir(parents=True,exist_ok=True)
    name=project['title']
    body=f'<a class="back-link" href="../../index.html">← Projects</a><div class="project-heading"><div><p class="eyebrow">{project["status"]}</p><h1>{escape(name)}</h1><p class="description">{escape(project["description"])}</p></div><dl class="specs"><div><dt>Material</dt><dd>{escape(project["material"])}</dd></div><div><dt>Size</dt><dd>{escape(project["dimensions"])}</dd></div></dl></div>'
    hero=asset(ROOT/'projects'/project['slug']/project['hero'])
    body+=f'<figure class="project-hero"><a href="{href(hero["large"],folder)}" data-lightbox data-caption="{escape(name)}">{image(project,project["hero"],folder,name,eager=True)}</a></figure>'
    body+='<nav class="project-resources" aria-label="Files and guides">'
    for guide in project['guides']:
        body+=f'<a href="../../guides/{project["slug"]}/{guide["file"]}">{escape(guide["title"])} <span aria-hidden="true">↗</span></a>'
    body+=f'<a href="{href(model_bundle(project),folder)}" download>Model sources (.zip) <span aria-hidden="true">↓</span></a></nav>'
    body+='<section class="views"><h2>Views</h2><div class="view-grid">'
    views={view['file']:view for view in project['views']}
    labels={'hero':'Assembly view','persp':'Perspective view','front':'Front elevation','side':'Side elevation','top':'Top view','exploded':'Exploded assembly','joint':'Joint detail','corner_top':'Upper corner','side_bottles':'Side view with bottles','lap':'Half-lap joint','eggcrate':'Shelf and divider assembly','motion':'Assembly sequence','stile':'Side panel','scandi_base':'Square-leg attachment','waterfall':'Panel layout'}
    stages={'01':'Parts before assembly','02':'Wall frame','03':'Applied bottom','04':'Dividers and pencil riser','05':'Sliding lid fit'}
    source_folder=ROOT/'projects'/project['slug']
    for subfolder in ('renders','photos'):
        for source in sorted((source_folder/subfolder).glob('*')):
            if source.suffix.lower() not in ('.png','.svg','.jpg','.jpeg','.webp'):continue
            relative=str(source.relative_to(source_folder))
            stem=source.stem
            caption=stages.get(stem[-2:]) if '_stage' in stem else labels.get(stem)
            if not caption:
                caption=stem.replace('beauty_','').replace('guide_','').replace('L2_','Short box: ').replace('L3_','Tall box: ').replace('finger','Finger joints').replace('butt','Butt joints').replace('_',' ').capitalize()
            views.setdefault(relative,{'file':relative,'caption':caption})
    views.pop(project['hero'],None)
    for view in views.values():
        info=asset(ROOT/'projects'/project['slug']/view['file']);caption=view['caption']
        body+=f'<figure><a href="{href(info["large"],folder)}" data-lightbox data-caption="{escape(caption)}">{image(project,view["file"],folder,caption)}</a><figcaption>{escape(caption)}</figcaption></figure>'
    body+='</div></section>'
    body+='<section class="project-notes"><h2>Notes</h2>'+''.join(f'<p>{escape(note)}</p>' for note in project['notes'])+'</section>'
    (folder/'index.html').write_text(page(name,project['description'],body,folder,route=f'projects/{project["slug"]}/'))

def home():
    base=OUT
    body='<div class="page-heading"><h1>Projects</h1><p>Designs and build guides.</p></div><div class="project-grid">'
    for project in PROJECTS:
        url=f'projects/{project["slug"]}/index.html'
        body+=f'<article class="project-card"><a class="project-image" href="{url}">{image(project,project["hero"],base,project["title"],eager=project==PROJECTS[0])}</a><div class="card-heading"><h2><a href="{url}">{escape(project["title"])}</a></h2><span>{project["status"]}</span></div><p>{escape(project["description"])}</p></article>'
    body+='</div>'
    (OUT/'index.html').write_text(page('Projects','Woodworking designs, project files and build guides.',body,base))

def guide_index():
    folder=OUT/'guides';folder.mkdir(exist_ok=True)
    body='<div class="page-heading"><h1>Build guides</h1><p>Instructions, drawings and cut lists.</p></div><div class="guide-list">'
    for project in PROJECTS:
        for guide in project['guides']:
            body+=f'<a class="guide-row" href="{project["slug"]}/{guide["file"]}"><span><span class="eyebrow">{escape(project["title"])}</span><strong>{escape(guide["title"])}</strong></span><span aria-hidden="true">↗</span></a>'
    body+='</div>'
    (folder/'index.html').write_text(page('Build guides','Woodworking build guides and drawings.',body,folder,active='guides',route='guides/'))

def readme():
    rows=[]
    site_url=DATA['url'].rstrip('/')
    for p in PROJECTS:
        guides=' · '.join(f'[{g["title"]}]({site_url}/guides/{p["slug"]}/{g["file"]})' for g in p['guides']) or '—'
        rows.append(f'| [{p["title"]}]({site_url}/projects/{p["slug"]}/) | {p["description"]} | {p["status"]} | {guides} |')
    template=(HERE/'readme.md.in').read_text()
    (ROOT/'README.md').write_text(template.replace('{{PROJECTS}}','\n'.join(rows)).replace('{{SITE_URL}}',site_url))

def main():
    subprocess.run([sys.executable,str(ROOT/'lib/build_guides.py')],check=True)
    OUT.mkdir(exist_ok=True)
    # Output is disposable; remove old project pages when the catalog changes.
    for name in ('projects','guides','downloads','assets'):
        target=OUT/name
        if target.exists():shutil.rmtree(target)
    (OUT/'assets').mkdir(exist_ok=True)
    tokens=(ROOT/'lib/guide_style.css').read_text().split('* {',1)[0]
    (OUT/'assets/site.css').write_text(tokens+'\n'+(HERE/'style.css').read_text())
    shutil.copy2(HERE/'site.js',OUT/'assets/site.js')
    for project in PROJECTS:copy_guides(project);project_page(project)
    home();guide_index();readme()
    print(f'Website: {OUT}/index.html')

if __name__=='__main__':main()
