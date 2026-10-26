from doc_engine import CHAPTERS,BASE,event_table
import json
BY={c.slug:c for c in CHAPTERS}

x=BY['problem-users']
x.h('Requirement-to-evidence traceability')
x.table(['Contract','Failure it prevents','Review chapter','Minimum artifact'],[
('Stable node identity','Values assigned to the wrong physical zone','Telemetry','Node mapping and a selected-client capture'),
('Boot/sequence key','Reboot or QoS replay creates duplicate identity','MQTT','Before/after boot and key inventory'),
('Source/receive separation','Old backlog looks live','Data quality','Timestamp/clock fixture comparison'),
('Channel-specific status','One failed sensor becomes a healthy record','Hardware sensing','Disconnected-channel evidence'),
('V/I pairing policy','P uses unrelated operating points','Power and energy','Conversion-time/pairing record'),
('Two-valid-endpoint integration','Outage becomes invented energy','Power and energy','Excluded intervals and partial-energy export'),
('Applicable calibration','Scaling is mistaken for system accuracy','Calibration','Reference/DUT points and coefficient revision'),
('Environmental gate','Clouds become equipment-fault certainty','Analytics','G/T/quality and timer timeline'),
('Event/workflow separation','Acknowledgement erases a real condition','Alerts','Event/action revisions'),
('Cross-client revision','Clients disagree about which event was handled','Shared workflow','Same event in Qt/web/app'),
('Commit outcome','A changing display is mistaken for durable history','Local storage','Transaction and row inventory'),
('Recovery manifest','A backup cannot reconstruct context','Observability','Restore and known-record checks'),
('Published release identity','Commands run against an unknown build','Deployment','Artifact/runtime/configuration manifest'),
('Safe scope','Bench sensor becomes an assumed plant interface','Risk register','Approved electrical review')])
x.p('A test can cover several requirements, but each requirement still needs a traceable result. Record the test identity and result artifact rather than marking an entire chapter “verified”. When a requirement is changed, identify the affected tests, clients and historical interpretation before accepting the new revision.')

x=BY['embedded-os']
x.h('Account and storage responsibility model — reference')
x.table(['Resource','Proposed access owner','Access rationale'],[
('Application code/artifact','Controlled administrator/release process','Routine operators should not alter the running artifact'),
('Runtime configuration','Approved configuration maintainer','Review identity, thresholds and revision before change'),
('Runtime secrets','Required service account only','Limit disclosure through shell, logs and exports'),
('Telemetry/history files','Writer plus approved readers','Keep commit and read responsibilities distinct'),
('Event-action audit','Authorized workflow service','Prevent client-local edits from erasing accountability'),
('Calibration records','Approved metrology/release owner','Treat coefficients as controlled engineering evidence'),
('Backups','Approved backup/restore role','Protect history and retain recoverability'),
('Operator exports','Authorized operator/reviewer scope','Include context without exposing credentials'),
('OS package updates','Approved administrator','Preserve dependency/platform compatibility'),
('Qt session','Operator account under approved setup','Monitoring need not inherit root privileges')])
x.p('An application directory may need to be read-only to the service while its data directory is writable. Apply permissions to the actual release layout, not to guessed paths. Before changing ownership to suppress an error, determine which process should own the operation and preserve a note of the intended permission boundary.')
x.h('What a command-line base does and does not imply')
x.table(['Inference','Correct interpretation'],[
('“Command-line based” means no graphical interface','Incorrect: the Ubuntu base can host a Qt engineering interface'),
('“Embedded” means the ESP32 runs Linux','Incorrect: the node and Ubuntu gateway are separate'),
('A shell prompt establishes application health','Incorrect: readiness and sensor freshness need their own checks'),
('A custom launcher establishes a new OS distribution','Incorrect: it is an application environment unless broader evidence exists'),
('A gateway-kit BOM identifies the deployed board','Incorrect: actual hardware must be recorded'),
('Remote monitoring needs a public shell','Incorrect: client access and administration are separate boundaries')])

