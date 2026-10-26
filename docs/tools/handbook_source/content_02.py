from doc_engine import c,event_table,mermaid
import json

x=c('Companion App','companion-app')
x.p('The companion app is a team-confirmed part of the monitoring ecosystem. It extends access to engineering context; it is not evidence of a particular mobile operating system, notification provider, packaging format or app-store release. Those details must be published from the actual app build rather than inferred from the word “app”.')
x.table(['App concern','Required behavior','Release detail to supply'],[
('Identity','Show the selected site, zone and node','Approved navigation and account scope'),
('Freshness','Distinguish source age from phone/network connection','Refresh policy and data-age computation'),
('Quality','Carry invalid/stale/environmental-gate meaning','Supported state mapping and accessible indicators'),
('Events','Preserve event ID, condition and revision','Acknowledgement capability and authorization rules'),
('Connectivity','Show disconnection without inventing live values','Actual caching and reconnect policy'),
('History','Preserve time window, timezone and gaps','Supported trend/history scope'),
('Security','Protect session material and minimize local retention','Actual storage, session-expiry and logout behavior'),
('Distribution','Identify the real build and supported platform','Signed artifact or approved installation instructions')])
x.h('Mobile interpretation checks')
event_table(x,[('The app reconnects after a long outage','First distinguish historical backfill from a current observation','Source time, receive time and displayed freshness'),('A user acknowledges an event','Apply only the released authorization/workflow contract','Actor, event identity, action time and next revision'),('The phone changes timezone','Preserve UTC identity; relabel display time clearly','Same source record in both timezone views'),('An app process is suspended','Do not imply continuous receipt from a foreground-only session','App lifecycle and last-confirmed update indication'),('A cached screen opens without access','Mark it offline/last known and show its time','Cache state and exact stored observation time'),('Another client changes event workflow','Reconcile event revision rather than overwriting blindly','Conflict/revision outcome')])
x.p('An engineer should not need to guess whether a red indicator means a plant condition, a sensor issue, a stale cache or an expired session. The app must name the category and preserve the route back to the underlying event or observation. If push notifications are part of a later published release, they must carry identity and source/event time; this handbook does not claim that push has already been implemented.')
x.h('App publication record')
x.table(['Field','Value to obtain from the team'],[
('Platform target','Actual supported OS/device families'),
('Build identifier','App release/version and backend compatibility'),
('Install artifact','Approved signed build or distribution link'),
('Access method','Actual approved connection and authentication path'),
('Offline behavior','What is cached, for how long and with which quality indication'),
('Local data policy','Retention, logout clearing and export scope'),
('Event capability','View-only, acknowledgement or additional approved workflow'),
('Support route','Owner and reproducible issue-report procedure')])

x=c('Shared Monitoring Workflow','shared-workflow')
x.fig('ecosystem_workflow','Observation → validation → context → engineer inspection → recorded outcome. A diagnostic event informs human action; it does not authorize switching.')
x.procedure('One observation, several clients',[
 'A sensor node acquires the approved channels and records conversion/clock status.',
 'Firmware packages the observation with stable node identity, boot identity and sequence.',
 'The message crosses the transport boundary; delivery can be retried or replayed.',
 'The gateway validates schema, units, ranges, time and identity before accepting the record.',
 'Persistence records the transaction outcome without counting duplicate delivery twice.',
 'Qualified V/I produce power, while valid neighboring observations determine energy increments.',
 'Analysis evaluates expected output only when the environmental and data-quality gates allow it.',
 'The event engine separates observation condition, persistence, notification and human workflow.',
 'Qt, website and app present compatible identity, units, freshness and event revision.',
 'The engineer inspects within an approved work scope and records the physical finding.',
 'Post-action monitoring establishes whether the condition actually cleared.',
 'The outcome becomes future review context, not a retroactive rewrite of raw measurements.'])
x.h('Cross-client consistency fixture')
x.p('The following values are arithmetic/UI fixtures, not recorded plant data. A release review can inject an equivalent controlled fixture through an approved test interface and compare what each client renders. Do not insert it into operational history as if it were a real observation.')
x.table(['Field','Illustrative fixture','Consistency rule'],[
('Node','bench-node-01','Exactly the same selected identity'),
('Voltage','21.6 V','No implicit kV or different measurement point'),
('Current','3.20 A','Precision and unit explained'),
('Calculated power','69.12 W','21.6 × 3.20 on every surface'),
('Expected power','88.3 W','Same model/configuration revision'),
('Shortfall','21.72% before display rounding','(88.3 − 69.12) / 88.3'),
('Irradiance','800 W/m²','Radiometric context, not lux'),
('Panel temperature','45 °C','Sensor/mounting context retained'),
('Illustrative accumulated energy','0.280 kWh','Same integration window and exclusions'),
('Quality','Valid fixture','Same freshness and validity semantics'),
('Event','Reference persistent shortfall event','Same ID, onset and revision')])
x.h('Read versus action permissions')
x.table(['Operation','Monitoring permission','Additional gate'],[
('View recent telemetry','Approved read scope','Correct site/node authorization'),
('Read history','Approved retention/window scope','Export/privacy policy'),
('Acknowledge an event','Explicit workflow permission','Actor/time/event revision'),
('Record an inspection finding','Authorized maintenance workflow','Traceable note and physical outcome'),
('Change threshold or calibration','Not a routine view operation','Controlled configuration change'),
('Restart services or alter OS','Not a browser/app monitoring right','Approved administrator procedure'),
('Switch PV equipment','Outside the demonstrator','Separate certified control and work authorization')])
x.p('A client is consistent when it preserves engineering meaning, not when every pixel is identical. Rounding, chart aggregation and screen density may differ, but raw identity, quality, unit, event state and effective configuration cannot silently diverge.')

