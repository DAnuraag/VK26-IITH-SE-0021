#!/usr/bin/env python3
"""Reproduce ARKA documentation figures and calculated example datasets.
No chart is a record of measured plant, software or laboratory performance.
Existing SVG masters are editable assets; this script refreshes PNG fallbacks.
"""
from pathlib import Path
import csv,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import cairosvg
from vector_canvas import SVG,N,B,C,T,G,LINE,L,TL,A,AL
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/assets';DATA=ROOT/'docs/data'
OUT.mkdir(parents=True,exist_ok=True);DATA.mkdir(parents=True,exist_ok=True)
FIGURES=[]

def record(name,description,basis='Reference architecture / proposed operating contract'):
 FIGURES.append({'name':name,'svg':name+'.svg','png':name+'.png','description':description,'basis':basis})

def canvas(w=1320,h=520):
 s=SVG(w,h);s.rect(0,0,w,h,'white','none',0);return s

def block(s,x,y,w,h,head,body=(),color=C,fill=L,size=20):
 s.rect(x,y,w,h,fill,LINE,7)
 s.text(x+15,y+30,head,size,color,700,maxw=w-30)
 if body:s.lines(x+15,y+59,body,17.2,G,maxw=w-30,lead=1.28)

def save(s,name,desc,basis='Reference architecture / proposed operating contract'):
 s.save(name);record(name,desc,basis)

def flow(name,groups,desc,foot=None):
 s=canvas(1320,345);gap=25;w=(1280-gap*(len(groups)-1))/len(groups)
 for i,(head,body) in enumerate(groups):
  x=20+i*(w+gap);block(s,x,46,w,220,head,body,T if i%2 else C,TL if i%2 else L,21)
  if i<len(groups)-1:s.line(x+w+2,151,x+w+gap-2,151,T,2,arrow='tarr')
 if foot:s.text(660,318,foot,18,G,500,'middle',maxw=1270)
 save(s,name,desc)

# Existing masters (same diagram content as the project presentation).
for name,description,basis in [
 ('ecosystem_overview','Onsite Ubuntu platform, Qt/Python, website and companion app','Stage 1 scope + team-confirmed software capabilities'),
 ('ecosystem_architecture','Field, messaging, embedded gateway and client interfaces','Logical architecture; detailed contracts are reference design'),
 ('ecosystem_workflow','Sensing-to-engineer inspection and recorded outcome','Documented user journey extended with connected clients'),
 ('electrical_connections','Pin-referenced Kelvin sensing and isolated I2C','Proposed low-voltage connection; TI pin tables'),
 ('mechanical_layout','Board allocation, enclosure dimensions and tab load','Proposed geometry; analytical assumptions, not EDA/FEA'),
 ('enclosure_assembly','Exploded sensor-node enclosure','Proposed seven-part STEP packaging concept'),
 ('anomaly_flow','Quality gating, residual and persistence','Proposed anomaly acceptance logic'),
 ('hmi_reference_layout','Electrical/environmental interface example','Illustrative layout/values, not an actual software capture'),
 ('verification_roadmap','Forward verification and release plan','Four-month relative plan, not completed milestones')]:
 p=OUT/(name+'.svg')
 if p.exists():
  text=p.read_text()
  if 'data-docs-background' not in text:
   import re
   text=re.sub(r'(<svg\b[^>]*>)',r'\1<rect data-docs-background="white" x="0" y="0" width="100%" height="100%" fill="#ffffff"/>',text,count=1)
   p.write_text(text)
  cairosvg.svg2png(url=str(p),write_to=str(OUT/(name+'.png')),scale=1.65,background_color='white');record(name,description,basis)

# Ubuntu runtime stack and ownership.
s=canvas(1320,520)
layers=[(22,'ENGINEER ACCESS','Qt / PySide6 onsite UI | website | companion app',T,TL),(117,'APPLICATION SERVICES','Python ingestion | quality | power / energy | analysis | alerts',C,L),(212,'LOCAL DATA + TRANSPORT','MQTT broker | telemetry / event persistence | export / recovery',C,L),(307,'LINUX PLATFORM','Ubuntu command-line base | process supervision | users | storage',B,'#EFF3FA')]
for y,head,sub,color,fill in layers:
 s.rect(25,y,1270,78,fill,LINE,7);s.text(43,y+29,head,20,color,700);s.text(43,y+59,sub,22,N,500,maxw=1228)