x=BY['qt-ui']
x.h('Reference client snapshot')
x.p('This proposed snapshot shape illustrates how one client update can carry identity, quality and meaning together. It is an interface-review fixture, not the built product\'s unpublished payload or a screen capture. The fixture never changes its source timestamp merely because a client renders it again.')
x.code('json',json.dumps({'snapshot_basis':'documentation fixture','client_contract_revision':'REFERENCE-ONLY','snapshot_revision':10,'record_identity':{'site_id':'bench-site','zone_id':'zone-a','node_id':'bench-node-01','boot_id':'documentation-boot-01','seq':100},'time':{'source_utc':'2026-01-01T00:00:00Z','receive_utc':'2026-01-01T00:00:00.400Z','snapshot_utc':'2026-01-01T00:00:00.600Z','clock_status':'synced','source_age_s':0.6},'channels':{'voltage':{'value':21.6,'unit':'V','quality':'valid'},'current':{'value':3.2,'unit':'A','quality':'valid'},'irradiance':{'value':800.0,'unit':'W/m2','quality':'valid'},'panel_temperature':{'value':45.0,'unit':'degC','quality':'valid'}},'derived':{'power_w':69.12,'expected_power_w':88.3,'shortfall_fraction':round((88.3-69.12)/88.3,9),'analysis_gate':'qualified_reference_fixture','analysis_policy_revision':'REFERENCE-ONLY'},'health':{'source_state':'fresh','transport_state':'connected_reference_fixture','persistence_state':'committed_reference_fixture'},'event':{'event_id':None,'revision':None,'condition_state':'no_event_in_this_snapshot','workflow_state':None}},indent=2))
x.h('Visual interpretation rules')
x.table(['UI element','Engineering rule'],[
('Value card','Unit and channel status remain adjacent to the number'),
('Last-known card','Retain source time and a visible stale/offline meaning'),
('Trend axis','State time basis, units and range; do not hide missing intervals'),
('Energy total','Name the time window and show partial coverage when needed'),
('Event badge','Distinguish active condition, acknowledged workflow and data fault'),
('Node selector','The selected identity must match every displayed panel'),
('Color','Never be the only carrier of fault/quality meaning'),
('Rounding','Display precision must not imply accuracy beyond calibration'),
('Model result','Show the applicable baseline/policy and gate reason'),
('Busy state','Do not freeze interaction while waiting for I/O'),
('Export action','Preserve window/identity rather than exporting only a screenshot'),
('Error dialog','Name the failed boundary without exposing credentials')])

x=BY['python-backend']
x.h('Reference semantic-envelope checks')
x.p('The helper below supplements structural schema validation. It demonstrates a few necessary semantic checks but is not a complete security, plausibility, calibration or timestamp validator. Production ingestion must use the actual released contract and a reviewed reject/quarantine policy.')
x.code('python', '''# Reference checks AFTER strict JSON and JSON Schema validation.
# topic_site/topic_node must come from an already validated topic parser.
def semantic_reasons(payload, topic_site, topic_node, known_calibrations):
    reasons = []
    source = payload["source"]
    time = payload["time"]
    measurements = payload["measurements"]
    status = payload["quality"]["channel_status"]
    if source["site_id"] != topic_site:
        reasons.append("topic_site_mismatch")
    if source["node_id"] != topic_node:
        reasons.append("topic_node_mismatch")
    if time["clock_status"] == "synced" and time["source_utc"] is None:
        reasons.append("synced_without_source_utc")
    value_keys = {
        "voltage": "voltage_v",
        "current": "current_a",
        "irradiance": "irradiance_w_m2",
        "panel_temperature": "panel_temperature_c",
    }
    for channel, value_key in value_keys.items():
        value = measurements[value_key]
        if value is None and status[channel] == "valid":
            reasons.append(f"null_valid_{channel}")
        if status[channel] == "missing" and value is not None:
            reasons.append(f"missing_with_value_{channel}")
    if payload["calibration_id"] not in known_calibrations:
        reasons.append("unknown_calibration")
    current = measurements["current_a"]
    if current is not None and current < 0:
        reasons.append("reverse_current_outside_unidirectional_bench_scope")
    return reasons

# Additional release policy still needs:
# - authenticated site/node scope;
# - UTC parsing, uncertainty, age and future-time handling;
# - per-channel conversion age and V/I alignment;
# - instrument/calibration applicability;
# - duplicate-body collision detection;
# - storage and resource limits;
# - reject/quarantine audit without sensitive payload leakage.''')
x.h('Ingestion outcome contract')
x.table(['Outcome','Record effect','Derived/event effect'],[
('Accepted new','One immutable committed observation','Eligible only under applicable quality/time/replay policy'),
('Duplicate same body','No second observation','No second energy or event side effect'),
('Key/body conflict','Preserve identity fault evidence','No silent replacement of accepted history'),
('Structural reject','No trusted telemetry record','No derived metrics from guessed fields'),
('Semantic quarantine','Retain reason/context under approved policy','No calibrated/live interpretation until resolved'),
('Commit failure','Known uncommitted/pending outcome','Do not claim durable history'),
('Analysis gated','Raw qualified data can still be retained','Explicit unavailable/gated analysis, not healthy score')])