x=c('Hardware Sensing Plan','hardware-sensing')
x.p('The primary submission uses an ESP32-S3 sensing node for voltage, current, irradiance, temperature and relevant environmental/inverter context. The part-level design here is a proposed low-voltage reference implementation. It is not a claim of fabricated PCB, measured calibration or certified plant installation.')
x.table(['Channel','Proposed element','Engineering quantity','Important boundary'],[
('Voltage/current','INA226 plus 10 milliohm Kelvin shunt','DC bus V; shunt-derived A','INA226 bus rating is 36 V, not a PV string interface'),
('Irradiance','SP-110-SS pyranometer plus ADS1115','W/m² from calibration sensitivity','A lux sensor is not an equivalent substitute'),
('Panel temperature','Powered three-wire DS18B20','°C at a documented mounting point','Air temperature is not automatically module temperature'),
('Controller','ESP32-S3 DevKitC-1 reference','Acquisition, identity and transport','Separate from the Ubuntu engineering gateway'),
('Optional node battery','Appropriately scaled voltage channel','Node supply/battery diagnostic','Not plant battery SOC or pack protection'),
('Inverter/environment data','Approved read-only interface if available','Relevant operating context','Vendor mapping and electrical interface must be reviewed')])
x.h('Proposed operating envelope')
x.table(['Parameter','Reference / target','What is not claimed'],[
('Bench DC input','12–24 V nominal','Permission to connect at a plant string voltage'),
('Bench current','0–5 A; targets evaluated above 0.5 A','Verified operation under fault or reverse-current conditions'),
('Maximum planned load point','24 V × 5 A = 120 W','A load rating certified by this document'),
('Irradiance analysis range','0–1500 W/m² target','Accuracy through every spectral/angular condition'),
('Temperature characterization','−10 to 85 °C target window','Enclosure operation throughout the sensor\'s absolute range'),
('Acquisition cadence','1 Hz reference target','Measured end-to-end timing'),
('Voltage/current error','≤1% target above 0.5 A, after calibration','The INA226 IC accuracy as total assembly accuracy'),
('Power error','≤2% target after calibration','A completed system-accuracy test')])
x.h('Acquisition coherence')
x.p('Power is meaningful when V and I describe the same operating state. Record conversion timing and the maximum acceptable pairing interval. Slow temperature conversion must not block the complete node loop; temperature may have its own acquisition timestamp/age. If a channel is missing, mark that channel missing rather than using a previous reading without age context.')
x.table(['Failure source','Observable symptom','Design response'],[
('Loose Kelvin lead','Current offset/noise not explained by load','Separate sense and load paths; inspect polarity and contact'),
('Wrong ADC gain','Irradiance clipping or scale error','Record gain/range in calibration context'),
('Temperature sensor CRC failure','Untrustworthy digital conversion','Flag invalid and retain diagnostic status'),
('Sensor shade/soiling','Low irradiance reference independent of plant condition','Inspect reference mounting and maintenance'),
('I²C pull-up/rise-time issue','Timeouts or intermittent conversion reads','Check both isolated bus domains and compatible low levels'),
('Supply dropout','Node reboot or changing measurements','Review regulation, startup/current demand and boot identity'),
('Clock not synchronized','Unknown absolute source time','Retain monotonic uptime and explicit clock status')])
x.h('Evidence required before assembly release')
x.bullets(['Pin-accurate schematic, net names, connector polarity and component orderable suffixes.','Actual board layout, creepage/clearance review and power-domain isolation inspection.','Bench setup diagram with current-limited source, rated load, reference meter and safe disconnect.','Calibration record covering coefficients, reference uncertainty, date, temperature and applicable channel range.','Firmware/configuration revisions used for every acceptance run.','Photographs of the actual assembly and wiring, clearly separate from drawings or CAD renders.'],check=True)