for y in [101,196,291]:s.line(660,y,660,y+15,T,1.8,arrow='tarr')
s.text(660,451,'FIELD NODE: ESP32-S3 firmware is a separate compute boundary; it does not run Ubuntu.',20,G,500,'middle',maxw=1250)
s.text(660,488,'Ubuntu-based application environment ≠ newly written kernel / distribution',19,G,500,'middle',maxw=1250)
save(s,'runtime_stack','Runtime layers and separation of gateway from sensor-node firmware','Known software technologies; logical service decomposition')

# Startup/recovery reference dependency graph.
s=canvas(1320,475)
for x,h,b in [(15,'PLATFORM READY',['Ubuntu boots','Storage mounted','Service user available']),(350,'DATA SERVICES',['Broker reachable','Database opened','Schema/config checked']),(685,'APPLICATION READY',['Backend workers start','Clock/quality state set','Qt receives snapshots']),(1020,'OPERATOR READY',['Data age visible','Faults / events restored','Engineer confirms scope'])]:
 block(s,x,34,285,178,h,b,C,L,20)
 if x<1020:s.line(x+286,120,x+333,120,T,2,arrow='tarr')
s.path('M1162 213 L1162 281 L157 281 L157 213',A,1.8,dash='6 5',arrow='aarr')
s.text(660,271,'Fault or dependency loss → expose degraded state → diagnose → controlled restart',20,A,600,'middle',maxw=1250)
block(s,25,324,400,111,'NEVER HIDE', ['Unavailable data / invalid config','Do not substitute “healthy” values'],A,AL,20)
block(s,460,324,400,111,'VERIFY RECOVERY',['No duplicate committed samples','Correct release / calibration context'],T,TL,20)
block(s,895,324,400,111,'CAPTURE EVIDENCE',['Startup log / service status','As-left operator data / event state'],C,L,20)
save(s,'boot_recovery','Reference startup dependencies, degraded state and controlled recovery')

# Qt worker boundaries.
s=canvas(1320,470)
block(s,20,46,290,170,'ACQUISITION WORKER',['MQTT / node records','Validate envelope / units','Never block the UI thread'])
block(s,352,46,290,170,'ANALYSIS / WRITER',['Derive P and valid energy','Deduplicate / persist','Evaluate event conditions'],T,TL)
block(s,684,46,290,170,'QUEUED SNAPSHOT',['Immutable identity + time','Quality + event revision','Bounded update cadence'])
block(s,1016,46,284,170,'QT UI THREAD',['Render cards / trends','Show stale / unavailable','Handle operator inputs'],T,TL)
for x in [311,643,975]:s.line(x,131,x+39,131,T,2,arrow='tarr')
s.rect(20,254,1280,74,AL,LINE,7);s.text(42,284,'THREAD RULE',19,A,700)
s.text(42,311,'Worker threads do I/O; Qt widgets change only in the UI thread through an explicit queued boundary.',20,N,500,maxw=1230)
s.path('M1156 217 L1156 384 L164 384 L164 217',C,1.6,dash='5 4',arrow='arr')
s.text(660,419,'Operator filters / acknowledgement requests do not become plant-control commands.',19,G,500,'middle',maxw=1250)
save(s,'qt_workers','Reference nonblocking Qt worker, storage and rendering boundaries')

# Access boundaries, not a claim of deployed remote security.
s=canvas(1320,470)
s.rect(12,14,820,440,TL,'#B3D8C4',9);s.text(34,43,'ONSITE TRUST ZONE',21,T,700)
block(s,32,78,322,153,'EMBEDDED PLATFORM',['Ubuntu + Python backend','Local history / alerts','Qt engineer interface'],T,'white')
block(s,417,78,389,153,'ACCESS BOUNDARY',['Authenticated read access','Network route / policy review','Detailed protocol to be released'],A,AL)
s.line(355,150,416,150,T,2,arrow='tarr')
block(s,891,48,400,143,'WEBSITE',['Common monitoring identity','Browser session / data-age state'],C,L)
block(s,891,259,400,143,'COMPANION APP',['Engineer monitoring context','Network-dependent remote access'],C,L)
s.path('M807 151 L859 151 L859 119 L890 119',T,1.8,arrow='tarr')
s.path('M859 151 L859 329 L890 329',T,1.8,arrow='tarr')
block(s,33,277,772,125,'WAN LOSS IS NOT LAN LOSS',['The local HMI/history should remain useful without WAN access.','Remote clients still require an approved, available network path.'],T,'white')
save(s,'client_access','Onsite and remote access boundaries with local-first behavior')