x=BY['website']
x.h('Browser-visible failure contract — reference')
x.table(['Failure category','Display meaning','Safe user option'],[
('Session expired','Access must be renewed','Use approved sign-in without exposing secrets'),
('Scope denied','The requested site/action is not authorized','Return to permitted scope or contact owner'),
('Connection unavailable','Current remote context cannot be obtained','Read labeled last-known context if policy permits'),
('Contract incompatible','Client/backend do not agree on the representation','Use a compatible published release'),
('Node stale','The source observation is not current','Inspect source/link context, not browser refresh alone'),
('Sensor invalid','A channel cannot support interpretation','Read the reason and restrict calculations'),
('Storage degraded','Visible context may not be durable','Notify maintainer and retain evidence'),
('Analysis unavailable','No current qualified performance conclusion','Continue qualified raw monitoring'),
('Event revision conflict','The reviewed event changed before the action','Refresh/review and retry only as authorized'),
('Export incomplete','Requested window cannot be fully represented','Download with explicit coverage or refine scope')])
x.p('A browser refresh is not a repair method for a sensor or writer fault. A page may reconnect successfully while its newest source observation is still stale. The UI should expose these states separately so the engineer can report the correct failure boundary rather than repeatedly reopening the site.')

x=BY['companion-app']
x.h('Mobile offline/cache review')
x.table(['Cache field','Purpose','Must remain true after reconnect'],[
('Record identity','Know which observation was retained','Does not become a new source record'),
('Source UTC and clock status','Interpret age honestly','Does not reset to phone receipt/redraw time'),
('Node/site mapping','Avoid stale selection ambiguity','Still matches the current authorized scope'),
('Channel units and quality','Avoid a naked cached number','Invalid/missing meaning remains visible'),
('Event ID/revision','Avoid actions against unknown state','Reconcile before a new workflow action'),
('Cache creation/expiry','Apply actual retention policy','Does not override source age'),
('Client contract revision','Interpret stored fields','Migrate/reject incompatible cache explicitly'),
('Session/access state','Prevent unauthorized reuse','Revalidate according to actual released policy')])
x.h('Accessibility and compact-screen criteria')
x.bullets(['Keep node identity, quality and source age visible before secondary chart detail.','Use text or shape alongside color for active/stale/invalid states.','Show units without relying on a tooltip that a touch-only user cannot access.','Preserve usable touch targets and avoid accidental acknowledgement.','Make confirmation/context clear for any authorized event action.','Do not reduce long event reasons to an unexplained red icon.','Avoid changing a time window or node selection silently when rotating/resuming.','State the display timezone and retain UTC in exports or detailed evidence.'])

