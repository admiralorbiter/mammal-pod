# Technical Architecture
## Flask, SQLite, HTML/CSS, and a focused JavaScript experiment layer

## 1. Architectural stance

Project MAMMAL should be technically conservative and scientifically strict.

Use:

- Flask for routing, protocol/session control, APIs, and administration;
- SQLAlchemy + Alembic for relational persistence and migrations;
- SQLite with foreign keys, transactions, and WAL where useful;
- Jinja + HTMX for ordinary app flows;
- Alpine.js only where a small client state machine improves usability;
- jsPsych for timing-sensitive perceptual and keyboard trials;
- browser `MediaRecorder` for speech capture;
- filesystem artifact storage with SQLite metadata;
- replaceable ASR and acoustic-analysis adapters;
- Python analysis packages producing frozen Parquet/JSON outputs.

Do not use a JavaScript framework as the scientific state authority.

## 2. Boundary diagram

```text
                         FLASK APPLICATION
┌─────────────────────────────────────────────────────────────────┐
│ Protocol registry   Session controller   Admin/review interface │
│ Item-bank service   Trial ingestion      Observer orchestration │
└───────────────┬───────────────────────┬─────────────────────────┘
                │                       │
                ▼                       ▼
      SERVER-RENDERED FLOWS       JSPSYCH EXPERIMENT RUNNER
      voice/semantic/memory       RDK/manual timed tasks
                │                       │
                └───────────┬───────────┘
                            ▼
                   APPEND-ONLY TRIAL EVENTS
                            │
            ┌───────────────┼────────────────┐
            ▼               ▼                ▼
        SQLITE DB       ARTIFACT STORE    JOB/PROCESSOR QUEUE
                            │
                            ▼
               ASR / ACOUSTIC / OBSERVER OUTPUTS
                            │
                            ▼
                   FROZEN ANALYSIS EXPORTS
```

## 3. Suggested repository shape

```text
mammal/
├── README.md
├── AGENTS.md
├── pyproject.toml
├── .gitignore
├── alembic.ini
├── docs/
├── schemas/
├── templates/                 # research record templates
├── config/
│   ├── protocols/
│   ├── observers/
│   └── environments/
├── src/
│   └── mammal/
│       ├── app.py
│       ├── config.py
│       ├── db.py
│       ├── models/
│       ├── protocols/
│       ├── items/
│       ├── trials/
│       ├── events/
│       ├── artifacts/
│       ├── capture/
│       │   ├── audio.py
│       │   ├── manual.py
│       │   └── confidence.py
│       ├── psychophysics/
│       │   ├── jspsych_bridge.py
│       │   ├── rdk.py
│       │   └── timing.py
│       ├── scoring/
│       ├── observers/
│       │   ├── contracts.py
│       │   ├── generic.py
│       │   ├── solver.py
│       │   ├── audio.py
│       │   └── personalized.py
│       ├── processors/
│       │   ├── asr.py
│       │   ├── acoustics.py
│       │   └── exports.py
│       ├── analysis/
│       ├── reports/
│       ├── web/
│       │   ├── routes/
│       │   ├── templates/
│       │   └── static/
│       └── cli.py
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── end_to_end/
│   ├── fixtures/
│   └── synthetic_participant/
├── vendor/
│   └── jspsych-rdk/
└── instance/
    └── local config only
```

The live data root is configured separately and ignored.

## 4. SQLite use

SQLite stores:

- participants;
- experiments;
- protocols;
- item metadata;
- sessions/episodes;
- trials;
- events;
- answers;
- confidence;
- outcomes;
- artifact metadata;
- processor runs;
- observer runs/predictions;
- state snapshots;
- claims/decisions/deviations.

Use:

- foreign keys;
- transactions;
- schema versioning;
- uniqueness constraints;
- WAL if browser/worker concurrency needs it;
- integrity checks;
- idempotency keys for job retries.

Binaries remain on disk.

## 5. Artifact storage

Suggested root:

