from doc_engine import c,event_table,mermaid

x=c('Executive Overview','executive-overview')
x.fig('ecosystem_overview','The monitoring ecosystem combines field telemetry, an Ubuntu-based onsite platform and three engineering access surfaces. This is a logical architecture illustration, not a software screenshot.')
x.p('ARKA AI connects the electrical output of a solar installation to the conditions under which that output was produced. Voltage and current establish what the monitored DC point is delivering; irradiance and panel temperature help explain why the output changes. The system combines these signals with local history and interpretable anomaly context so an engineer can decide when inspection is warranted.')
x.p('The onsite software environment uses an Ubuntu command-line Linux base, a Qt / PySide6 engineering interface and a Python backend. The project team confirms that the embedded platform, website and companion app have been built as one monitoring ecosystem. The three access surfaces are complementary views of the same engineering context, not three separate definitions of plant health.')
x.p('This handbook documents the project architecture and supplies explicit reference contracts, operating procedures and acceptance methods. The inspected public repository contains documentation rather than a released implementation tree. Consequently, exact entry points, service-unit names, deployed versions, endpoint routes and application build commands must come from the actual release manifest before installation on a gateway. Reference examples below are not disguised release artifacts.')
x.table(['Engineering question','What ARKA AI contributes','What remains an engineer responsibility'],[
('What is the monitored point producing?','Time-aligned V, I, calculated P and valid-interval energy','Confirm measurement point, calibration and safe sensing interface'),
('Is output low for current conditions?','Irradiance/temperature context and expected-output comparison','Review environmental transients and physical operating conditions'),
('Can monitoring continue without WAN?','Local gateway, history and onsite interface architecture','Verify actual LAN, power, storage and recovery behavior'),
('Can different clients discuss one event?','Shared node, timestamp, quality and event identity','Confirm actual cross-client agreement and authorized access'),
('Should equipment be inspected?','Persistent-deviation and data-fault context','Authorize inspection and record the physical finding'),
('Can the system switch plant equipment?','No plant-control path in the read-only demonstrator','Retain certified protection and separate safety interlocks')])
x.h('Capability and evidence map')
x.table(['Area','Documented / confirmed position','Evidence boundary'],[
('Ubuntu-based embedded environment','Implemented software scope confirmed by the team','Exact image, architecture and release manifest not published'),
('Qt / PySide6 interface','Implemented onsite engineering UI confirmed','Illustrations here are not captures from the running interface'),
('Python backend','Implemented backend confirmed','Exact framework, process layout and storage release are unspecified'),
('Website and companion app','Built as connected monitoring clients','No public URL, platform target or release package was supplied'),
('ESP32-S3 / MQTT sensing architecture','Primary project-submission architecture','Exact firmware release and executed bench records are not supplied'),
('Sensor parts, PCB allocation, enclosure','Proposed engineering design','Not routed EDA, released CAD, FEA or fabrication proof'),
('Accuracy, detection and timing goals','Acceptance targets','No measured achievement is claimed'),
('Technical documentation','This handbook and its linked engineering assets','Upload the complete asset folder with the Markdown file'),
('Prototype video','Publication pending','No fabricated playback URL is provided')])
x.h('How to use the handbook')
x.bullets(['Judges: read the architecture, implementation milestones, target/evidence matrix and prototype-video status before evaluating numeric claims.','Onsite engineers: begin with the operating boundary, startup checks, quality states and troubleshooting decision path.','Software maintainers: use the identity, telemetry, persistence and cross-client contracts as a review baseline; reconcile examples with the released code.','Hardware reviewers: examine the proposed pin-referenced connection, separate power domains, metrology plan and enclosure assumptions.','Future contributors: preserve the distinction between measured records, calculated examples, reference designs and planned tests.'])
x.quote('**Hard boundary:** the current hardware demonstrator is read-only, 12–24 V DC and no more than 5 A. Do not connect this sensing concept directly to live plant PV strings.')

