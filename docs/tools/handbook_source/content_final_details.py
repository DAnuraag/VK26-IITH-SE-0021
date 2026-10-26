from doc_engine import CHAPTERS
import json
BY={c.slug:c for c in CHAPTERS}

x=BY['firmware']
x.h('Reference node-health message')
x.p('Health metadata explains acquisition and transport behavior without pretending to be another electrical sample. This fixture supplies no measured counters; null means that the actual value must come from the running node. The real firmware must publish its own supported health contract.')
x.code('json',json.dumps({'message_basis':'reference health contract','message_type':'health','node_id':'bench-node-01','boot_id':None,'firmware_revision':None,'reset_reason':None,'uptime_ms':None,'clock':{'status':None,'source_utc':None,'synchronization_uncertainty_s':None},'acquisition':{'intended_cadence_hz':1,'completed_cycles':None,'missed_deadlines':None,'last_conversion_status':{}},'queue':{'capacity_target_records':600,'pending_records':None,'overflow_count':None,'first_pending_seq':None,'last_pending_seq':None,'durability_policy':None},'transport':{'connection_state':None,'reconnect_count':None,'last_publish_outcome':None,'last_confirmed_delivery_seq':None},'power':{'supply_diagnostic_available':None,'optional_battery_voltage_v':None}},indent=2))
x.h('Reset and loss accounting')
x.table(['Transition','Identity effect','Evidence boundary'],[
('Normal reconnect without reboot','Keep boot identity and immutable sequence','Network delivery may repeat'),
('Actual controller reboot','Establish new boot identity','RAM queue may be lost unless durable behavior is verified'),
('Queue overflow','Keep explicit missing/lost record inventory','Do not claim a complete ten-minute history'),
('Configuration reload','Preserve effective configuration revision','Do not reinterpret earlier records silently'),
('Clock becomes qualified','Keep prior time-quality state','Earlier unsynced UTC is not invented retrospectively')])

x=BY['data-quality']
x.h('Coverage is not a single percentage')
x.p('Different conclusions require different coverage. A record can contribute valid electrical power while missing temperature; it may therefore support a raw power trend but not the temperature-corrected baseline. Similarly, a valid instantaneous power point does not establish the energy contribution of an adjacent unknown interval. Report coverage for the claim being made.')
x.table(['Claim','Coverage inventory to retain'],[
('Voltage trend','Valid voltage points, source-time basis and gaps'),
('Current trend','Valid current points, calibrated range and direction'),
('Instantaneous power','Accepted V/I pairs and pairing age'),
('Energy','Included intervals, excluded seconds and integration revision'),
('Expected-output comparison','Qualified G/T/output/model intervals'),
('Persistent alert','Continuous qualifying duration and gate transitions'),
('Detection metrics','Labeled events, excluded cases and evaluation split'),
('Uptime','Defined component/path and observation method'),
('Local-first operation','WAN-only condition with surviving local dependencies')])
x.h('Time-window reporting')
x.code('text', '''Recommended export labels:
    requested window: start UTC to end UTC
    available source window: first source UTC to last source UTC
    display timezone: explicitly named
    valid electrical-pair count: actual count
    included energy duration: actual seconds
    excluded energy duration: actual seconds, by reason
    qualified analysis duration: actual seconds
    clock-uncertain records: actual count
    backfilled records: actual count

Do not equate “records received” with continuous measurement coverage.
Do not add overlapping excluded intervals twice.
State whether window endpoints are inclusive or half-open.
A half-open [start, end) convention avoids adjacent-window double counting.''')

x=BY['mechanical']
x.h('Fit and assembly tolerance review')
x.table(['Interface','Dimension / tolerance to establish','Failure prevented'],[
('PCB to supports','Hole positions, boss height and board clearance','Board stress or unsupported connectors'),
('Lid to body','Mating faces, fastener engagement and tolerance stack','Interference or loose closure'),
('Gasket to groove','Compression, width and corner continuity','Untested seal assumed from nominal thickness'),
('Cable to gland','Actual cable diameter, grip and bend radius','Ingress path or conductor strain'),
('Plate to case','Fastener access, contact and electrical isolation','Unexpected thermal/ground path'),
('Controller to lid','Component height and cable/service loop','Crushed components or inaccessible connectors'),
('Isolation region','Actual clearance to conductors and hardware','Barrier defeated by mounting or routing'),
('Service opening','Removal sequence and wire retention','Damage during inspection')])
x.p('Nominal outer dimensions alone cannot prove internal fit. A finished concept should be checked with actual component models and an assembly sequence. Keep any future manufacturing drawing revision distinct from the envelope STEP files supplied here.')

x=BY['configuration']
x.h('Configuration validation failures')
x.table(['Candidate problem','Required decision'],[
('Unknown schema revision','Reject until supported by the actual release'),
('Site/node identity missing','Do not start an ambiguously scoped monitor'),
('Clock uncertainty limit absent','Do not assert qualified physical source age'),
('Energy maximum interval absent','Require cadence-specific reviewed policy'),
('Baseline coefficients absent','Keep raw monitoring; mark model unavailable'),
('Stability criterion absent','Do not claim the environmental gate is validated'),
('Clear policy absent','Do not invent event-clear behavior in a client'),
('Secret reference unreadable','Expose access/dependency fault without logging the secret'),
('Calibration ID unknown','Restrict interpretation according to quarantine policy'),
('Threshold changed only in one client','Reject divergent local interpretation; reconcile revision')])