flow('firmware_cycle',[
 ('ACQUIRE',['V / I shunt + bus','Irradiance ADC','Temperature conversion']),
 ('QUALIFY',['Range / sensor status','Calibration revision','Monotonic identity']),
 ('RECORD',['Source time / quality','Sequence + boot ID','Retain outage record']),
 ('PUBLISH',['MQTT telemetry','QoS 1 design target','Explicit reconnect state'])],
 'Reference sensor acquisition and publish cycle','Sampling / reconnect design must be verified on the actual firmware release.')

# Power domains, consistent with the connection diagram.
s=canvas(1320,455)
block(s,20,28,340,140,'EXTERNAL 5 V',['Rated regulated source','Current limiting / disconnect'],C,L)
block(s,423,28,350,140,'CONTROLLER DOMAIN',['DevKit regulator → 3V3_CTRL','ESP32 + ADC + temperature'],T,TL)
block(s,886,28,414,140,'MEASURED DOMAIN',['Isolated DC/DC → TLV76033','3V3_ISO → INA226 / ISO side 2'],C,L)
s.line(361,100,422,100,T,2,arrow='tarr');s.path('M190 169 L190 216 L1092 216 L1092 169',C,2,arrow='arr')
s.text(660,249,'Isolated power branch crosses an engineered boundary; the nominal converter output is unregulated.',18.5,G,500,'middle',maxw=1270)
s.line(830,10,830,427,A,1.7,'6 5')
s.rect(20,296,1280,121,AL,LINE,7)
s.text(40,330,'GND_CTRL ≠ GND_ISO',25,A,700)
s.lines(40,361,['Do not bridge domains through USB shields, grounded oscilloscopes or unreviewed probe connections.','Component withstand ratings do not establish safe working voltage of the complete assembly.'],19,G,maxw=1240)
save(s,'power_domains','Separate power/ground domains, isolated branch and common bridge hazards','Proposed node power design; not a safety certification')

flow('irradiance_chain',[
 ('PYRANOMETER',['SP-110-SS','Nominal 0.2 mV','per W/m²']),
 ('ANALOG INPUT',['AIN0 referenced to','GND_CTRL','Review filtering / rails']),
 ('ADS1115',['Candidate ±0.512 V','16-bit code scale','Verify actual PGA']),
 ('ENGINEERING VALUE',['Apply actual calibration','W/m² + quality','Alignment / mounting'])],
 'Nominal irradiance signal chain and proposed ADC range','ADC resolution is not instrument accuracy; preserve the actual calibration certificate.')

# QoS/replay sequence diagram.
s=canvas(1320,520);xs=[140,470,800,1140]
for x,head in zip(xs,['NODE','BROKER','GATEWAY','DATABASE']):
 s.rect(x-111,16,222,49,L,LINE,6);s.text(x,47,head,20,C,700,'middle');s.line(x,66,x,487,LINE,1.4,'5 5')
messages=[(0,1,111,'boot=A / seq=104'),(1,2,169,'deliver QoS 1 record'),(2,3,227,'INSERT unique node/boot/seq'),(1,2,285,'redeliver same record'),(2,3,343,'conflict → no duplicate row'),(0,1,401,'reconnect / replay stored seq'),(2,3,459,'backfill keeps source time')]
for a,b,y,label in messages:
 s.line(xs[a],y,xs[b]-9,y,T,1.9,arrow='tarr');s.text((xs[a]+xs[b])/2,y-10,label,17.5,G,500,'middle',maxw=abs(xs[b]-xs[a])-18)
save(s,'mqtt_replay','Reference QoS 1 redelivery and idempotent persistence sequence')

