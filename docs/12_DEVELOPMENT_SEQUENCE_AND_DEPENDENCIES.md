# Development Sequence and Dependencies
## No calendar estimates; advancement is gate-based

Each stage depends on previous scientific and technical contracts.

```text
M0 Founding freeze                       [COMPLETED & VERIFIED]
 ↓
M1 Core provenance kernel                [COMPLETED & VERIFIED]
 ↓
M2 Manual trial vertical slice           [COMPLETED & VERIFIED]
 ↓
M3 Voice acquisition vertical slice      [COMPLETED & VERIFIED]
 ↓
M4 Confidence and no-feedback protocol   [COMPLETED & VERIFIED]
 ↓
M5 E00 qualification and replay          [COMPLETED & VERIFIED]
 ├───────────────┐
 ↓               ↓
M6 Item banks    M7 Psychophysics engine [COMPLETED & VERIFIED]
 └───────┬───────┘
         ↓
M8 Human Self baseline engine            [COMPLETED & VERIFIED]
         ↓
M9 Generic observer ladder               [COMPLETED & VERIFIED]
         ↓
M10 Acoustic/public-signal pipeline      [COMPLETED & VERIFIED]
         ↓
M11 Personalized prequential models      [COMPLETED & VERIFIED]
         ↓
M12 Future-memory subsystem              [COMPLETED & VERIFIED]
         ↓
M13 Intervention/feedback mode           [COMPLETED & VERIFIED]
         ↓
M14 Publication/release pipeline         [PENDING DEPLOYMENT]
```

### Current Status:
- **Milestones M0 through M13** are fully implemented, tested across 100/100 automated tests, and live-verified with real human participant data across manual choice, spoken voice prosody, visual psychophysics RDK, and two-phase prospective memory (JOL).
- **Upcoming Work:** Expansion of the calibrated item bank (500+ items across Nelson-Narens/Tauber norms and science corpora) and longitudinal baseline data collection prior to milestone M14.

## M0 — Founding freeze

### Build

- founding documents;
- decision log;
- ethics path;
- repository conventions;
- protocol/item/observer schemas;
- private data-root contract.

### Exit gate

- core terms and boundaries accepted;
- initial domain program accepted;
- ethics determination plan documented;
- no unresolved issue blocks data modeling.

## M1 — Core provenance kernel

### Dependencies

M0.

### Build

- SQLAlchemy models/migrations;
- Experiment, Protocol, Item, Episode, Trial, Event, Artifact;
- hash service;
- append-only event API;
- integrity checks;
- backup manifest format.

### Exit gate

- synthetic trial can be created and replayed;
- raw/derived lineage is queryable;
- database can be rebuilt from fixture import;
- corruption tests fail safely.

## M2 — Manual trial vertical slice

### Dependencies

M1.

### Build

- visual prompt;
- forced-choice/manual answer;
- answer lock;
- confidence after lock;
- no-feedback mode;
- deterministic scoring;
- session UI.

### Exit gate

- state-transition rules enforced server-side;
- no answer edit after lock;
- complete event timeline;
- export reproduces score.

This slice allows early semantic/reasoning engineering without audio.

## M3 — Voice acquisition vertical slice

### Dependencies

M1 and M2 state machine.

### Build

- browser MediaRecorder;
- raw file save before processing;
- transcript adapter;
- canonical-answer parsing;
- correction events;
- microphone qualification.

### Exit gate

- raw audio never lost when ASR fails;
- transcript versions preserved;
- answer lock uses canonical participant response;
- audio/session replay works after restore.

## M4 — Confidence and observation-mode hardening

### Dependencies

M2/M3.

### Build

- no-default 0–100 confidence UI;
- confidence latency;
- observation-mode feature hiding;
- block/session feedback policies;
- answer-only control protocol support.

### Exit gate

- confidence cannot influence already locked answer through UI/API;
- no personalized conclusion visible in observation mode;
- prompt/version differences logged.

## M5 — E00 qualification, doctor, and replay

### Dependencies

M1–M4.

### Build

