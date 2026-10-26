from doc_engine import c,event_table,mermaid
import json

x=c('Power, Energy and Local Storage','storage-energy')
x.p('Electrical power and energy need explicit measurement points and timing. DC power at the proposed shunt/bus location is not automatically inverter AC power, delivered grid energy or plant yield. The original project requires V/A/W/Wh/kWh and local history; the following formulas and SQL are reference implementations for that requirement.')
x.h('Power and energy definitions')
x.code('text', '''Instantaneous DC power:
    P_W = V_V × I_A
For matched readings of 21.6 V and 3.20 A:
    P = 69.12 W

Trapezoidal interval energy for two accepted endpoints:
    delta_Wh = 0.5 × (P_previous + P_current) × delta_t_s / 3600
    E_Wh = sum of accepted interval contributions
    E_kWh = E_Wh / 1000

Example accepted interval:
    P_previous = 60 W; P_current = 80 W; delta_t = 5 s
    delta_Wh = 0.5 × 140 × 5 / 3600 = 0.097222... Wh

Do not integrate when:
    either endpoint is invalid or missing;
    elapsed time is nonpositive;
    elapsed time exceeds the approved gap threshold;
    identity/boot/time continuity is not established.
Do not treat a missing interval as zero generation.
Keep excluded duration and the policy revision.''')
x.fig('energy_gaps','Calculated 10-minute power/energy example at 5 s spacing. Samples from t=250 through 320 s are invalid, so intervals from the last valid endpoint at 245 s to the next at 325 s are excluded. The flat energy trace is unknown contribution, not proof of zero generation.')
x.h('Reference integration helper')
x.code('python', '''from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class PowerPoint:
    node_id: str
    boot_id: str
    elapsed_s: float
    power_w: float | None
    valid: bool

def integrate_interval(previous, current, max_gap_s=2.0):
    """Return qualified Wh and excluded seconds for one interval."""
    dt = current.elapsed_s - previous.elapsed_s
    if dt <= 0 or not isfinite(dt):
        return {"wh": 0.0, "excluded_s": 0.0,
                "reason": "nonpositive_or_invalid_time"}
    same_source = (
        current.node_id == previous.node_id
        and current.boot_id == previous.boot_id
    )
    values = (previous.power_w, current.power_w)
    valid_values = all(v is not None and isfinite(v) for v in values)
    if not same_source:
        reason = "identity_discontinuity"
    elif not previous.valid or not current.valid or not valid_values:
        reason = "invalid_endpoint"
    elif dt > max_gap_s:
        reason = "gap_exceeds_policy"
    else:
        contribution = 0.5 * sum(values) * dt / 3600.0
        return {"wh": contribution, "excluded_s": 0.0, "reason": "valid"}
    return {"wh": 0.0, "excluded_s": dt, "reason": reason}

# This reference function does not claim a completed application test.
# The released policy must define reverse power and clock transitions.
# Never sum the same committed interval twice during replay.''')
x.h('Local persistence model')
x.fig('storage_model','Proposed logical telemetry, events, calibration and configuration entities. SQLite/WAL is a reference choice, not a verified engine in the built release.')
x.p('A local store supports offline history and inspection evidence, but only if commit outcomes, identity and backup behavior are explicit. The reference schema separates raw observations from derived values and human workflow. It retains source and receive times independently. Use a migration strategy and actual implementation review before adopting any SQL below.')
x.code('sql', '''-- Reference SQLite schema. Not a released application database.
PRAGMA foreign_keys = ON;
-- WAL is a reference deployment option, not proof of crash safety.
PRAGMA journal_mode = WAL;

CREATE TABLE calibration_record (
    calibration_id TEXT PRIMARY KEY,
    channel TEXT NOT NULL,
    device_identity TEXT NOT NULL,
    coefficient_json TEXT NOT NULL,
    reference_identity TEXT NOT NULL,
    applicable_range_json TEXT NOT NULL,
    reviewed_utc TEXT,
    record_sha256 TEXT NOT NULL
);

CREATE TABLE configuration_revision (
    config_revision TEXT PRIMARY KEY,
    schema_version TEXT NOT NULL,
    config_sha256 TEXT NOT NULL,
    effective_utc TEXT,
    approved_by TEXT,
    reason TEXT NOT NULL
);

CREATE TABLE telemetry_record (
    record_id INTEGER PRIMARY KEY,
    site_id TEXT NOT NULL,
    zone_id TEXT NOT NULL,
    node_id TEXT NOT NULL,
    boot_id TEXT NOT NULL,
    seq INTEGER NOT NULL CHECK (seq >= 0),
    source_utc TEXT,
    receive_utc TEXT NOT NULL,
    uptime_ms INTEGER NOT NULL CHECK (uptime_ms >= 0),
    clock_status TEXT NOT NULL,
    voltage_v REAL,
    current_a REAL,
    irradiance_w_m2 REAL,
    panel_temperature_c REAL,
    channel_quality_json TEXT NOT NULL,
    calibration_id TEXT NOT NULL,
    config_revision TEXT NOT NULL,
    firmware_revision TEXT NOT NULL,
    envelope_sha256 TEXT NOT NULL,
    raw_payload_json TEXT NOT NULL,
    UNIQUE (node_id, boot_id, seq)
);

CREATE INDEX telemetry_node_source
    ON telemetry_record(node_id, source_utc);
CREATE INDEX telemetry_receive
    ON telemetry_record(receive_utc);

CREATE TABLE derived_metric (
    metric_id INTEGER PRIMARY KEY,
    record_id INTEGER NOT NULL REFERENCES telemetry_record(record_id),
    metric_revision TEXT NOT NULL,
    power_w REAL,
    expected_power_w REAL,
    residual_fraction REAL,
    analysis_quality TEXT NOT NULL,
    UNIQUE (record_id, metric_revision)
);

CREATE TABLE energy_interval (
    interval_id INTEGER PRIMARY KEY,
    previous_record_id INTEGER NOT NULL REFERENCES telemetry_record(record_id),
    current_record_id INTEGER NOT NULL REFERENCES telemetry_record(record_id),
    integration_revision TEXT NOT NULL,
    elapsed_s REAL NOT NULL CHECK (elapsed_s > 0),
    contribution_wh REAL,
    included INTEGER NOT NULL CHECK (included IN (0, 1)),
    exclusion_reason TEXT,
    UNIQUE (previous_record_id, current_record_id, integration_revision)
);

CREATE TABLE event_record (
    event_id TEXT PRIMARY KEY,
    node_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    policy_revision TEXT NOT NULL,
    condition_onset_utc TEXT,
    qualified_alert_utc TEXT,
    latest_revision INTEGER NOT NULL,
    condition_state TEXT NOT NULL,
    workflow_state TEXT NOT NULL
);

CREATE TABLE event_action (
    action_id INTEGER PRIMARY KEY,
    event_id TEXT NOT NULL REFERENCES event_record(event_id),
    expected_revision INTEGER NOT NULL,
    resulting_revision INTEGER NOT NULL,
    actor_identity TEXT NOT NULL,
    action_utc TEXT NOT NULL,
    action_type TEXT NOT NULL,
    note TEXT,
    outcome TEXT NOT NULL
);''')
x.p('Calibration and configuration identifiers are preserved even when records are quarantined for unknown applicability. The reference SQL therefore does not force an unverified calibration relationship into a trusted foreign-key match. A real release may use a separate quarantine store, approved foreign keys and normalized quality tables; document that actual choice.')
x.h('Retention capacity model')
x.fig('retention_model','Calculated raw payload growth for ten nodes at 1 Hz and an assumed 200 bytes per record. The 1.5× and 2× curves are planning scenarios, not database benchmarks.')
x.code('text', '''Records per node per day = 86400
Records for 10 nodes over 30 days = 25920000
Assumed compact record size = 200 bytes
Raw bytes = 10 × 200 × 86400 × 30 = 5184000000
Decimal storage = 5.184 GB
Binary storage ≈ 4.828 GiB

1.5× planning scenario = 7.776 GB
2× planning scenario = 10.368 GB
Neither factor includes an independently measured write amplification.
A 64 GB device must also hold OS, indexes, WAL, logs and backups.
The verbose reference JSON above is larger than 200 bytes.
Measure actual serialized and on-disk sizes before approving retention.''')
x.h('Reference diagnostic queries')
x.code('sql', '''-- Latest source observations for a selected node.
SELECT node_id, boot_id, seq, source_utc, receive_utc, clock_status
FROM telemetry_record
WHERE node_id = :approved_node_id
ORDER BY source_utc DESC
LIMIT 20;

-- Count records by boot to investigate a reboot boundary.
SELECT boot_id, COUNT(*) AS row_count, MIN(seq), MAX(seq)
FROM telemetry_record
WHERE node_id = :approved_node_id
GROUP BY boot_id;

-- Explain missing integrated time instead of assuming zero generation.
SELECT exclusion_reason, SUM(elapsed_s) AS excluded_seconds
FROM energy_interval
WHERE included = 0
GROUP BY exclusion_reason;

-- Compare event condition with operator workflow.
SELECT event_id, event_type, condition_state, workflow_state,
       latest_revision, policy_revision
FROM event_record
WHERE node_id = :approved_node_id;

-- These are read-only examples for the reference schema only.
-- Verify actual schema and access permissions before using a query.''')

