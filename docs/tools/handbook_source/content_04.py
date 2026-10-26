from doc_engine import c,event_table,mermaid,REG
import json
from pathlib import Path

x=c('Troubleshooting and Failure Diagnosis','troubleshooting')
x.fig('fault_isolation','Diagnose by failed boundary: platform → node → transport → persistence → analysis → presentation. Avoid destroying evidence through indiscriminate restarts.')
x.p('Begin with scope and evidence. Is the failure visible for one node, all nodes, only one client or only historical export? Preserve release/configuration, source/receive time, boot/sequence and event revision before changing the system. An apparently recovered display is insufficient if history, source freshness or event state remains inconsistent.')
x.table(['Symptom scope','First boundary to inspect','Do not assume'],[
('One sensor channel','Conversion, wiring, status and calibration','The entire gateway is faulty'),
('One node, all channels','Node power, boot, link and topic identity','Every physical solar component failed'),
('All nodes simultaneously','Broker, gateway, common network and time','Every node independently lost calibration'),
('Qt only','Session/display/thread/data adapter','Ingestion has stopped'),
('Website only','Remote path/session/client compatibility','Onsite monitoring is unavailable'),
('App only','App lifecycle, cache, access and release','Current source values are being received'),
('History only','Writer, window/time basis and retention','Live display guarantees durable history'),
('Anomaly score only','Input gates, baseline and policy revision','Missing analysis means healthy operation'),
('Energy only','Interval identity, gaps and time','Summing visible points yields trustworthy kWh')])
mermaid(x,'''flowchart TD
    S[Observed problem] --> Q{Scope?}
    Q -->|one channel| C[Inspect conversion and channel quality]
    Q -->|one node| N[Inspect node power boot identity and link]
    Q -->|all nodes| G[Inspect broker gateway storage and clock]
    Q -->|one client| U[Inspect client access cache and revision]
    C --> R[Preserve evidence and use approved corrective action]
    N --> R
    G --> R
    U --> R
    R --> V[Verify fresh identity and committed history]
    V --> E[Verify event and cross-client consistency]
    E --> H[Record recovery and handover]''')
for title,body in [
('The gateway boots but monitoring is not ready','A Linux login or running process does not prove application readiness. Inspect failed dependencies, effective configuration, storage availability and broker connection in that order. Record the exact startup error and release identity before applying the approved recovery procedure. Do not manufacture an application command from the documentation package.'),
('The Qt window is blank or does not open','Separate display/session/plugin problems from backend health. Check the actual Qt release, display/session configuration and application log. Determine whether ingestion/history continues before restarting the backend. Use only the release-specific launch path and retain a sanitized screen/error record.'),
('The Qt interface freezes during updates','Inspect UI-thread ownership, blocking I/O and render-queue growth in the actual code. Compare writer/analysis progress with interface interaction. Reducing chart rendering load may help diagnose the boundary but must not silently discard stored measurements or suppress quality faults.'),
('One node becomes stale','Check last source time, last receive time, boot identity, sequence and broker/topic scope. Inspect safe node power and LAN status before assuming a plant fault. Recovery must demonstrate a genuinely current observation, not merely the arrival of old backlog.'),
('All nodes become stale together','Review gateway clock, broker, common network and ingestion readiness. Compare OS time state with the last received records. A common-path failure is more plausible than simultaneous independent sensor faults, but preserve evidence rather than making a diagnosis from likelihood alone.'),
('Voltage looks plausible but current is wrong','Inspect shunt polarity, Kelvin lead placement, configured resistance/current LSB and signed-register interpretation with the bench de-energized as required by the approved procedure. Compare against a suitable reference within the safe scope. Register CAL=2048 is scaling arithmetic, not proof of current calibration.'),
('Irradiance clips or has the wrong scale','Confirm the actual sensor sensitivity, ADC PGA/input configuration, unit conversion and calibration record. Check sensor orientation, shade and soiling. Do not apply a lux-to-irradiance assumption or change the baseline to hide a sensing-chain problem.'),
('Temperature is missing or implausible','Inspect conversion completion, CRC, power/pull-up arrangement and mounting. A sensor contact problem can mimic a physical thermal change. Mark the channel invalid/missing and gate temperature-dependent analysis until qualified data returns; do not reuse an old temperature without age context.'),
('Power differs between clients','Compare node and sample identity before comparing rounding. Check V/I pairing, unit mapping, derived-metric revision and cache/source time. A website showing a different observation can disagree numerically without the multiplication being wrong; the client must make that distinction visible.'),
('Energy jumps after reconnect','Investigate duplicate committed intervals, replay ordering, source-time discontinuities and gap policy. Review unique node/boot/sequence keys and integration-revision identity. Do not “fix” the display by subtracting energy manually; preserve the raw records and correct a versioned derivation.'),
('Energy appears flat through an outage','A qualified integrator can stop accumulating because contribution is unknown, not because generation stopped. Inspect excluded duration and endpoint validity. Present partial energy and its coverage window rather than silently interpolating across the outage.'),
('A residual spike creates too many alerts','Review irradiance stability, V/I/environment timing, baseline applicability and persistence behavior. Confirm that a quality-gate loss resets/holds according to the published rule. Do not raise thresholds without a controlled policy revision and a false-alert/missed-event review.'),
('An acknowledged alert is still active','This can be correct: acknowledgement is a human workflow action, while active describes the condition. Review the physical finding, current qualified input and clear policy. Do not use acknowledgement as a substitute for a verified maintenance outcome.'),
('The website/app shows old data as live','Inspect source timestamp, clock status, caching and reconnect logic. Compare the same source record in Qt. The remote adapter must not reset observation age on receipt or redraw; retain offline/backfill state until a qualified current sample is available.'),
('The database cannot accept writes','Preserve the error, disk/mount state, free space and pending-record count. Follow the release-specific space/retention/repair policy. A live card can continue changing while nothing is durable, so expose the write fault. Do not delete the only copy of history or blindly copy an active WAL database.'),
('A clock step corrupts age or integration','Retain source UTC, receive UTC and monotonic timing context. Exclude invalid/nonpositive intervals and quarantine implausible future observations under the reviewed policy. A time-service restart is not permission to relabel earlier samples or bridge an uncertain interval.'),
('A reconnect creates duplicate event entries','Check whether event identity is stable across subscriber restart and replay. Compare policy revision, onset and source evidence. Telemetry deduplication and event idempotency are separate responsibilities; one cannot be assumed from the other.'),
('Remote access fails while onsite monitoring works','Check the approved access path, session, client/backend compatibility and WAN status. Preserve local monitoring if its dependencies are healthy. Do not expose the broker or gateway shell publicly as an improvised remote-access fix.')]:
 x.h(title,4);x.p(body)
