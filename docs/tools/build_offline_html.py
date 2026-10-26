#!/usr/bin/env python3
"""Render the handbook as a self-contained, network-independent visual reader."""
from pathlib import Path
import base64,html,json,mimetypes,re
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2]
ASSETS=ROOT/'docs/assets'
source=(ROOT/'README.md').read_text(encoding='utf-8')
md=MarkdownIt('commonmark',{'html':True,'typographer':False}).enable('table').enable('strikethrough')
soup=BeautifulSoup(md.render(source),'html.parser')

def data_uri(path):
 mime={'.svg':'image/svg+xml','.ttf':'font/ttf','.step':'model/step'}.get(path.suffix)
 mime=mime or mimetypes.guess_type(str(path))[0] or 'application/octet-stream'
 return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode('ascii')

board=soup.find('div',attrs={'align':'center'})
board['class']='title-board'
# Isolate SVGs as data-URI images; repeated SVG definition IDs cannot collide.
for image in list(soup.find_all('img')):
 path=(ROOT/image['src']).resolve()
 name=path.stem
 image['src']=data_uri(path)
 image['data-figure']=name
 image['id']='figure_'+name
 image['loading']='lazy'
 image['decoding']='async'
 parent=image.find_parent('p')
 if parent:
  caption=parent.find_next_sibling('p')
  is_caption=caption and caption.get_text().lstrip().startswith('Figure —')
  figure=soup.new_tag('figure')
  parent.replace_with(figure)
  for child in list(parent.contents):figure.append(child.extract())
  if is_caption:
   cap=soup.new_tag('figcaption')
   for child in list(caption.contents):cap.append(child.extract())
   figure.append(cap);caption.decompose()
# Horizontal table scrolling is local; the complete page does not overflow.
for table in list(soup.find_all('table')):
 if table.find_parent('div',class_='title-board'):continue
 wrapper=soup.new_tag('div',attrs={'class':'table-scroll','tabindex':'0'})
 table.wrap(wrapper)
# Assign chapter numbering in the companion, without altering the Markdown.
chapter_number=2
for heading in soup.find_all('h2'):
 if heading.get_text().strip()=='Contents':continue
 span=soup.new_tag('span',attrs={'class':'section-number'})
 span.string=f'{chapter_number:02d}'
 heading.insert(0,span);chapter_number+=1
# Store each linked download once, rather than repeating a PDF data URI.
downloads={};folders={}
for link in soup.find_all('a',href=True):
 href=link['href']
 if href.startswith(('https://','http://')):
  link['target']='_blank';link['rel']='noopener noreferrer';continue
 if href.startswith('#'):continue
 path=(ROOT/href).resolve()
 if not path.is_relative_to(ROOT):raise ValueError('Link escapes package: '+href)
 if path.is_file() and path.suffix.lower() in ('.svg','.png'):
  name=path.stem
  if path.suffix.lower()=='.svg':
   link['data-open-figure']=name;link['href']='#figure_'+name
  else:
   link['data-png']=name;link['href']='#figure_'+name
 elif path.is_file():
  downloads[href]={'name':path.name,'uri':data_uri(path)}
  link['data-download']=href;link['href']='#download'
 elif path.is_dir():
  paths=[]
  for child in sorted(path.iterdir()):
   if child.is_file():
    key=child.relative_to(ROOT).as_posix()
    downloads[key]={'name':child.name,'uri':data_uri(child)};paths.append(key)
  folders[href]=paths
  link['data-folder']=href;link['href']='#folder'
 else:raise FileNotFoundError(href)
# Checklist characters remain functional without a remote Markdown extension.
for li in soup.find_all('li'):
 if li.contents and isinstance(li.contents[0],str) and li.contents[0].startswith('[ ] '):
  li.contents[0].replace_with('☐ '+str(li.contents[0])[4:])
chapters=re.findall(r'<a id="([^\"]+)"></a>\n## ([^\n]+)',source)
nav=''.join(f'<a href="#{html.escape(slug)}">{html.escape(title)}</a>' for slug,title in chapters)
font_css=''
for family,filename,weight in [('DM Sans','DMSans-Regular.ttf',400),('DM Sans','DMSans-Bold.ttf',700),('Poppins','Poppins-Regular.ttf',400),('Poppins','Poppins-Bold.ttf',700)]:
 font_css+=f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};font-display:swap;src:url('{data_uri(ROOT/'docs/fonts'/filename)}') format('truetype');}}\n"