x=c('Edge Analytics and Explainable Anomaly Logic','analytics')
x.fig('anomaly_flow','Proposed quality-gated expected-output comparison and persistence logic. Predictive-maintenance support is not a validated failure-date forecast.')
x.p('ARKA AI uses local context to turn monitoring data into an inspectable maintenance signal. An initial explainable baseline can compare measured DC power against expected output for the present irradiance and panel temperature. More advanced models are future options, not prerequisites for representing quality honestly. Every deployed model needs a defined scope, input/calibration lineage, version and evaluation dataset.')
x.h('Reference baseline')
x.code('text', '''Illustrative linear baseline:
    P_expected = P_ref × (G / G_ref)
                 × [1 + gamma × (T_panel − T_ref)]
Where:
    P_ref is a healthy reference at the SAME measurement point;
    G_ref is the reference irradiance (often 1000 W/m²);
    T_ref is the reference temperature (often 25 °C);
    gamma is an applicable power-temperature coefficient per °C.

Guarded normalized shortfall:
    residual = (P_expected − P_measured) / max(P_expected, P_floor)

Requirements before interpretation:
    valid and sufficiently time-aligned measurements;
    applicable healthy reference and coefficient;
    expected power above the chosen floor;
    G >= 200 W/m² initial gate;
    irradiance sufficiently stable under a documented criterion;
    no known startup/maintenance/curtailment exclusion.

This simplified model does not inherently model MPPT, shading geometry,
spectral mismatch, inverter clipping, soiling, cable losses or curtailment.
Fit/validate the baseline at the actual DC measurement location.''')
x.p('The reference panel rating and temperature coefficient are not supplied, so no particular P_ref or gamma is asserted as a project measurement. The 88.3 W HMI expectation is an illustrative display value, not a derived claim about an identified module. Define “stable irradiance” quantitatively in a released policy; the original material does not establish its exact window/slope threshold.')
x.h('Residual persistence timing')
x.fig('residual_persistence','Calculated example: a 20% shortfall begins at t=120 s. With valid/stable context and a 15% gate, 180 elapsed seconds qualify at t=300 s. The first qualifying sample starts at zero elapsed persistence; it does not count as one second.')
x.code('python', '''# Reference state machine. It uses elapsed monotonic time, not sample count.
class PersistentShortfall:
    def __init__(self, threshold=0.15, required_s=180.0, max_gap_s=2.0):
        self.threshold = threshold
        self.required_s = required_s
        self.max_gap_s = max_gap_s
        self.started_at = None
        self.previous_time = None
        self.previous_qualified = False

    def update(self, time_s, residual, gates_ok):
        dt = None if self.previous_time is None else time_s - self.previous_time
        continuous = dt is not None and 0 < dt <= self.max_gap_s
        qualified = gates_ok and residual is not None and residual > self.threshold
        if not qualified:
            self.started_at = None
            state = "not_qualifying"
        elif not continuous or not self.previous_qualified:
            self.started_at = time_s
            state = "pending"
        else:
            elapsed = time_s - self.started_at
            state = "qualified" if elapsed >= self.required_s else "pending"
        elapsed = 0.0 if self.started_at is None else time_s - self.started_at
        self.previous_time = time_s
        self.previous_qualified = qualified
        return {"state": state, "persistence_s": elapsed}

# In this reference, a gate loss or unacceptable gap resets persistence.
# A deployed alternative must publish its hold/reset/clear semantics.
# Acknowledgement is deliberately not part of this condition timer.''')
x.h('Fault taxonomy and confounders')
x.table(['Observation','Possible explanations','Inspection context'],[
('Persistent low power with stable G/T','Electrical loss, shade, soiling, baseline mismatch','Confirm measurement point, load/MPPT and reference-sensor condition'),
('Low current with plausible voltage','Reduced loading, disconnected path or irradiance change','Inspect safely under authorized electrical procedure'),
('Voltage outside normal bench range','Source/load condition, miswire or sensing fault','Do not diagnose from a clipped/saturated monitor'),
('Abrupt temperature jump','Sensor contact/CRC issue or real thermal change','Compare sensor quality and physical mounting'),
('All channels stop together','Node power, Wi-Fi, broker or gateway issue','Use sequence, boot and dependency state'),
('Only irradiance deviates','Reference shading, dirt, cable or ADC problem','Inspect pyranometer mounting and signal chain'),
('Frequent short residual spikes','Clouds, timing mismatch or unstable operating point','Review environmental stability and alignment'),
('Expected power implausible','Wrong model, rating, units or revision','Suspend performance classification pending model review')])
x.h('Validation for predictive-maintenance claims')
x.table(['Evaluation item','Required definition'],[
('Target event','What physical/operational condition is being predicted or detected'),
('Label process','Who verifies the condition and with what evidence'),
('Dataset split','Time/site separation that prevents leakage'),
('Class balance','Actual positive/negative event inventory'),
('Precision','TP / (TP + FP), with zero-denominator handling'),
('Recall','TP / (TP + FN), with zero-denominator handling'),
('Detection latency','Condition onset to qualified visible event'),
('False-alert burden','Events per operating time under intended conditions'),
('Model scope','Plant/node/environment window where the model is applicable'),
('Uncertainty','Confidence intervals or justified limitations for the sample size'),
('Drift review','Input/label changes and recalibration/retraining trigger'),
('Explainability','Input, baseline, residual, gate and policy available to the engineer')])
x.p('The proposed held-out targets are at least 90% precision and 85% recall. They have not been demonstrated in supplied records. Detecting a persistent deviation is not the same as predicting remaining useful life. Avoid language that promises a failure date, guaranteed generation recovery or safe autonomous action.')