x.h('Recovery acceptance')
x.table(['Recovered boundary','Evidence needed before closing the issue'],[
('Sensor','Valid conversions and an appropriate reference comparison'),
('Node','Current source time, boot/sequence continuity and channel quality'),
('Transport','Expected topic/identity, bounded backlog and duplicate handling'),
('Writer','Committed rows, integrity and no lost/duplicated interval claim'),
('Analysis','Applicable policy/model, qualified inputs and explainable event state'),
('Qt','Responsive interaction and a qualified current snapshot'),
('Remote client','Correct source age, scope and event revision'),
('Whole system','Common node/window agreement plus recorded cause/action')])

x=c('Observability, Backup and Preventive Maintenance','observability')
x.fig('backup_recovery','Consistent backup → manifest/checksum → protected retention → restore on a controlled copy → verify records and operating context.')
x.h('Health inventory')
x.table(['Health signal','Interpretation','Follow-up'],[
('Platform uptime/reset','Gateway continuity','Compare with application/node boot context'),
('Node boot identity','Firmware restart boundary','Review reset reason and sequence'),
('Source/receive horizon','Observation versus ingestion progress','Check backlog or clock uncertainty'),
('Channel validity counts','Sensor-path health','Inspect recurring channel-specific reasons'),
('Broker reconnect count','Transport stability','Review common network/power conditions'),
('Pending queue depth','Backpressure/backlog','Check bounds and live-data scheduling'),
('Duplicate/conflict counts','Delivery repetition versus identity error','Investigate changed-body collisions separately'),
('Write failures','Persistence health','Check disk, mount, schema and permissions'),
('Free space / WAL / logs','Capacity pressure','Use approved retention/checkpoint policy'),
('Analysis-gated duration','Unavailable performance conclusions','Review environment and data quality'),
('Event action failures','Workflow/access/revision conflicts','Review authorization and concurrency outcome'),
('Backup age and restore status','Recoverability','Schedule/rehearse recovery rather than trusting file existence')])
x.h('Reference backup manifest')
x.code('json',json.dumps({'manifest_basis':'reference backup contract','backup_id':None,'created_utc':None,'source_release':None,'schema_revision':None,'configuration_revision':None,'calibration_revisions':[],'window':{'first_source_utc':None,'last_source_utc':None,'last_committed_identity':None},'contents':{'telemetry':None,'events_and_actions':None,'configuration':None,'calibration':None,'necessary_metadata':None},'consistency_method':None,'sha256_manifest':None,'secret_handling':None,'storage_access_scope':None,'restore_check':{'performed_utc':None,'target_copy':None,'integrity_outcome':None,'known_record_checks':[]}},indent=2))
x.procedure('Create and verify a backup',[
 'Identify the actual storage engine and approved consistency method.',
 'Capture release/schema/configuration/calibration identities.',
 'Use a supported online backup or controlled shutdown snapshot as appropriate.',
 'Do not assume copying only an active SQLite main file includes current WAL state.',
 'Include event actions and metadata needed to interpret telemetry.',
 'Create checksums and a time/window manifest without exposing secrets.',
 'Store under the approved access and retention policy.',
 'Restore to an isolated controlled copy, not over the only operational dataset.',
 'Run integrity checks and compare known telemetry/event identities.',
 'Record restore outcome, limitations and reviewer.'])
x.h('Preventive-maintenance cadence — proposed')
x.table(['Cadence / trigger','Activity','Evidence'],[
('Before each bench session','Cables, enclosure, current limit and identity/freshness','Operator pre-check'),
('Daily while operating','Review gaps, stale duration, storage and active events','Operational health note'),
('Weekly while operating','Review reconnects, recurring sensor faults and backup status','Trend and action record'),
('Scheduled metrology interval','Compare against suitable references','Calibration/check record'),
('After reassembly','Inspect contacts, mounting and isolation boundaries','Reassembly verification'),
('After software change','Verify contracts, configuration and rollback','Release acceptance record'),
('After unexpected reset','Review power, reset and data continuity','Incident/recovery note'),
('Before public submission','Sanitize evidence and verify links/assets','Publication checklist')])
x.p('A maintenance schedule needs actual operating experience and the sensor/instrument manufacturer guidance. The intervals above are a proposed working rhythm, not a claim that the team has already completed recurring field service. Escalate unexpected heating, damaged wiring or uncertain isolation through the authorized electrical process rather than continuing a documentation-led experiment.')