# Envelope contract.
s=canvas(1320,445)
for x,head,body in [
 (20,'IDENTITY',['site_id / zone_id / node_id','boot_id / sequence','schema_version / record_id']),
 (453,'MEASUREMENTS',['voltage_v / current_a','irradiance_w_m2 / temperature_c','units + calibration_revision']),
 (886,'TIME + QUALITY',['source_time_utc / receive_time','clock uncertainty / sample age','valid / stale / fault / backfill'])]:
 block(s,x,39,414,192,head,body,C,L,20)
s.rect(20,278,1280,124,TL,LINE,7)
s.text(42,311,'SHARED CLIENT CONTEXT',21,T,700)
s.lines(42,345,['Qt, website and companion app must not silently disagree about sample identity, age, units or event state.','Unknown schema / malformed data is rejected or quarantined; it does not become a healthy measurement.'],19,G,maxw=1237)
save(s,'telemetry_contract','Reference telemetry envelope and shared-client context')

# Logical data model; names explicitly reference schema in README.
s=canvas(1320,510)
items=[(25,31,382,174,'TELEMETRY',['PK: node + boot + sequence','Source / receive UTC + quality','V / I / G / T + calibration ID']),
 (468,31,382,174,'CALIBRATION',['PK: calibration revision','Reference instrument / uncertainty','Coefficients + validity period']),
 (911,31,382,174,'EVENT',['PK: event ID + revision','Node / window / condition state','Onset / alert / clear times']),
 (25,287,382,174,'EXPORT MANIFEST',['Window + timezone + units','Schema / filter / gap policy','File checksum + release context']),
 (468,287,382,174,'MAINTENANCE NOTE',['Operator / acknowledgement UTC','Inspection result + evidence','Correction / verified outcome']),
 (911,287,382,174,'CONFIGURATION',['Revision + scope + change author','Threshold / persistence / roles','Effective time + audit trail'])]
for x,y,w,h,head,body in items:block(s,x,y,w,h,head,body,T if y>250 else C,TL if y>250 else L,20)
s.line(408,117,467,117,C,1.8,arrow='arr');s.line(851,117,910,117,C,1.8,arrow='arr')
s.path('M1102 206 L1102 247 L659 247 L659 286',T,1.8,arrow='tarr')
save(s,'storage_model','Reference telemetry, calibration, event, maintenance and configuration relations')

flow('quality_states',[
 ('VALID',['Fresh measurement','Known units / range','Usable clock context']),
 ('DEGRADED',['Clock uncertain','Late / backfilled','Display with reason']),
 ('UNAVAILABLE',['Stale beyond policy','Missing / sensor fault','No healthy substitution']),
 ('RECOVERED',['Recheck identity / age','Do not join energy gaps','Expose recovery state'])],
 'Measurement-quality vocabulary and recovery requirements','Quality labels are an explicit operating contract, not green/red decoration.')

flow('alert_lifecycle',[
 ('QUALIFY',['Data valid / stable','Expected-power context','Residual exceeds gate']),
 ('PERSIST',['180 s initial target','Reset on false condition','Invalidity cannot count']),
 ('ALERT',['Emit identity + reason','Keep onset / alert time','Visible in all clients']),
 ('INSPECT / CLOSE',['Engineer acknowledges','Record inspection result','Clear by explicit policy'])],
 'Reference alert lifecycle and engineer-led maintenance','Acknowledgement does not prove the condition disappeared; the pilot does not switch plant equipment.')

flow('validation_pipeline',[
 ('HEALTHY / TUNING',['Fit baseline only here','Tune initial thresholds','Keep event groups intact']),
 ('LOCKED EVALUATION',['Chronological separation','Normal transient windows','Controlled anomaly cases']),
 ('EVENT METRICS',['TP / FP / FN definitions','Precision / recall','Qualifying alert latency']),
 ('RELEASE EVIDENCE',['Conditions + uncertainty','Raw records + timestamps','Review / disposition'])],
 'Reference event-level validation and leakage controls','Targets ≥90% precision and ≥85% recall are not measured achievements.')