x=c('Alerts, Acknowledgement and Maintenance Workflow','alerts')
x.fig('alert_lifecycle','Reference condition and human-workflow sequence. Acknowledged does not mean cleared or repaired.')
x.p('An alert has at least two axes: the physical/data condition and the human handling state. A technician may acknowledge a still-active shortfall, or a transient may clear before anyone reviews it. Keeping those axes separate prevents an operator action from erasing the engineering reason for the event.')
x.table(['Condition state','Meaning','Workflow consequence'],[
('Not qualifying','Residual/gates do not meet onset rule','No persistent-performance event from this rule'),
('Pending','Qualified shortfall has begun but persistence is incomplete','Show context without claiming a qualified alert'),
('Active','Persistence/onset policy reached','Create or update a traceable event'),
('Condition cleared','Clear policy satisfied','Retain event history and require appropriate closure'),
('Data unavailable','Observation cannot support condition decision','Show data-health reason; do not imply recovery')])
x.table(['Workflow state','Meaning','Required audit'],[
('New','Event not yet reviewed','Event identity, onset, alert time, reason and revision'),
('Acknowledged','Authorized person has seen/accepted handling','Actor, action UTC and referenced event revision'),
('Inspecting','Approved maintenance process underway','Task/permit scope as applicable'),
('Resolved','Action/outcome recorded and closure rule met','Finding, action, verification window and reviewer'),
('Closed without repair','Documented explanation or non-fault outcome','Reason and evidence; raw observations preserved')])
x.h('Reference event envelope')
x.code('json',json.dumps({'example_basis':'documentation fixture, not a recorded event','event_id':'reference-shortfall-event-01','node_id':'bench-node-01','event_type':'persistent_power_shortfall','policy_revision':'REFERENCE-ONLY','revision':1,'condition':{'state':'active','onset_utc':'2026-01-01T00:00:00Z','qualified_alert_utc':'2026-01-01T00:03:00Z','residual_fraction':0.20,'threshold_fraction':0.15,'persistence_s':180,'quality_gate':'qualified_reference_fixture'},'workflow':{'state':'new','acknowledged_by':None,'acknowledged_utc':None},'evidence':{'first_seq':120,'latest_seq':300,'boot_id':'documentation-boot-01','calibration_id':'REFERENCE-ONLY','config_revision':'REFERENCE-ONLY'}},indent=2))
x.h('Concurrent acknowledgement')
x.p('A client action should name the event and the revision the operator reviewed. If another client has already changed that revision, the backend should apply the released concurrency rule rather than overwriting blindly. The response must distinguish successful acknowledgement, already-acknowledged state, permission failure and revision conflict. Exact API routes are not published here.')
x.code('text', '''reference acknowledgement request:
    event_id
    expected_revision
    actor/session identity from authenticated context
    action type
    optional inspection note

server checks:
    approved site/event scope
    workflow permission
    current event revision
    transition validity
    audit persistence

response semantics:
    action outcome
    resulting event revision
    current condition state
    current workflow state
    authoritative action time
    conflict/retry reason when not accepted''')
x.h('Maintenance closure checklist')
x.bullets(['Confirm the inspected node/zone matches the event identity.','Record the approved work scope and physical finding without exposing unsafe work instructions.','Preserve the original observations, environmental gates and model revision.','Record the action separately from the acknowledgement.','Observe a suitable post-action window with valid data.','If the condition persists, keep it active or reopen under a documented rule.','Distinguish sensor/data repair from a confirmed solar-equipment repair.','Close with evidence and reviewer identity rather than clearing the display alone.'],check=True)