x=c('CAD, Packaging and Thermal Studies','mechanical')
x.fig('enclosure_assembly','Proposed seven-part sensor-node assembly. STEP exchange geometry is supplied; it is not a fabricated or ingress-tested enclosure.')
x.p('The mechanical concept packages the sensing node, not the Ubuntu gateway. Its purpose is to examine board allocation, cable routing, mounting and service access before detailed fabrication. The STEP files are concept geometry and do not establish material certification, manufacturing tolerances, fastener strength, sealing or electrical insulation performance.')
x.table(['Concept element','Nominal input','Status / constraint'],[
('Outer envelope','155 × 115 × 75 mm','Proposed sensor-node case'),
('Shell wall','3 mm','Concept dimension; manufacturing review pending'),
('Lid thickness','3.5 mm','Concept dimension'),
('Gasket thickness','1.5 mm','Compression/groove/sealing design not validated'),
('Aluminum backplate','125 × 85 × 3 mm','Proposed mechanical/thermal support'),
('Main PCB envelope','110 × 70 × 1.6 mm','Envelope only; no routed board supplied'),
('Controller envelope','62 × 25 mm','Placement allowance, not verified 3D component clearance'),
('Interface subassembly','Separate concept envelope','Actual connector/cable clearance to be checked'),
('Ingress goal','IP65','Untested design target, not an assigned rating')])
x.fig('mechanical_layout','Concept board placement, cable/service clearances and analytical mounting-load assumptions. This is not native EDA, FEA or a fabrication drawing.')
x.h('Delivered CAD assets')
x.table(['File','Content'],[
('`01_pc_body_concept.step`','Case body concept'),('`02_pc_lid_concept.step`','Lid concept'),('`03_silicone_gasket_concept.step`','Gasket concept'),('`04_aluminum_backplate_concept.step`','Backplate concept'),('`05_pcb_envelope.step`','PCB envelope'),('`06_controller_envelope.step`','Controller envelope'),('`07_isolated_interface_envelope.step`','Interface envelope'),('`ARKA_AI_enclosure_assembly_CONCEPT.step`','Combined concept assembly'),('`dimensions.json`','Nominal dimension record'),('`CAD_README.txt`','Concept use/limitations')])
x.p('All files above are in [docs/cad](docs/cad/). STEP exchange files can be inspected in a compatible CAD tool. They are not a native manufacturing release. Reconcile actual component models, connector insertion paths, cable bend radii and assembly tolerances before producing hardware.')
x.h('Cantilever hand calculation')
x.code('text', '''Assumed rectangular aluminum mounting tab:
    F = 10 N
    free length L = 20 mm
    width b = 20 mm
    thickness t = 3 mm
    elastic modulus E = 69000 N/mm²

Small-deflection cantilever end-load model:
    sigma = 6 F L / (b t²)
          = 6 × 10 × 20 / (20 × 3²)
          = 6.67 N/mm² = 6.67 MPa
    delta = 4 F L³ / (E b t³)
          = 4 × 10 × 20³ / (69000 × 20 × 3³)
          ≈ 0.00859 mm

This ignores holes, fillets, contact, fasteners, vibration and fatigue.
No material yield, factor of safety or FEA result is established.
Use the actual geometry and alloy for release review.''')
x.h('Thermal budget')
x.fig('thermal_budget','Calculated maximum effective thermal resistance versus ambient temperature at 3 W and a 65 °C interior limit. Solar heating is excluded and no temperature measurement is plotted.')
x.code('text', '''Proposed screening condition:
    internal dissipation = 3 W
    ambient = 45 °C
    target interior temperature <=65 °C
    allowable rise = 20 °C
    required effective thermal resistance <=20 / 3
                                         <=6.67 °C/W

The effective value represents the whole heat-rejection path.
It is not the junction-to-ambient rating of a single component.
Direct solar load, wind, mounting and cable heat paths are excluded.
Those effects require a revised model and actual thermal testing.''')
x.h('Mechanical acceptance review')
x.bullets(['Inspect actual component/connector heights and the full assembly sequence.','Check that cable glands, strain relief and service loops do not compromise isolation.','Review fastener access, torque, board support and removal without wire damage.','Assess gasket compression and material compatibility using the actual manufactured case.','Measure temperatures under controlled load/ambient and record sensor placement.','Review outdoor UV, condensation, corrosion and thermal cycling if the scope expands.','Retain IP65 as a target until an appropriate assembly test establishes performance.','Do not label a hand calculation or STEP view as finite-element evidence.'],check=True)

