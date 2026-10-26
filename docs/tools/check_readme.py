#!/usr/bin/env python3
"""Check documentation structure/contracts/calculations, not product acceptance."""
from pathlib import Path
from collections import Counter
import ast,csv,hashlib,io,json,math,re,sqlite3,sys,unittest
import xml.etree.ElementTree as ET
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup
from jsonschema import Draft202012Validator,FormatChecker
from PIL import Image
import yaml
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'docs/tools'))
from reference_math import *
raw=(ROOT/'README.md').read_bytes()
text=raw.decode('utf-8')
failures=[]
checks=[]
def check(name,condition,detail=None):
 checks.append({'name':name,'passed':bool(condition),'detail':detail})
 if not condition:failures.append(name)
check('exact_5000_LF_terminated_lines',raw.count(b'\n')==5000 and len(text.splitlines())==5000)
check('UTF8_no_BOM_no_CR',not raw.startswith(b'\xef\xbb\xbf') and b'\r' not in raw)
check('single_final_newline',raw.endswith(b'\n') and not raw.endswith(b'\n\n'))
check('title_board_is_first',text.startswith('<div align="center">') and '<h1>ARKA AI</h1>' in text[:1000])
check('no_numbered_generic_control_register',not re.search(r'^- \*\*(?:[A-Z]{3}-\d{3}|Reading control \d+)',text,re.M))
check('blank_lines_normal_separation',sum(not x.strip() for x in text.splitlines())/5000<0.18)
in_code=False
blank_run=0
maximum_outside_blank_run=0
for line in text.splitlines():
 if line.startswith('```'):
  in_code=not in_code;blank_run=0
 elif not in_code:
  blank_run=blank_run+1 if not line.strip() else 0
  maximum_outside_blank_run=max(maximum_outside_blank_run,blank_run)
check('no_excess_blank_runs_outside_code',maximum_outside_blank_run<=1,maximum_outside_blank_run)
parser=MarkdownIt('commonmark',{'html':True}).enable('table').enable('strikethrough')
tokens=parser.parse(text)
rendered=parser.render(text)
soup=BeautifulSoup(rendered,'html.parser')
ids=[tag['id'] for tag in soup.select('[id]')]
check('unique_explicit_anchors',len(ids)==len(set(ids)))
missing_links=[];broken_anchors=[];external=[]
for tag in soup.find_all(['a','img']):
 value=tag.get('href') if tag.name=='a' else tag.get('src')
 if not value:continue
 if value.startswith('#'):
  if value[1:] not in ids:broken_anchors.append(value)
 elif value.startswith(('https://','http://')):external.append(value)
 else:
  path=value.split('#',1)[0]
  target=(ROOT/path).resolve()
  if not target.is_relative_to(ROOT) or not target.exists():missing_links.append(value)
check('all_internal_anchor_links_resolve',not broken_anchors,broken_anchors)
check('all_relative_links_and_images_resolve',not missing_links,missing_links)
registry=json.loads((ROOT/'docs/assets/figure_registry.json').read_text())
images=soup.find_all('img')
check('38_inline_technical_figures',len(images)==38,len(images))
check('registry_contains_38_distinct_figures',len(registry)==38 and len({r['name'] for r in registry})==38)
svg_issues=[]
for figure in registry:
 svg=ROOT/'docs/assets'/figure['svg'];png=ROOT/'docs/assets'/figure['png']
 if not svg.exists() or not png.exists():svg_issues.append(figure['name']+':missing');continue
 try:
  root=ET.fromstring(svg.read_bytes())
  image=Image.open(png);image.verify()
  definitions=[e.attrib['id'] for e in root.iter() if 'id' in e.attrib]
  if len(definitions)!=len(set(definitions)):svg_issues.append(figure['name']+':duplicate_svg_id')
  for element in root.iter():
   if element.tag.rsplit('}',1)[-1]=='script':svg_issues.append(figure['name']+':script')
   for key,value in element.attrib.items():
    if key.rsplit('}',1)[-1]=='href' and value.startswith(('http:','https:')):
     svg_issues.append(figure['name']+':external_dependency')
 except Exception as error:svg_issues.append(figure['name']+':'+str(error))
check('SVG_and_PNG_integrity_no_remote_dependencies',not svg_issues,svg_issues)
# Code blocks are complete, parsable examples in their stated language.
fences=[t for t in tokens if t.type=='fence']
code_errors=[];schema_blocks=0;python_blocks=0;yaml_blocks=0;json_blocks=0
sql=[]
for index,token in enumerate(fences):
 try:
  if token.info=='json':json.loads(token.content);json_blocks+=1
  elif token.info=='python':ast.parse(token.content);python_blocks+=1
  elif token.info=='yaml':yaml.safe_load(token.content);yaml_blocks+=1
  elif token.info=='sql':sql.append(token.content)
 except Exception as error:code_errors.append({'block':index,'language':token.info,'error':str(error)})