x=c('Installation and Development Environment','installation')
x.p('A runnable product installation requires the actual source or release artifact, dependency lock, gateway target, configuration schema and start commands. Those were not present in the inspected public repository root. This section therefore separates a release handover checklist from installation of the documentation toolchain included in this package.')
x.h('Product-release handover gate')
x.table(['Item','Why installation depends on it','Present status'],[
('Gateway hardware/architecture','Determines OS image, drivers and artifacts','Exact built hardware not supplied'),
('Ubuntu image/release','Determines supported packages and update policy','Ubuntu base confirmed; exact version unspecified'),
('Application source/artifact','Provides the executable code','Not published in the inspected root'),
('Dependency lock','Pins compatible Python/Qt/network/storage libraries','Not supplied'),
('Backend entry point','Defines actual launch command','Not supplied; no invented filename'),
('Qt entry point','Defines approved session/display launch','Not supplied'),
('Broker configuration','Defines listener, topic scope and credentials','Exact deployed settings unspecified'),
('Data path/schema','Defines migration and backup behavior','Reference schema in this handbook only'),
('Web/app build artifacts','Defines supported access clients','Built confirmed; release details not supplied'),
('Configuration/secrets','Defines safe site identity and access','Reference examples only'),
('Calibration record','Defines trusted coefficients/ranges','No executed record supplied'),
('Rollback procedure','Defines recovery from an unsuccessful update','Must accompany product release')])
x.h('Documentation package layout')
x.code('text', '''ARKA_AI_Documentation/
├── README.md                     # Exactly 5,000 physical lines
├── README.html                   # Offline visual companion
├── requirements-docs.txt          # Documentation dependencies, not product deps
└── docs/
    ├── assets/                   # 38 SVG masters + PNG fallbacks
    │   └── figure_registry.json
    ├── cad/                      # Proposed packaging STEP / source assets
    ├── data/                     # Calculated/planned CSV datasets
    ├── fonts/                    # Embedded figure fonts and OFL licenses
    ├── references/
    │   ├── ARKA_AI_Stage1.pdf
    │   └── ARKA_AI_Ecosystem_Presentation.pdf
    └── tools/
        ├── render_figures.py      # Python diagrams/charts/data
        ├── vector_canvas.py       # Standalone SVG drawing helper
        ├── reference_math.py      # Executable documentation calculations
        ├── test_reference_math.py # Documentation arithmetic/edge-case checks
        ├── check_readme.py        # Line/link/schema/data checks
        ├── build_offline_html.py  # Self-contained visual companion
        ├── build_handbook.py      # Rebuild the authored 5,000-line README
        └── handbook_source/      # Authored chapters and Markdown renderer''')
x.h('Reproduce documentation figures')
x.p('The following commands operate on this documentation package only. They do not install or start the ARKA monitoring software. Use a virtual environment and review dependency versions for the host platform. Font files and their licenses are bundled so the diagrams do not depend on a remote font service.')
x.code('bash', '''# Start from the extracted documentation-package root.
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-docs.txt

# Regenerate diagrams, PNG fallbacks and calculated/planned CSV files.
python docs/tools/render_figures.py

# Run documentation calculations and structural checks.
python -m unittest discover -s docs/tools -p 'test_reference_math.py'
python docs/tools/check_readme.py

# Rebuild the offline companion after an intentional README/asset edit.
python docs/tools/build_offline_html.py

# None of these commands launches the unpublished product application.''')
x.h('Release-specific setup sequence')
x.procedure('Before installing the actual monitoring release',[
 'Obtain the team-approved artifact/source and verify its manifest/checksum.',
 'Confirm target hardware, Ubuntu version and storage/display/network requirements.',
 'Read installation and migration instructions for that exact release.',
 'Back up any existing configuration, calibration and historical records.',
 'Create least-privilege service/operator identities using the approved account policy.',
 'Install the locked runtime without substituting arbitrary latest packages.',
 'Provision broker/access secrets outside public source and exported diagnostics.',
 'Load reviewed site/node mapping and calibration/configuration revisions.',
 'Run controlled startup, quality and local-connectivity checks.',
 'Record acceptance evidence and establish the rollback point before handover.'])
x.p('A cloned README is not a runtime application. Avoid a fabricated quick-start that invokes files the repository does not contain. When the team publishes a release, replace this handover boundary with tested commands and retain a record of the supported environment.')