x=c('Electrical Connections and Register Calculations','electrical')
x.fig('electrical_connections','Proposed pin-referenced sensing connection for the low-voltage bench. It is a documentation schematic, not a routed EDA design or permission for plant wiring.')
x.h('Signal and address allocation')
x.table(['Signal','Proposed connection','Review note'],[
('I²C SDA','ESP32-S3 GPIO8','Verify exact DevKit variant and board multiplexing'),
('I²C SCL','ESP32-S3 GPIO9','Pull-up/rise-time review on each isolated side'),
('INA226','Address 0x40','A0/A1 low to the measured-domain ground'),
('ADS1115','Address 0x48','ADDR low to controller-domain ground'),
('Pyranometer','SP-110-SS output to ADS1115 AIN0','Use sensor calibration and correct return connection'),
('Temperature data','DS18B20 DQ to GPIO4','Powered three-wire mode, proposed 4.7 kohm pull-up'),
('INA ALERT','Optional; not routed in this concept','Do not imply a wired interrupt that is not shown'),
('ESP32-S3 GPIO35–37','Avoid in proposed N8R8 reference','May be reserved by module PSRAM variant')])
x.h('INA226DGS pin reference')
x.table(['Pin','Name','Proposed connection'],[
(1,'A1','GND_ISO; selects reference address'),(2,'A0','GND_ISO; selects reference address'),(3,'ALERT','Optional diagnostic output; not routed here'),(4,'SDA','Isolated I²C measured side'),(5,'SCL','Isolated I²C measured side'),(6,'VS','3V3_ISO with local decoupling'),(7,'GND','GND_ISO'),(8,'VBUS','Monitored bus voltage sense'),(9,'IN−','Kelvin shunt low-side sense'),(10,'IN+','Kelvin shunt high-side sense')])
x.h('ISO1540 pin reference')
x.table(['Pin','Name','Proposed connection'],[
(1,'VCC1','3V3_CTRL'),(2,'SDA1','Controller-side SDA'),(3,'SCL1','Controller-side SCL'),(4,'GND1','GND_CTRL'),(5,'GND2','GND_ISO'),(6,'SCL2','Measured-side SCL'),(7,'SDA2','Measured-side SDA'),(8,'VCC2','3V3_ISO')])
x.p('ISO1540 side 1 has an offset-low behavior that must be checked against the controller and connected device low-level thresholds. Add the manufacturer-recommended local bypass capacitors and verify pull-ups and bus capacitance on each side. Component-level isolation data does not establish the safe working voltage of the complete assembly.')
x.h('ADS1115DGS pin reference')
x.table(['Pin','Name','Proposed connection'],[
(1,'ADDR','GND_CTRL for 0x48'),(2,'ALERT/RDY','Optional conversion-ready; not required by this concept'),(3,'GND','GND_CTRL'),(4,'AIN0','Pyranometer positive output'),(5,'AIN1','Unused input handled according to reviewed configuration'),(6,'AIN2','Unused input handled according to reviewed configuration'),(7,'AIN3','Unused input handled according to reviewed configuration'),(8,'VDD','3V3_CTRL with local bypass'),(9,'SDA','Controller-side SDA'),(10,'SCL','Controller-side SCL')])
x.h('Shunt and INA226 register arithmetic')
x.code('text', '''R_shunt = 10 milliohm = 0.010 ohm
I_max = 5 A
V_shunt_max = I_max × R_shunt
            = 5 × 0.010 = 0.050 V = 50 mV
P_shunt_max = I_max² × R_shunt
            = 25 × 0.010 = 0.25 W
Proposed shunt nominal rating = at least 1 W
Nominal dissipation / rating = 0.25 / 1 = 25%

INA226 shunt register LSB = 2.5 microvolt
Selected current_LSB = 0.00025 A per count
CAL = 0.00512 / (current_LSB × R_shunt)
    = 0.00512 / (0.00025 × 0.010)
    = 2048 decimal = 0x0800
Power register LSB = 25 × current_LSB
                   = 0.00625 W per count
At 5 A, nominal current count = 20000
At 50 mV, nominal shunt count = 20000''')
x.fig('shunt_transfer','Calculated 10 milliohm shunt voltage and dissipation from 0 to 5 A. No measured shunt temperatures or current-error results are shown.')
x.p('The register calibration value establishes numeric scaling; it is not physical calibration of the assembled current path. Real uncertainty includes shunt tolerance and temperature coefficient, Kelvin routing, ADC/gain offset, reference instrumentation and operating conditions. Check signed-register handling, conversion-ready behavior, saturation and the actual configured averaging/conversion time.')
x.h('Electrical review checklist')
x.bullets(['Verify package orientation against the actual manufacturer drawing; do not wire from a top/bottom view assumption.','Separate load-current conductors from Kelvin sense conductors at the shunt terminals.','Protect the source/load path using the approved bench arrangement; a monitoring IC is not a fuse.','Check bus voltage against IC maximum conditions and the smaller approved demonstration envelope.','Inspect isolated return nets and all temporary USB, debugger and oscilloscope connections.','Do not connect a grounded probe across an intended isolation barrier without an approved measurement arrangement.','Confirm unused inputs, test points and exposed conductors are handled before energizing.'],check=True)

