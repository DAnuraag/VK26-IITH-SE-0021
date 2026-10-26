from pathlib import Path
import textwrap,json,re
BASE=Path(__file__).resolve().parents[3]
REG={x['name']:x for x in json.loads((BASE/'docs/assets/figure_registry.json').read_text())}
CHAPTERS=[]
class Chapter:
 def __init__(self,title,slug):self.title=title;self.slug=slug;self.blocks=[];CHAPTERS.append(self)
 def raw(self,s):self.blocks.append(('raw',s.strip('\n')));return self
 def p(self,s):
  for p in s.strip().split('\n\n'):
   self.blocks.append(('p',' '.join(p.split())))
  return self
 def h(self,s,level=3):return self.raw('#'*level+' '+s)
 def bullets(self,items,check=False):
  for x in items:self.blocks.append(('li',('[ ] ' if check else '')+x))
  return self
 def table(self,heads,rows):
  def esc(v):return str(v).replace('|',' / ').replace('\n','<br>')
  self.raw('| '+' | '.join(map(esc,heads))+' |\n| '+' | '.join(['---']*len(heads))+' |\n'+'\n'.join('| '+' | '.join(map(esc,r))+' |' for r in rows));return self
 def code(self,lang,code):return self.raw('```'+lang+'\n'+code.strip('\n')+'\n```')
 def fig(self,name,caption):
  f=REG[name];return self.raw(f'[![{f["description"]}](docs/assets/{name}.svg)](docs/assets/{name}.svg)\n\n*Figure — {caption}*')
 def quote(self,s):return self.raw('> '+s)
 def procedure(self,title,steps):
  self.h(title,4)
  for i,s in enumerate(steps,1):self.blocks.append(('step',(i,s)))
  return self
 def render(self,width=83,choices=None):
  out=[f'<a id="{self.slug}"></a>',f'## {self.title}','']
  for idx,(kind,data) in enumerate(self.blocks):
   if idx and self.blocks[idx-1][0] in ('li','step') and kind not in ('li','step') and out[-1] != '':
    out.append('')
   w=choices.get((self.slug,idx),width) if choices else width
   if kind=='raw':lines=data.splitlines()
   elif kind=='p':lines=textwrap.wrap(data,width=w,break_long_words=False,break_on_hyphens=False)
   elif kind=='li':lines=textwrap.wrap(data,width=w-2,initial_indent='- ',subsequent_indent='  ',break_long_words=False,break_on_hyphens=False)
   elif kind=='step':
    n,s=data;prefix=f'{n}. ';lines=textwrap.wrap(s,width=w-len(prefix),initial_indent=prefix,subsequent_indent=' '*len(prefix),break_long_words=False,break_on_hyphens=False)
   out+=lines
   # List items run consecutively; other content uses normal Markdown separation.
   if kind not in ['li','step']:out+=['']
  return out

def c(title,slug):return Chapter(title,slug)

def event_table(ch,items):
 ch.table(['Condition / input','Expected handling','Evidence to retain'],items)

def mermaid(ch,source):
 ch.raw('<details>\n<summary>Expandable diagram source</summary>\n')
 ch.code('mermaid',source)
 ch.raw('</details>')