x=c('Configuration and Secret Management','configuration')
x.p('Configuration is engineering evidence: it determines channel scope, thresholds, timing, quality gates and access. The reference YAML below is deliberately not production-ready. Null fields identify choices that need an actual reviewed value. Secrets are referenced through protected runtime storage, never embedded in documentation.')
x.h('Reference configuration shape')
x.code('yaml', '''# Reference contract; not an actual released ARKA configuration file.
schema_version: "reference-1"
config_revision: "REFERENCE-ONLY"
site:
  site_id: "bench-site"
  zone_id: "zone-a"
  node_ids:
    - "bench-node-01"
  display_timezone: "Asia/Kolkata"
  storage_time_basis: "UTC"

acquisition:
  cadence_hz: 1
  maximum_voltage_current_pair_age_s: null  # Requires review.
  temperature_max_age_s: null              # Requires review.
  node_queue_capacity_records: 600
  overflow_policy: null                    # Must be documented/tested.

quality:
  live_display_age_target_s: 3
  stale_after_s: 5
  source_clock_uncertainty_limit_s: null
  future_time_tolerance_s: null
  bench_voltage_min_v: 12
  bench_voltage_max_v: 24
  bench_current_max_a: 5
  characterized_temperature_min_c: -10
  characterized_temperature_max_c: 85
  irradiance_analysis_max_w_m2: 1500

transport:
  node_gateway_protocol: "MQTT"
  topic_root: "arka/v1"
  qos: 1
  broker_uri: null                         # Actual approved endpoint.
  credential_reference: null               # Protected secret locator.
  tls_policy: null                         # Actual deployed policy.
  reconnect_backoff_policy: null
  retained_sample_freshness: "source_time_checked"

storage:
  engine: null                             # Release must declare it.
  data_directory: null
  retention_days_target: 30
  node_count_target: 10
  nominal_payload_bytes_assumption: 200
  proposed_device_capacity_gb: 64
  low_space_warning_threshold: null
  low_space_stop_threshold: null
  backup_policy_revision: null

energy:
  method: "trapezoid_with_two_valid_endpoints"
  maximum_interval_s: null                 # Cadence-specific review.
  integrate_across_boot: false
  missing_interval_policy: "exclude_and_report"
  reverse_power_policy: null

analysis:
  expected_output_model_revision: null
  healthy_reference_power_w: null
  reference_irradiance_w_m2: 1000
  reference_temperature_c: 25
  temperature_coefficient_per_c: null
  minimum_expected_power_w: null
  irradiance_gate_min_w_m2: 200
  irradiance_stability_window_s: null
  irradiance_stability_limit: null
  residual_threshold_fraction: 0.15
  persistence_s: 180
  alert_end_to_end_target_s: 210
  quality_gate_loss_policy: "reset_reference_timer"
  condition_clear_threshold_fraction: null
  condition_clear_persistence_s: null

access:
  client_contract_revision: null
  operator_role_policy: null
  administrator_role_policy: null
  session_policy_revision: null
  audit_retention_policy: null

calibration:
  voltage_current_record_id: null
  irradiance_record_id: null
  temperature_record_id: null

# Missing required values should fail review/startup clearly.
# Do not convert a null safety/metrology setting into a permissive default.''')
x.h('Configuration change procedure')
x.procedure('Apply a controlled revision',[
 'State the problem, intended change and affected nodes/clients.',
 'Review the candidate against the actual schema and operating envelope.',
 'Evaluate whether calibration, analysis, energy or access meaning will change.',
 'Back up the current approved revision and document the rollback condition.',
 'Obtain the appropriate engineering/administrative approval.',
 'Apply the candidate through the released mechanism, not an undocumented client-local edit.',
 'Verify effective revision and behavior across backend, Qt, website and app.',
 'Record the transition time; do not relabel earlier records with the new revision.',
 'Retain the old revision so previous events remain interpretable.'])
x.h('Secret lifecycle')
x.table(['Stage','Required handling','Unacceptable practice'],[
('Creation','Approved strong per-scope credentials','Shared public demo password for operational access'),
('Provisioning','Protected path/account with least privilege','Credentials pasted into README or screenshot'),
('Runtime','Only the required service/account can read','World-readable environment or unrestricted shell access'),
('Logging','Redact tokens, passwords and private key material','Publishing raw authorization headers'),
('Rotation','Controlled change and reconnect validation','Assuming all clients updated because one connected'),
('Revocation','Remove compromised/retired identities','Leaving abandoned node credentials active'),
('Backup','Protected/encrypted handling as policy requires','Putting secrets in an unprotected evidence ZIP'),
('Publication','Sanitized examples with explicit reference status','A plausible-looking secret that users might deploy')])

x=c('Running, Packaging and Deployment','deployment')
x.fig('release_contract','Reference handover chain from source/release identity through checksums, configuration, acceptance evidence and rollback.')
x.p('The operating environment, backend, Qt UI and remote clients should be handed over as compatible releases. Do not infer a working deployment from a repository badge or a successful documentation build. The actual product package must identify what runs, on what hardware, with which data contract and which recovery procedure.')
x.h('Release manifest shape')
x.code('json',json.dumps({'manifest_basis':'reference handover contract; no product release asserted','release_id':None,'source_commit':None,'artifact_sha256':None,'build':{'gateway_architecture':None,'ubuntu_release':None,'python_version':None,'qt_pyside_version':None,'dependency_lock_sha256':None},'entrypoints':{'backend':None,'onsite_ui':None,'service_supervisor':None},'contracts':{'telemetry_schema':None,'client_contract':None,'storage_schema':None,'analysis_policy':None,'configuration_schema':None},'clients':{'website_release':None,'app_release':None,'approved_access_description':None},'operations':{'data_directory':None,'backup_procedure_revision':None,'migration_procedure_revision':None,'rollback_procedure_revision':None,'acceptance_record_id':None},'approvals':{'release_owner':None,'reviewer':None,'approval_utc':None}},indent=2))
x.h('Deployment states and gates')
x.table(['Gate','Required condition','Failure response'],[
('Artifact verification','Source/release and checksum match','Stop; obtain the correct artifact'),
('Platform match','Hardware/OS/runtime supported','Do not force-install incompatible packages'),
('Backup complete','Config/calibration/history recoverable','Do not migrate without a recovery point'),
('Configuration review','Identity, thresholds and secret references approved','Keep prior revision / fail readiness'),
('Migration review','Schema path and rollback implications understood','Do not run arbitrary migration SQL'),
('Service readiness','Required dependencies actually available','Expose degraded state and diagnose'),
('Onsite acceptance','Current identity/time/quality and history agree','Do not call release ready from process liveness'),
('Remote acceptance','Website/app observe compatible context','Restrict remote release until compatible'),
('Handover','Operator knows limits, support and rollback','Retain maintenance ownership')])
x.h('Controlled shutdown')
x.procedure('Stop without losing meaning',[
 'Record the reason, operator and expected monitoring interruption.',
 'Stop new workflow actions through the approved maintenance mode if available.',
 'Allow the writer to finish or explicitly report pending/uncommitted records.',
 'Stop application services using the released supervisor, not arbitrary process killing.',
 'Close the UI and preserve event/configuration state as designed.',
 'Shut down the gateway OS through the approved platform procedure.',
 'Remove bench power only after the storage/platform is safe for removal.',
 'On restart, reconcile last committed identity, backlog and current freshness.'])
x.h('Rollback decision')
x.p('Rollback is not just restoring executable files. A storage migration, configuration change or event-policy revision may be incompatible with the previous binary. The release must define which data/configuration snapshot is restored, whether newer history is preserved separately and how operators are informed of the resulting evidence boundary. Rehearse recovery on a controlled copy before relying on it onsite.')
x.table(['Rollout fault','Evidence to preserve','Rollback concern'],[
('Backend fails before readiness','Release/config identity and startup error','Do not erase the cause by repeated reinstalling'),
('UI fails but backend records','Dependency and writer status','Avoid losing valid history during frontend repair'),
('Migration incompatible','Schema version and failed transaction','Use reviewed backup and migration recovery'),
('Remote client contract mismatch','Client/backend revisions and rejected fields','Restore compatible client or gateway pair'),
('Unexpected threshold behavior','Policy revision and event inputs','Restore policy without rewriting earlier evidence'),
('Storage pressure after update','Disk/WAL/log/record sizes','Recover capacity without deleting irreplaceable evidence')])