x=c('Problem, Users and Requirements','problem-users')
x.p('Solar production is conditioned by sunlight, module temperature and electrical operating point. A lower instantaneous power value does not, by itself, establish equipment damage. Equally, a display of acceptable voltage does not prove that current, energy or plant availability is satisfactory. A useful maintenance view must preserve the relationship between output, environmental context, time and measurement quality.')
x.p('The original project submission identifies delayed and fragmented monitoring as the integration problem. ARKA AI responds with distributed acquisition and a common local intelligence layer. It does not claim that capable inverter monitoring or solar analytics did not already exist. Where approved read-only inverter telemetry is available, the project should integrate it rather than duplicate certified control functions.')
x.table(['Persona','Primary decision','Required context','Unsafe shortcut to avoid'],[
('Onsite engineer','Whether to inspect a zone','Valid output, source time, irradiance, panel temperature, active event','Diagnosing from a stale last-known value'),
('Maintenance technician','Which authorized task to perform','Zone identity, event reason, safe work scope, prior actions','Treating an app notification as an electrical work permit'),
('Plant operator','How to prioritize issues','Multiple zone states, quality, event age and acknowledgement','Ranking faults solely by a raw AI score'),
('Asset owner','Whether monitoring evidence supports action','Traceable trends, assumptions and documented outcomes','Interpreting modeled waiting-time reduction as measured ROI'),
('Software maintainer','Which boundary failed','Node sequence, broker state, backend logs and client revision','Restarting every component before preserving evidence'),
('Electrical reviewer','Whether the sensing arrangement is appropriate','Ratings, topology, isolation, reference uncertainty and protection','Extending a low-voltage monitor to string voltage by assumption')])
x.h('Functional requirement baseline')
x.table(['ID','Requirement','Acceptance evidence'],[
('FR-01','Identify the monitored site, zone and node','The same identity appears in storage, Qt, website and app'),
('FR-02','Retain V/I and environment with time and units','Exported records preserve source/receive time and unit names'),
('FR-03','Derive power from synchronized V and I','Arithmetic checks plus reference-meter comparison'),
('FR-04','Integrate energy only across valid intervals','Gap-injection procedure and explicit excluded-time inventory'),
('FR-05','Expose stale, invalid and unavailable states','Timeout and sensor-fault captures from each client'),
('FR-06','Compare output with a contextual healthy baseline','Documented model inputs, quality gates and held-out events'),
('FR-07','Record acknowledgement separately from condition state','Event audit preserves both operator action and sensor condition'),
('FR-08','Keep onsite monitoring independent of continuous WAN','Controlled WAN-off exercise with local data/history checks'),
('FR-09','Deduplicate replayed records','Unique committed node/boot/sequence keys after reconnect'),
('FR-10','Preserve engineering evidence','Versioned calibration, configuration, export and maintenance context')])
x.h('Nonfunctional requirements')
x.table(['Concern','Design intent','Review method'],[
('Safety','Read-only low-voltage demonstration; no protection replacement','Hazard review and approved test setup'),
('Responsiveness','Nonblocking acquisition and clear data-age display','Qt interaction and controlled latency tests'),
('Availability','Visible degradation rather than silent healthy defaults','Dependency-loss and restart exercises'),
('Traceability','Raw observation distinguishable from derived metrics','Schema, event and export audits'),
('Maintainability','Explicit release/configuration/calibration identity','Rebuild and rollback rehearsal'),
('Access control','Viewing context does not grant shell or plant authority','Role and network-permission review'),
('Scalability','Modular zones with a shared gateway architecture','Load/retention tests at a defined node count'),
('Portability','Separate domain logic from a particular client display','Cross-client contract tests')])
x.p('Requirements are testable statements, not a substitute for test results. An inconclusive or not-executed result is a valid release-review outcome; omitting it is not equivalent to a pass. Expand the scope only after the relevant engineering gate is satisfied.')

