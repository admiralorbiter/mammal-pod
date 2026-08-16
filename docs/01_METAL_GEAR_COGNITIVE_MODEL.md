# Metal Gear Cognitive Model
## Internal branding and epistemic architecture

The Metal Gear framing is intentionally tongue-in-cheek, but it is not decorative. It gives memorable names to roles, layers, and failure modes that otherwise become easy to blur.

Every term has a conventional research translation suitable for publication.

## 1. Project identity

### PROJECT MAMMAL

**Metacognitive Assessment & Machine Modeling of an Adaptive Learner**

Conventional translation:

> Intensive longitudinal N-of-1 metacognition and external-prediction study.

### Mammal Pod

The evidence-backed longitudinal model of the participant.

It may contain:

- trial history;
- domain-specific state estimates;
- observer predictions;
- calibration summaries;
- model versions;
- corrections;
- uncertainty;
- accepted and rejected interpretations.

It must never collapse into one opaque vector claimed to represent the participant.

## 2. Roles

### Big Boss — the living original

Jonathan is the participant and final authority.

Mammal Pod contains records and models. It does not contain Jonathan.

### Solid — the mirror

The explicit Self channel:

- locked first-order answer;
- explicit confidence;
- prospective judgment of future performance;
- optional later self-explanation when a protocol requests it.

Publication translation:

> participant self-report / metacognitive judgment.

### Mantis — the watcher

External observer models.

Variants:

- **Mantis/Item:** item difficulty only;
- **Mantis/Text:** prompt plus frozen answer transcript;
- **Mantis/Audio:** permitted speech signal;
- **Mantis/Solver:** independent task solve;
- **Mantis/Personal:** prior participant history;
- **Mantis/Future:** prediction of later cognitive outcome.

Publication translation:

> generic, multimodal, reconstructive, or personalized observer.

### Liquid — perturbation

Any condition that intentionally changes the participant or interaction:

- feedback;
- personalized advice;
- modality manipulation;
- confidence prompts presented concurrently;
- task coaching;
- showing Mammal Pod's conclusions.

Publication translation:

> intervention or experimental manipulation.

### Solidus — ratified claims

The frozen claim ledger:

- preregistered hypotheses;
- accepted findings;
- explicit uncertainty;
- supersession links;
- review conditions.

Publication translation:

> preregistration, decision log, and canonical claim record.

### CODEC — interaction layer

The application surface used to:

- receive mission brief;
- complete trials;
- lock answers;
- record confidence;
- review session status;
- enter debrief mode when allowed.

### Mother Base — infrastructure

The repository, local data root, backup system, workers, schemas, and analysis environment.

## 3. Four inheritance layers

### GENE — durable substrate

- original prompt;
- option order;
- raw audio;
- event timestamps;
- stimulus parameters;
- browser/display metadata;
- content hashes;
- immutable trial identity.

> **The archive is the genome, not the person.**

### MEME — transmitted and derived content

- transcript;
- canonical answer;
- explicit confidence;
- observer forecast;
- analysis summary;
- explanation;
- generated report.

MEME can be copied, recombined, and misunderstood.

### SCENE — context

- domain;
- task family;
- difficulty;
- modality;
- session;
- visual condition;
- device/browser;
- feedback history;
- recent performance;
- declared fatigue/context variables;
- whether an intervention has occurred.

A claim without Scene is usually too broad.

### SENSE — lived meaning

- what certainty felt like;
- embodied effort;
- frustration;
- surprise;
- personal significance;
- meaning that resists formalization.

SENSE is preserved cautiously. It is not inferred from prosody or latency without participant ratification.

## 4. System map

```text
                         BIG BOSS
                    living participant
                           │
                           ▼
                         TRIAL
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       GENE / MEME                SCENE / SENSE
       evidence/report            context/meaning
              │                         │
              └────────────┬────────────┘
                           ▼
                    ┌────────────┐
                    │ MAMMAL POD │
                    │ evidence   │
                    │ estimates  │
                    │ conflicts  │
                    │ uncertainty│
                    └─────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
            SOLID        MANTIS       SOLIDUS
          self report   observers      claims
              │            │            │
              └────────────┼────────────┘
                           ▼
                         CODEC
                           │
                           ▼
                       BIG BOSS
```

## 5. Named failure modes

### S3 Contamination

Liquid changes behavior. Mammal Pod later treats the changed behavior as independent evidence of a pre-existing trait.

Controls:

- separate observation and intervention phases;
- log every intervention;
- use pre-intervention baselines;
- never silently merge data across phases.

### Venom Problem

Big Boss starts performing Mammal Pod's description of him.

Controls:

- hide personalized conclusions during measurement;
- tentative language;
- explicit right to reject;
- periodic fit review;
- alternative models.

### Patriots Problem

Hidden curation determines what questions are shown and therefore what version of the participant gets measured.

Controls:

- inspectable item selection;
- frozen item-bank versions;
- log excluded/suppressed items;
- randomization seeds;
- no invisible model-generated curriculum in confirmatory blocks.

### Phantom Memory

A transcription error, model summary, or plausible observer explanation becomes treated as historical fact.

Controls:

- raw evidence immutability;
- derivation chains;
- source labels;
- correction events;
- no overwrite.

### Les Enfants Determinism

Repeated behavior is treated as fixed identity.

Controls:

- domain/time bounds;
- longitudinal change models;
- uncertainty;
- historical versions;
- explicit alternative explanations.

### Mantis Confound

An observer appears to know the participant when it is merely better at solving the item.

Controls:

- separate Independent Solver from personalized observer;
- compare generic and personalized observers;
- future-state tasks where the outcome does not exist at forecast time.

### Shadow Moses Leakage

Current or future ground truth leaks into the observer context or personal history.

Controls:

- prequential data assembly;
- frozen visibility contracts;
- audit current-outcome exclusion;
- tests that predict before scoring.

### CODEC Reactivity

The response interface changes the first-order decision or confidence policy.

Controls:

- answer lock before confidence;
- modality experiments;
- answer-only control blocks;
- exact prompt/version logging.

## 6. Final authority test

Before a new capability is enabled, ask:

> **Does this make Mammal Pod more useful to Big Boss—or does it increase the shadow's power over the living original?**