x=c('BOM, Budget and Procurement Assumptions','bom-budget')
x.p('The following costs are planning estimates in INR. They are not supplier quotations, purchased inventory or procurement confirmations. Quantities reflect one proposed demonstrator with shared irradiance-reference and gateway resources. Taxes, delivery, exchange-rate changes, tooling and replacements require an actual procurement review.')
x.table(['Item','Proposed part / scope','Quantity','Line estimate'],[
('Controller','ESP32-S3-DevKitC-1-N8R8','1','₹1,300'),
('V/I measurement','INA226 + 10 milliohm / ≥1 W Kelvin shunt','1 set','₹650'),
('Isolation','ISO1540 + B0505S-1WR3 + TLV76033','1 set','₹1,100'),
('Irradiance ADC','ADS1115 breakout','1','₹300'),
('Panel temperature','DS18B20, cable and mount','1','₹250'),
('Irradiance reference','Apogee SP-110-SS','1','₹32,000'),
('Gateway planning allowance','Raspberry Pi 4B 4 GB, 64 GB card and supply','1 set','₹6,800'),
('Node supply','External 5 V / 3 A; proposed GST18A05-P1J','1','₹1,000'),
('Enclosure/mounting','Case, gasket, glands and aluminum plate','1 set','₹1,600'),
('PCB/protection','2-layer FR4 and protective components','1 set','₹1,200'),
('Harness/passives','Terminals, cable, fuse and passives','1 set','₹500')])
x.fig('budget_breakdown','Estimated line-cost distribution. The pyranometer and gateway are shared planning resources; the chart does not show actual expenditure.')
x.code('text', '''Estimated subtotal = ₹46,700
Contingency = 20% × ₹46,700 = ₹9,340
Estimated total with contingency = ₹56,040

Node-only scope in this cost model:
    ₹46,700 − ₹32,000 reference − ₹6,800 gateway = ₹7,900

This is not a production unit price or per-zone installed cost.
Shared sensor placement and gateway capacity must be reviewed.
Gateway BOM identity does not identify the actual built Ubuntu target.''')
x.h('Procurement assumptions')
x.table(['Resource','Planning lead-time assumption','Unverified issue'],[
('Common controller/analog parts','India, approximately 1–2 weeks','Actual stock, suffix and authentic source'),
('Pyranometer','Import, approximately 3–6 weeks','Quote, customs, calibration record and delivery'),
('Gateway/storage kit','India, approximately 1–2 weeks','Actual target compatibility and sustained-write suitability'),
('Case/plate/harness','Local, approximately 1–2 weeks','Material, gland, finish and sealing details'),
('PCB','Local, approximately 1–2 weeks','Reviewed layout, fabrication files and assembly yield')])
x.h('Quote-comparison checklist')
x.bullets(['Match full orderable suffix, package, grade and supplied calibration where relevant.','Record quote date, currency, taxes, freight, warranty and validity.','Confirm that a breakout module\'s analog path and pull-ups match the reviewed schematic.','Evaluate substitute parts against measurement, isolation, logic and thermal requirements.','Review enclosure/gland material and actual environmental scope.','Retain supplier authenticity and incoming-inspection records.','Separate shared-resource cost from incremental node cost.','Update the budget revision without claiming that a quote has become a purchase.'],check=True)
x.p('The machine-readable estimate is [proposed_bom.csv](docs/data/proposed_bom.csv). Preserve its estimate and lead-time qualifications in any proposal derived from it. Procurement evidence should include actual quotations or invoices only after they genuinely exist.')

x=c('Performance Targets and Measurement Methodology','performance')
x.table(['Metric','Target / planning assumption','Method','Result status'],[
('Acquisition','1 Hz','Source-interval distribution and missed-deadline count','Not supplied'),
('Onsite display age','≤3 s','Qualified source-time to visible-snapshot age','Not supplied'),
('Stale state','After >5 s','Controlled timeout and state capture','Not supplied'),
('Node buffer','600 records, roughly 10 minutes at 1 Hz','Sequence inventory and overflow/recovery review','Not supplied'),
('Retention scale','10 nodes over 30 days','Actual on-disk growth, indexes/WAL/logs/backup','Not supplied'),
('V/I accuracy','≤1% above 0.5 A after calibration','Reference-point error with uncertainty policy','Not supplied'),
('Power accuracy','≤2% after calibration','Direct matched-point power comparison','Not supplied'),
('Persistent residual','>15% for 180 s with valid/stable G ≥200 W/m²','Condition/onset/gate/timer timeline','Not supplied'),
('Visible alert','≤210 s for a qualifying event','Onset to visible qualified event','Not supplied'),
('Precision','≥90% on held-out labeled events','TP/(TP+FP), counts and uncertainty','Not supplied'),
('Recall','≥85% on held-out labeled events','TP/(TP+FN), counts and uncertainty','Not supplied'),
('Thermal screen','3 W; 45 °C ambient; interior ≤65 °C','Controlled instrumented thermal run','Not supplied')])
x.fig('latency_model','Illustrative allocation of the 210-second alert budget. The allocation is a model, not a measured latency trace or percentile distribution.')
x.h('Latency instrumentation')
x.table(['Timestamp','Definition','Why it matters'],[
('t_condition','Controlled/verified qualifying condition onset','Defines what the delay is measured from'),
('t_observation','Node acquisition time for the evidence','Separates sensing delay'),
('t_receive','Gateway envelope arrival','Separates transport/backlog delay'),
('t_commit','Known persistence outcome','Separates a live path from durable evidence'),
('t_qualified','Persistence/analysis condition qualified','Identifies intentional decision delay'),
('t_client','Snapshot/event visible in the chosen client','Completes the user-visible delay'),
('t_acknowledge','Human acknowledgement','Separate workflow time, not system detection latency')])
x.p('The initial 210 s target contains 180 s of persistence plus 30 s allowed for the surrounding sensing/transport/processing/display path. Measure the actual end-to-end distribution with synchronized clocks or a justified shared observation method. Report count, conditions, median, upper percentiles and maximum rather than one favorable screenshot.')
x.h('Illustrative inspection-wait comparison')
x.code('text', '''Model assumptions:
    manual inspection rounds are 4 hours apart;
    a fault begins uniformly between rounds;
    average manual wait = 4 / 2 = 2 hours = 7200 seconds;
    monitoring alert delay is the proposed 210-second target.

Modeled waiting-time reduction:
    (7200 − 210) / 7200 × 100 = 97.0833...%

Separate large-plant arithmetic illustration:
    affected capacity = 5 kW (not the bench demonstrator rating)
    shortfall = 10%
    opportunity power = 0.5 kW
    over 2 hours = 1.0 kWh
    over 210 seconds = 0.0291667 kWh

Neither calculation is a measured yield or revenue recovery.
Actual repair time, fault distribution and downtime are not included.
An earlier alert does not guarantee an earlier authorized repair.''')
x.h('Illustrative confusion-matrix arithmetic')
x.p('These are invented counts solely to explain evaluation, not ARKA validation data: TP=18, FP=2, FN=3 and TN=77. The totals show why a headline accuracy value is not enough for maintenance events. The real release must report its own labeled-event inventory and separated holdout.')
x.table(['Metric','Calculation from the illustrative counts','Value'],[
('Precision','18 / (18 + 2)','90.00%'),
('Recall','18 / (18 + 3)','85.71%'),
('Specificity','77 / (77 + 2)','97.47%'),
('Accuracy','(18 + 77) / 100','95.00%'),
('F1','2 × 18 / (2 × 18 + 2 + 3)','87.80%')])
x.h('Measurement report fields')
x.table(['Field','Required reporting content'],[
('Scope','Node/plant condition and measurement location'),
('Release','Firmware, gateway, client, config and model revisions'),
('Clock basis','Synchronization method and uncertainty'),
('Dataset','Record/event count, window and exclusions'),
('Method','Controlled input or verified natural-event definition'),
('Statistics','Distribution and uncertainty, not only the best case'),
('Failures','Lost data, timeouts, resets and rejected events'),
('Acceptance','Criterion, guardband and pass/fail/inconclusive outcome'),
('Traceability','Raw records, export manifest and checksums'),
('Limitations','Conditions where the result cannot be generalized')])