x=c('Power Domains and Sensor Conversion Chains','power-domains')
x.fig('power_domains','External 5 V powers the controller branch and a separately regulated isolated branch. GND_CTRL and GND_ISO must not be bridged by unintended wiring.')
x.p('The proposed external source is regulated 5 V. One branch supplies the DevKit controller-side regulator and controller-domain sensors. A second branch uses a B0505S-1WR3 isolated 5 V/5 V converter followed by a TLV76033 regulator for the isolated 3.3 V measurement domain. The B0505S output is unregulated; it is not treated as a precision 5 V rail.')
x.table(['Domain / element','Reference value','Required review'],[
('External source','Regulated 5 V','Peak current, protection, current limit and safe disconnect'),
('Controller rail','3V3_CTRL from reviewed DevKit path','Actual board regulator, Wi-Fi transient current and GPIO limits'),
('Isolated converter','B0505S-1WR3, nominal 1 W','Load range, regulation, startup, ripple and thermal behavior'),
('Isolated LDO','TLV76033, 3.3 V, 100 mA rating','Input headroom, dropout, stability and heat'),
('INA226 domain','3V3_ISO / GND_ISO','Bypass and safe sensing common-mode conditions'),
('ISO1540 sides','Separate VCC/GND pairs','No accidental return bridge'),
('ADS1115/DS18B20','Controller-side supply and return','Input range and routing'),
('External instrumentation','May be earth-referenced','USB/debug/probe paths must be reviewed')])
x.code('text', '''Reference LDO heat estimate:
    P_LDO ≈ (V_in − V_out) × I_out
For an illustrative 5.0 V input and 30 mA load:
    P_LDO ≈ (5.0 − 3.3) × 0.030 = 0.051 W
This is not a measured isolated-domain load.
Use worst-case converter voltage and actual current for release.
Check LDO dropout and minimum headroom at the low-input condition.
Check device temperature and startup under the real enclosure load.''')
x.h('Pyranometer conversion')
x.fig('irradiance_chain','Radiometric sensor → ADC conversion → calibrated W/m² with range, quality and mounting context.')
x.p('The SP-110-SS is a passive pyranometer, not a general ambient-light sensor. Its nominal sensitivity is 0.2 mV per W/m², equivalent to 5 W/m² per mV; use the actual sensor calibration coefficient when supplied. Its published output range reaches about 400 mV. Orientation, cleanliness, horizon/shading, cosine response and spectral conditions affect the meaning of a site measurement.')
x.code('text', '''Nominal irradiance conversion:
    G_W_m2 = sensor_output_mV / 0.2
Example arithmetic:
    800 W/m² → 160 mV
    1000 W/m² → 200 mV
    1500 W/m² → 300 mV
Reference ADS1115 PGA choice:
    full_scale = ±0.512 V
    voltage_LSB = 0.512 / 32768 V = 15.625 microvolt
    nominal irradiance_LSB = 0.015625 mV / 0.2
                           = 0.078125 W/m²
The numeric LSB is not system irradiance accuracy.
Input common-mode and absolute pin limits still apply.''')
x.fig('irradiance_transfer','Calculated nominal pyranometer/ADC transfer. Quantization is not a substitute for calibration, mounting review or sensor uncertainty.')
x.h('Temperature and optional supply sensing')
x.table(['Item','Reference handling','Reason'],[
('DS18B20 mode','Powered three-wire rather than assuming parasite-power support','Avoids an unstated conversion-power arrangement'),
('Conversion time','Up to 750 ms at 12-bit per datasheet','Schedule conversion without blocking the complete loop'),
('Integrity','Check CRC and conversion completion','A digital response is not automatically a valid temperature'),
('Mounting','Document panel contact, adhesive/insulation and location','Module temperature differs from surrounding air'),
('Known device accuracy','±0.5 °C in the stated −10 to 85 °C range','Do not extend that claim across the entire absolute range'),
('Optional battery channel','Only with reviewed scaling/reference and chemistry context','Node battery voltage is not a validated SOC estimate')])

x=c('ESP32-S3 Firmware Reference','firmware')
x.fig('firmware_cycle','Proposed one-second acquisition/publish cycle. Exact firmware task layout and shipped release are not available in the inspected repository.')
x.p('Firmware is responsible for truthful observation identity and channel status before networking is considered. The node should not publish a normal number simply because a conversion failed or a buffer was empty. Keep sensor acquisition, conversion state, clock state, record assembly and delivery outcome separately inspectable.')
x.h('Reference task responsibilities')
x.table(['Task','Responsibility','Failure handling'],[
('Boot/configuration','Load node identity and applicable calibration/configuration','Enter a named fault/degraded state if required data is absent'),
('Clock/uptime','Maintain monotonic timing and UTC-quality context','Retain clock uncertainty, never invent a source UTC'),
('Electrical sampling','Obtain compatible V/I conversions and status','Flag timeout/saturation/misaligned pairs'),
('Environment sampling','Schedule irradiance and temperature reads','Preserve age and channel quality'),
('Record assembly','Produce one immutable identity/envelope','Do not mutate a record during retry'),
('Local queue','Bound pending records and preserve ordering policy','Count overflow/loss rather than claiming unlimited buffering'),
('MQTT publishing','Connect, publish and observe acknowledgement state','Use bounded retry/backoff and explicit reconnect state'),
('Health/reporting','Expose reboot, queue and channel diagnostics','Separate a healthy transport from valid measurements')])
x.h('Reference cycle pseudocode')
x.code('text', '''on boot:
    establish a new boot identity
    load and validate node/configuration/calibration identity
    initialize sensors and monotonic scheduler
    mark source UTC unsynchronized until qualified
    initialize bounded pending-record queue

at each one-second acquisition deadline:
    record monotonic observation time
    read electrical conversion pair and conversion status
    collect irradiance conversion and sensor status
    collect completed temperature conversion if available
    preserve age of any independently sampled channel
    evaluate channel range/status without hiding raw errors
    build immutable record with boot identity and sequence
    attach UTC only with its clock-quality state
    enqueue or record an explicit overflow/loss outcome
    increment sequence within the defined wrap policy
    schedule the next temperature conversion as needed

network worker:
    connect with approved identity/credentials
    subscribe only if required by the reviewed firmware contract
    publish according to bounded queue/retry policy
    observe delivery state without declaring persistence complete
    retain source identity when retransmitting
    report backlog and reconnect state

watchdog / supervisor:
    check task progress rather than merely network traffic
    preserve reset reason where the platform supports it
    avoid retry loops that starve acquisition
    establish a new boot identity after a genuine reboot''')