x=c('Project Scope and Ecosystem Boundaries','scope')
x.p('The project is a monitoring, diagnostic and decision-support layer. The sensor node measures an approved low-voltage demonstration point. The Ubuntu gateway hosts the onsite software environment and local intelligence. The website and app provide connected engineering access. Physical plant protection, switching interlocks, electrical work authorization and inverter controls remain outside this demonstrator.')
x.table(['Boundary','Inside current documentation','Excluded / separately approved'],[
('Electrical','12–24 V DC, ≤5 A bench sensing concept','Direct utility PV string connection'),
('Compute','ESP32-S3 node plus a separate Ubuntu gateway','Running Ubuntu on the ESP32'),
('Onsite OS','Ubuntu base with ARKA application stack','A newly written kernel or new general-purpose distribution'),
('UI','Qt / PySide6 onsite engineering interface','Unverified claims about particular screen layouts or toolkit widgets'),
('Connected clients','Team-confirmed website and companion app','Invented hosting URLs, mobile targets or app-store listings'),
('Analytics','Expected-output residual and maintenance support','Guaranteed failure-date or remaining-life prediction'),
('Response','Engineer notification, acknowledgement and recorded action','Autonomous plant switching'),
('Evidence','Design calculations, reference contracts and proposed tests','Fabricated measurement logs or passed certifications')])
x.h('Local-first is a dependency statement')
x.p('A WAN outage can remove remote connectivity while the onsite LAN, broker, gateway and terminal continue working. A LAN outage can disconnect a node even if the internet remains available. A gateway power failure can interrupt all local services regardless of WAN state. These are different failures and require different indications, recovery procedures and evidence.')
event_table(x,[('WAN unavailable; LAN intact','Keep onsite UI and local history useful; remote sessions indicate connection loss','Gateway/Qt capture plus remote last-confirmed time'),('Node Wi-Fi unavailable','Mark the affected node stale; buffer/replay is a target to verify','Node sequence before/after outage and source-time gap'),('Broker unavailable','Ingestion degrades explicitly; no current value is invented','Broker/worker status and recovery ordering'),('Storage unavailable','Do not claim a sample was committed; raise persistence fault','Write error, pending state and recovered row inventory'),('Gateway restarted','Restore appropriate event/history context and validate service dependencies','Release/config identity and restart/replay evidence')])
x.h('Publication and implementation are different')
x.p('The project team confirms the software platform and clients as built. The inspected repository root currently publishes a README rather than those implementation files. That publication gap prevents this handbook from naming actual process executables, API routes or build commands as verified. It does not negate the team statement. Release-specific deployment details should be attached to the repository when source and build artifacts are published.')
x.h('Change gate for expanded plant scope')
x.bullets(['Identify the new measurement point and its maximum operating/fault conditions before choosing a sensing interface.','Obtain qualified electrical review of working voltage, transient category, insulation, grounding, protection and enclosure.','Keep the monitoring data path separate from certified plant protection and any future control chain.','Retest timestamp, quality and consistency contracts after adding inverter, SCADA, battery or fleet-level inputs.','Publish the evidence and limitations that justify the larger scope rather than relabeling this low-voltage circuit.'])

