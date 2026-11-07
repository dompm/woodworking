"""Shared Markdown-to-guide presentation for the constructs used by project notes."""
from html import escape
from pathlib import Path
import re

def render_markdown(source, *, base_dir, page_links=None):
    page_links=page_links or {}
    def inline(text):
        text=escape(text)
        def link(m):
            label,url=m.groups();url=page_links.get(url,url)
            return f'<a href="{url}">{label}</a>'
        text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,text)
        text=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',text)
        return re.sub(r'`([^`]+)`',r'<code>\1</code>',text)
    lines=source.splitlines();out=[];i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line=='---':out.append('<hr>');i+=1;continue
        if line.startswith('```'):
            code=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            out.append('<pre><code>'+escape('\n'.join(code))+'</code></pre>');i+=1;continue
        heading=re.match(r'^(#{1,6}) (.+)',line)
        if heading:
            level=len(heading[1]);title=heading[2];slug=re.sub(r'[^a-z0-9]+','-',title.lower()).strip('-')
            out.append(f'<h{level} id="{slug}">{inline(title)}</h{level}>');i+=1;continue
        img=re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)',line)
        if img:
            alt,url=img.groups();assert (base_dir/url).exists(),url
            out.append(f'<figure><a href="{escape(url)}"><img src="{escape(url)}" alt="{escape(alt)}" loading="lazy"></a><figcaption>{escape(alt)}</figcaption></figure>');i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]);i+=1
            out.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+inline(c)+'</th>' for c in rows[0])+'</tr></thead><tbody>')
            for row in rows[2:]:out.append('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>')
            out.append('</tbody></table></div>');continue
        ordered=bool(re.match(r'^\d+\. ',line));unordered=line.startswith('- ')
        if ordered or unordered:
            tag='ol' if ordered else 'ul';pattern=r'^\d+\. (.*)' if ordered else r'^- (.*)'
            out.append('<'+tag+'>')
            while i<len(lines):
                match=re.match(pattern,lines[i].strip())
                if not match:break
                item=[match[1]];i+=1
                while i<len(lines) and lines[i].startswith('  ') and lines[i].strip():item.append(lines[i].strip());i+=1
                out.append('<li>'+inline(' '.join(item))+'</li>')
            out.append('</'+tag+'>');continue
        paragraph=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|!\[|\||```|\d+\. |[-] )',lines[i].strip()):paragraph.append(lines[i].strip());i+=1
        out.append('<p>'+inline(' '.join(paragraph))+'</p>')
    return '\n'.join(out)


def write_guide(source_path, output_path, *, page_links=None, navigation=()):
    source_path=Path(source_path);output_path=Path(output_path)
    content=source_path.read_text()
    title=content.splitlines()[0].lstrip('# ')
    css=Path(__file__).with_name('guide_style.css').read_text()
    nav=''.join(f'<a href="{escape(url)}">{escape(label)}</a>' for label,url in navigation)
    body=render_markdown(content,base_dir=source_path.parent,page_links=page_links)
    output_path.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><style>{css}</style></head><body><main><nav>{nav}</nav>{body}<footer>Images open at full size when selected. Generated from the editable Markdown guide.</footer></main></body></html>')
    return output_path