x.h('Firmware acceptance cases')
event_table(x,[('Power-on without network','Acquire/label local status under the approved buffer policy','Boot ID, clock status and queue outcome'),('Temperature conversion still pending','Do not block all channels or label old data new','Per-channel time/age and conversion state'),('Sensor unplugged','Publish missing/invalid status where transport permits','Channel reason and no fabricated zero'),('MQTT reconnect','Replay preserves immutable keys and source time','Sequence inventory and duplicate outcome'),('Queue reaches capacity','Apply documented loss/backpressure policy','First/last retained sequence and overflow count'),('Sequence limit reached','Use reviewed wrap/epoch policy','No duplicate key across the transition'),('Clock obtains UTC after startup','Preserve prior unsynchronized records honestly','Before/after time-quality states'),('Watchdog resets controller','New boot identity and reset context','No collision with the previous boot sequence')])
x.p('A 600-record buffer at 1 Hz represents ten minutes only when every acquisition produces one record and all 600 slots are available to that node. Payload size, overhead, persistence and power-loss behavior must be tested on the actual hardware. “Buffer target” does not imply durable flash-backed recovery.')

x=c('MQTT Transport, Replay and Offline Behavior','mqtt')
x.fig('mqtt_replay','Reference QoS 1 redelivery path: a duplicate delivery must not duplicate a committed record or energy contribution.')
x.p('MQTT is the node-to-gateway messaging architecture in the primary project source. QoS 1 permits duplicate delivery; it does not provide an exactly-once database transaction. The system therefore needs an application identity and an idempotent persistence policy. The precise broker, TLS/credential provisioning and web/app transport remain release details.')
x.h('Reference topic contract')
x.code('text', '''# Proposed topic namespace; not an exposed deployment endpoint.
arka/v1/sites/{site_id}/nodes/{node_id}/telemetry
arka/v1/sites/{site_id}/nodes/{node_id}/health

# Example documentation scope, not an actual live site.
arka/v1/sites/bench-site/nodes/bench-node-01/telemetry

# Topic identifiers must match payload identity.
# Do not permit arbitrary topic path segments from unvalidated input.
# Plant switching/control topics are outside this demonstrator.
# A retained last-value record is still subject to source-age checks.''')
x.table(['Transport setting','Reference policy','Verification'],[
('Telemetry QoS','QoS 1 proposed','Duplicates and reconnect behavior tested explicitly'),
('Record identity','node_id + boot_id + seq','Unique committed key and collision review'),
('Cadence','1 Hz target','Measured source interval and client age'),
('Freshness','Stale after >5 s, assuming qualified source time','Timeout with controlled current-time/clock state'),
('Queue','600 records per node reference target','Capacity, loss and reset durability tests'),
('Reconnect','Bounded backoff with observable state','No unbounded queue or CPU/network storm'),
('Retained delivery','Never inherently fresh','Source-time and session/availability semantics'),
('Credentials','Per approved provisioning and least privilege','No public secret in README or example payload'),
('WAN failure','Local path should remain useful when LAN/services survive','Separate WAN-only test from full network failure')])
x.h('Replay decisions')
event_table(x,[('Same immutable key and same body','Treat as duplicate delivery','One committed row; no duplicate metric increment'),('Same key but different body','Flag identity/collision fault; do not silently overwrite','Both candidate hashes and decision reason'),('New key with older source time','Apply backfill policy and preserve source time','Historical insertion position and analysis policy'),('Sequence gap','Record missing interval; do not infer zero generation','Gap bounds and affected integration time'),('Backlog overtakes live traffic','Use defined scheduling/backpressure policy','Live age plus backlog depth'),('Broker acknowledgement received','Delivery success only, not guaranteed DB commit','Separate publish and writer outcomes'),('Gateway restarts during replay','Recover idempotently from committed state','Before/after key inventory'),('Old retained sample arrives on connect','Evaluate age and clock quality before live display','Source/receive time distinction')])
x.code('python', '''# Reference idempotency concept, not the released backend.
def record_key(payload):
    source = payload["source"]
    return (
        source["node_id"],
        source["boot_id"],
        source["seq"],
    )

def handle_redelivery(writer, payload):
    key = record_key(payload)
    outcome = writer.insert_if_absent(key, payload)
    if outcome == "inserted":
        return "committed_new_record"
    if outcome == "same_record_exists":
        return "duplicate_delivery"
    if outcome == "key_body_conflict":
        return "identity_fault"
    return "persistence_failure"''')
x.p('Clock uncertainty limits age claims. With synchronized clocks, compare source UTC against the qualified gateway clock and report the accepted uncertainty. Without that basis, gateway receive time can describe arrival age but cannot establish the age of the physical observation during backlog replay. Preserve monotonic node uptime and clock status rather than pretending otherwise.')