x=c('End-to-End System Architecture','architecture')
x.fig('ecosystem_architecture','Field acquisition, MQTT transport, the embedded Linux gateway and engineer-facing clients. Internal service boundaries are a reference decomposition; web/app protocols must be reconciled with the release.')
x.p('The architecture has four responsibilities: acquire trustworthy observations, transport them without losing identity, turn valid observations into traceable context, and present that context to an engineer. Client rendering is the last step; a polished graph cannot repair an ambiguous source timestamp, an uncalibrated input or a duplicated record.')
x.table(['Stage','Producer','Consumer','Contract'],[
('Measurement','Electrical/environmental sensor','ESP32-S3 firmware','Range, conversion status, units and calibration context'),
('Record assembly','Node acquisition cycle','Node buffer/publisher','Node identity, boot identity, sequence and source-time quality'),
('Transport','Node MQTT publisher','Broker/subscriber','Topic scope, envelope, delivery status and reconnect behavior'),
('Validation','Gateway ingestion worker','Derived-metric/store pipeline','Schema, plausibility, identity, clock and quality decision'),
('Persistence','Gateway writer','Local record store','Unique key, transaction outcome and retained raw context'),
('Analysis','Qualified measurements','Event service','Expected output, residual, gate and persistence revision'),
('Presentation','Common monitoring state','Qt / website / app','Value, age, quality, unit and event revision'),
('Maintenance','Authorized engineer','Event/inspection record','Actor, action time, finding and verified outcome')])
mermaid(x,'''flowchart LR
    F[Electrical and environmental sensing] --> N[ESP32-S3 node]
    N --> M[MQTT broker]
    M --> I[Python ingestion and quality checks]
    I --> S[Local telemetry records]
    I --> D[Power and valid-interval energy]
    D --> A[Expected-output and anomaly logic]
    A --> E[Event state]
    S --> C[Shared monitoring context]
    E --> C
    C --> Q[Qt onsite HMI]
    C --> W[Website]
    C --> P[Companion app]
    Q --> H[Engineer inspection]
    W --> H
    P --> H
    H --> R[Recorded maintenance outcome]''')
x.h('Record ownership')
x.p('The node owns observation identity; the gateway owns receive time and ingestion decisions; derived services own metric/event revision; the engineer owns an acknowledgement or maintenance note. None of these roles should overwrite a different role\'s evidence. Replayed telemetry may arrive now while describing an older observation; the display must not infer freshness from arrival alone.')
x.table(['Information','Authoritative basis','Must not be confused with'],[
('Source time','Node observation plus clock-quality context','Gateway receipt time'),
('Receive time','Gateway receipt clock','Physical event onset'),
('Power','Defined V/I pair and formula','Inverter AC power at another measurement point'),
('Energy','Integrated valid interval and gap policy','Uninterrupted output through missing samples'),
('Anomaly onset','First qualifying event-condition time','Operator acknowledgement'),
('Acknowledgement','Authorized human action','Condition clearance or completed repair'),
('Configuration revision','Released parameter set','Ad hoc client-local threshold'),
('Calibration revision','Applicable metrology record','ADC register scaling alone')])
x.h('Design decisions that require the release manifest')
x.bullets(['Whether MQTT terminates in the same process as the backend or in a separate service.','Which persistence engine/schema the built release uses; SQLite/WAL below is a reference design.','How website/app clients access common data: exact protocol, routes, authentication and update mode.','How Qt receives snapshots and how UI-thread ownership is enforced.','How the operating environment launches the application and supervises failures.','Which hardware platform, OS image, Python/Qt versions and dependency lock are deployed.'])