# Security segmentation.
s=canvas(1320,475)
for x,w,head,body,fill in [(18,386,'SENSOR TRUST ZONE',['Node publishes scoped telemetry','No peer administration','Protect broker credentials'],L),(466,386,'LOCAL SERVICE ZONE',['Non-root application account','Read-only client data boundary','Separate shell administration'],TL),(914,386,'ENGINEER ACCESS',['Qt / website / app sessions','Authorized node / site scope','Audit acknowledgements'],L)]:
 block(s,x,43,w,205,head,body,T if fill==TL else C,fill,20)
for x in [405,853]:s.line(x+2,146,x+58,146,T,1.8,arrow='tarr')
s.rect(18,294,1282,127,AL,LINE,7)
s.text(39,328,'REVIEW BEFORE REMOTE EXPOSURE',22,A,700)
s.lines(39,362,['Transport protection, authorization, update provenance and recovery must be tested on the real deployment.','A monitoring client is not a plant-control endpoint; never expose the gateway shell as a public feature.'],19,G,maxw=1237)
save(s,'security_zones','Reference least-privilege boundaries and remote-access review gates')

flow('operator_journey',[
 ('BEGIN SHIFT',['Confirm site / node','Check time / quality','Review active events']),
 ('MONITOR',['Compare V / I / P / G / T','Use a common time window','Separate outage from fault']),
 ('INSPECT',['Acknowledge / prioritize','Use safe work permit','Record field observation']),
 ('HAND OVER',['Record outstanding actions','Export traceable evidence','Leave operating state clear'])],
 'Onsite engineer shift-to-handover workflow','No diagnosis from stale numbers alone; maintenance work follows site authorization.')

flow('backup_recovery',[
 ('CAPTURE',['Use consistent DB backup','Include WAL-aware method','Save config / calibration IDs']),
 ('VERIFY',['Checksum + schema revision','Open copy read-only','Verify time-window inventory']),
 ('RESTORE',['Isolated rehearsal first','Release / config compatible','Preserve source record IDs']),
 ('RECONCILE',['Compare counts / events','Check no replay duplicates','Record recovery evidence'])],
 'Reference consistent backup and recovery checks','Copying only an active SQLite main file is not a complete backup policy.')

flow('calibration_chain',[
 ('REFERENCE',['Instrument identity','Current calibration status','Uncertainty / range']),
 ('TEST SETUP',['Rated current-limited PSU','Reference connection review','Stable load / environment']),
 ('COMPARISON',['V / I / P test matrix','Error + repeatability','Shunt / cable temperature']),
 ('RECORD',['Coefficients / revision','Uncertainty + pass criterion','Raw as-found / as-left data'])],
 'Metrology evidence chain from reference to released coefficients','A programmed ADC scaling register is not evidence that this calibration occurred.')

flow('fault_isolation',[
 ('DEFINE SYMPTOM',['Which node / client?','Since which source time?','Missing, stale or invalid?']),
 ('LOCATE BOUNDARY',['Sensor / firmware','LAN / broker / ingest','Store / analysis / client']),
 ('CHECK SAFELY',['Read-only logs / status','Identity and clock context','No live-string probing']),
 ('VERIFY FIX',['Reproduce valid data','Check all clients / events','Save before / after evidence'])],
 'Boundary-oriented troubleshooting instead of indiscriminate restarts','A recovered display is not enough: verify source freshness and persisted identity.')

flow('release_contract',[
 ('PIN RELEASE',['OS / architecture','Runtime dependencies','Source / artifact checksum']),
 ('CHECK CONFIG',['Broker / storage access','Site / node / calibration','Permissions / secret source']),
 ('STAGE UPDATE',['Consistent backup','Isolated smoke tests','Explicit rollback point']),
 ('ACCEPT',['Qt / web / app agreement','Restart / offline behavior','Operator acceptance record'])],
 'Reference deployment-release controls for the existing software ecosystem','Service names, entry points, package versions and platform targets require the actual release manifest.')