x=c('Telemetry Schema and Data Contracts','telemetry')
x.fig('telemetry_contract','Reference envelope groups identity, measurements, time and quality. The built release must publish its actual schema and compatibility policy.')
x.p('The following schema is a proposed interoperability contract for documentation and tests. It does not assert that the unpublished implementation already uses these exact keys. It makes units and identity explicit, supports missing measurements with null, and avoids representing a failed sensor as zero. Domain plausibility and calibration checks are additional semantic steps after structural validation.')
x.h('Field dictionary')
x.table(['Path','Type','Meaning / constraint'],[
('schema_version','string','Envelope version; reference value 1.0'),
('message_type','string','Reference telemetry record type'),
('source.site_id','identifier','Approved site scope; must match topic'),
('source.zone_id','identifier','Physical/logical zone; documented mapping'),
('source.node_id','identifier','Stable node identity; must match topic'),
('source.boot_id','string','New identity for each actual node boot'),
('source.seq','integer','Monotonic within a boot under defined wrap policy'),
('time.source_utc','RFC 3339 string or null','Observation UTC, not gateway receipt time'),
('time.uptime_ms','integer','Monotonic node uptime in milliseconds'),
('time.clock_status','enum','synced, uncertain or unsynced'),
('measurements.voltage_v','number or null','Monitored DC bus voltage'),
('measurements.current_a','number or null','Signed current; approved bench direction checked semantically'),
('measurements.irradiance_w_m2','number or null','Radiometric irradiance, not lux'),
('measurements.panel_temperature_c','number or null','Documented panel sensor temperature'),
('quality.channel_status','object','Independent status for each required channel'),
('calibration_id','string','Applicable coefficient/reference record'),
('firmware_revision','string','Actual firmware release identity'),
('gateway.receive_utc','gateway-added metadata','Arrival UTC; not supplied as source observation time'),
('gateway.ingest_outcome','gateway-added metadata','Accepted, duplicate, rejected or quarantined'),
('gateway.config_revision','gateway-added metadata','Policy used for validation and derived context')])
x.h('Complete reference JSON Schema')
schema={
 '$schema':'https://json-schema.org/draft/2020-12/schema',
 '$id':'urn:arka:reference:telemetry:1.0',
 'title':'ARKA reference telemetry envelope',
 'description':'Reference contract, not a published implementation schema.',
 'type':'object','additionalProperties':False,
 'required':['schema_version','message_type','source','time','measurements','quality','calibration_id','firmware_revision'],
 'properties':{
  'schema_version':{'const':'1.0'},'message_type':{'const':'telemetry'},
  'source':{'type':'object','additionalProperties':False,'required':['site_id','zone_id','node_id','boot_id','seq'],'properties':{
   'site_id':{'$ref':'#/$defs/identifier'},'zone_id':{'$ref':'#/$defs/identifier'},'node_id':{'$ref':'#/$defs/identifier'},
   'boot_id':{'type':'string','minLength':8,'maxLength':64},'seq':{'type':'integer','minimum':0,'maximum':4294967295}}},
  'time':{'type':'object','additionalProperties':False,'required':['source_utc','uptime_ms','clock_status'],'properties':{
   'source_utc':{'anyOf':[{'type':'string','format':'date-time'},{'type':'null'}]},
   'uptime_ms':{'type':'integer','minimum':0,'maximum':9007199254740991},
   'clock_status':{'enum':['synced','uncertain','unsynced']}}},
  'measurements':{'type':'object','additionalProperties':False,
   'required':['voltage_v','current_a','irradiance_w_m2','panel_temperature_c'],
   'properties':{
    'voltage_v':{'type':['number','null'],'minimum':0,'maximum':36},
    'current_a':{'type':['number','null'],'minimum':-5,'maximum':5},
    'irradiance_w_m2':{'type':['number','null'],'minimum':0,'maximum':2000},
    'panel_temperature_c':{'type':['number','null'],'minimum':-55,'maximum':125}}},
  'quality':{'type':'object','additionalProperties':False,'required':['channel_status'],'properties':{
   'channel_status':{'type':'object','additionalProperties':False,'required':['voltage','current','irradiance','panel_temperature'],'properties':{
    'voltage':{'$ref':'#/$defs/channelStatus'},'current':{'$ref':'#/$defs/channelStatus'},'irradiance':{'$ref':'#/$defs/channelStatus'},'panel_temperature':{'$ref':'#/$defs/channelStatus'}}}}},
  'calibration_id':{'type':'string','minLength':1,'maxLength':64},
  'firmware_revision':{'type':'string','minLength':1,'maxLength':64}},
 '$defs':{
  'identifier':{'type':'string','minLength':1,'maxLength':48,'pattern':'^[A-Za-z0-9][A-Za-z0-9_-]*$'},
  'channelStatus':{'enum':['valid','invalid','missing','uncertain','out_of_range']}}}