x=c('Ubuntu-Based Embedded Operating Environment','embedded-os')
x.fig('runtime_stack','Logical runtime layers. The Ubuntu engineering terminal and the ESP32-S3 field node are separate compute systems.')
x.p('The embedded operating environment is based on Ubuntu command-line Linux with the ARKA software stack above it. It provides a maintainable base for onsite application services, operator access and administration. The project does not claim a new kernel, an independently developed distribution, an immutable Ubuntu Core deployment or a particular CPU architecture without the corresponding release record.')
x.table(['Layer','Responsibility','Release evidence'],[
('Ubuntu base','Kernel/userspace, device access, accounts, storage and networking','Actual image identity and supported gateway hardware'),
('Service supervision','Start/restart/shutdown ordering and dependency visibility','Reviewed units or equivalent process-launch configuration'),
('Python runtime','Backend execution and dependency isolation','Interpreter version, environment and locked package manifest'),
('Qt / PySide6','Onsite interface, rendering and event-driven interaction','Actual UI package and supported display/session configuration'),
('Transport','Broker/subscriber connectivity and authenticated scope','Broker version/configuration and credential source'),
('Persistence','Durable records and recovery behavior','Schema/revision, backup procedure and integrity checks'),
('Engineer operation','Monitoring without routine administrative privileges','Approved operating guide and least-privilege account'),
('Administration','Controlled maintenance, updates and diagnostics','Named authorized role, audit and rollback path')])
x.h('Operating modes')
x.table(['Mode','Expected state','Operator interpretation'],[
('Starting','Application/dependencies not yet ready','No measurements are assumed live'),
('Monitoring','Data is fresh, range-checked and contextualized','Use the qualified values and event reason'),
('Degraded','A dependency, clock or data channel is impaired','Read the reason and restrict conclusions'),
('Offline local','Remote connectivity absent but onsite path available','Continue approved local monitoring'),
('Recovering','Dependencies return; identity and records reconcile','Watch backfill and freshness before trusting live status'),
('Maintenance','Authorized change/review in progress','Preserve scope, backup and explicit handover'),
('Stopped','Application intentionally unavailable','No “healthy” state should remain implied')])
x.p('Do not confuse an Ubuntu shell with an operator HMI. Routine monitoring should not require root access, package installation or editing service files. Administrative actions must be limited to approved maintainers and should preserve a record of the release, configuration and reason for change. A website user should not inherit gateway-shell authority.')
x.h('Read-only platform inventory')
x.p('The following Linux commands are general inventory examples, not ARKA launch commands. Their output describes the actual gateway on which they are executed; no output is supplied here as if it had been captured from the team\'s device.')
x.code('bash', '''# Platform and boot context: read-only inventory.
uname -a
cat /etc/os-release
hostnamectl
uptime
# CPU / memory / storage capacity.
lscpu
free -h
df -h
lsblk -f
# Network state; redact private addresses before public publication.
ip -brief address
ip route
# Time basis and synchronization status.
timedatectl status
# Inspect failures without restarting services.
systemctl --failed
journalctl -b -p warning --no-pager''')
x.h('Record before a change')
x.table(['Record','Why it matters'],[
('OS release and architecture','Prevents installing a package built for a different target'),
('Application source/artifact checksum','Ties behavior to a particular deployed release'),
('Interpreter and dependency lock','Makes runtime differences diagnosable'),
('Qt platform/session configuration','Separates display/plugin failures from backend failure'),
('Broker and storage identities','Makes connectivity and migration assumptions explicit'),
('Configuration/calibration revisions','Explains a threshold or numeric change without rewriting history'),
('Backup and rollback point','Supports a controlled return to the previous operating state'),
('Operator handover note','Prevents a maintainer\'s shell activity from becoming an unexplained outage')])
x.p('Gateway hardware is not inferred from the node enclosure. A Raspberry Pi kit appears in the planning BOM, but the team has not published the exact hardware used for the built Ubuntu environment. Select installation media, display drivers and storage accordingly only after that platform is identified.')

x=c('Boot, Application Services and Recovery','boot-recovery')
x.fig('boot_recovery','Reference startup and recovery dependencies. Actual service names and entry points are release-specific.')
x.p('A service reporting that it started does not prove that monitoring is ready. Readiness requires accessible configuration, valid persistence, a usable time basis, a functioning ingestion path and an interface able to show the appropriate data state. Keep process liveness separate from application readiness and sensor freshness.')
x.table(['Dependency','Ready condition','Degraded indication','Recovery check'],[
('Storage mount','Expected path exists with correct owner/space','Persistence unavailable','Open/backup checks before accepting writes'),
('Configuration','Version, required fields and scope accepted','Configuration invalid','Show revision after corrected load'),
('Broker','Authenticated connection and intended subscription','Telemetry unavailable','Observe connection and topic scope'),
('Database','Schema compatible and transactions available','Write fault / read-only fault','Confirm no duplicate committed records'),
('Clock','UTC basis and uncertainty represented','Clock uncertain','Preserve source/receive distinction'),
('Analysis','Model/configuration revision available','Analysis unavailable','No healthy score substituted'),
('Qt session','Interface responds and shows data age','Interface unavailable','Render a current qualified snapshot'),
('Remote path','Approved access and reachable endpoint','Remote disconnected','Reconcile event and freshness state')])
mermaid(x,'''stateDiagram-v2
    [*] --> PlatformStarting
    PlatformStarting --> ServicesChecking
    ServicesChecking --> Monitoring: required dependencies ready
    ServicesChecking --> Degraded: configuration or data service fault
    Monitoring --> Degraded: loss of required dependency
    Degraded --> Recovering: dependency restored
    Recovering --> Monitoring: identity and quality reconciled
    Recovering --> Degraded: reconciliation failed
    Monitoring --> Maintenance: authorized maintenance
    Maintenance --> ServicesChecking: controlled restart
    Maintenance --> [*]: approved shutdown''')
