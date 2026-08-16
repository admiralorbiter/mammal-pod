# Data and Epistemic Model

## 1. Design objective

The data model must preserve the difference among:

- stimulus;
- participant behavior;
- raw recording;
- transcription;
- canonical scoring;
- participant confidence;
- observer-visible evidence;
- observer prediction;
- personalized state;
- interpretation;
- accepted claim;
- intervention;
- behavior after intervention.

The system should make it easier to be wrong safely.

## 2. Episode and trial

### Episode

A bounded participant session or research episode.

Suggested fields:

```yaml
id:
participant_id:
experiment_id:
protocol_version:
started_at:
ended_at:
mode: observation | intervention
status:
environment:
notes:
```

### Trial

A single first-order decision and its associated metacognitive/observer record.

```yaml
id:
episode_id:
item_id:
trial_index:
condition:
randomization_seed:
option_order:
prompt_shown_at:
completed_at:
```

## 3. Event sourcing

Trial state is derived from append-only events.

Core events:

- `trial.created`
- `prompt.shown`
- `stimulus.started`
- `stimulus.ended`
- `answer.capture_started`
- `answer.capture_ended`
- `answer.locked`
- `confidence.prompt_shown`
- `confidence.locked`
- `trial.completed`
- `transcription.created`
- `transcription.corrected`
- `outcome.scored`
- `feedback.shown`
- `observer.started`
- `observer.completed`
- `observer.failed`
- `claim.proposed`
- `claim.ratified`
- `claim.rejected`
- `data.withdrawal_requested`

Every event has:

```yaml
id:
event_type:
occurred_at:
recorded_at:
actor:
trial_id:
payload:
schema_version:
```

## 4. Core entities

### Participant

- pseudonymous stable ID;
- consent/ethics records;
- preferences;
- no identity-level model fields.

### Experiment

- research question;
- status;
- protocol hash;
- analysis-plan hash;
- ethics determination;
- preregistration ID;
- code commit;
- item-bank versions.

### Protocol

- trial flow;
- modality;
- confidence scale;
- feedback policy;
- exclusion rules;
- visibility contracts;
- stopping rules;
- analysis plan references.

### Item

- immutable content/version;
- domain/family;
- source/license;
- ground truth;
- option order template;
- difficulty metadata;
- partition;
- verification record.

### Answer

- modality;
- locked canonical answer;
- raw audio artifact;
- original transcript;
- response latencies;
- parser/scorer version.

### Confidence

- value;
- modality;
- lock time;
- optional raw audio;
- confidence scale/version.

### Outcome

- correct/incorrect or graded score;
- scoring rule/version;
- scorer provenance.

### Artifact

- raw or derived;
- MIME type;
- path;
- SHA-256;
- bytes;
- source artifact IDs;
- processor version;
- retention class.

### ObserverRun

- observer type;
- model/checkpoint/version/digest;
- prompt/visibility contract;
- history cutoff;
- temperature/seed;
- code commit;
- started/completed status.

### ObserverPrediction

- trial ID;
- `P(participant correct)`;
- compliance;
- raw output;
- latency;
- allowed evidence manifest.

### ParticipantStateSnapshot

Used only by personalized models.

- history cutoff;
- feature/model version;
- state representation;
- uncertainty;
- no current/future outcome.

### Claim

- conventional wording;
- Metal Gear shorthand;
- evidence IDs;
- scope/domain/time;
- uncertainty;
- status;
- ratification;
- superseded_by.

## 5. Epistemic labels

Every derived statement carries one:

- **RAW:** direct immutable artifact/event;
- **PARSED:** deterministic extraction;
- **SCORED:** result of declared scoring rule;
- **OBSERVED:** descriptive empirical pattern;
- **MODELED:** statistical/model estimate;
- **INTERPRETED:** explanation or inference;
- **RATIFIED:** accepted participant/project claim;
- **UNKNOWN:** unresolved.

## 6. Data authority

Authority order:

1. raw artifact/event;
2. deterministic parser/scorer with version;
3. participant correction linked to raw evidence;
4. observer/model output;
5. synthesis/interpretation;
6. accepted claim ledger.

Higher layers do not rewrite lower layers.

## 7. Personalization history

A personalized prediction must store:

- maximum event/trial timestamp visible;
- exact trial IDs visible;
- feature set;
- outcome availability;
- prompt/model state;
- whether audio/text/timing was allowed.

Prequential leakage tests should reconstruct the visible history and assert that current/future outcome fields are absent.

## 8. Data withdrawal and deletion

Because the participant is identifiable to himself, de-identification is not the only issue.

Support:

- exclusion from future model training/analysis;
- tombstoned withdrawal event;
- raw-media deletion if explicitly requested and legally/ethically permitted;
- impact report listing derived artifacts/models affected;
- separation between historical published aggregate claims and removable raw media.

Do not promise impossible deletion from already published public datasets.

## 9. Export classes

### Private full export

Contains identifiable raw media and complete event history.

### Reproducible analysis export

Contains trial-level variables required for analysis, with direct identifiers removed where possible.

### Public research export

May include:

- de-identified trial data;
- derived acoustic features;
- code;
- protocols;
- item metadata when licensing permits;
- synthetic fixtures.

Raw audio is not public by default.

## 10. Database invariants

- foreign keys enabled;
- WAL mode when concurrency requires;
- immutable artifact hashes;
- unique canonical trial IDs;
- transaction around critical state transitions;
- no `ANSWER_LOCKED` without answer artifact/value;
- no `CONFIDENCE_LOCKED` before answer lock;
- no observer prediction without visibility manifest;
- no personalized observer history extending beyond trial time;
- backup/restore verification;
- schema migrations versioned.
