# Experiment Program and Gates

The program advances through evidence gates rather than calendar milestones.

## Program overview

```text
E00  Instrument qualification
 ↓
E01  Domain-specific Human Self baselines
 ↓
E02  Generic observer ladder
 ↓
E03  Speech/public-signal decomposition
 ↓
E04  Response-modality crossover
 ↓
E05  Personalized Mantis
 ↓
E06  Future-memory prediction
 ↓
E07  Cross-domain synthesis
 ↓
E08  Feedback/intervention study
```

Perceptual qualification (`P00`) runs before confirmatory perceptual trials.

## E00 — Instrument qualification

### Question

Can the system preserve a complete, immutable, replayable trial record?

### Includes

- synthetic trials;
- manual answer trials;
- speech capture;
- confidence locking;
- transcription correction;
- scoring;
- observer replay;
- export/reimport;
- backup/restore.

### Exit gate

- no critical event omissions in the qualification corpus;
- answer cannot change after lock;
- confidence cannot precede answer lock;
- raw audio hashes verify after backup/restore;
- corrections preserve original artifacts;
- every trial can be replayed deterministically from protocol + item + event log;
- shared export reproduces analysis input exactly.

No cognitive result is interpreted during E00.

## P00 — visual/perceptual qualification

### Question

Can the fixed uncorrected-vision setup present and record a stable random-dot motion task?

### Exit gate

- fixed display/browser protocol recorded;
- frame delivery meets protocol limits;
- visibility/acuity screening completed and documented;
- left/right response mapping works without systematic hardware errors;
- coherence manipulation produces a usable mixed-error range;
- repeated threshold blocks are acceptably stable;
- no severe response-position bias;
- no eye strain or participant safety concern requiring protocol change.

Failure creates a new visual protocol version; it does not invite ad hoc parameter changes inside a frozen block.

## E01 — Human Self baselines

Run separately by domain.

### Question

How well does explicit confidence predict the participant's own correctness?

### Primary outcomes

- accuracy;
- Brier score;
- AUROC2;
- confidence level/bias;
- calibration curve or intercept/slope;
- response latency;
- compliance.

### Conditional outcomes

- Type-1 `d′` and `c` for suitable forced-choice designs;
- meta-d′ / M-ratio when confidence categories and class counts are sufficient.

### Exit gate

- protocol compliance passes;
- both correct and incorrect classes are sufficiently represented for the planned estimands;
- estimates meet preregistered precision requirements from simulation;
- session instability and learning trends are reported;
- no hidden feedback contamination.

## E02 — Generic observer ladder

Freeze E01 target trials.

### Observers

- Item Only;
- Visible Answer Text;
- Independent Solver;
- optional same-task generic model panel.

### Question

Does Self contain behavioral correctness information beyond the strongest prespecified external observer?

### Exit gate

- observer visibility contracts pass tests;
- no target confidence leakage;
- high observer compliance;
- shared valid intersection remains representative enough for inference;
- pairwise and joint contrasts use paired trial IDs;
- failed gate produces diagnostic status.

## E03 — speech/public-signal decomposition

### Observers

- transcript only;
- timing only;
- acoustic features only;
- audio+transcript;
- combined public-signal model.

### Question

Does emitted behavior contain correctness information beyond explicit Self confidence?

### Key contrasts

- Audio vs Transcript;
- Public Signals vs Self;
- Public Signals vs Item Only;
- Public Signals controlling for domain and difficulty.

### Exit gate

- feature extraction is reproducible;
- model evaluation is held out by session/block;
- no current confidence leakage;
- audio quality gate passes;
- predictions are generated without using current outcome.

## E04 — response modality crossover

### Question

Does spoken versus manual first-order response change accuracy, latency, confidence, or metacognitive discrimination?

### Design

Randomized repeated crossover within the participant.

Primary first manipulation:

- manual/keyboard answer;
- spoken final answer;
- same visual prompt;
- same confidence interface;
- counterbalanced item sets.

### Gate

- enough repeated periods/blocks for planned crossover analysis;
- no uncontrolled protocol drift;
- order/period effects examined;
- reporting follows relevant CENT/SCRIBE elements.

## E05 — personalized Mantis

### Question

Does prior participant history improve prediction beyond generic and statistical observers?

### Evaluation

Prequential only.

For trial `t`:

```text
history = completed trials before t
predict t
reveal outcome t
append t to history
```

### Required baselines

- domain base rate;
- item-only model;
- recent-accuracy logistic model;
- item-difficulty model;
- response-time model;
- knowledge-tracing/participant-state baseline where appropriate;
- generic LLM observer.

### Exit gate

- no future leakage;
- history window/version frozen;
- personalization gain has paired uncertainty;
- improvement replicates across held-out sessions or blocks;
- explanation does not exceed evidence.

## E06 — future memory

### Question

Who better predicts later recall: Self, generic Mantis, or personalized Mantis?

### Conditions

- immediate JOL;
- delayed JOL, if included;
- optional retrospective confidence after a practice retrieval;
- later cued recall.

### Gate

- outcome is generated after forecast;
- prediction timing is explicit;
- retrieval-practice effects are modeled or controlled;
- item pairing and delay conditions are frozen;
- missing future tests are reported, not silently dropped.

## E07 — cross-domain synthesis

### Question

Which participant-level features generalize, and which remain domain-specific?

### Rules

- do not pool raw AUROC2/meta-d′ across domains without a model;
- report confidence bias and discrimination separately;
- compare personalized gain by domain;
- test transfer prospectively;
- preserve task-format differences.

## E08 — Mammal Pod feedback/intervention

### Question

What happens when the participant sees or acts on the external model?

This is the first phase that intentionally opens the Pod.

Possible interventions:

- calibration feedback;
- pre-answer warning;
- post-answer disagreement signal;
- domain-specific strategy prompt;
- model-of-me summary.

### Gate

- pre-intervention baseline frozen;
- intervention is randomized or otherwise explicitly designed;
- S3 Contamination and Venom Problem controls are active;
- no post-intervention behavior is misclassified as natural baseline.

## Formal horizon gates

### Gate A — instrument validity

E00 and P00 pass.

### Gate B — Self construct validity

At least one domain produces stable, interpretable Self estimates.

### Gate C — observer validity

Generic observers produce valid predictions under frozen visibility contracts.

### Gate D — personalization validity

Personalized Mantis is evaluated prequentially against simple and generic baselines.

### Gate E — publication readiness

Ethics determination, preregistration, frozen code/data manifests, analysis reproducibility, claim ledger, and reporting checklist are complete.