x.procedure('Reference startup acceptance',[
 'Identify the deployed release and the authorized operator before applying bench power.',
 'Confirm that the regulated supplies and current limit match the approved low-voltage setup.',
 'Inspect platform boot/service status without inventing application readiness from a process ID.',
 'Confirm the intended configuration and calibration revisions are loaded.',
 'Open the onsite interface and verify selected site/node identity and displayed time basis.',
 'Check a current sequence/source-time record through acquisition, persistence and presentation.',
 'Confirm that absent channels show unavailable or an explicit reason rather than zero.',
 'Record any degraded dependency, startup delay and recovery action in the acceptance log.'])
x.h('Reference service-unit shape')
x.p('This is a deployment pattern, not a shipped ARKA service. Replace the symbolic executable/account/configuration paths only from a reviewed release manifest. The dependency list must match the actual broker/storage layout. Do not install this example unchanged.')
x.code('ini', '''[Unit]
Description=Reference ARKA backend service pattern
After=network-online.target
Wants=network-online.target
# Add actual broker/mount dependencies only after review.

[Service]
Type=simple
User=RELEASE_DEFINED_NONROOT_ACCOUNT
Group=RELEASE_DEFINED_APPLICATION_GROUP
WorkingDirectory=/RELEASE_DEFINED_WORKING_DIRECTORY
EnvironmentFile=/RELEASE_DEFINED_PROTECTED_ENV_FILE
ExecStart=/RELEASE_DEFINED_ABSOLUTE_EXECUTABLE
Restart=on-failure
RestartSec=5
TimeoutStopSec=30
NoNewPrivileges=true
PrivateTmp=true
# Read/write paths and hardening must match actual devices/storage.
# Do not grant broad privileges merely to suppress a startup error.

[Install]
WantedBy=multi-user.target''')
x.p('A restart policy cannot replace fault diagnosis. Bound repeated failures so that an invalid configuration, migration problem or unavailable disk does not create a rapid restart loop. On recovery, verify event state and persistence before calling the system ready. Qt may remain useful by displaying the dependency fault even when current measurements are unavailable.')