- engineering protocol;
- synthetic participant;
- end-to-end session tests;
- artifact verification;
- backup/restore;
- export/reimport;
- `mammal doctor`.

### Exit gate

E00 instrument qualification in `04_EXPERIMENT_PROGRAM_AND_GATES.md` passes.

No real scientific baseline begins before M5.

## M6 — Domain item-bank system

### Dependencies

M1, scoring from M2.

### Build

- item schemas;
- source/license fields;
- partitions;
- verification workflow;
- randomization;
- retirement/supersession;
- semantic and formal engineering banks;
- future-memory item generator/validator foundations.

### Exit gate

- confirmatory partition cannot be served in engineering mode;
- item hash/version stable;
- leakage and option-format checks pass;
- answer keys independently verified.

## M7 — Psychophysics engine and P00

### Dependencies

M1, M2, M5; item/protocol framework.

### Build

- jsPsych integration;
- vendored RDK plugin;
- display qualification;
- frame logging;
- visual acuity/condition record;
- staircase/calibration runner;
- held-out fixed-difficulty runner.

### Exit gate

P00 passes.

Perceptual data before this gate are engineering/diagnostic only.

## M8 — Human Self baseline engine

### Dependencies

M5, and M6/M7 for relevant domains.

### Build

- domain session scheduler;
- Self analysis;
- Brier/AUROC/calibration;
- SDT/meta-d′ where applicable;
- simulation-based precision planner;
- blinded/hidden result mode.

### Exit gate

At least one domain produces stable Self estimates under a frozen exploratory protocol.

## M9 — Generic observer ladder

### Dependencies

M8 frozen target manifests.

### Build

- visibility contract compiler;
- Item, Text, Solver observers;
- observer compliance;
- paired analysis;
- Human PAI;
- clean observer prompt separation.

### Exit gate

Observer validity gate passes on synthetic and exploratory target sets.

## M10 — Acoustic/public-signal pipeline

### Dependencies

M3 audio corpus, M8 target outcomes, M9 observer infrastructure.

### Build

- acoustic feature extraction;
- audio quality gate;
- transcript/timing/audio observer contracts;
- session-held-out evaluation;
- Audio Leakage Gain reports.

### Exit gate

Feature extraction reproducible and held-out public-signal predictions valid.

## M11 — Personalized prequential models

### Dependencies

Sufficient frozen historical trials; M9/M10 baselines.

### Build

- history compiler;
- prequential runner;
- simple statistical baselines;
- generic/personalized matched observers;
- leakage tests;
- longitudinal reports.

### Exit gate

Personalization Gain can be computed without future leakage and compared to simple baselines.

## M12 — Future-memory subsystem

### Dependencies

M1–M6, M8 analysis, M11 personalization.

### Build

- encoding events;
- JOL timing conditions;
- recall scheduling/event eligibility;
- cued recall scoring;
- missing recall handling;
- future-state observers.

### Exit gate

Forecasts are frozen before outcomes; recall events and contamination risks are auditable.

## M13 — Intervention/feedback mode

### Dependencies

Stable observation baseline; claim/feedback governance.

### Build

- controlled feedback conditions;
- model disclosure UI;
- randomized/crossover assignment;
- intervention event model;
- S3/Venom checks.

### Exit gate

Intervention effects can be separated from observation data.

## M14 — Publication and release pipeline

### Dependencies

Frozen experiment and analysis.

### Build

- OSF registration package;
- code/data manifests;
- SCRIBE/CENT checklist generator;
- private/public export;
- reproducible analysis container/environment;
- manuscript tables/figures;
- archival release.

### Exit gate

A clean environment reproduces the manuscript results from the public or controlled data package.

## Cross-cutting dependencies

### Ethics

Confirmatory human data cannot begin until the required determination exists.

### Precision planning

Confirmatory N cannot freeze until exploratory data support simulation.

### Model governance

Personalized/observer experiments cannot freeze until models and prompts are versioned.

### Privacy

Public release cannot proceed until the audio/identifiability policy is frozen.

### No skipped gates

A later module may be prototyped in isolation, but it cannot produce confirmatory evidence if its dependencies have not passed.
