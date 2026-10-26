"""Vector primitives and outlined labels for ARKA engineering figures."""
from pathlib import Path
from html import escape
import math, json
import numpy as np
import cairosvg
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs'/'assets';OUT.mkdir(parents=True,exist_ok=True)
FD=ROOT/'docs'/'fonts'
N='#17243A';B='#23418B';C='#007FB5';T='#009D7B';G='#526780';LINE='#D9E5EF';L='#F5F9FC';TL='#EDF9F4';A='#AC7315';AL='#FFF5E3'
FONTS={w:TTFont(str(FD/f'DMSans-{name}.ttf')) for w,name in [(400,'Regular'),(500,'Medium'),(600,'SemiBold'),(700,'Bold')]}
GLYPHS={w:f.getGlyphSet() for w,f in FONTS.items()}

def measure(txt,size,weight=400):
    f=FONTS[weight];cm=f.getBestCmap();hm=f['hmtx'].metrics;upm=f['head'].unitsPerEm
    return sum(hm[cm.get(ord(c),'.notdef')][0] for c in str(txt))*size/upm

class SVG:
    def __init__(self,w,h):
        self.w=w;self.h=h;self.s=[];self.glyphs={}
        self.defs=['''<linearGradient id="solar" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#17365D"/><stop offset="1" stop-color="#21698A"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#A2D7EC" stop-opacity=".30"/><stop offset=".45" stop-color="#A2D7EC" stop-opacity="0"/><stop offset="1" stop-color="#FFFFFF" stop-opacity=".15"/></linearGradient>
<linearGradient id="body" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E5EDF3"/><stop offset="1" stop-color="#BFCCD8"/></linearGradient>
<linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#DDE7EE"/><stop offset=".47" stop-color="#B7C9D6"/><stop offset="1" stop-color="#E0E9EF"/></linearGradient>
<linearGradient id="pcb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3EB293"/><stop offset="1" stop-color="#187B68"/></linearGradient>
<linearGradient id="tealbar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#86D6BE"/><stop offset="1" stop-color="#009D7B"/></linearGradient>
<linearGradient id="bluebar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#AAD1E5"/><stop offset="1" stop-color="#2C87B0"/></linearGradient>
<linearGradient id="areafill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#38B991" stop-opacity=".18"/><stop offset="1" stop-color="#38B991" stop-opacity="0"/></linearGradient>
<marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#8CA5B8"/></marker>
<marker id="tarr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#009D7B"/></marker>
<marker id="aarr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#AC7315"/></marker>''']
    def add(self,a):self.s.append(a)
    def rect(self,x,y,w,h,fill='white',stroke=LINE,r=10,sw=1.3,opacity=1):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>')
    def card(self,x,y,w,h,fill='white',stroke=LINE,r=12):
        self.rect(x,y+3,w,h,'#203F5D','none',r,opacity=.035)
        self.rect(x,y,w,h,fill,stroke,r)
    def line(self,x1,y1,x2,y2,color=LINE,sw=1.8,dash='',arrow=''):
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+(f' marker-end="url(#{arrow})"' if arrow else '')+'/>')
    def path(self,d,color=LINE,sw=1.8,fill='none',dash='',arrow='',opacity=1):
        self.add(f'<path d="{d}" stroke="{color}" stroke-width="{sw}" fill="{fill}" stroke-linejoin="round" stroke-linecap="round" opacity="{opacity}"'+(f' stroke-dasharray="{dash}"' if dash else '')+(f' marker-end="url(#{arrow})"' if arrow else '')+'/>')
    def poly(self,p,fill,stroke=LINE,sw=1.2,opacity=1):
        self.add('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in p)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" opacity="{opacity}"/>')
    def circle(self,x,y,r,fill='white',stroke=LINE,sw=1.3):self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def ellipse(self,x,y,rx,ry,fill,opacity=1,stroke='none',sw=1):self.add(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" opacity="{opacity}" stroke="{stroke}" stroke-width="{sw}"/>')
    def text(self,x,y,txt,size=22,color=N,weight=400,anchor='start',maxw=None):
        txt=str(txt);wid=measure(txt,size,weight)
        if maxw and wid>maxw:size=size*maxw/wid;wid=maxw
        if anchor=='middle':x-=wid/2
        elif anchor=='end':x-=wid
        f=FONTS[weight];cm=f.getBestCmap();gs=GLYPHS[weight];unit=f['head'].unitsPerEm;hm=f['hmtx'].metrics;scale=size/unit
        uses=[];xx=0
        for c in txt:
            gl=cm.get(ord(c),'.notdef');key=(weight,gl)
            if key not in self.glyphs:
                pen=SVGPathPen(gs);gs[gl].draw(pen);gid='g'+str(len(self.glyphs))
                self.glyphs[key]=(gid,pen.getCommands())
            gid,_=self.glyphs[key]
            if c!=' ':uses.append(f'<use xlink:href="#{gid}" transform="translate({xx:.4f} 0)"/>')
            xx+=hm[gl][0]
        self.add(f'<g aria-label="{escape(txt,quote=True)}" fill="{color}" transform="translate({x:.4f} {y:.4f}) scale({scale:.7f} {-scale:.7f})">'+''.join(uses)+'</g>')
    def lines(self,x,y,lines,size=19,color=G,weight=400,anchor='start',lead=1.26,maxw=None):
        for i,t in enumerate(lines):self.text(x,y+i*size*lead,t,size,color,weight,anchor,maxw)
    def icon(self,name,x,y,size=32,color=C,bg=None):
        if bg:self.circle(x+size/2,y+size/2,size*.72,bg,'none')
        paths={
         'solar':'M3 9 L26 5 L30 24 L7 28 Z M10 8 L14 27 M18 6 L22 25 M5 16 L28 12 M7 22 L29 19 M11 28 L11 31 M26 25 L26 29',
         'chip':'M8 7 H25 V25 H8 Z M12 11 H21 V21 H12 Z M12 2 V7 M18 2 V7 M24 2 V7 M12 25 V30 M18 25 V30 M24 25 V30 M2 11 H8 M2 17 H8 M2 23 H8 M25 11 H31 M25 17 H31 M25 23 H31',
         'wifi':'M3 11 Q17 -1 31 11 M8 17 Q17 8 26 17 M13 22 Q17 18 21 22 M17 27 L17 27',
         'server':'M6 3 H28 V12 H6 Z M6 16 H28 V25 H6 Z M11 7 H12 M11 20 H12 M17 7 H24 M17 20 H24 M17 25 V31 M9 31 H25',
         'chart':'M5 3 V28 H31 M9 22 L15 16 L21 19 L29 7 M26 7 H29 V11',
         'monitor':'M3 3 H31 V24 H3 Z M17 24 V30 M10 30 H24 M7 17 L12 12 L18 15 L27 7',
         'shield':'M17 2 L29 7 V17 Q28 26 17 31 Q6 26 5 17 V7 Z M11 16 L15 20 L24 11',
         'clock':'M17 3 A14 14 0 1 0 17 31 A14 14 0 1 0 17 3 M17 8 V17 L24 21',
         'file':'M7 2 H23 L29 8 V31 H7 Z M23 2 V8 H29 M11 14 H24 M11 20 H24 M11 26 H20',
         'split':'M5 5 H15 V15 H5 Z M20 19 H30 V29 H20 Z M20 5 H30 V15 H20 Z M5 19 H15 V29 H5 Z',
         'eye':'M2 17 Q17 -1 32 17 Q17 35 2 17 Z M22 17 A5 5 0 1 0 12 17 A5 5 0 1 0 22 17 M4 30 L30 4',
         'bell':'M8 24 V15 Q8 6 17 6 Q26 6 26 15 V24 L30 27 H4 Z M13 29 Q17 35 21 29 M17 2 V6',
         'wrench':'M21 3 Q29 1 31 10 L25 16 L18 14 L6 29 L2 25 L17 11 L15 5 L21 3',
         'scan':'M4 10 V3 H11 M23 3 H30 V10 M30 24 V31 H23 M11 31 H4 V24 M9 17 H25 M13 11 V23 M21 11 V23',
         'temp':'M14 6 A4 4 0 0 1 22 6 V21 A8 8 0 1 1 14 21 Z M18 10 V25 M27 8 H31 M27 14 H31',
         'sun':'M17 9 A8 8 0 1 0 17 25 A8 8 0 1 0 17 9 M17 1 V5 M17 29 V33 M1 17 H5 M29 17 H33 M5 5 L8 8 M26 26 L29 29 M5 29 L8 26 M26 8 L29 5',
         'bolt':'M19 1 L5 20 H16 L13 33 L30 13 H19 Z',
         'link':'M13 20 L21 12 M13 9 L18 4 Q23 -1 29 5 Q34 10 29 15 L24 20 M21 24 L16 29 Q11 34 5 28 Q0 23 5 18 L10 13',
        }
        self.add(f'<g transform="translate({x} {y}) scale({size/34:.4f})" fill="none" stroke="{color}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="{paths[name]}"/></g>')
    def badge(self,x,y,label,color=C,fill=L,size=17,pad=12,h=30):
        w=measure(label,size,600)+pad*2
        self.rect(x,y,w,h,fill,'none',h/2)
        self.text(x+w/2,y+h*.69,label,size,color,600,'middle')
        return w
    def save(self,name):
        gs=''.join(f'<path id="{gid}" d="{path}"/>' for gid,path in self.glyphs.values())
        b=(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}"><defs>'+''.join(self.defs)+gs+'</defs>'+''.join(self.s)+'</svg>').encode()
        (OUT/(name+'.svg')).write_bytes(b)
        cairosvg.svg2png(bytestring=b,write_to=str(OUT/(name+'.png')),scale=1.65)
        print(name,self.w,self.h,len(b),'bytes')