flow('maker_progress',[
 ('FOUNDATION',['Solar monitoring scope','ESP32 / MQTT gateway','Monitoring-first safety']),
 ('ONSITE PLATFORM',['Ubuntu-based environment','Qt / PySide6 UI','Python backend built']),
 ('CONNECTED CLIENTS',['Website built','Companion app built','One monitoring ecosystem']),
 ('ENGINEERING HANDOFF',['Detailed documentation','Release / test evidence','Real prototype video'])],
 'Documented foundation and team-confirmed software milestones','Hardware calibration / field approval are separate from software implementation status.')

# Calculated plots use only explicit mathematical models or proposed test points.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.labelcolor':N,'text.color':N,'axes.edgecolor':'#A7BDCD','xtick.color':G,'ytick.color':G,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'path','grid.color':'#E2EAF1','axes.axisbelow':True})
def axnew(w=11,h=4.5):
 fig,ax=plt.subplots(figsize=(w,h));fig.patch.set_facecolor('white');ax.set_facecolor('white');ax.grid(True,alpha=.75);return fig,ax

def chart(fig,name,desc,basis):
 fig.tight_layout(pad=1.5);fig.savefig(OUT/(name+'.svg'),format='svg',bbox_inches='tight',facecolor='white');fig.savefig(OUT/(name+'.png'),dpi=170,bbox_inches='tight',facecolor='white');plt.close(fig);record(name,desc,basis)
def csvdata(name,headers,rows):
 with (DATA/(name+'.csv')).open('w',newline='') as f:
  w=csv.writer(f);w.writerow(headers);w.writerows(rows)

# Shunt transfer / dissipation.
i=np.linspace(0,5,101);v=i*.010*1000;p=i*i*.010
fig,ax=axnew();ax.plot(i,v,color=C,lw=2.8,label='V_shunt = I × 0.010 ohm');ax.set_xlabel('Current / A');ax.set_ylabel('Shunt voltage / mV')
a2=ax.twinx();a2.plot(i,p,color=T,lw=2.5,ls='--',label='P_shunt = I² × 0.010 ohm');a2.set_ylabel('Shunt dissipation / W',color=T);a2.set_ylim(0,.3);a2.spines['top'].set_visible(False)
ax.scatter([5],[50],color=C,s=40);ax.annotate('5 A → 50 mV / 0.25 W',(5,50),(-150,-30),textcoords='offset points',color=C)
ax.legend(loc='upper left');a2.legend(loc='lower right');csvdata('shunt_transfer',['basis','current_a','shunt_mv','shunt_power_w'],[['calculated',round(a,4),round(b,5),round(c,6)] for a,b,c in zip(i,v,p)])
chart(fig,'shunt_transfer','Calculated current-to-shunt-voltage and heating curves','Ohm/Joule laws; not measured calibration or thermal performance')

# Nominal pyranometer transfer.
g=np.linspace(0,1500,101);mv=.2*g;code=(mv/1000)/(.512/32768)
fig,ax=axnew();ax.plot(g,mv,color=C,lw=2.8);ax.set_xlabel('Irradiance / W m⁻²');ax.set_ylabel('Nominal sensor signal / mV');ax.scatter([800,1500],[160,300],color=T,s=40)
ax.annotate('800 W/m² → 160 mV',(800,160),(-130,30),textcoords='offset points',color=T);ax.annotate('0.2 mV per W/m²',(1100,220),(4,-45),textcoords='offset points',color=C)
csvdata('irradiance_transfer',['basis','irradiance_w_m2','nominal_mv','candidate_adc_code'],[['nominal calculated',round(a,3),round(b,3),round(c,3)] for a,b,c in zip(g,mv,code)])
chart(fig,'irradiance_transfer','Nominal SP-110-SS transfer and candidate ADC scaling','Manufacturer nominal sensitivity; calibration coefficient must come from the actual instrument')