```text
MAMMAL_DATA_ROOT/
├── raw/
│   ├── audio/
│   ├── protocol_snapshots/
│   └── observer_outputs/
├── derived/
│   ├── wav/
│   ├── transcripts/
│   ├── acoustic_features/
│   └── reports/
├── exports/
│   ├── private/
│   ├── analysis/
│   └── public/
├── database/
└── backups/
```

Artifact IDs are content-addressed or accompanied by SHA-256.

## 6. Protocol engine

A protocol defines:

- trial state machine;
- allowed modalities;
- item bank/partition;
- randomization;
- feedback;
- confidence scale;
- stopping rules;
- observer contracts;
- analysis-plan reference;
- ethics/preregistration references.

Protocol snapshots are immutable once a frozen experiment begins.

## 7. Trial acquisition

### Server-driven flow

Best for:

- spoken knowledge/reasoning trials;
- confidence entry;
- future-memory encoding/recall;
- session administration.

### jsPsych flow

Best for:

- RDK presentation;
- precise keyboard responses;
- reaction-time blocks;
- randomized modality trials if integrated carefully.

jsPsych returns a signed/hashed result payload to Flask. Flask validates protocol, item, trial identity, and transition order before committing events.

## 8. Audio pipeline

```text
MediaRecorder raw WebM
      ↓ raw save + hash
ASR job
      ↓
transcript artifact + metadata
      ↓
optional correction event
      ↓
acoustic feature job
      ↓
versioned feature table
```

Adapters:

- local faster-whisper/whisper.cpp;
- optional manual transcription;
- Praat/parselmouth/librosa feature extraction;
- future multimodal model adapter.

No observer sees audio unless its visibility contract permits it.

## 9. Observer execution

Observer jobs are reproducible units containing:

- frozen target trial manifest;
- visibility contract;
- prompt compiler version;
- model adapter/version;
- output schema;
- run seed/config;
- raw response artifact;
- parsed probability;
- compliance result.

Observer runs never update target trials.

## 10. Personalized state

Start with simple explicit histories and statistical models.

Do not build an opaque vector store as the canonical Mammal Pod.

Canonical state is inspectable:

- prior trial table;
- feature definitions;
- model parameters/version;
- history cutoff;
- uncertainty;
- performance summaries.

Embeddings may be derived caches later, never sole authority.

## 11. Job execution

A simple database-backed durable job queue is sufficient.

Jobs:

- transcription;
- audio derivation;
- acoustic features;
- scoring;
- observer calls;
- exports;
- report generation;
- backup verification.

Requirements:

- idempotent or version-producing;
- retry-safe;
- failure does not corrupt raw capture;
- input/output artifact IDs recorded.

## 12. Security and privacy

- local-first data root;
- secrets outside Git;
- least-privilege observer exports;
- raw audio not sent externally without explicit run policy;
- encrypted backup where practical;
- export audit log;
- participant-controlled deletion/withdrawal path.

## 13. Testing strategy

### Unit

- schemas;
- state transitions;
- scorers;
- visibility compilers;
- statistics;
- hashing.

### Integration

- audio capture ingestion;
- ASR correction;
- jsPsych payload validation;
- observer jobs;
- export/reimport;
- migration integrity.

### End-to-end

- synthetic participant completes a full session;
- frozen target observer battery;
- prequential personalization with leakage traps;
- backup/restore/replay;
- report regeneration.

### Scientific regression fixtures

- known calibration examples;
- known AUROC/Brier/meta-d′ fixtures;
- response-bias fixtures;
- missingness selection fixture;
- current-outcome leakage fixture;
- RDK frame/timing fixture where feasible.

## 14. Developer tooling

Provide CLI commands such as:

```text
mammal doctor
mammal db check
mammal artifacts verify
mammal protocol validate <file>
mammal experiment freeze <id>
mammal session start <protocol>
mammal observer run <contract> <target_manifest>
mammal export analysis <experiment>
mammal report build <experiment>
mammal backup verify
```

## 15. Deliberate non-features at founding

- no passive screen recording;
- no wearable integration;
- no continuous microphone;
- no autonomous feedback;
- no identity dashboard;
- no vector database requirement;
- no model fine-tuning;
- no multi-participant account system;
- no cloud dependency for core capture.