x=c('Onsite Engineer Operating Guide','operator-guide')
x.fig('operator_journey','A normal operator session begins with identity/freshness and ends with a traceable inspection or handover.')
x.h('Pre-session checks')
x.bullets(['Confirm the authorized bench/monitoring scope and that no live string wiring is implied.','Inspect the enclosure, cables and safe disconnect; do not open/rewire energized equipment.','Confirm site, zone, node and measurement point before reading numbers.','Verify source time, clock state and last update age.','Check sensor/channel quality and backend/storage health.','Confirm that displayed thresholds/calibration apply to the selected node.','Review active events and previous maintenance notes before starting a new task.'],check=True)
x.procedure('Read a live observation',[
 'Select the intended node and confirm its identity in the detail view.',
 'Check freshness and channel validity before interpreting a value.',
 'Read voltage/current/power with units and the actual measurement location.',
 'Check irradiance and panel temperature alongside a power change.',
 'Read the history window to distinguish a persistent pattern from a transient.',
 'If analysis is gated or unavailable, do not infer a healthy plant state.',
 'If a persistent event is active, inspect its reason, onset, policy and evidence.',
 'Acknowledge only through the approved workflow and within your authority.'])
x.procedure('Handle a persistent-shortfall event',[
 'Verify that the event belongs to the selected physical zone/node.',
 'Check whether data is current and the environmental gate was qualified.',
 'Review expected-output assumptions and any known load/curtailment condition.',
 'Read the residual and persistence history rather than one isolated number.',
 'Record acknowledgement separately from the intended inspection action.',
 'Follow the authorized maintenance/electrical work process; the alert is not a permit.',
 'Record what was physically found, including a non-fault or sensor issue.',
 'Observe valid post-action data before recording resolution.',
 'Preserve unresolved conditions and hand over clearly if the shift ends.'])
x.h('Decision table at the console')
x.table(['What you see','First interpretation','Next approved action'],[
('Fresh valid power lower than expected','A qualified deviation may exist','Review environment, baseline and persistent event'),
('Stale values on all nodes','Common path may be impaired','Check gateway/broker/time before inspecting every panel'),
('One invalid current channel','Electrical data-health issue','Stop power/energy conclusions for that channel'),
('Low irradiance with analysis gated','Unsuitable detection context','Wait for qualified conditions; retain history'),
('History gap','Unknown interval','Review outage; do not assume no generation'),
('Acknowledged but active event','Human has seen an ongoing condition','Continue authorized handling'),
('Remote disconnected but Qt live','Remote-path issue possible','Continue local monitoring and report connectivity'),
('Storage fault with live values','History may not be durable','Notify maintainer and preserve evidence')])
x.h('Shift handover record')
x.code('text', '''Shift / operator:
Site / zone / node:
Application release and configuration revision:
Calibration revision:
Monitoring time window (UTC plus display zone):
Active condition events and event revisions:
Acknowledgements made:
Inspection scope and physical findings:
Any data gaps / uncertain clocks / invalid channels:
Storage / network / service concerns:
Actions taken and authorized by:
Outstanding tasks and owner:
Evidence/export identifiers:
Next review / handover time:''')
x.p('Do not clear an alarm merely to make the dashboard green. Do not repeatedly reboot a node to hide a sensor fault. A useful handover states what is known, what remains uncertain and what action is authorized next. Preserve photos/notes securely and avoid public exposure of credentials or sensitive plant details.')

x=c('Website and App Connectivity / Access','client-connectivity')
x.p('Remote access is a distinct boundary from the node MQTT path. The architecture confirms connected website/app monitoring, but not whether the built clients use HTTP polling, streaming, WebSocket, another protocol or a particular hosting model. Review the actual release contract before opening ports, publishing DNS or configuring authentication.')
x.table(['Path','Known role','Release questions'],[
('Node → broker/gateway','MQTT telemetry architecture','Broker listener, credential scope, transport security and reconnect'),
('Gateway → Qt','Onsite engineering context','Actual process boundary and snapshot/update mechanism'),
('Gateway/common data → website','Browser monitoring','Actual route/protocol, hosting, session and cache policy'),
('Gateway/common data → app','Companion monitoring','Actual endpoint/protocol, platform and session policy'),
('Engineer → gateway administration','Controlled maintenance','Approved identity, network reachability and audit'),
('System → plant equipment','No control path in this demonstrator','Any future path requires independent safety/security approval')])
x.h('Connection-state vocabulary')
x.table(['State','Meaning','Must not imply'],[
('Connected','A particular client/path is connected','Every sensor value is valid and fresh'),
('Reconnecting','The path is being restored','Historical cached data has become live'),
('Unauthorized','Session/scope is not accepted','The plant or node is electrically faulty'),
('Contract mismatch','Client/backend versions do not agree','Values should be guessed/coerced'),
('Backend unavailable','Remote service cannot supply context','A local sensing failure is proven'),
('Node stale','Source observation age exceeded policy','The entire internet connection is down'),
('Backfilling','Historical records are arriving','The physical event just occurred'),
('Offline cached','Only retained client context is available','Continuous operational coverage')])
x.procedure('Controlled remote-path acceptance',[
 'Use only the team-approved endpoint and account scope.',
 'Record gateway/backend and client release identities.',
 'Select the same node and time window in Qt and the remote client.',
 'Compare sample identity, V/I/P, environmental units, quality and event revision.',
 'Disconnect WAN only while retaining approved local connectivity.',
 'Confirm Qt/local history behavior and explicit remote disconnection.',
 'Reconnect and compare source time, backlog and live state without duplicate events.',
 'Test session expiry/logout and scope restriction through approved test accounts.',
 'Retain sanitized captures and exact conditions for the acceptance record.'])