# Power / energy example with explicit gap exclusion.
t=np.arange(0,601,5);power=75+8*np.sin(t/90);valid=~((t>=250)&(t<=320));shown=np.where(valid,power,np.nan)
fig,axes=plt.subplots(2,1,figsize=(11,6.3),sharex=True,gridspec_kw={'height_ratios':[2,1]})
axes[0].plot(t,shown,color=C,lw=2.5,label='Illustrative power profile');axes[0].fill_between(t,0,shown,color='#CCE6F1',alpha=.7);axes[0].axvspan(245,325,color='#F6DAB4',alpha=.7,label='Intervals without two valid endpoints');axes[0].set_ylabel('Power / W');axes[0].legend(loc='lower left');axes[0].grid(True)
energy=np.zeros(len(t))
for k in range(1,len(t)):energy[k]=energy[k-1]+((power[k-1]+power[k])/2*(t[k]-t[k-1])/3600 if valid[k-1] and valid[k] else 0)
axes[1].plot(t,energy,color=T,lw=2.5);axes[1].set_ylabel('Valid energy / Wh');axes[1].set_xlabel('Elapsed time / s');axes[1].grid(True)
csvdata('energy_gaps',['basis','elapsed_s','power_w','valid','valid_energy_wh'],[['illustrative calculated',int(a),round(b,6),bool(c),round(e,6)] for a,b,c,e in zip(t,power,valid,energy)])
chart(fig,'energy_gaps','Illustrative trapezoidal energy accumulation excluding unknown intervals','Calculated example, not plant telemetry or a meter-comparison result')

# Residual / persistence, known example event.
t=np.arange(0,481);r=np.where((t>=120)&(t<=360),.20,.03);r[(t>=50)&(t<75)]=.12;timer=np.zeros_like(t)
for k in range(1,len(t)):
 timer[k]=timer[k-1]+1 if (r[k]>.15 and r[k-1]>.15) else 0
fig,axes=plt.subplots(2,1,figsize=(11,6.1),sharex=True)
axes[0].plot(t,r*100,color=C,lw=2.5,label='Illustrative residual');axes[0].axhline(15,color=A,ls='--',lw=1.8,label='Initial 15% gate');axes[0].set_ylabel('Residual / %');axes[0].legend(loc='upper right');axes[0].grid(True)
axes[1].plot(t,timer,color=T,lw=2.6,label='Qualifying persistence');axes[1].axhline(180,color=A,ls='--');axes[1].axvline(300,color=T,ls=':',label='180 s reached at t=300 s');axes[1].set_ylabel('Persistence / s');axes[1].set_xlabel('Elapsed time / s');axes[1].legend(loc='upper left');axes[1].grid(True)
csvdata('residual_persistence',['basis','elapsed_s','residual_fraction','timer_s'],[['illustrative calculated',int(a),round(float(b),4),int(c)] for a,b,c in zip(t,r,timer)])
chart(fig,'residual_persistence','Illustrative qualifying residual and 180-second persistence','Reference algorithm timing; stable/valid irradiance assumed; not measured alert performance')

# Retention sizing assumptions.
days=np.arange(0,31);raw=10*200*86400*days/1e9
fig,ax=axnew()
for f,col,label in [(1,C,'Raw payload'),(1.5,T,'1.5× planning scenario'),(2,A,'2× planning scenario')]:ax.plot(days,raw*f,color=col,lw=2.4,label=label)
ax.set_xlabel('Retention / days');ax.set_ylabel('Decimal storage / GB');ax.legend(loc='upper left');ax.annotate('30 days raw = 5.184 GB',(30,5.184),(-210,-30),textcoords='offset points',color=C)
csvdata('retention_model',['basis','days','raw_gb','planning_1_5x_gb','planning_2x_gb'],[['calculated capacity model',int(d),round(x,6),round(x*1.5,6),round(x*2,6)] for d,x in zip(days,raw)])
chart(fig,'retention_model','Raw ten-node retention and explicitly assumed overhead scenarios','10 nodes × 200 B × 1 Hz; overhead factors are not SQLite benchmark results')

# Planned V/I calibration matrix, all cells are power setpoint arithmetic.
vs=[12,18,24];cs=[.5,1,2,4,5];fig,ax=axnew(11,4.6)
for y,vv in enumerate(vs):
 for x,ii in enumerate(cs):
  pw=vv*ii;ax.add_patch(Rectangle((x-.46,y-.43),.92,.86,facecolor=plt.cm.Blues(.15+.65*pw/120),edgecolor='white',lw=2));ax.text(x,y,f'{pw:g} W',ha='center',va='center',color='white' if pw>65 else N,fontsize=14,fontweight='bold')