x=c('Risk Register and Safety Mitigations','risk-register')
x.p('This is a proposed engineering risk register, not a signed plant safety assessment. Priority labels indicate review urgency, not measured probability. Qualified personnel must review electrical and deployment hazards for the actual setup. Certified protection and authorized work processes remain independent of the monitoring platform.')
x.table(['Risk ID','Hazard / failure','Priority','Mitigation / release gate'],[
('R-01','Direct live-string connection to the bench circuit','Critical','Prohibit; use a separately engineered rated interface'),
('R-02','Isolation defeated by USB, ground or probe path','High','Review every return/instrument connection before energizing'),
('R-03','Shunt/load wiring overheats','High','Rated source/load/conductors, current limit and thermal review'),
('R-04','Stale last-known value looks live','High','Source-age/quality visible across all clients'),
('R-05','Invalid channel becomes a normal zero','High','Null/status contract and fault-injection tests'),
('R-06','Duplicate replay inflates energy','High','Immutable key plus interval idempotency'),
('R-07','Clock discontinuity corrupts time/energy','High','Clock quality, monotonic timing and interval exclusions'),
('R-08','Environmental transients cause false alerts','Medium','Stable/valid irradiance gate and persistence review'),
('R-09','Baseline misses real faults or mislabels normal conditions','High','Applicable model and separated labeled evaluation'),
('R-10','Storage exhaustion silently loses history','High','Capacity margin, write-health state and retention policy'),
('R-11','Unauthorized remote access or event action','High','Least privilege, approved transport and workflow audit'),
('R-12','Unsafe expectation of predictive certainty','High','Explain scope; no unvalidated failure-date guarantee'),
('R-13','Enclosure solar heating exceeds internal limit','High','Outdoor heat-load model and measured thermal test'),
('R-14','Untested IP goal mistaken for certification','High','Keep target label; obtain actual assembly evidence'),
('R-15','Configuration/calibration changes erase context','Medium','Revisioned raw/derived records and controlled change'),
('R-16','Release migration destroys recoverability','High','Consistent backup and rehearsed rollback'),
('R-17','Public evidence exposes secrets or personal/site data','Medium','Sanitized publication review and permission'),
('R-18','Website/app assumes monitoring grants control authority','High','Separate read/workflow/admin/control permissions')])
x.h('Stop conditions for a demonstration')
x.bullets(['Unexpected heating, smell, visible damage, unstable supply or unsafe exposed conductors.','Uncertain polarity, unknown instrument ground path or isolation-domain bridge.','A source/load rating or operating point outside the approved bench scope.','An invalid/unqualified measurement being used to justify an electrical action.','A required safety/work authorization or qualified supervisor is absent.','A condition that cannot be made safe through the approved shutdown/disconnect procedure.'])
x.h('Residual-risk ownership')
x.table(['Area','Review owner role','Evidence before expanding scope'],[
('Electrical interface','Qualified electrical reviewer','Ratings, topology, protection and insulation review'),
('Metrology','Measurement/calibration reviewer','Traceable calibration and uncertainty decision'),
('Firmware/data','Firmware/backend maintainer','Identity, time, loss and replay verification'),
('Analytics','Model/validation owner','Labeled evaluation, confounders and limits'),
('Operations','Authorized site/maintenance owner','Work process and handover'),
('Security','Deployment/access owner','Actual controls and tested permissions'),
('Mechanical/environment','Packaging reviewer','Fit, thermal and ingress evidence')])
x.p('A future release can accept, mitigate or reject a risk only with a named owner and supporting evidence. This document deliberately does not declare residual risk acceptable for a real plant installation.')