x=c('Qt / PySide6 Onsite Engineering UI','qt-ui')
x.fig('qt_workers','Reference separation between I/O/analysis work and the Qt rendering thread. This is a design pattern, not an audit of unpublished source.')
x.p('The onsite interface is the engineer-facing part of the embedded platform. Its responsibility is to make measurement identity, data age, quality and maintenance context visible at the point of use. A changing chart is not sufficient evidence that the selected node is connected, that the clock is trustworthy or that values have been committed to history.')
x.table(['Interface responsibility','Essential context','Interaction expectation'],[
('Live electrical values','V, I, P, unit, source time and quality','Changing node keeps identity unambiguous'),
('Energy view','Wh/kWh, integration window and gap policy','Range selection does not imply missing energy was recovered'),
('Environment','Irradiance, temperature and mounting/calibration context','Low light and rapid clouds are distinguishable from a fault'),
('History','Time basis, selection window and missing intervals','Zoom/filter preserves the original records'),
('Events','Condition reason, onset, alert time and workflow state','Acknowledgement is explicit and attributable'),
('Health','Sensor, link, time, storage and backend status','Degraded dependencies are visible without a shell'),
('Export','Node/window, units and revision manifest','Exported evidence can be interpreted after the session ends'),
('Configuration','Role, current revision and change scope','Routine viewing does not grant administrator authority')])
x.fig('hmi_reference_layout','Interface illustration using example values: 21.6 V × 3.20 A = 69.12 W; expected 88.3 W implies approximately 21.7% shortfall. This is not a running-software capture or test record.')
x.h('UI-state acceptance')
event_table(x,[('First launch before telemetry','Show starting / no data; do not render healthy zero','Startup capture and first accepted record identity'),('No new node data after freshness timeout','Mark stale, retain last-known value with source time','Last sequence/time and visible stale transition'),('A sensor value is invalid','Show the affected channel reason, not a plausible replacement','Raw status and channel-quality capture'),('Backend writer cannot commit','Expose persistence fault independently of link state','Backend error plus UI quality state'),('Time window contains missing data','Show gaps; do not connect an uninterrupted energy story','Trend/export with excluded interval'),('A late record is replayed','Keep historical source time and backfill status','History position versus current live card'),('An event is acknowledged','Record actor/time and preserve condition state','Event revision before/after action'),('Two clients view the same event','Use a common event identity and revision','Qt and remote captures for the same event')])
x.h('Thread and update rules')
x.bullets(['I/O and sensor/network waits belong outside the Qt widget thread.','Worker-to-UI communication should deliver a bounded, explicit snapshot through a queued boundary.','Only the UI thread changes Qt widgets; a direct cross-thread widget update is not an acceptable shortcut.','A high ingestion rate should not create an unbounded rendering queue or freeze operator interaction.','Downsampling a chart must not alter the underlying stored measurement or hide gap flags.','A frontend display cache must not reinterpret gateway-receipt time as a fresh physical observation.','Operator acknowledgement/filter requests are not plant switching commands.','Capture actual screen/build evidence when publishing the release; retain the illustrative status of figures here.'])

x=c('Python Backend','python-backend')
x.p('The Python backend is part of the team-confirmed onsite software platform. Its documented role is to connect acquisition to analysis, history, alerts and common client context. The exact framework, modules, deployment processes and release entry points have not been published. The decomposition below is a reference responsibility map rather than a claim that particular source files exist.')
x.table(['Responsibility','Input','Output','Failure boundary'],[
('Envelope parser','Broker payload and topic','Typed identity/units/time record','Malformed or unsupported schema'),
('Quality evaluator','Sensor status, ranges and clock context','Per-channel and record-quality decision','Invalid or uncertain observation'),
('Idempotent writer','Validated record plus source identity','Committed row or explicit duplicate outcome','Storage/transaction failure'),
('Derived metrics','Matched V/I and valid elapsed interval','Power and qualified energy contribution','Unmatched samples or missing time'),
('Baseline/residual','Valid output and G/T context','Expected output and normalized shortfall','Missing model or unsuitable environment'),
('Event engine','Residual, gate and persistence state','Versioned condition/alert event','Invalid data or inconsistent event state'),
('Client adapter','Shared telemetry/event snapshots','Qt/web/app representation','Stale cache, identity or authorization issue'),
('Export/audit','Requested window and permissions','Traceable file plus manifest','Incomplete window or missing revision context')])
x.h('Reference ingest transaction')
x.code('text', '''receive topic and payload
check topic scope and schema version
parse without coercing unknown units to known units
attach gateway receive time
validate identity, source-time status and channel status
form the immutable node/boot/sequence key
begin persistence transaction
    attempt idempotent insert
    if the key already exists:
        compare envelope identity; record duplicate outcome
    else:
        preserve raw values and quality decision
commit or report persistence failure
update derived/event state only according to the chosen replay policy
publish a client snapshot with sample identity and quality
never treat broker receipt as proof of committed history''')
x.h('Compute and evidence separation')
x.p('A raw record, a corrected engineering value, an energy contribution and an alert are different records of reasoning. Preserve the coefficients or policy revision that produced a derived value. An operator note may annotate a record but should not silently rewrite the raw observation. Reprocessing a historical window must produce a clearly versioned analysis result, not an unexplained change to earlier evidence.')
x.table(['Case','Backend decision','Client-visible consequence'],[
('Unknown calibration revision','Retain/quarantine with explicit reason','Do not claim calibrated accuracy'),
('Duplicate QoS 1 delivery','Idempotent commit outcome','No duplicate energy increment'),
('Late valid record','Store by source identity/time; label backfill','History may update without claiming a new live observation'),
('Clock step backward','Preserve receipt and clock uncertainty','Do not integrate a negative elapsed interval'),
('Storage full','Expose write fault and apply bounded recovery policy','Live visibility does not imply durable retention'),
('Model absent','Keep measurements available; analysis unavailable','No healthy anomaly score invented'),
('Configuration changes','Start a new effective revision','Event interpretation retains the appropriate prior policy'),
('Client disconnects','Keep backend contract independent of a viewer','Remote absence does not erase local events')])
x.h('Reference observability fields')
x.table(['Signal','Unit / category','Reason'],[
('ingest_record_count','count per outcome','Separates accepted, duplicate, rejected and quarantined records'),
('last_source_time','UTC with uncertainty','Identifies the observation horizon'),
('last_receive_time','UTC','Identifies the ingestion horizon'),
('writer_queue_depth','records','Reveals backpressure'),
('write_failure_count','count','Shows durable-storage failure separately from link success'),
('analysis_policy_revision','identifier','Makes result interpretation reproducible'),
('active_event_revision','identifier','Allows cross-client consistency checks'),
('clock_status','qualified state','Prevents transport-age mistakes'),
('process_uptime','monotonic elapsed time','Separates current process health from historical data availability')])