x=BY['mqtt']
x.h('Illustrative delivery timeline')
x.p('All times below are relative documentation fixtures. They explain why delivery, storage and source freshness require separate state. The source clock is assumed synchronized for this example. The exact scheduler and backlog priority are release decisions.')
x.table(['Gateway elapsed time','Input / state','Correct interpretation'],[
('0.0 s','Source observation seq 100 at source t=0','Candidate current observation'),
('0.4 s','Gateway receives seq 100','Arrival recorded independently'),
('0.5 s','Writer commits seq 100','One durable record'),
('0.8 s','Same seq/body delivered again','Duplicate, not another sample'),
('1.0 s','Node produces seq 101','New immutable observation'),
('1–8 s','Node transport unavailable','Source freshness degrades; buffer policy applies'),
('6.1 s','Newest committed source remains t=0','Stale under >5 s reference policy'),
('8.0 s','Connection returns with seq 101 backlog','Arrival does not make source t=1 current'),
('8.2 s','Historical records replay','Idempotent backfill by source identity'),
('8.4 s','Current seq with source t=8 arrives','Potentially fresh after quality/clock checks'),
('8.5 s','Writer commit succeeds','Current durable horizon advances'),
('8.6 s','All clients receive compatible context','Each displays the same source identity/age meaning')])

x=BY['electrical']
x.h('Register conversion review points')
x.table(['Quantity','Reference conversion','Review concern'],[
('INA226 shunt voltage','signed raw × 2.5 microvolt','Sign extension and ±81.92 mV range'),
('INA226 bus voltage','raw × 1.25 mV','36 V IC limit does not enlarge bench scope'),
('INA226 current','signed raw × configured current LSB','Actual CAL and shunt value must match'),
('INA226 power','raw × 25 × configured current LSB','Do not confuse LSB scaling with system calibration'),
('ADS1115 input','signed raw × selected PGA LSB','Actual gain, mux, common-mode and completion state'),
('DS18B20 temperature','decode actual resolution and valid conversion','CRC, conversion age and mounting still apply')])
x.p('At the reference ±0.512 V ADS1115 setting, a 160 mV nominal irradiance signal corresponds to 10,240 counts before correction. At 21.6 V, the INA226 nominal bus register is 17,280 counts. These are arithmetic check points, not acquired register dumps. Do not publish them as logs from the actual prototype.')

x=BY['storage-energy']
x.h('Export manifest and coverage')
x.p('An export must remain understandable when separated from the running UI. Include the selected identity, window, time basis, units, quality, calibration/configuration and coverage. If a client exports an aggregated trend, name the aggregation and preserve access to the raw evidence used for a claim.')
x.code('json',json.dumps({'manifest_basis':'reference export contract','export_id':None,'created_utc':None,'requested_by_scope':None,'selection':{'site_id':None,'zone_id':None,'node_ids':[],'start_utc':None,'end_utc':None,'display_timezone':None},'contents':{'telemetry_rows':None,'event_rows':None,'raw_or_aggregated':None,'aggregation_method':None},'coverage':{'valid_integrated_seconds':None,'excluded_seconds':None,'exclusion_reasons':{},'first_source_utc':None,'last_source_utc':None},'revisions':{'gateway_release':None,'schema':None,'configuration':None,'calibration_ids':[],'integration_policy':None,'analysis_policy':None},'units':{'voltage':'V','current':'A','power':'W','energy':'Wh','irradiance':'W/m2','temperature':'degC'},'checksums':[],'limitations':[]},indent=2))
x.h('Write-volume sensitivity')
x.table(['Assumed bytes/record','10 nodes × 1 Hz × 30 days','Scope'],[
('100 B','2.592 GB raw','Compact planning scenario'),
('200 B','5.184 GB raw','Baseline capacity assumption'),
('400 B','10.368 GB raw','Doubled-payload sensitivity'),
('800 B','20.736 GB raw','Verbose-payload sensitivity'),
('1600 B','41.472 GB raw','Large-envelope sensitivity')])
x.p('The sensitivity table excludes indexes, transaction/WAL overhead, logs, OS and backup copies in every row. The nominal 64 GB allowance is not a guaranteed retention result. Measure the actual serialized record, insertion behavior, filesystem growth and write endurance on the selected storage device.')