x=c('Maker Journey and Implementation Milestones','maker-journey')
x.fig('maker_progress','Progression from the original sensing concept to the team-confirmed embedded/software ecosystem, followed by evidence publication and forward validation.')
x.p('The maker journey starts with the original Stage 1 submission: ESP32-S3 sensing, MQTT, a local gateway, Python/PySide6 visualization, local history and edge analysis for solar monitoring. That document established the system intent and staged validation direction. It did not establish the part-level circuit, measured accuracy or certification.')
x.p('The team subsequently confirms the implementation of an Ubuntu command-line-based embedded environment, Qt UI, Python backend, website and companion app. The project therefore extends beyond a single dashboard concept into an onsite/connected monitoring ecosystem. These are implementation milestones reported by the team, not future capabilities invented for this handbook.')
x.p('The engineering documentation expands the original concept into explicit interfaces, calculations, proposed packaging, a budget and testable acceptance criteria. This work supports review and reproducibility; it does not convert a drawing or numerical target into completed hardware evidence. Publishing source, captures and executed records is the next evidence step.')
x.table(['Milestone','Basis','Status meaning'],[
('Identify solar monitoring problem and users','Original Stage 1 project submission','Documented foundation'),
('Define ESP32-S3 / MQTT / gateway chain','Original Stage 1 architecture','Documented architecture'),
('Build Ubuntu-based onsite platform','Explicit team statement','Implemented software milestone confirmed by team'),
('Build Qt / Python engineering stack','Explicit team statement','Implemented software milestone confirmed by team'),
('Build website and companion app','Explicit team statement','Implemented connected-client milestone confirmed by team'),
('Integrate monitoring ecosystem','Explicit team statement','Shared ecosystem confirmed; exact mechanics await publication'),
('Develop part-level low-voltage reference','Engineering proposal and manufacturer references','Proposed design'),
('Develop enclosure and analytical screens','STEP concept and calculations','Concept / calculated, not fabricated or FEA'),
('Define validation/acceptance protocol','This handbook and engineering presentation','Planned verification'),
('Publish reproducible release and real captures','Required handover artifacts','Publication gap to close'),
('Execute physical/integration/holdout tests','Actual signed datasets and reports required','No supplied result claimed')])
x.h('What changed from the original submission')
x.table(['Original foundation','Documented extension','Boundary retained'],[
('Local Python/PySide6 HMI','Ubuntu-based onsite engineering environment','No claim of a newly written operating-system kernel'),
('Local monitoring/history','Qt plus website and companion app ecosystem','Remote network access is not WAN-independent'),
('Edge analysis and maintenance support','Explicit baseline, residual, persistence and audit contracts','No guaranteed failure-date prediction'),
('Staged prototype validation','Pin-level reference, calibration plan and fault matrix','No fabricated calibration or pass results'),
('Future multi-zone/security/SCADA','Versioned contracts and forward roadmap','Future integration is not presented as deployed')])
x.h('Evidence that will strengthen the journey')
x.bullets(['Authentic device/lab photographs with permission and truthful captions.','Actual Qt, website and app captures with release and source-time context.','A published runtime source/artifact and dependency/configuration manifest.','Executed calibration, reconnect, retention and cross-client test records.','A real prototype recording that shows the implemented ecosystem and its limits.','A maintained issue/release history connecting findings to revisions.'],check=True)
x.p('No faculty endorsement, maker photograph, manufacturing milestone, award, procurement record or production deployment is invented. Add those only from authentic project evidence and retain the distinction between demonstrated behavior and planned expansion.')

x=c('Roadmap and Future Development','roadmap')
x.fig('verification_roadmap','Relative four-month forward verification plan. Month labels are planning phases, not dates of completed work.')
x.table(['Relative phase','Work package','Exit evidence'],[
('Month 1','Reconcile runtime release, node identities and pin-level design; establish metrology','Release manifest, reviewed schematic and calibration method'),
('Month 2','Execute bench conversion/timing/replay tests and common-client fixtures','Datasets, screenshots and fault/recovery inventory'),
('Month 3','Run environmental/confounder studies and held-out event evaluation','Labeled split, metrics, limits and false-alert burden'),
('Month 4','Exercise retention/backup/rollback, review risks and publish demo evidence','Acceptance pack, operator guide, real video and known-issue list')])
x.h('Expansion gates')
x.table(['Future capability','Prerequisite','Not implied today'],[
('More zones/nodes','Measured capacity, identity and time-quality review','Unlimited fleet scalability'),
('SCADA/inverter integration','Approved read-only interface and vendor mapping','Direct inverter control'),
('Node-battery visibility','Reviewed voltage sensing and chemistry/load context','Validated SOC or remaining-life prediction'),
('Fleet analytics','Cross-site schema, access and comparable data-quality policy','Deployed multi-site cloud platform'),
('Advanced predictive models','Representative labels and leakage-controlled evaluation','A trained model with guaranteed failure dates'),
('Outdoor deployment','Rated interface, environment/thermal/sealing evidence','IP65 certification from a concept case'),
('Remote hardening','Published actual protocol/authentication and tested controls','Production security certification'),
('Plant control','Independent safety/control architecture and approvals','Authority to switch equipment through this monitor')])
x.p('Prioritize evidence and correctness before additional screens or headline metrics. A smaller reproducible demonstrator with clear quality handling is more defensible than a broad feature list that cannot be traced to artifacts. Treat dates, owners and dependencies as a real project plan once the team approves them; the relative phases above are not commitments on behalf of unnamed members.')
x.h('Suggested issue categories')
x.bullets(['Runtime publication and reproducible build.','Node identity, timing and channel-quality verification.','Metrology and physical assembly evidence.','Cross-client consistency and access behavior.','Replay, persistence, retention and restore.','Baseline confounders and labeled-event evaluation.','Packaging, thermal and environmental qualification.','Operator handover, video publication and known limitations.'])