x.code('json',json.dumps(schema,indent=2))
x.p('The numeric schema bounds are structural guardrails, not permission to energize outside the 12–24 V bench envelope. In particular, a physically impossible or out-of-characterized-range value needs a semantic decision even if its JSON type and broad device range are valid. Validate null/status agreement: a missing value cannot simultaneously be advertised as a valid measurement. Enable format checking explicitly in validators that treat date-time as annotation by default.')
x.h('Valid-value documentation fixture')
fixture={'schema_version':'1.0','message_type':'telemetry','source':{'site_id':'bench-site','zone_id':'zone-a','node_id':'bench-node-01','boot_id':'documentation-boot-01','seq':100},'time':{'source_utc':'2026-01-01T00:00:00Z','uptime_ms':100000,'clock_status':'synced'},'measurements':{'voltage_v':21.6,'current_a':3.2,'irradiance_w_m2':800.0,'panel_temperature_c':45.0},'quality':{'channel_status':{'voltage':'valid','current':'valid','irradiance':'valid','panel_temperature':'valid'}},'calibration_id':'REFERENCE-ONLY','firmware_revision':'REFERENCE-ONLY'}
x.code('json',json.dumps(fixture,indent=2))
x.h('Missing-temperature fixture')
missing=json.loads(json.dumps(fixture));missing['source']['seq']=101;missing['time']['source_utc']='2026-01-01T00:00:01Z';missing['time']['uptime_ms']=101000;missing['measurements']['panel_temperature_c']=None;missing['quality']['channel_status']['panel_temperature']='missing'
x.code('json',json.dumps(missing,indent=2))
x.h('Unsynchronized-clock fixture')
unsynced=json.loads(json.dumps(fixture));unsynced['source']['boot_id']='documentation-boot-02';unsynced['source']['seq']=0;unsynced['time']={'source_utc':None,'uptime_ms':1000,'clock_status':'unsynced'}
x.code('json',json.dumps(unsynced,indent=2))
x.h('Semantic rejection and quarantine cases')
x.table(['Input problem','Decision','Why structural parsing alone is insufficient'],[
('Topic node differs from payload node','Reject / quarantine identity mismatch','Well-formed JSON can still describe the wrong scope'),
('Unsupported schema version','Reject or dedicated compatibility path','Do not guess field interpretation'),
('Value is null but channel status is valid','Reject / quarantine inconsistency','Null is not a valid zero'),
('Clock says synced but source UTC is null','Reject / quarantine clock inconsistency','Age cannot be qualified'),
('Source time far in the future','Quarantine with clock reason','Prevent negative-age live status'),
('Negative current in an approved unidirectional bench','Flag reverse/out-of-scope condition','Broad signed device range is not the operating policy'),
('Unknown calibration ID','Retain as unqualified or quarantine by policy','A string is not proof of calibrated accuracy'),
('Duplicate key with a changed body','Identity fault','A duplicate must be immutable'),
('NaN / Infinity / string numerals','Reject nonstandard or wrong-type number','Strict JSON must not coerce these into trusted measurements'),
('Irradiance supplied in lux under a W/m² key','Reject unit mapping','A numeric range cannot establish radiometric meaning'),
('Temperature outside characterized range','Mark scope/quality restriction','Sensor absolute range differs from validated assembly performance'),
('Receive time substituted for source time','Reject provenance error','Backlog arrival is not a new observation')])

x=c('Data Quality, Clocks and Freshness','data-quality')
x.fig('quality_states','Quality governs whether a record can support engineering interpretation. A transport connection and a normal-looking number do not establish validity.')
x.p('Quality is multi-dimensional. A record can be structurally valid but stale; current in the transport sense but uncalibrated; fresh electrically but unsuitable for a baseline because sunlight is changing quickly. Keep these reasons independently available even if the interface also shows a concise overall state.')
x.table(['State / dimension','Meaning','Allowed interpretation'],[
('Valid channel','Conversion/status/range accepted under applicable calibration','Use within characterized scope'),
('Missing channel','No trustworthy value supplied','Do not substitute zero'),
('Invalid channel','Conversion, CRC, range or integrity failure','Exclude affected calculations'),
('Uncertain channel','Calibration, mounting or interpretation uncertainty','Restrict confidence and show reason'),
('Fresh observation','Qualified source age within threshold','Current context subject to other quality gates'),
('Stale observation','Source age >5 s reference threshold','Last-known history, not current plant state'),
('Clock unsynchronized','Absolute source UTC not qualified','Arrival/uptime context only'),
('Backfilled record','Arrived after its observation window','Historical use under explicit replay policy'),
('Environment gated','Low/rapidly changing irradiance or unsuitable context','Do not accumulate a fault timer'),
('Analysis unavailable','Missing model/dependency or invalid input','No healthy score or forecast invented')])
x.h('Reference freshness logic')
x.code('python', '''from datetime import datetime, timezone

# Reference logic only; deployed clock uncertainty must be explicit.
def freshness(source_utc, clock_status, now_utc, stale_after_s=5.0):
    if clock_status != "synced" or source_utc is None:
        return {"state": "clock_uncertain", "age_s": None}
    source = datetime.fromisoformat(source_utc.replace("Z", "+00:00"))
    if source.tzinfo is None or now_utc.tzinfo is None:
        return {"state": "invalid_clock", "age_s": None}
    age_s = (now_utc - source).total_seconds()
    if age_s < 0:
        return {"state": "future_time", "age_s": age_s}
    return {
        "state": "stale" if age_s > stale_after_s else "fresh",
        "age_s": age_s,
    }

# The helper has no access to actual node clocks or live telemetry.
# Production policy must account for synchronization uncertainty.
# Receive time is recorded independently rather than passed as source time.''')
x.h('Time-basis review')
x.table(['Clock situation','Required treatment','Evidence'],[
('Node starts without UTC','Publish unsynced/null UTC and monotonic uptime','Initial record and clock-status transition'),
('Gateway UTC steps','Avoid negative/huge integration intervals','Clock-change log plus interval exclusions'),
('Node reboots','New boot identity even if sequence restarts at zero','Boot boundary and duplicate-key test'),
('Client timezone changes','Display may change; record UTC does not','Same record shown in two selected zones'),
('Record replayed late','Preserve source time and mark backfill','Source versus receive timestamps'),
('Clock uncertainty overlaps freshness boundary','Show uncertainty; use approved conservative policy','Synchronization bounds and classification'),
('Daylight-saving display shift','UTC identity remains monotonic','Window labels and export time basis')])
x.h('Quality propagation rules')
x.bullets(['Power needs an accepted V/I pair; a valid voltage does not repair an invalid current.','Energy needs two valid adjacent endpoints and an acceptable elapsed interval.','Expected-output comparison needs valid environmental context and a valid model/configuration revision.','A quality fault can itself create a data-health event without becoming a solar-performance fault.','A dashboard summary must not hide the reason that a detailed channel is unavailable.','Backfilled data may improve history without changing the assertion that a live link was unavailable.','Retain the excluded-duration inventory so energy confidence can be interpreted later.','When quality rules change, version the policy and preserve the original raw record.'])