x=BY['validation']
x.h('Focused acceptance playbooks')
x.procedure('WAN-only outage playbook',[
 'Record the active local release, node/source identity and event revision.',
 'Confirm the planned test interrupts WAN only and does not compromise electrical safety.',
 'Verify the LAN, gateway, broker and onsite UI are initially functioning.',
 'Interrupt the approved external access path under authorized conditions.',
 'Observe whether local acquisition/history and Qt remain useful.',
 'Observe website/app disconnection and source-age behavior.',
 'Restore access and distinguish backfill from a qualified live observation.',
 'Compare common event identity/revision and retain sanitized captures.',
 'Record pass/fail/inconclusive against the local-first requirement.'])
x.procedure('QoS duplicate/replay playbook',[
 'Use a controlled test dataset outside operational history.',
 'Record the initial committed key and energy-interval inventory.',
 'Deliver a reference record followed by an identical redelivery.',
 'Confirm one committed observation and no duplicate energy contribution.',
 'Replay an older source-time record and inspect its history/live treatment.',
 'Exercise a same-key/different-body fixture through the approved test harness.',
 'Verify a named identity-conflict outcome rather than silent overwrite.',
 'Restart the test subscriber/writer only through the approved procedure.',
 'Reconcile keys, events and integration intervals after recovery.'])
x.procedure('Freshness/clock playbook',[
 'Use qualified clocks or a controlled reference-time harness.',
 'Record the source, receive and client-visible timestamps independently.',
 'Stop new observations and verify the stale transition after >5 s.',
 'Inject an explicitly labeled unsynchronized-clock fixture.',
 'Verify that receive age is not advertised as physical-observation age.',
 'Exercise future and nonpositive-time examples without changing a live plant clock.',
 'Confirm excluded integration intervals and visible clock-quality reason.',
 'Restore the qualified time basis and review the recovery transition.'])
x.procedure('Cross-client event playbook',[
 'Select one controlled node/event fixture in Qt, website and app.',
 'Compare identity, units, source time, gate and event revision.',
 'Perform an authorized acknowledgement from one client.',
 'Verify the condition stays active when the physical/data rule remains active.',
 'Review the resulting workflow/action audit in the other clients.',
 'Exercise a stale-revision action using approved test identities.',
 'Confirm the released conflict policy and authoritative resulting revision.',
 'Record any representation mismatch without correcting the fixture locally.'])

x=BY['security']
x.h('Broker/access scope review — reference')
x.table(['Identity class','Minimum intended scope','Forbidden shortcut'],[
('Sensor node','Its approved site/node telemetry/health publication','Publish to another node or arbitrary wildcard topic'),
('Gateway ingestion','Approved telemetry subscription scope','Use a universal administrator credential for convenience'),
('Monitoring reader','Approved client data scope','Read private broker/system topics without need'),
('Event operator','Approved event-action scope','Change sensor calibration or platform users'),
('Administrator','Explicit maintenance scope','Leave broad credentials in client code'),
('Retired node','No active operational credential','Retain access indefinitely after removal')])
x.h('Sanitization before evidence publication')
x.table(['Material','Remove / protect','Retain for interpretation'],[
('Logs','Secrets, tokens and unnecessary private addresses','UTC, error category and sanitized record identity'),
('Screenshots','Passwords, personal accounts and sensitive site detail','Build, node/time/quality context where approved'),
('Exports','Unauthorized site/person identifiers','Units, window, revisions and coverage'),
('Configuration','Secret values and private credential paths','Schema, nonsecret thresholds and revision'),
('Video','Visible credentials and unauthorized people/sites','Authentic behavior and stated test conditions'),
('Backup manifest','Sensitive access locations or key material','Checksums, schema and restoration context')])

x=BY['performance']
x.h('Executable documentation arithmetic')
x.p('The following bundled module makes the numerical examples reproducible. It is documentation tooling, not recovered product source and not an implemented hardware/backend release. Running its tests verifies only these formulas and edge cases. The tests do not establish sensor accuracy, timing, app behavior, plant performance or certification.')
x.code('python',(BASE/'docs/tools/reference_math.py').read_text())
x.h('Arithmetic and edge-case test source')
x.p('These unit tests are included so another reviewer can reproduce the documentation checks. Their fixtures are labeled references; none is an actual plant event or captured prototype result. Execute them with the documentation command shown in Installation.')
x.code('python',(BASE/'docs/tools/test_reference_math.py').read_text())