x=c('Prototype Video and Review Evidence','prototype-video')
x.quote('**JUDGES / REVIEWERS: [OPEN THE PROJECT DOCUMENTATION](docs/references/ARKA_AI_Stage1.pdf) · [OPEN THE ECOSYSTEM REVIEW](docs/references/ARKA_AI_Ecosystem_Presentation.pdf) · [OPEN THE CANONICAL REPOSITORY](https://github.com/DAnuraag/VK26-IITH-SE-0021).**')
x.quote('**PROTOTYPE VIDEO — A verified playback URL has not been supplied. Video publication is pending; this handbook does not link to a fabricated or unavailable recording.**')
x.h('Evidence index')
x.table(['Artifact','What it supports','What it does not establish'],[
('[Original Stage 1 PDF](docs/references/ARKA_AI_Stage1.pdf)','Primary project architecture and intended scope','Measured implementation performance'),
('[Ecosystem presentation PDF](docs/references/ARKA_AI_Ecosystem_Presentation.pdf)','Software scope, engineering proposals and review narrative','A complete released runtime or executed tests'),
('[Architecture figures](#architecture)','Logical system/data boundaries','Actual deployment topology by themselves'),
('[Proposed circuit](#electrical)','Pin-level low-voltage reference review','Routed PCB or plant-safe interface'),
('[Calculated/planned data](docs/data/figure_index.csv)','Reproducible technical-documentation charts','Plant telemetry or metrology results'),
('[CAD concepts](docs/cad/)','Packaging/placement concept','Fabrication, FEA, ingress or thermal qualification'),
('[Validation strategy](#validation)','Testable methods and acceptance targets','Completed or passed test cases'),
('[Public repository](https://github.com/DAnuraag/VK26-IITH-SE-0021)','Canonical review/publication location','Unpublished source, releases or a missing video')])
x.h('Recommended genuine recording sequence')
x.procedure('When the team records the prototype',[
 'Show project identity, actual device and approved low-voltage test arrangement.',
 'Identify the release and the source of displayed readings.',
 'Demonstrate the Ubuntu-based onsite environment without exposing secrets.',
 'Show the real Qt UI and Python-backed monitoring context.',
 'Show the actual website and app using the same node/event context.',
 'Demonstrate an authorized controlled data-quality or connectivity case.',
 'Show the system distinguishing stale/backfill from a current observation.',
 'Explain the proposed alert criteria and distinguish any simulated fixture.',
 'Show an acknowledgement/inspection workflow if implemented in the demonstrated release.',
 'State the current limits and evidence still being collected.',
 'Publish an accessible verified playback URL and add its date/build context here.'])
x.h('Publication readiness')
x.bullets(['The video link opens for the intended reviewers without an undisclosed access requirement.','Every screenshot/photo is authentic or explicitly labeled illustrative.','No password, token, private key, internal account or sensitive site detail is visible.','The build, test conditions and any injected examples are stated.','Numeric results have a dataset/method rather than only a narration.','The README and asset folder are published together so relative figures load.','Known limitations and pending test cases remain visible.'],check=True)