x=c('Calibration and Measurement Uncertainty','calibration')
x.fig('calibration_chain','Reference metrology chain: known source/reference → DUT comparison → coefficient/revision → residual review → retained evidence.')
x.p('Calibration of the complete measurement path is different from programming an IC calibration register. Use a traceable reference of suitable uncertainty, record the setup and loading, cover the intended operating window and preserve both raw and corrected observations. The current numeric accuracy values are acceptance targets, not demonstrated results.')
x.fig('calibration_matrix','Fifteen planned V/I test points: 12, 18 and 24 V against 0.5, 1, 2, 4 and 5 A. Every cell is calculated load power, not measured error or a passed calibration result.')
x.table(['Planned voltage','0.5 A load','1 A load','2 A load','4 A load','5 A load'],[
('12 V','6 W','12 W','24 W','48 W','60 W'),('18 V','9 W','18 W','36 W','72 W','90 W'),('24 V','12 W','24 W','48 W','96 W','120 W')])
x.h('Calibration record fields')
x.table(['Field','Required content'],[
('Record ID / revision','Immutable reference and any superseding revision'),
('DUT identity','Node, board, sensor serials and firmware'),
('Measurement channel','Voltage, current, irradiance or panel temperature'),
('Reference instrument','Make/model/serial, certificate and uncertainty'),
('Setup','Connection, range, load, lead placement and mounting'),
('Environment','Ambient/board/sensor temperature and relevant conditions'),
('Point list','Applied reference, raw reading, corrected reading and repeat count'),
('Coefficient fit','Model form, units, offsets and applicable range'),
('Residuals','Pointwise errors, repeatability and outlier handling'),
('Acceptance rule','Target, uncertainty/guardband policy and decision'),
('Time and personnel','Date, operator and reviewer'),
('Applicability','Effective revision and devices/channels covered')])
x.h('Uncertainty budget structure')
x.table(['Contribution','Example mechanism','Evaluation approach'],[
('Reference instrument','Calibration/measurement uncertainty','Certificate and selected range'),
('Shunt resistance','Tolerance, self-heating, temperature coefficient','Measured value and temperature characterization'),
('Analog conversion','Gain/offset/noise/quantization','Datasheet plus repeated-point observation'),
('Lead/contact arrangement','Non-Kelvin drop and resistance change','Connection review and repeat assembly'),
('Timing alignment','V/I mismatch under changing load','Measured pairing interval and transient test'),
('Pyranometer','Calibration, angular/spectral response and soiling','Sensor record plus mounting/maintenance evidence'),
('Temperature mounting','Thermal contact and local gradient','Mounting characterization against a suitable reference'),
('Fit residual','Correction-model mismatch','Held-out calibration/check points'),
('Drift','Aging, thermal cycling and reassembly','Scheduled reference recheck'),
('Reporting','Rounding and unit transformation','Software arithmetic and export tests')])
x.code('text', '''Reference pointwise error:
    absolute_error = DUT_value − reference_value
    relative_error_percent = 100 × absolute_error / reference_value
Do not divide by a zero reference.
Use absolute error / noise criteria near zero current.

For independent small V/I standard uncertainties:
    u_P / P ≈ sqrt((u_V / V)² + (u_I / I)²)
For correlated contributions, include covariance.
For conservative bounded errors of 1% in V and 1% in I:
    upper product bound = 1.01 × 1.01 − 1 = 2.01%
A stated ≤2% power target therefore needs direct verification.
Do not call the product target proven from rounded channel targets.''')
x.procedure('Proposed calibration sequence',[
 'Review the approved bench and instrument ratings before connecting the DUT.',
 'Record instrument identity, uncertainty, firmware/configuration and ambient conditions.',
 'Check zero/offset and polarity before applying larger current.',
 'Apply the planned point matrix with a suitable rated source/load and safe current limit.',
 'Allow appropriate stabilization and record repeated raw/reference observations.',
 'Fit only the approved coefficient form and retain uncorrected values.',
 'Evaluate residuals and independent check points; include uncertainty in the decision.',
 'Assign a calibration revision only after review and record its applicability.',
 'Repeat a check after reassembly or meaningful thermal/mechanical change.',
 'Publish the actual record separately from the test-point figure.'])