check('all_JSON_Python_YAML_blocks_parse',not code_errors,code_errors)
try:
 db=sqlite3.connect(':memory:')
 db.executescript(sql[0])
 for query in sql[1].split(';'):
  if query.strip():db.execute(query,{'approved_node_id':'reference-node'}).fetchall()
 db.close();sql_ok=True
except Exception as error:sql_ok=False;code_errors.append({'SQL':str(error)})
check('reference_SQL_schema_and_queries_execute',sql_ok)
schema=json.loads((ROOT/'docs/data/telemetry_reference.schema.json').read_text())
Draft202012Validator.check_schema(schema)
validator=Draft202012Validator(schema,format_checker=FormatChecker())
schema_errors=[]
for filename in ['telemetry_fixture_valid.json','telemetry_fixture_missing_temperature.json','telemetry_fixture_unsynced.json']:
 record=json.loads((ROOT/'docs/data'/filename).read_text())
 for error in validator.iter_errors(record):schema_errors.append(filename+':'+error.message)
check('reference_telemetry_fixtures_validate',not schema_errors,schema_errors)
# Validate calculated plot datasets, including interval-boundary treatment.
with (ROOT/'docs/data/residual_persistence.csv').open() as f:rows=list(csv.DictReader(f))
first=[int(r['elapsed_s']) for r in rows if float(r['timer_s'])>=180]
check('persistence_180_elapsed_seconds_at_t300',bool(first) and first[0]==300)
with (ROOT/'docs/data/energy_gaps.csv').open() as f:rows=list(csv.DictReader(f))
total=0;excluded=0
for previous,current in zip(rows,rows[1:]):
 dt=float(current['elapsed_s'])-float(previous['elapsed_s'])
 valid=previous['valid']=='True' and current['valid']=='True'
 if valid:total+=0.5*(float(previous['power_w'])+float(current['power_w']))*dt/3600
 else:excluded+=dt
check('energy_example_excludes_80_seconds',math.isclose(excluded,80))
check('energy_dataset_matches_valid_endpoint_integration',math.isclose(total,float(rows[-1]['valid_energy_wh']),abs_tol=2e-6))
with (ROOT/'docs/data/proposed_bom.csv').open() as f:bom=list(csv.DictReader(f))
subtotal=sum(int(r['Estimated line INR'].replace(',','')) for r in bom)
check('BOM_46700_subtotal_56040_with_contingency',subtotal==46700 and round(subtotal*1.2)==56040)
check('node_only_scope_7900',subtotal-32000-6800==7900)
check('raw_retention_5184000000_bytes',raw_storage_bytes()==5184000000)
# These unit tests cover the documentation module only.
stream=io.StringIO()
suite=unittest.defaultTestLoader.discover(str(ROOT/'docs/tools'),pattern='test_reference_math.py')
result=unittest.TextTestRunner(stream=stream,verbosity=1).run(suite)
check('documentation_math_unit_tests',result.wasSuccessful(),{'executed':result.testsRun,'failures':len(result.failures),'errors':len(result.errors)})
# Offline companion checks are structural here; browser checks are recorded separately.
html_path=ROOT/'README.html';html_checks={}
if html_path.exists():
 page=BeautifulSoup(html_path.read_text(),'html.parser')
 embedded=page.select('img[data-figure]')
 network_assets=[]
 for node in page.find_all(['img','script','link']):
  reference=node.get('src') or node.get('href','')
  if reference and not reference.startswith(('data:','#')):network_assets.append(reference)
 html_checks={'embedded_figures':len(embedded),'external_asset_requests':network_assets}
 check('offline_HTML_embeds_all_38_figures',len(embedded)==38)
 check('offline_HTML_has_no_network_asset_dependencies',not network_assets,network_assets)
else:check('offline_HTML_exists',False)
report={
 'status':'PASS' if not failures else 'FAIL',
 'scope':'Documentation integrity and reference calculations only; not hardware/application acceptance.',
 'readme':{'physical_lines':raw.count(b'\n'),'utf8_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'blank_lines':sum(not x.strip() for x in text.splitlines()),'chapters_including_title_board':40,'rendered_Markdown_tables':sum(t.type=='table_open' for t in tokens),'technical_figures':len(images),'code_blocks':len(fences),'python_blocks':python_blocks,'json_blocks':json_blocks,'yaml_blocks':yaml_blocks},
 'reference_tests':{'executed':result.testsRun,'failures':len(result.failures),'errors':len(result.errors)},
 'offline_HTML':html_checks,
 'checks':checks,
 'failed_checks':failures,
 'evidence_boundaries':['Charts use calculated/planned/illustrative inputs, not measured plant telemetry.','Hardware calibration, integration timing, held-out detection and certification results were not supplied.','Software capabilities are team-confirmed; exact unpublished runtime mechanics remain release-specific.']
}
(ROOT/'docs/data/documentation_quality_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','readme','reference_tests','failed_checks']},indent=2))
if failures:sys.exit(1)