ax.set_xlim(-.6,4.6);ax.set_ylim(-.6,2.6);ax.set_xticks(range(5),[str(x) for x in cs]);ax.set_yticks(range(3),[str(x) for x in vs]);ax.set_xlabel('Planned current / A');ax.set_ylabel('Planned voltage / V');ax.grid(False)
csvdata('calibration_matrix',['basis','voltage_v','current_a','calculated_load_w'],[['planned test point',v,i,v*i] for v in vs for i in cs])
chart(fig,'calibration_matrix','Planned bench test-point matrix with calculated load power','Test plan only; cells are P=VI, not calibration errors or passed test results')

# Thermal requirement model.
a=np.arange(20,56);theta=(65-a)/3
fig,ax=axnew();ax.plot(a,theta,color=C,lw=2.7);ax.scatter([45],[20/3],color=T,s=55);ax.axvline(45,color=T,ls=':');ax.axhline(20/3,color=T,ls=':');ax.set_xlabel('Ambient temperature / °C');ax.set_ylabel('Maximum effective thermal resistance / °C W⁻¹');ax.annotate('45 °C → ≤6.67 °C/W',(45,20/3),(-220,35),textcoords='offset points',color=T)
csvdata('thermal_budget',['basis','ambient_c','interior_limit_c','dissipation_w','maximum_theta_c_w'],[['calculated requirement',int(x),65,3,round(y,6)] for x,y in zip(a,theta)])
chart(fig,'thermal_budget','Calculated thermal-resistance requirement for a 65 °C interior target','3 W steady dissipation; direct solar loading excluded; not a thermal test')

# Budget: exact published planning estimates, no vendor verification.
with (DATA/'proposed_bom.csv').open() as f:rows=list(csv.DictReader(f))
labels=[r['Component'] for r in rows];cost=[int(r['Estimated line INR'].replace(',','')) for r in rows];order=np.argsort(cost)
fig,ax=axnew(11,6.7);ax.barh(np.arange(len(rows)),np.array(cost)[order]/1000,color=[T if cost[k]>=10000 else C for k in order]);ax.set_yticks(np.arange(len(rows)),[labels[k] for k in order]);ax.set_xlabel('Estimated line cost / thousand INR');ax.grid(axis='y',visible=False)
for pos,k in enumerate(order):ax.text(cost[k]/1000+.2,pos,f'₹{cost[k]:,}',va='center',fontsize=10)
ax.set_xlim(0,39)
chart(fig,'budget_breakdown','Proposed BOM line costs with the shared irradiance reference','Planning prices only; subtotal ₹46,700, contingency total ₹56,040')

# Modeled wait comparison and proposed target budget.
fig,axes=plt.subplots(1,2,figsize=(12,4.6),gridspec_kw={'width_ratios':[1.1,1]})
axes[0].barh(['Inspection model','Qualifying-event target'],[7200,210],color=[C,T]);axes[0].set_xscale('log');axes[0].set_xlabel('Wait / s (logarithmic scale)');axes[0].grid(axis='x');axes[0].text(7200,0,' 2 h',va='center');axes[0].text(210,1,' 210 s',va='center');axes[0].set_xlim(1,15000)
axes[1].barh([0],[180],color=C,label='Persistence: 180 s');axes[1].barh([0],[30],left=[180],color=T,label='Processing/transport margin: 30 s');axes[1].set_yticks([]);axes[1].set_xlabel('Target qualifying alert budget / s');axes[1].set_xlim(0,230);axes[1].legend(loc='upper center',bbox_to_anchor=(.5,-.19),fontsize=9);axes[1].grid(axis='x')
csvdata('latency_model',['basis','metric','seconds'],[['illustrative calculated','mean manual wait',7200],['design target','qualifying visible alert',210],['reference policy','persistence',180],['assumed allocation','other path allowance',30]])
chart(fig,'latency_model','Illustrative inspection wait comparison and 210-second design budget','97.08% modeled wait reduction is not measured yield recovery')

# Persist human-readable technical figure registry.
(OUT/'figure_registry.json').write_text(json.dumps(FIGURES,indent=2))
with (DATA/'figure_index.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['name','svg','png','description','basis']);w.writeheader();w.writerows(FIGURES)
print('Documentation figures:',len(FIGURES),'(SVG + PNG each)')
