# Risks, Ethics, and Governance

## 1. Ethics posture

Project MAMMAL is intended for publication and involves intervention/interaction with a living identifiable participant.

Self-experimentation does not automatically remove human-subject research obligations. Multiple institutional policies explicitly treat investigator-participants as human subjects.

Before confirmatory data collection intended for publication:

- seek a formal IRB/ethics determination appropriate to affiliation and publication venue;
- preserve the written determination;
- document self-consent;
- describe additional safeguards for the investigator-participant;
- do not claim retroactive approval.

If no institutional IRB is available, obtain qualified guidance on an appropriate independent review/determination path before proceeding to confirmatory research.

Engineering and private self-tracking may occur separately, but must not be retroactively relabeled as approved confirmatory human-subject research.

## 2. Risk categories

### Physical/visual discomfort

Random-dot motion and screen tasks may cause strain, headache, nausea, or discomfort.

Controls:

- participant stop control;
- short sessions;
- high-contrast visible stimuli;
- qualification gate;
- no punitive completion goals;
- log adverse events;
- protocol review if symptoms occur.

### Psychological/identity risk

Personalized models may produce discouraging or identity-shaping claims.

Controls:

- hidden results during observation;
- bounded language;
- participant authority;
- intervention gate;
- no clinical labels;
- explicit uncertainty;
- claim ratification.

### Privacy/identifiability

Voice, trial history, and domain performance are highly identifying.

Controls:

- local-first storage;
- raw audio outside Git;
- access controls;
- encrypted backups where practical;
- separate public derived dataset;
- deletion/withdrawal process;
- no default public raw audio.

### Data loss

Controls:

- atomic raw save;
- hashes;
- backup verification;
- restore rehearsals;
- derived data rebuildability.

### Scientific self-deception

The participant is also investigator and may consciously or unconsciously change behavior, analysis, or item selection.

Controls:

- preregistration;
- frozen code/item banks;
- blinded/hidden summaries;
- external methodological review;
- automated pipelines;
- deviation ledger;
- confirmatory/exploratory separation.

## 3. Metal Gear risk register

### S3 Contamination

Intervention-created behavior treated as natural evidence.

### Venom Problem

Participant performs the model's description.

### Patriots Problem

Hidden curation shapes the measured participant.

### Phantom Memory

Derived record becomes mistaken for lived fact.

### Les Enfants Determinism

Longitudinal pattern becomes identity destiny.

### Mantis Confound

Task-solving advantage becomes mistaken for person modeling.

### Shadow Moses Leakage

Future/current ground truth leaks into prediction.

### CODEC Reactivity

Interface changes the behavior it measures.

Each protocol names relevant failure modes and controls.

## 4. Observation silence

During Observation Mode, CODEC may show:

- session progress;
- successful capture;
- equipment status;
- protocol identity;
- neutral completion summary.

It must not show:

- current correctness unless protocol permits;
- Mantis prediction;
- domain weakness;
- calibration profile;
- personality/identity inference;
- personalized advice.

## 5. Self-consent record

The participant-consent document should state:

- project purpose;
- procedures;
- risks/discomfort;
- audio collection;
- data retention;
- publication/data-sharing plan;
- right to stop;
- right to withdraw future use where feasible;
- limits of deletion after publication;
- conflicts arising from investigator-participant dual role;
- non-clinical nature.

Use a neutral external reviewer if required or helpful.

## 6. Adverse-event and stopping log

Record:

- event type;
- severity;
- related task/protocol;
- participant action;
- whether session stopped;
- protocol decision;
- ethics notification if applicable.

No diagnosis is generated.

## 7. Model risks

### Hallucinated observer rationale

Observer rationales are optional derived artifacts and not evidence of actual computation.

### Model/version drift

Freeze checkpoints and prompts for inferential runs.

### Provider data handling

No identifiable raw media sent to external providers without explicit approved policy.

### Overfitting personalization

Use held-out/prequential evaluation and simple baselines.

### Model feedback loop

Personalized outputs remain hidden until an intervention study.

## 8. Question-bank risks

- copyrighted content;
- answer-key errors;
- duplicate exposure;
- model-generated leakage;
- trivial option cues;
- hidden cultural/domain bias;
- difficulty drift.

Controls are documented in item-bank governance.

## 9. Public-release policy

Default public release:

- code;
- protocols;
- schemas;
- synthetic data;
- de-identified/derived trial table if approved;
- acoustic features if privacy review allows;
- analysis scripts;
- reports.

Default non-public:

- raw voice;
- direct identifiers;
- private notes;
- unredacted observer prompts containing personal history;
- live database.

## 10. Governance decisions

High-impact decisions require explicit records:

- ethics status;
- new sensor;
- feedback/intervention activation;
- public data release;
- identity-level claim;
- protocol change after preregistration;
- new external provider;
- raw-media retention change.

## 11. Final governance question

> Does this capability improve the quality of evidence about Big Boss—or merely increase Mammal Pod's authority over him?
