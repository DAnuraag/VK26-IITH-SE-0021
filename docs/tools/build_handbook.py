#!/usr/bin/env python3
"""Build the 5,000-line engineering handbook from authored chapter sources.

The final adjustment uses ordinary 72–88-column soft wrapping of prose only.
No sentences, empty records, numbered controls or blank-line padding are added.
"""
from pathlib import Path
import sys,json,textwrap,hashlib
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'handbook_source'
if not SOURCE.exists(): SOURCE=HERE
sys.path.insert(0,str(SOURCE))
import content_01,content_02,content_03,content_04
import content_expansions,content_final_details
from doc_engine import CHAPTERS,BASE
TARGET=5000
HEADER='''<div align="center">
  <a id="top"></a>
  <p><strong>☀ &nbsp; S O L A R &nbsp; I N T E L L I G E N C E</strong></p>
  <h1>ARKA AI</h1>
  <h3>Intelligent Edge-AI Monitoring &amp; Performance Optimization<br>System for Solar Power Plants</h3>
  <p><strong>Local intelligence. Connected monitoring. Engineer-led decisions.</strong></p>
  <p>
    <code>Ubuntu</code> &nbsp; <code>Qt / PySide6</code> &nbsp; <code>Python</code><br>
    <code>ESP32-S3</code> &nbsp; <code>MQTT</code> &nbsp; <code>Website + App</code>
  </p>
  <table>
    <tr>
      <th>Application ID</th>
      <th>Theme</th>
      <th>Sub-theme</th>
    </tr>
    <tr>
      <td align="center"><strong>VK26-IITH-SE-0021</strong></td>
      <td align="center">Sustainable Energy</td>
      <td align="center">Renewable Energy Harvesting<br>&amp; Generation Systems</td>
    </tr>
  </table>
  <p><strong>A field-to-engineer monitoring ecosystem</strong><br>ESP32-S3 sensing → Ubuntu-based onsite platform → Qt, website &amp; companion app</p>
  <p>
    <a href="https://github.com/DAnuraag/VK26-IITH-SE-0021"><strong>PROJECT REPOSITORY &amp; REVIEW HUB</strong></a><br>
    <a href="docs/references/ARKA_AI_Stage1.pdf"><strong>PROJECT DOCUMENTATION</strong></a> &nbsp; · &nbsp;
    <a href="#prototype-video"><strong>PROTOTYPE VIDEO / PUBLICATION STATUS</strong></a>
  </p>
  <p>
    <a href="#architecture">Architecture</a> &nbsp; · &nbsp;
    <a href="#embedded-os">Embedded OS</a> &nbsp; · &nbsp;
    <a href="#website">Website</a> &nbsp; · &nbsp;
    <a href="#companion-app">App</a> &nbsp; · &nbsp;
    <a href="#installation">Installation</a> &nbsp; · &nbsp;
    <a href="#validation">Validation</a> &nbsp; · &nbsp;
    <a href="#risk-register">Safety</a>
  </p>
</div>

> **REVIEWERS:** start with the [architecture](#architecture),
> [implementation milestones](#maker-journey) and [validation/evidence](#validation).
> **A verified prototype-video URL is not yet supplied; [see publication status](#prototype-video).**

**Document basis:** original Stage 1 submission, team-confirmed software scope,
manufacturer references and explicitly labeled proposed engineering contracts.
**Visual evidence:** 38 technical figures with editable SVGs and PNG fallbacks;
calculated/planned charts are not measured prototype results.

**Operating boundary:** read-only low-voltage demonstrator, **12–24 V DC, ≤5 A**.
**Never connect this reference circuit directly to live plant PV strings.**

<a id="contents"></a>
## Contents

<details open>
<summary><strong>Open the complete engineering handbook index</strong></summary>

1. [Title board and review hub](#top)
'''
HEADER+='\n'.join(f'{i}. [{ch.title}](#{ch.slug})' for i,ch in enumerate(CHAPTERS,2))
HEADER+='\n\n</details>\n\n'

def block_count(kind,data,width):
 if kind=='p':return len(textwrap.wrap(data,width=width,break_long_words=False,break_on_hyphens=False))
 if kind=='li':return len(textwrap.wrap(data,width=width-2,initial_indent='- ',subsequent_indent='  ',break_long_words=False,break_on_hyphens=False))
 if kind=='step':
  n,s=data;prefix=f'{n}. '
  return len(textwrap.wrap(s,width=width-len(prefix),initial_indent=prefix,subsequent_indent=' '*len(prefix),break_long_words=False,break_on_hyphens=False))
 return None

def render(width,choices):
 out=HEADER.rstrip('\n').split('\n')+['']
 for ch in CHAPTERS:
  if out[-1]!='':out+=['']
  out+=ch.render(width,choices)
 # A single final line ending, not a blank-line pad.
 while out and out[-1]=='':out.pop()
 return out

BASE_WIDTH=76
lines=render(BASE_WIDTH,{})
delta=TARGET-len(lines)
# Select ordinary source-wrap widths without changing substantive content.
choices={}
remaining=delta
for ch in CHAPTERS:
 for idx,(kind,data) in enumerate(ch.blocks):
  if not remaining or kind not in ('p','li','step'):continue
  initial=block_count(kind,data,BASE_WIDTH)
  possibilities=[]
  for width in range(72,89):
   difference=block_count(kind,data,width)-initial
   if difference and difference*remaining>0 and abs(difference)<=abs(remaining):
    possibilities.append((abs(width-BASE_WIDTH),width,difference))
  if possibilities:
   _,width,difference=min(possibilities)
   choices[ch.slug,idx]=width
   remaining-=difference
if remaining:
 raise RuntimeError(f'Authored content cannot fit target with normal wrapping: {remaining}')
lines=render(BASE_WIDTH,choices)
assert len(lines)==TARGET,(len(lines),TARGET)
text='\n'.join(lines)+'\n'
assert text.count('\n')==TARGET
assert len(text.splitlines())==TARGET
assert '\r' not in text
(BASE/'README.md').write_text(text,encoding='utf-8',newline='\n')
report={'physical_lines':TARGET,'utf8_bytes':len(text.encode()),'chapter_count_including_title_board':len(CHAPTERS)+1,'technical_figures':38,'sha256':hashlib.sha256(text.encode()).hexdigest(),'base_prose_wrap_columns':BASE_WIDTH,'prose_wrap_adjustments':len(choices),'wrap_range_columns':[72,88],'blank_lines':sum(not x for x in lines),'padding_lines_added':0}
(BASE/'docs/data/handbook_build.json').write_text(json.dumps(report,indent=2)+'\n')
# Export the actual reference contracts used in the handbook.
for name,obj in [('telemetry_reference.schema.json',content_02.schema),('telemetry_fixture_valid.json',content_02.fixture),('telemetry_fixture_missing_temperature.json',content_02.missing),('telemetry_fixture_unsynced.json',content_02.unsynced)]:
 (BASE/'docs/data'/name).write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps(report,indent=2))