x.h('No invented endpoint examples')
x.p('This handbook intentionally avoids a fake production /api/live route, a guessed public domain or a localhost URL embedded in a website/app guide. If a browser-based release uses a separate backend, browser code must use the approved reachable origin/path; the user\'s device is not the gateway\'s loopback interface. Record that actual deployment route in the release manifest.')
x.h('Evidence to attach when access is published')
x.table(['Artifact','Content'],[
('Access map','LAN/remote boundaries and approved connection method'),
('Client contract','Versioned fields, event revisions, errors and cache semantics'),
('Role map','Who may read, export, acknowledge and administer'),
('Session policy','Expiry, revocation, logout and recovery'),
('Certificate/transport policy','Actual trust and provisioning method'),
('Compatibility matrix','Gateway/backend and website/app release pairs'),
('Recovery record','WAN-off and reconnect test evidence'),
('Support note','How to report a failing connection without exposing secrets')])

x=c('Testing and Validation Strategy','validation')
x.fig('validation_pipeline','Proposed progression from inspection and calibration to fault injection, integration, holdout evaluation and release review. No completed execution is implied.')
x.p('Validation should distinguish the documentation\'s own arithmetic/structure checks from tests of the actual hardware, runtime and connected clients. The bundle includes executable checks for formulas and file integrity. It does not include measured proof that the physical demonstrator or unpublished application meets its acceptance targets.')
x.h('Verification layers')
x.table(['Layer','Question','Evidence artifact'],[
('Document integrity','Are lines, assets, links and calculations coherent?','Generated documentation quality report'),
('Static design review','Do pin maps, domains and ratings make sense?','Reviewed schematic/layout and issue record'),
('Metrology','Do calibrated channels meet target under stated uncertainty?','Reference/DUT dataset and signed calibration record'),
('Firmware behavior','Do timing, status, identity and buffering behave correctly?','Controlled logs and sequence inventory'),
('Backend correctness','Do parsing, dedup, metrics and storage preserve meaning?','Test cases and database/export evidence'),
('UI consistency','Do Qt/website/app represent the same context?','Common-fixture captures and comparison'),
('Recovery','Do faults degrade and recover explicitly?','Injected-fault timeline and post-recovery audit'),
('Analytics','Does held-out event detection meet the stated criteria?','Labeled split, predictions and metrics'),
('Release readiness','Can another engineer reproduce/operate/rollback?','Manifest, acceptance record and handover')])
x.h('Proposed acceptance matrix')
x.table(['Test ID','Controlled condition','Expected evidence / decision'],[
('T-EL-01','Inspect unpowered pin/polarity/domain wiring','Reviewed net/pin map and no return bridge'),
('T-EL-02','Apply approved 12 V low-current point','Stable readings, safe setup and reference comparison'),
('T-EL-03','Apply matrix points up to approved 24 V / 5 A','V/I error and load rating evidence at each point'),
('T-EL-04','Check zero/near-zero current','Absolute noise/offset rule, not relative division by zero'),
('T-EL-05','Inspect shunt heating at maximum planned current','Actual temperature and drift under stated ambient'),
('T-IR-01','Apply documented irradiance reference conditions','Sensor/ADC coefficient and residual evidence'),
('T-IR-02','Check sensor shading/soiling context','Data-quality/inspection response without false certainty'),
('T-TM-01','Compare mounted temperature sensor with reference','Mounting, stabilization and uncertainty record'),
('T-TM-02','Inject temperature CRC/disconnect fault','Invalid/missing state rather than a fake normal value'),
('T-FW-01','Acquire at 1 Hz under expected networking load','Interval distribution and missed-deadline count'),
('T-FW-02','Disconnect network during acquisition','Documented queue/backpressure/loss behavior'),
('T-FW-03','Exercise 600-record backlog target','Capacity and first/last sequence inventory'),
('T-FW-04','Reboot the node','New boot identity and preserved/reset behavior'),
('T-FW-05','Start without UTC','Explicit unsynced state and monotonic uptime'),
('T-MQ-01','Replay duplicate QoS 1 deliveries','One committed key and no duplicate energy'),
('T-MQ-02','Send same key with changed body','Identity fault preserved without overwrite'),
('T-MQ-03','Deliver an old retained observation','Source-age classification remains stale/backfill'),
('T-SC-01','Supply malformed JSON','Controlled reject; backend stays responsive'),
('T-SC-02','Supply unsupported schema','Explicit compatibility error/quarantine'),
('T-SC-03','Supply wrong field type/units','No silent numeric/unit coercion'),
('T-SC-04','Supply null with valid status','Semantic inconsistency rejected/quarantined'),
('T-TI-01','Inject future source time','Clock issue, not negative-age healthy state'),
('T-TI-02','Step source/gateway clock backward','No negative energy interval'),
('T-ST-01','Restart writer during a transaction','Atomic/known commit outcome and integrity check'),
('T-ST-02','Approach storage thresholds','Visible pressure and approved retention response'),
('T-ST-03','Restore a consistent backup on a copy','Integrity plus known records/event/config context'),
('T-EN-01','Integrate a constant-power fixture','Correct Wh using elapsed seconds'),
('T-EN-02','Inject an invalid endpoint/gap','Excluded interval/time retained'),
('T-EN-03','Replay a committed integration interval','No second energy increment'),
('T-AI-01','Residual briefly exceeds threshold','No premature persistent alert'),
('T-AI-02','Residual qualifies continuously for 180 s','Onset/persistence/alert times recorded'),
('T-AI-03','Drop environmental quality during timer','Released reset/hold policy visible'),
('T-AI-04','Use low G or near-zero expected power','Gate/denominator protection rather than unstable score'),
('T-AI-05','Evaluate separated held-out events','Precision, recall, counts and uncertainty reported'),
('T-UI-01','Open Qt before first sample','No live-zero or healthy startup assumption'),
('T-UI-02','Keep UI interactive under update load','Measured interaction/update behavior'),
('T-UI-03','Compare fixture in all three clients','Identity, units, age, quality and event agreement'),
('T-EV-01','Acknowledge an active condition','Workflow changes without clearing condition'),
('T-EV-02','Acknowledge concurrently from two clients','Defined revision/conflict outcome'),
('T-NW-01','Remove WAN only','Onsite path continues if LAN/services remain'),
('T-NW-02','Remove node LAN connectivity','Affected source becomes stale; local history remains'),
('T-NW-03','Restore connectivity with backlog','Idempotent backfill and correct live age'),
('T-AC-01','Use a least-privilege read account','No unauthorized acknowledgement/admin scope'),
('T-AC-02','Expire/revoke session','Explicit access failure without misleading plant alarm'),
('T-PK-01','Inspect enclosure/cable entry','Actual fit and barrier integrity'),
('T-PK-02','Run reviewed thermal condition','Measured ambient/interior/device temperatures'),
('T-RL-01','Deploy and roll back a controlled copy','Compatible data/config recovery'),
('T-RL-02','Complete operator handover','Limits, owner and evidence available')])
x.h('Test record template')
x.code('yaml', '''test_record:
  test_id: null
  purpose: null
  status: "not_executed"  # Other states require actual evidence.
  operator: null
  reviewer: null
  execution_utc: null
  dut:
    node_id: null
    board_revision: null
    firmware_revision: null
    gateway_release: null
    config_revision: null
    calibration_revision: null
  setup:
    instruments: []
    source_and_load_ratings: null
    connection_diagram: null
    ambient_conditions: null
    safety_authorization: null
  method:
    preconditions: []
    controlled_input: null
    steps: []
    stop_conditions: []
  acceptance:
    target: null
    uncertainty_policy: null
    decision_rule: null
  observations:
    raw_dataset: null
    timestamps: null
    screenshots_or_photos: []
    unexpected_behavior: null
  result:
    measured_value: null
    uncertainty: null
    pass_fail_inconclusive: null
    limitations: null
  evidence:
    manifest: null
    checksums: []
    review_note: null''')