CSS=r'''
:root{--navy:#142b43;--ink:#24394e;--muted:#60758a;--blue:#087fa7;--teal:#008b70;--line:#dce7ed;--paper:#fff;--ground:#edf3f7;--soft:#f5f9fb;--amber:#9a6717}
*{box-sizing:border-box}[hidden]{display:none!important}html{scroll-behavior:smooth;scroll-padding-top:82px}
body{margin:0;background:var(--ground);color:var(--ink);font:16px/1.75 'DM Sans',Arial,sans-serif}
a{color:var(--blue);text-decoration:none;text-underline-offset:3px}a:hover{text-decoration:underline}button,input{font:inherit}
.topbar{position:sticky;top:0;z-index:20;background:#102b40;color:white;border-bottom:3px solid var(--teal);box-shadow:0 3px 16px #102b4020}
.topbar-inner{max-width:1540px;margin:auto;display:flex;align-items:center;justify-content:space-between;padding:13px 28px;gap:20px}
.wordmark{font-family:Poppins,sans-serif;font-weight:700;font-size:17px;letter-spacing:.06em;color:white}.wordmark small{display:block;font:10px/1.2 'DM Sans',sans-serif;letter-spacing:.17em;opacity:.68}
.toptools{display:flex;gap:14px;align-items:center}.toptools a{color:#d6eceb;font-size:12px;font-weight:700}.toptools button{border:1px solid #486476;background:#19394e;color:white;padding:6px 13px;border-radius:5px;cursor:pointer;font-size:12px}
#progress{position:absolute;bottom:-3px;left:0;height:3px;width:0;background:#61d5b2}
.layout{display:grid;grid-template-columns:246px minmax(0,1110px);max-width:1440px;margin:32px auto;gap:28px;padding:0 24px}
.sidebar{position:sticky;top:100px;align-self:start;max-height:calc(100vh - 125px);display:flex;flex-direction:column;overflow:hidden}
.sidebar h2{font:700 11px/1.4 Poppins,sans-serif;letter-spacing:.14em;color:var(--muted);margin:0 0 14px;padding:0;border:0}
.sidebar input{border:1px solid #cedde7;background:white;border-radius:5px;padding:10px 12px;font-size:12px;width:100%;margin-bottom:12px;color:var(--ink)}
.sidebar nav{overflow:auto;padding-right:8px}.sidebar a{display:block;font-size:12px;line-height:1.5;padding:7px 10px;border-left:2px solid transparent;color:var(--muted)}
.sidebar a:hover,.sidebar a.active{color:var(--teal);background:#e2f1ec;border-left-color:var(--teal);text-decoration:none}
.sidebar .nav-foot{font-size:10px;color:var(--muted);padding:14px 10px;border-top:1px solid #d3e0e8;margin-top:12px}
main{min-width:0;background:white;border:1px solid #dce6ed;border-radius:12px;padding:46px 52px;box-shadow:0 12px 55px #233f5410}
.title-board{margin:-46px -52px 34px;padding:46px 40px 36px;border-radius:12px 12px 0 0;background:linear-gradient(150deg,#f1f8f9 0%,#fff 48%,#edf7f1 100%);border-bottom:1px solid var(--line);position:relative;overflow:hidden}
.title-board:before{content:'';position:absolute;left:0;right:0;top:0;height:5px;background:linear-gradient(90deg,#087fa7,#00a27c)}
.title-board h1{font:700 66px/1.12 Poppins,sans-serif;letter-spacing:-3px;color:var(--navy);margin:18px 0 16px}
.title-board h3{font:400 20px/1.55 Poppins,sans-serif;color:var(--navy);margin:0 auto 18px;max-width:860px}
.title-board p{font-size:13px;line-height:1.85;margin:14px auto;max-width:900px}.title-board p:first-of-type{font-size:10px;letter-spacing:.12em;color:var(--teal)}
.title-board code{font:700 10px/2 'DM Sans',sans-serif;letter-spacing:.04em;background:white;border:1px solid #d6e5e9;border-radius:5px;padding:4px 9px;color:#2b566a;white-space:nowrap}
.title-board table{margin:24px auto;border-collapse:separate;border-spacing:0;width:100%;font-size:11px;overflow:hidden;border:1px solid var(--line);border-radius:7px}
.title-board th{background:#eaf2f5;color:var(--muted);font:700 9px/1.5 'DM Sans',sans-serif;letter-spacing:.08em;text-transform:uppercase;padding:11px}
.title-board td{padding:13px 10px;background:#ffffffbd;line-height:1.55;border-top:1px solid var(--line)}
.title-board tr>*+*{border-left:1px solid var(--line)}
h2{font:700 25px/1.35 Poppins,sans-serif;letter-spacing:-.7px;color:var(--navy);margin:58px 0 24px;padding:0 0 15px;border-bottom:2px solid #dce8ed;scroll-margin-top:90px}
h3{font:700 17px/1.5 Poppins,sans-serif;color:#1d5167;margin:34px 0 14px;letter-spacing:-.25px}
h4{font:700 14px/1.55 'DM Sans',sans-serif;margin:25px 0 10px;color:var(--navy)}
.section-number{font:700 13px/1 Poppins,sans-serif;color:var(--teal);letter-spacing:.03em;display:inline-block;min-width:37px;vertical-align:middle}
p{margin:15px 0}p:has(>a[id]:only-child){height:0;margin:0;padding:0}a[id]{scroll-margin-top:90px}
strong{font-weight:700;color:#193d51}blockquote{margin:24px 0;padding:18px 22px;background:#edf7f3;border-left:4px solid var(--teal);border-radius:0 6px 6px 0;font-size:13px;line-height:1.8}
blockquote p{margin:0}blockquote:first-of-type{background:#f0f6f9;border-left-color:var(--blue)}
ul,ol{padding-left:25px}li{padding-left:4px;margin:6px 0}li::marker{color:var(--teal);font-weight:700}
details{border:1px solid var(--line);border-radius:7px;margin:22px 0;padding:14px 20px;background:#fafcfd}summary{cursor:pointer;color:#1d5268;font-size:13px}details[open]>summary{margin-bottom:16px}
details ol{column-count:2;column-gap:35px;font-size:12px;padding-left:23px}details li{break-inside:avoid;margin:5px 0;line-height:1.65}
figure{margin:28px 0;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:white;box-shadow:0 4px 17px #1d405506}
figure a{display:block;cursor:zoom-in}figure img{display:block;width:100%;height:auto;background:white;padding:12px}
figcaption{background:var(--soft);padding:14px 18px;border-top:1px solid var(--line);font-size:12px;line-height:1.7;color:var(--muted)}figcaption em{font-style:normal}
.table-scroll{margin:22px 0;overflow:auto;border:1px solid var(--line);border-radius:6px;max-width:100%;background:white}
table{border-collapse:collapse;width:100%;font-size:12px;line-height:1.65}th{text-align:left;vertical-align:top;background:#eaf2f6;font-weight:700;color:#235169;padding:12px 14px;border-bottom:1px solid #cddde7}
td{vertical-align:top;padding:11px 14px;border-bottom:1px solid #e5edf2}tr:nth-child(even) td{background:#f8fbfc}tr:last-child td{border-bottom:0}
td+td,th+th{border-left:1px solid #e5edf2}td code,th code{font-size:10px;overflow-wrap:anywhere}
code{font:12px/1.65 ui-monospace,SFMono-Regular,Consolas,'Liberation Mono',monospace;background:#edf3f6;padding:2px 5px;border-radius:4px;color:#265772}
pre{max-width:100%;overflow:auto;background:#142b3e;color:#daebf3;border:1px solid #234358;padding:22px 24px;border-radius:7px;margin:22px 0;font-size:12px;line-height:1.7;tab-size:4}
pre code{background:transparent;color:inherit;padding:0;font-size:inherit;border-radius:0;white-space:pre}
hr{border:0;border-top:1px solid var(--line);margin:34px 0}.reader-footer{font-size:11px;color:var(--muted);margin:45px 0 0;padding-top:22px;border-top:1px solid var(--line)}
.mobile-only{display:none}button:focus-visible,a:focus-visible,input:focus-visible,summary:focus-visible{outline:3px solid #53bca4;outline-offset:3px}
dialog{border:1px solid #8ba5b8;border-radius:10px;padding:0;box-shadow:0 15px 80px #0007;background:#fff;color:var(--ink);max-width:96vw;max-height:94vh;width:1320px}dialog::backdrop{background:#102437d9}
.dialog-head{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:14px 20px;border-bottom:1px solid var(--line);background:var(--soft)}
.dialog-head strong{font-size:13px}.dialog-head button,.dialog-head a{font-size:12px;cursor:pointer;padding:7px 11px;border-radius:4px;border:1px solid #cbdce5;background:white;color:#1c5369;white-space:nowrap}
.dialog-actions{display:flex;gap:8px;align-items:center}.figure-viewport{overflow:auto;padding:12px;max-height:78vh;text-align:center;background:white}.figure-viewport img{display:block;max-width:100%;height:auto;margin:auto;background:white}.figure-viewport.zoomed img{max-width:none;width:auto;max-height:none}
#folder-dialog{width:720px}#folder-list{padding:22px 28px;overflow:auto;max-height:70vh;font-size:13px}#folder-list a{display:block;padding:8px;border-bottom:1px solid var(--line)}
@media(min-width:1550px){.layout{margin-top:42px}}
@media(max-width:1160px){.layout{display:block;max-width:1080px;padding:0 22px;margin:24px auto}.sidebar{display:none}.mobile-only{display:inline-block}.sidebar.drawer{display:flex;position:fixed;left:12px;top:80px;width:310px;background:#f0f6fa;z-index:25;padding:22px;box-shadow:0 8px 55px #1236;border:1px solid var(--line);border-radius:8px;max-height:calc(100vh - 110px)}main{padding:38px 40px}.title-board{margin:-38px -40px 30px;padding:36px 28px}}
@media(max-width:650px){body{font-size:14px}.topbar-inner{padding:11px 14px;gap:10px}.wordmark{font-size:14px}.wordmark small{font-size:8px}.toptools{gap:8px}.toptools>a{display:none}.layout{padding:0 9px;margin:12px auto}main{padding:24px 18px;border-radius:8px}.title-board{margin:-24px -18px 23px;padding:28px 14px;border-radius:8px 8px 0 0}.title-board h1{font-size:49px;letter-spacing:-2px;margin:16px 0 12px}.title-board h3{font-size:15px}.title-board p{font-size:11px}.title-board th{font-size:8px;padding:8px 5px}.title-board td{font-size:9px;padding:10px 5px}.title-board code{font-size:9px;padding:3px 6px}h2{font-size:21px;margin-top:42px;letter-spacing:-.5px}h3{font-size:16px}.section-number{font-size:11px;min-width:30px}details{padding:12px 14px}details ol{column-count:1;font-size:12px}blockquote{padding:14px 16px;font-size:12px}figure img{padding:5px}figcaption{font-size:10px;padding:11px 13px}table{font-size:11px;min-width:490px}.title-board table{min-width:0}td,th{padding:9px 10px}pre{padding:16px;font-size:10.5px}.dialog-head{padding:12px;gap:8px;align-items:flex-start}.dialog-head strong{font-size:11px}.dialog-head button,.dialog-head a{font-size:10px;padding:5px 7px}.dialog-actions{gap:4px}}
@media print{body{background:white;font-size:10pt}.topbar,.sidebar,.reader-footer,.dialog-actions{display:none!important}.layout{display:block;margin:0;padding:0;max-width:none}main{border:0;box-shadow:none;padding:0}.title-board{margin:0 0 20px;padding:22px;border:1px solid #ddd}h2{break-before:page;font-size:20pt}h3,h4{break-after:avoid}figure,table{break-inside:avoid}.table-scroll{overflow:visible}pre{white-space:pre-wrap;overflow-wrap:anywhere;color:#111;background:#f5f5f5}pre code{white-space:pre-wrap}a{color:#146077}.title-board h1{font-size:42pt}}
'''
JS=r'''
const downloads=__DOWNLOADS__;
const folders=__FOLDERS__;
const figureDialog=document.getElementById('figure-dialog');
const folderDialog=document.getElementById('folder-dialog');
const fullFigure=document.getElementById('full-figure');
const viewport=document.querySelector('.figure-viewport');
let currentFigure='';
function imageFor(name){return document.querySelector('img[data-figure="'+name+'"]')}
function download(key){const item=downloads[key];if(!item)return;const a=document.createElement('a');a.href=item.uri;a.download=item.name;document.body.append(a);a.click();a.remove()}
function openFigure(name){const img=imageFor(name);if(!img)return;currentFigure=name;fullFigure.src=img.src;fullFigure.alt=img.alt;document.getElementById('figure-title').textContent=img.alt;const save=document.getElementById('save-svg');save.href=img.src;save.download=name+'.svg';viewport.classList.remove('zoomed');figureDialog.showModal()}
async function savePng(name){const img=imageFor(name);if(!img)return;const render=new Image();render.src=img.src;await render.decode();const canvas=document.createElement('canvas');canvas.width=render.naturalWidth*2;canvas.height=render.naturalHeight*2;const ctx=canvas.getContext('2d');ctx.fillStyle='white';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.drawImage(render,0,0,canvas.width,canvas.height);const a=document.createElement('a');a.href=canvas.toDataURL('image/png');a.download=name+'.png';document.body.append(a);a.click();a.remove()}
document.addEventListener('click',e=>{const a=e.target.closest('a');if(!a)return;if(a.dataset.openFigure){e.preventDefault();openFigure(a.dataset.openFigure)}else if(a.dataset.png){e.preventDefault();savePng(a.dataset.png)}else if(a.dataset.download){e.preventDefault();download(a.dataset.download)}else if(a.dataset.folder){e.preventDefault();const list=document.getElementById('folder-list');list.replaceChildren();document.getElementById('folder-title').textContent=a.dataset.folder;for(const key of folders[a.dataset.folder]||[]){const link=document.createElement('a');link.href='#download';link.dataset.download=key;link.textContent=downloads[key].name;list.append(link)}folderDialog.showModal()}else if(a.hash&&a.hash!=='#download'){document.querySelector('.sidebar').classList.remove('drawer')}});
document.getElementById('close-figure').onclick=()=>figureDialog.close();
document.getElementById('close-folder').onclick=()=>folderDialog.close();
document.getElementById('zoom-figure').onclick=()=>viewport.classList.toggle('zoomed');
document.getElementById('save-png').onclick=()=>savePng(currentFigure);
for(const dialog of [figureDialog,folderDialog])dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
document.getElementById('menu-toggle').onclick=()=>document.querySelector('.sidebar').classList.toggle('drawer');
document.getElementById('chapter-search').addEventListener('input',e=>{const term=e.target.value.toLowerCase();document.querySelectorAll('.sidebar nav a').forEach(a=>a.hidden=!a.textContent.toLowerCase().includes(term))});
const navLinks=[...document.querySelectorAll('.sidebar nav a')];
const sections=navLinks.map(a=>({a,node:document.getElementById(a.hash.slice(1))})).filter(s=>s.node);
let scheduled=false;
function scrollState(){scheduled=false;const max=document.documentElement.scrollHeight-innerHeight;document.getElementById('progress').style.width=(max>0?100*scrollY/max:0)+'%';let active=sections[0];for(const s of sections){if(s.node.getBoundingClientRect().top<155)active=s;else break}navLinks.forEach(a=>a.classList.toggle('active',active&&a===active.a))}
window.addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(scrollState)}},{passive:true});scrollState();
'''
JS=JS.replace('__DOWNLOADS__',json.dumps(downloads,separators=(',',':'))).replace('__FOLDERS__',json.dumps(folders,separators=(',',':')))
page='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ARKA AI — Engineering Handbook</title><meta name="description" content="ARKA AI technical handbook: sensing, Ubuntu, Qt/Python, website, app and engineering validation.">
<style>'''+font_css+CSS+'''</style></head><body>
<header class="topbar"><div class="topbar-inner"><a class="wordmark" href="#top">ARKA AI<small>ENGINEERING HANDBOOK</small></a><div class="toptools"><a href="#architecture">ARCHITECTURE</a><a href="#validation">VALIDATION</a><a href="#prototype-video">REVIEW EVIDENCE</a><button id="menu-toggle" class="mobile-only" type="button">Chapters</button><button type="button" onclick="window.print()">Print</button></div></div><div id="progress"></div></header>
<div class="layout"><aside class="sidebar" aria-label="Chapter navigation"><h2>ENGINEERING INDEX</h2><input id="chapter-search" aria-label="Find chapter" placeholder="Find a chapter…"><nav>'''+nav+'''</nav><div class="nav-foot">VK26-IITH-SE-0021<br>5,000-line Markdown source · 38 figures<br>Read-only low-voltage monitoring</div></aside><main id="handbook">'''+str(soup)+'''<div class="reader-footer">ARKA AI · Engineering handbook · VK26-IITH-SE-0021<br>Offline companion to README.md. SVG figures, fonts and linked local reference downloads are embedded. Product implementation evidence and proposed validation remain clearly distinguished.</div></main></div>
<dialog id="figure-dialog" aria-labelledby="figure-title"><div class="dialog-head"><strong id="figure-title">Technical figure</strong><div class="dialog-actions"><button id="zoom-figure" type="button">Actual size</button><a id="save-svg" href="#" download>SVG</a><button id="save-png" type="button">PNG</button><button id="close-figure" type="button" aria-label="Close figure">Close</button></div></div><div class="figure-viewport"><img id="full-figure" alt=""></div></dialog>
<dialog id="folder-dialog" aria-labelledby="folder-title"><div class="dialog-head"><strong id="folder-title">Reference assets</strong><button id="close-folder" type="button">Close</button></div><div id="folder-list"></div></dialog>
<script>'''+JS+'''</script></body></html>'''
(ROOT/'README.html').write_text(page,encoding='utf-8')
print(json.dumps({'output':'README.html','bytes':len(page.encode()),'embedded_figures':len(soup.select('img[data-figure]')),'embedded_downloads':len(downloads),'navigation_entries':len(chapters),'external_asset_requests':0},indent=2))