x=c('Website','website')
x.fig('client_access','Logical onsite/remote access boundaries. The website is part of the confirmed ecosystem; exact hosting, protocol and authorization configuration require release evidence.')
x.p('The website provides browser-based access to monitoring context. It should communicate the same engineering identity, time basis, quality and event state as the onsite platform. A remote user should be able to distinguish a network problem from an affected sensor node or a stale cached observation. No public website URL or frontend/backend framework was supplied, so neither is invented here.')
x.table(['Browser view concern','Contract to preserve','Review exercise'],[
('Site/node selection','Selection matches the record being rendered','Switch between nodes with visibly different identities'),
('Data age','Source time and connection state remain distinct','Disconnect remote access while keeping the local gateway alive'),
('Units','V/A/W/Wh/W/m²/°C are consistent','Compare a known reference fixture against Qt'),
('History','Window, timezone and gap policy are visible','Open a range containing a controlled outage'),
('Events','Same event ID/revision and condition meaning','Compare acknowledgement in onsite and remote views'),
('Authorization','A session sees only its approved scope','Review access using approved least-privilege test accounts'),
('Exports','Filters and revision context travel with the file','Reopen an exported window independently'),
('Recovery','A reconnect does not silently relabel old data live','Observe source time before/after connectivity returns')])
x.h('Publication checklist')
x.bullets(['Publish the real website URL only after its identity, ownership and intended access scope are confirmed.','State whether the site is LAN-only, remotely reachable through managed access, or hosted elsewhere; do not infer it from a screenshot.','Record the client release and compatible backend contract version.','Document session expiry, logout and reconnection behavior without exposing secrets or internal administration.','Provide real interface captures with build/time context; do not use the reference HMI illustration as proof of the website UI.','Keep remote monitoring distinct from a plant-control interface and from administrative gateway access.'],check=True)
x.p('The operational guide for a browser user begins with confirming identity and freshness, not with trusting a green connection icon. If the browser cannot reach the approved data path, last-known information must carry its source time and disconnection state. A remote failure should not require disabling protection or granting a public shell on the gateway.')