x=c('Glossary, References and Documentation Conventions','references')
x.h('Glossary')
x.table(['Term','Meaning in this project'],[
('ADC','Analog-to-digital converter; conversion resolution is not complete system accuracy.'),
('Age','Elapsed time since a qualified source observation, not merely a client redraw.'),
('Alert','A qualified event communicated for review; not a work permit or protection trip.'),
('App','The team-confirmed companion monitoring client; exact platform is unpublished.'),
('Backfill','Historical records arriving after their observation window.'),
('Baseline','Expected healthy output at the relevant measurement point and conditions.'),
('Boot identity','An identity distinguishing one actual node run from another.'),
('Calibration','A traceable relationship between reference and measured/corrected values.'),
('Channel quality','A sensor-specific validity, missing, uncertainty or range decision.'),
('Clock quality','The trust/uncertainty associated with source time.'),
('Configuration revision','The version of thresholds, scope and policies effective for a record.'),
('CRC','Cyclic redundancy check; an integrity check used by supported sensor protocols.'),
('Current LSB','Current represented by one configured monitor register count.'),
('Data health','Condition of sensing, clocks, transport and persistence, not solar performance.'),
('DC','Direct current; the proposed measurement point is a low-voltage DC point.'),
('Deduplication','Preventing repeated transport delivery from duplicating a committed record.'),
('DUT','Device under test.'),
('Edge analysis','Processing near the onsite monitoring data rather than requiring continuous WAN.'),
('Energy coverage','The intervals that contributed qualified energy, alongside excluded duration.'),
('Event revision','Version of event condition/workflow context used for consistent actions.'),
('Expected output','Modeled healthy output under stated assumptions, not guaranteed generation.'),
('FEA','Finite-element analysis; no completed native FEA is supplied here.'),
('Fresh','Source age is within policy and has a suitable clock basis.'),
('Gateway','Onsite computing/data boundary separate from the ESP32-S3 node.'),
('HMI','Human-machine interface for engineering monitoring.'),
('Holdout','Evaluation data separated from fitting/tuning to reduce leakage.'),
('I²C','Two-wire serial bus; isolated domains still need separate electrical review.'),
('Idempotency','Repeating a delivery/action does not create an unintended second effect.'),
('Ingress target','A desired enclosure protection level, not an untested certification.'),
('Irradiance','Radiant power per area in W/m²; not illuminance in lux.'),
('Kelvin sensing','Separate sense connections reduce load-path lead-drop error.'),
('kWh','Kilowatt-hour; 1000 Wh, an energy unit rather than power.'),
('LAN','Local-area network; distinct from external WAN availability.'),
('LDO','Low-dropout regulator; headroom, stability and heat still require review.'),
('Local-first','Onsite operation need not depend on continuous WAN when local dependencies survive.'),
('MQTT','Messaging transport used in the node-to-gateway architecture.'),
('Node','Field acquisition controller with explicit identity and boot/sequence context.'),
('Persistence','Durable storage outcome, not merely broker/client receipt.'),
('Precision','Fraction of predicted positive events that are confirmed positive.'),
('Pyranometer','Radiometric solar-irradiance instrument with calibration/mounting requirements.'),
('QoS 1','MQTT at-least-once delivery behavior; duplicates remain possible.'),
('Qt / PySide6','Qt for Python technology used by the onsite engineering UI.'),
('Recall','Fraction of true positive events that are detected.'),
('Reference contract','A proposed explicit interface/example, not an assertion of unpublished keys.'),
('Residual','Normalized difference between expected and measured output under valid gates.'),
('SCADA','Supervisory control/data-acquisition ecosystem; future integration needs approval.'),
('SOC','State of charge; node battery voltage alone does not establish a validated SOC model.'),
('Source time','When the node observed the measurement, with clock-quality context.'),
('Stale','A last-known observation older than the reference freshness threshold.'),
('STEP','CAD exchange format used for proposed assembly geometry.'),
('UTC','Common storage/record time basis; client display timezone is separate.'),
('WAL','Write-ahead log; backup consistency must account for the actual storage mode.'),
('WAN','Wide-area connectivity; not required for every local engineering function.'),
('Wh','Watt-hour; power integrated over qualified elapsed time.')])
x.h('Source hierarchy')
x.bullets(['Inspected implementation/configuration/test artifacts establish exact release mechanics and measured results.','Explicit team statements establish the reported implemented software scope.','The original Stage 1 PDF establishes the foundational architecture and intended project scope.','Proposed designs, calculated examples and future tests are identified as such.','The public repository README is supporting documentation, not independent evidence of completed tests.'])
x.h('Primary project references')
x.table(['Reference','Purpose'],[
('[Canonical repository](https://github.com/DAnuraag/VK26-IITH-SE-0021)','Project review and future publication hub'),
('[Original Stage 1 submission](docs/references/ARKA_AI_Stage1.pdf)','User-selected primary architecture/requirements source'),
('[Ecosystem review presentation](docs/references/ARKA_AI_Ecosystem_Presentation.pdf)','Current project narrative and proposed engineering studies'),
('[Proposed BOM CSV](docs/data/proposed_bom.csv)','Estimated costs and unverified lead-time assumptions'),
('[Figure index](docs/data/figure_index.csv)','Asset names, descriptions and evidence basis')])
x.h('Manufacturer references')
x.table(['Reference','Use / limitation'],[
('[TI INA226 product](https://www.ti.com/product/INA226) · [datasheet](https://www.ti.com/lit/ds/symlink/ina226.pdf)','Pinout, range and register scaling; not assembled-system accuracy'),
('[TI ISO1540](https://www.ti.com/product/ISO1540) · [datasheet](https://www.ti.com/lit/ds/symlink/iso1540.pdf)','Isolated bus behavior and ratings; not assembly working-voltage approval'),
('[TI ADS1115](https://www.ti.com/product/ADS1115) · [datasheet](https://www.ti.com/lit/ds/symlink/ads1115.pdf)','ADC PGA/rate/input behavior; not irradiance system accuracy'),
('[ESP32-S3 DevKitC-1 guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html)','Variant-specific pin/power review'),
('[Apogee SP-110-SS](https://www.apogeeinstruments.com/sp-110-ss-self-powered-pyranometer/) · [manual](https://www.apogeeinstruments.com/content/SP-110-manual.pdf)','Radiometric sensitivity, calibration and mounting'),
('[Analog Devices DS18B20](https://www.analog.com/en/products/ds18b20.html)','Temperature conversion, CRC and stated accuracy range'),
('[Mornsun B_S-1WR3 reference](https://www.mornsun-power.com/public/uploads/pdf/B_S-1WR3.pdf)','Unregulated converter/load/isolation review'),
('[TI TLV760](https://www.ti.com/lit/gpn/TLV760)','LDO headroom, current, bypass and thermal review')])
x.h('Software and standards references')
x.table(['Reference','Use / limitation'],[
('[Ubuntu Server documentation](https://documentation.ubuntu.com/server/)','Linux administration reference; does not identify the actual deployed version'),
('[Qt for Python](https://doc.qt.io/qtforpython-6/)','Qt/PySide programming and threading reference'),
('[Python documentation](https://docs.python.org/3/)','Language/runtime reference; actual version must be released'),
('[MQTT 3.1.1](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)','Delivery semantics reference, not deployed-broker evidence'),
('[JSON Schema 2020-12](https://json-schema.org/draft/2020-12)','Reference schema vocabulary/validation'),
('[SQLite backup documentation](https://www.sqlite.org/backup.html)','Consistent-backup reference for the proposed engine'),
('[IEC 61724-1:2021](https://webstore.iec.ch/en/publication/65561)','PV monitoring reference; no claimed system classification/compliance'),
('[IEC 61010-1](https://webstore.iec.ch/en/publication/4279)','Safety reference; no certification claimed'),
('[IEC IP-rating overview](https://www.iec.ch/ip-ratings)','Ingress terminology; IP65 remains an untested goal')])
x.h('Visual atlas')
x.table(['Figure / editable SVG','PNG fallback','Basis'],[(f'[{v["name"].replace("_"," ")}](docs/assets/{v["svg"]})',f'[PNG](docs/assets/{v["png"]})',v['basis']) for v in REG.values()])
x.h('Documentation conventions')
x.p('“Implemented” in the software capability statements reflects the explicit team update. “Proposed” identifies a design/reference contract awaiting reconciliation and acceptance. “Calculated” identifies arithmetic using stated inputs. “Illustrative” identifies explanatory values or layouts. “Target” identifies an acceptance goal. None of those terms should be substituted for a measured result, a released source artifact or an external certification.')
x.p('Tables and code examples retain units in keys or headings. Images contain functional/data labels rather than an overall presentation title; section titles and captions remain editable Markdown. SVG assets are preferred for detail and PNG fallbacks are supplied. The offline HTML companion embeds its resources and does not need a CDN to show the figures.')
x.p('The project license has not been supplied, so this handbook does not invent an open-source license grant. Bundled font license notices remain in docs/fonts. Consult the canonical repository owner before reusing project code or issuing a product release under a particular license.')
x.quote('**Final boundary:** ARKA AI supports informed engineering decisions. It does not replace certified electrical protection, qualified inspection or the evidence required to expand beyond the documented low-voltage monitoring scope.')