x.h('Result language')
x.table(['Use this term','Only when'],[
('Planned','Method/target exists but execution has not occurred'),
('Not executed','A scheduled case has no execution record'),
('Observed','A specific recorded run produced the stated behavior'),
('Passed','The documented acceptance rule and uncertainty policy were met'),
('Failed','A valid run did not meet the acceptance criterion'),
('Inconclusive','Setup/data/uncertainty prevents a defensible decision'),
('Calculated','The value follows from stated inputs and formula'),
('Illustrative','The content explains behavior without claiming an actual observation'),
('Certified','A relevant authorized certification record genuinely exists')])

x=c('Security, Privacy and Threat Model','security')
x.fig('security_zones','Proposed trust boundaries for node, gateway, operator and remote access. The figure is not evidence of a deployed security configuration.')
x.p('Monitoring can reveal site performance, maintenance activity and operational patterns. A read-only application still needs authorization, integrity and confidentiality controls. Security review must cover node provisioning, broker access, gateway administration, client sessions, backups, exports and update artifacts. Do not equate “no switching commands” with “no security risk”.')
x.table(['Asset','Threat / failure','Proposed mitigation','Evidence required'],[
('Telemetry integrity','Spoofed node or altered values','Approved identity, topic scope and transport/integrity policy','Provisioning and controlled unauthorized-publish test'),
('Historical records','Accidental overwrite or tamper','Append-oriented raw evidence, checksums and access control','Permission/integrity/restore checks'),
('Event workflow','Unauthorized acknowledgement or closure','Role checks and revisioned audit','Approved account-scope tests'),
('Credentials','Leak in logs, screenshots or repository','Protected secret source and redaction','Sanitized artifact review'),
('Gateway availability','Unbounded queue/reconnect/log growth','Bounded resources and low-space/health reporting','Load and outage exercise'),
('Remote session','Expired/stolen session retains access','Actual session/revocation policy','Expiry/logout/revocation tests'),
('Software supply chain','Unreviewed dependencies or artifact substitution','Locked dependencies, checksums and release review','Manifest and artifact verification'),
('Configuration','Wrong threshold/site mapping','Controlled revisions and approval','Before/after effective-revision record'),
('Backup','Lost or publicly exposed plant data','Protected storage and recovery policy','Backup-access and restore exercise'),
('Physical device','Unintended USB/debug exposure','Approved enclosure/access and maintenance process','Physical inspection and administrative policy')])
x.h('Least-privilege role baseline')
x.table(['Role','Typical monitoring rights','Not automatically granted'],[
('Viewer','Read approved site/node data and event context','Acknowledge, change configuration or obtain shell'),
('Operator','Read plus approved event handling','Modify calibration or operating system'),
('Maintenance engineer','Approved notes/inspection workflow','Plant switching authority solely from app access'),
('Administrator','Controlled application/platform maintenance','Unrestricted public exposure of credentials'),
('Reviewer','Sanitized evidence and documentation','Operational accounts or private site access')])
x.h('Privacy and evidence handling')
x.bullets(['Minimize personal names and sensitive plant-location details in public exports.','Obtain appropriate permission before publishing maker, laboratory, faculty or site photographs.','Keep credentials, session material, private keys and unredacted internal network details out of review packages.','Retain enough actor identity for an authorized operational audit without publishing unnecessary personal data.','Document where exported files are stored and who may access them.','Use an approved deletion/retention policy; do not improvise deletion of evidence during an incident.','Treat test accounts and simulated fixtures as distinct from operational identities.','A public repository link is not an invitation to expose a gateway directly to the internet.'])
x.h('Incident response outline')
x.procedure('Preserve, contain, recover',[
 'Record the observed symptom, scope and UTC time without exposing secrets.',
 'Preserve relevant logs, event revisions, configuration and artifact identities.',
 'Notify the authorized owner and restrict the affected access path as policy allows.',
 'Keep plant protection and electrical safety independent of monitoring recovery.',
 'Review whether telemetry/history/workflow integrity is affected.',
 'Rotate/revoke compromised credentials through the approved provisioning path.',
 'Restore a reviewed release/configuration or backup on a controlled basis.',
 'Verify identity, quality, history and client consistency before normal handover.',
 'Record lessons and the evidence boundary; do not silently delete the incident.'])
x.p('No penetration test, security certification or production-hardening result has been supplied. The measures above are a review baseline. Actual deployment controls and their acceptance evidence belong in the release record.')
