# PROJECT MAMMAL FOUNDING PACKET
## Compiled handoff copy


---

# SOURCE: `README.md`

# PROJECT MAMMAL
## Metacognitive Assessment & Machine Modeling of an Adaptive Learner
### Codename: Mammal Pod

**Research form:** publication-oriented intensive N-of-1 study  
**Participant:** one living original — Jonathan Lane  
**Repository role:** scientific instrument, provenance system, and longitudinal behavioral record  
**Primary question:**

> **When does an external model of a person predict that person's cognitive performance better than the person's explicit model of themselves?**

Project MAMMAL compares several informational vantage points:

- **Self:** Jonathan's locked answer and explicit confidence.
- **Generic Mantis:** an external model with no personal history.
- **Public-signal Mantis:** an observer allowed to see selected public cues such as answer text, latency, or speech.
- **Personalized Mantis:** an observer allowed to use only Jonathan's prior trials.
- **Independent Solver:** a model that can solve the current item, used to separate task competence from person modeling.
- **Future-State Mantis:** an observer predicting a later cognitive outcome, such as future recall, before that outcome exists.

The project is deliberately person-specific. It does not seek a population estimate or a universal claim about human metacognition. Its publication value comes from depth, provenance, construct separation, prequential prediction, and a reusable experimental architecture.

---

# Founding principles

1. **Big Boss remains the living original.** Mammal Pod is an evidence-backed model, not the person.
2. **Capture richly; interpret narrowly.** Preserve raw evidence and defer broad claims.
3. **Measurement precedes intervention.** Do not show personalized conclusions during an observation phase.
4. **Answer first, lock, then rate confidence.** Confidence elicitation must not silently merge with the first-order decision.
5. **A hypothesis pulls in a sensor.** Speech, latency, fatigue, or other inputs are added because a declared experiment needs them.
6. **Build the smallest reliable instrument that answers the current question.** Do not convert a probe into a platform because development is easy.
7. **No identity claim from sparse episodes.** Use time-bounded, domain-bounded language.
8. **Failed gates change epistemic status.** They do not become footnotes attached to confirmatory claims.
9. **The participant's current authority outranks the model.** Jonathan may contest, reinterpret, suspend, or retire any model-derived claim.
10. **Publishability is designed in from the beginning.** Protocol versions, ethics determination, preregistration, frozen analysis, and reproducible exports are first-class features.

---

# Locked founding decisions

- Separate repository from Les Enfants Terribles.
- Reuse LET's epistemic grammar and Metal Gear framing without sharing the live database.
- Preferred session budget: short, repeatable sessions of roughly 10–15 minutes.
- Four initial scientific domains:
  1. semantic/general knowledge;
  2. formal reasoning, with math/logic and short-code reasoning labeled separately;
  3. visual perception using random-dot motion;
  4. future memory using paired-associate learning and later recall.
- Voice-first final answers in semantic/reasoning/memory tasks.
- Manual left/right response for the initial perceptual reference condition.
- Numeric confidence shown only after answer lock.
- No trial-level correctness feedback during primary measurement blocks.
- Raw audio is a durable local artifact outside Git.
- Same desktop, browser, monitor, and approximately fixed viewing distance for perceptual sessions.
- Visual condition is initially **uncorrected vision**, explicitly documented; no claim of normal or corrected-to-normal vision.
- Flask + SQLite + server-rendered HTML/CSS for the application shell.
- jsPsych for timing-sensitive perceptual trials; HTMX and/or Alpine.js may support ordinary UI flows.
- Development order is controlled by dependencies and evidence gates, not time estimates.

---

# Read order

1. [`docs/00_PROJECT_CHARTER.md`](docs/00_PROJECT_CHARTER.md)
2. [`docs/01_METAL_GEAR_COGNITIVE_MODEL.md`](docs/01_METAL_GEAR_COGNITIVE_MODEL.md)
3. [`docs/02_RESEARCH_QUESTIONS_AND_NOVELTY.md`](docs/02_RESEARCH_QUESTIONS_AND_NOVELTY.md)
4. [`docs/03_RESEARCH_LANDSCAPE.md`](docs/03_RESEARCH_LANDSCAPE.md)
5. [`docs/04_EXPERIMENT_PROGRAM_AND_GATES.md`](docs/04_EXPERIMENT_PROGRAM_AND_GATES.md)
6. [`docs/05_DOMAIN_PROTOCOLS.md`](docs/05_DOMAIN_PROTOCOLS.md)
7. [`docs/06_PERCEPTUAL_PSYCHOPHYSICS_PROTOCOL.md`](docs/06_PERCEPTUAL_PSYCHOPHYSICS_PROTOCOL.md)
8. [`docs/07_INPUT_MODALITY_AND_ACQUISITION_CONTRACT.md`](docs/07_INPUT_MODALITY_AND_ACQUISITION_CONTRACT.md)
9. [`docs/08_DATA_AND_EPISTEMIC_MODEL.md`](docs/08_DATA_AND_EPISTEMIC_MODEL.md)
10. [`docs/09_OBSERVER_AND_PERSONALIZATION_ARCHITECTURE.md`](docs/09_OBSERVER_AND_PERSONALIZATION_ARCHITECTURE.md)
11. [`docs/10_STATISTICAL_ANALYSIS_PLAN.md`](docs/10_STATISTICAL_ANALYSIS_PLAN.md)
12. [`docs/11_TECHNICAL_ARCHITECTURE.md`](docs/11_TECHNICAL_ARCHITECTURE.md)
13. [`docs/12_DEVELOPMENT_SEQUENCE_AND_DEPENDENCIES.md`](docs/12_DEVELOPMENT_SEQUENCE_AND_DEPENDENCIES.md)
14. [`docs/13_RISKS_ETHICS_AND_GOVERNANCE.md`](docs/13_RISKS_ETHICS_AND_GOVERNANCE.md)
15. [`docs/14_PUBLICATION_AND_REPRODUCIBILITY_PLAN.md`](docs/14_PUBLICATION_AND_REPRODUCIBILITY_PLAN.md)
16. [`docs/15_PRODUCT_EXPERIENCE_AND_BRANDING.md`](docs/15_PRODUCT_EXPERIENCE_AND_BRANDING.md)
17. [`docs/16_DECISIONS_AND_OPEN_QUESTIONS.md`](docs/16_DECISIONS_AND_OPEN_QUESTIONS.md)
18. [`docs/17_RESEARCH_BIBLIOGRAPHY.md`](docs/17_RESEARCH_BIBLIOGRAPHY.md)
19. [`docs/18_SOURCE_LINEAGE.md`](docs/18_SOURCE_LINEAGE.md)

A compiled single-file handoff is generated as `PROJECT_MAMMAL_FOUNDING_PACKET.md`.

---

# Status language

- **Locked:** stable for the founding build or a frozen experiment.
- **Provisional:** current best design; must be validated before confirmatory use.
- **Open:** intentionally unresolved.
- **Diagnostic:** useful evidence that cannot support the primary claim.
- **Superseded:** preserved historical design no longer authoritative.
- **Deferred:** explicitly outside the current dependency chain.

---

# Repository boundary

Code, documentation, schemas, templates, and synthetic fixtures may live in Git.

The following do not belong in Git:

- raw participant audio;
- live SQLite database;
- identifiable private exports;
- local secrets or model credentials;
- derived files that can be regenerated and are too large for the repository.

The public repository should be reproducible without containing the private participant record.


---

# SOURCE: `AGENTS.md`

---
title: "Agent Rules for Project MAMMAL"
project: "Project MAMMAL"
project_code: "MAMMAL"
status: "active_rules"
version: "0.1"
owner: "Jonathan Lane"
---

# AGENTS.md

These rules apply to every human or AI agent planning, implementing, reviewing, analyzing, or documenting Project MAMMAL.

## 1. Primary behavior

Build the smallest reliable instrument that can answer the current experimental question.

Before substantive work, state:

- the research or design question;
- the smallest proposed change;
- the evidence that would justify keeping it;
- dependencies;
- what is explicitly out of scope.

Development speed is not evidence that a feature belongs in the instrument.

## 2. Read before acting

Read, in order:

1. `README.md`;
2. `docs/00_PROJECT_CHARTER.md`;
3. `docs/04_EXPERIMENT_PROGRAM_AND_GATES.md`;
4. `docs/08_DATA_AND_EPISTEMIC_MODEL.md`;
5. `docs/11_TECHNICAL_ARCHITECTURE.md`;
6. `docs/12_DEVELOPMENT_SEQUENCE_AND_DEPENDENCIES.md`;
7. `docs/13_RISKS_ETHICS_AND_GOVERNANCE.md`;
8. `docs/16_DECISIONS_AND_OPEN_QUESTIONS.md`.

## 3. Scope discipline

- Implement one meaningful vertical slice at a time.
- Do not add sensors without a named experiment.
- Do not add a personalized observer before generic and simple statistical baselines exist.
- Do not add live coaching during an observation phase.
- Do not build a participant dashboard that reveals model conclusions before the feedback/intervention protocol exists.
- Do not create confirmatory items live with an LLM.
- Do not silently change a frozen item bank, protocol, confidence scale, or analysis rule.
- Record adjacent ideas in the open-question ledger instead of expanding the current task.

## 4. Raw evidence is immutable

- Raw save precedes transcription, parsing, scoring, or model calls.
- Never edit raw audio or raw event payloads in place.
- Every artifact receives a SHA-256 hash.
- Every derived artifact declares its source artifacts and processor version.
- Transcription corrections append a correction event; they do not erase the original transcript.
- A failed ASR or observer call must never invalidate a successfully captured human response.
- Raw personal media never belongs in Git.

## 5. Epistemic separation

Keep distinct:

- what the prompt displayed;
- what Jonathan said;
- what the ASR transcript says;
- what answer was canonically locked;
- what the scorer concluded;
- what Jonathan reported as confidence;
- what an observer saw;
- what an observer predicted;
- what Mammal Pod inferred from prior history;
- what Jonathan later accepted or rejected;
- what changed after feedback or intervention.

Do not write identity-level conclusions from sparse evidence.

Preferred language:

> Across the currently observed semantic-knowledge trials, the model estimates...

Forbidden language:

> Jonathan is inherently bad at...

## 6. Observation and intervention

Observation Mode and Intervention Mode are separate protocol states.

During Observation Mode:

- hide personalized conclusions;
- hide current Mantis predictions;
- do not adapt item content using unregistered model judgments;
- do not provide trial-level correctness feedback unless the frozen protocol requires it.

If an intervention is shown, log:

- decision point;
- evidence available;
- intervention content;
- source/model/version;
- participant response;
- subsequent outcomes.

Never treat intervention-produced behavior as independent evidence of a pre-existing trait.

## 7. Participant authority

Big Boss is the living original.

Jonathan may:

- stop a session;
- withdraw a data segment from future analysis, subject to transparent tombstoning;
- correct a transcription;
- reject an interpretation;
- change future participation;
- retire the project.

A correction does not rewrite historical raw evidence.

## 8. Publication integrity

Before confirmatory data collection:

- obtain the appropriate ethics/IRB determination;
- freeze protocol and analysis;
- preregister or register the plan;
- freeze item-bank and observer versions;
- record code commit and environment manifest.

No ethics approval or exemption may be described retroactively.

## 9. Statistical discipline

- Report all prespecified primary outcomes.
- Separate exploratory from confirmatory analyses.
- Preserve session dependence in resampling or modeling.
- Do not select confidence bins, thresholds, domains, or observers after seeing confirmatory outcomes.
- A failed compliance gate makes the result diagnostic.
- Report Self on all valid Self trials as well as on shared observer intersections.
- Personalization must be evaluated prequentially.

## 10. Perceptual-task discipline

- Pin browser, display, plugin, and stimulus versions.
- Log actual frames and frame timing.
- Record viewport, device pixel ratio, refresh rate, and fullscreen state.
- Do not claim normal vision.
- Do not mix corrected and uncorrected vision inside a frozen protocol.
- If the visual condition changes, create a new protocol version.

## 11. Required evidence envelope

Every substantial agent result must include:

```markdown
## Result
What changed or was learned?

## Evidence
Tests, files, run IDs, hashes, figures, or citations.

## Epistemic status
Engineering / exploratory / diagnostic / confirmatory.

## Alternative explanations
What else could produce the result?

## Decision
Keep, revise, reject, or defer.

## Dependencies and next gate
What must be true before the next step?
```

## 12. No time estimates

Development plans use sequence, dependencies, and exit gates.

Do not estimate hours, days, weeks, or delivery dates.


---

# SOURCE: `docs/00_PROJECT_CHARTER.md`

# Project Charter
## Project MAMMAL

## 1. Mission

Project MAMMAL is a personal scientific instrument for measuring the relationship among:

- Jonathan's first-order cognitive performance;
- Jonathan's explicit self-monitoring;
- public behavioral signals such as answer content, latency, and speech;
- generic external model predictions;
- personalized model predictions based only on prior history;
- later cognitive outcomes such as future recall.

The project is designed to support a publishable intensive N-of-1 research program while remaining honest about its inferential population: **Jonathan Lane under the tested tasks, conditions, and periods**.

## 2. Core research question

> **When does an external model of this participant predict his cognitive performance better than his explicit model of himself?**

This decomposes into several subquestions:

1. How well does Self confidence discriminate correct and incorrect decisions?
2. How much of that signal can be recovered from item difficulty alone?
3. How much is recoverable from public behavior such as the locked answer, response time, or speech?
4. Does a personalized observer outperform a generic observer?
5. Does personalization outperform simple learner-model baselines?
6. Does the answer change across domains?
7. Who better predicts future cognitive states that cannot be solved at prediction time?
8. Does showing Mammal Pod's conclusions alter later behavior?

## 3. Inferential population

Primary inferential population:

> Jonathan Lane, using the frozen protocol and documented setup, on items sampled from the declared task families.

The project does not use N=1 as a disguised population study.

Any broader statement must be framed as:

- methodological possibility;
- hypothesis generation;
- instrument validation;
- or a claim requiring later replication.

## 4. Scientific contribution targets

Potential contributions, subject to literature review and empirical success:

- a provenance-rich framework for comparing human Self confidence to AI observers;
- a Human Privileged Access Index adapted from the Recurrence H0 observer architecture;
- separation of independent-solver skill, public-signal reading, and genuine personalization;
- prequential evaluation of a longitudinal model-of-one-person;
- comparison of explicit confidence with speech/prosody cues;
- future-memory prediction where ground truth does not exist at forecast time;
- domain-specific and cross-domain intensive metacognitive measurement;
- explicit handling of observation/intervention contamination.

## 5. Success criteria

The project succeeds if it can reliably produce any of the following:

- trustworthy estimates of Self calibration and discrimination within a domain;
- a valid comparison between Self and prespecified external observers;
- a reproducible speech/text/latency observer decomposition;
- evidence that personalized history adds predictive value over generic and statistical baselines;
- a future-state prediction experiment with honest prospective evaluation;
- a publishable methods or case-study manuscript with transparent limitations;
- a reusable open instrument that does not require releasing private raw media.

The project does not require a dramatic positive model-over-Self result to succeed.

## 6. Anti-goals

Project MAMMAL is not:

- a clinical diagnostic tool;
- a mental-health assessment;
- a general intelligence test;
- a universal metacognition score;
- a participant-ranking system;
- a passive surveillance platform;
- an identity oracle;
- a model leaderboard;
- a real-time coach during observation phases;
- proof that an AI knows the participant's mind;
- proof that introspection is absent when an observer wins;
- a reason to publish raw identifiable audio by default.

## 7. Operating philosophy

### Capture richly; interpret narrowly

Preserve raw signals because future questions may need them. Do not let signal availability create post-hoc hypotheses disguised as confirmatory tests.

### Observation before intervention

The model must first demonstrate predictive value without changing the behavior it later claims to predict.

### Simple baselines before romantic explanations

A personalized LLM must beat:

- item difficulty;
- domain base rate;
- recent accuracy;
- response latency;
- interpretable logistic/IRT/knowledge-tracing baselines.

### Domain before trait

Estimate semantic, formal, perceptual, and memory metacognition separately before discussing a cross-domain participant trait.

### The living participant outranks the representation

Mammal Pod may summarize evidence. It cannot define the participant.

## 8. Project boundary with LET

Project MAMMAL is a sibling of Les Enfants Terribles.

It inherits:

- Big Boss as living authority;
- GENE/MEME/SCENE/SENSE layers;
- Mammal Pod as evidence-backed model;
- CODEC-style interaction language;
- immutable raw evidence;
- observation/intervention separation;
- named failure modes.

It does not share LET's live canonical database.

Any bridge is explicit, versioned, and export-based.

## 9. Governing rule

> **Observed participant–instrument behavior is allowed to rewrite the plan, but only through explicit decisions and new protocol versions.**


---

# SOURCE: `docs/01_METAL_GEAR_COGNITIVE_MODEL.md`

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


---

# SOURCE: `docs/02_RESEARCH_QUESTIONS_AND_NOVELTY.md`

# Research Questions and Potential Novelty

## 1. Primary program question

> **Under what information conditions can an external computational observer predict this participant's cognitive performance better than the participant's explicit confidence?**

## 2. Primary constructs

### Self-monitoring

How well does explicit confidence predict the participant's own correctness?

### Public legibility

How much correctness information is present in externally observable behavior?

### Personalization

Does prior participant history improve prediction beyond a generic observer?

### Future-state modeling

Can an external model predict later recall or performance better than the participant's prospective judgment?

### Domain transfer

Do Self and observer advantages generalize across semantic, formal, perceptual, and memory domains?

### Reactivity

Does eliciting confidence, speaking, feedback, or model exposure change the behavior being measured?

## 3. Core estimands

The project should not collapse everything into one score.

### Self metacognitive discrimination

- AUROC2;
- Brier score;
- calibration intercept/slope;
- meta-d′ / M-ratio where appropriate.

### Human Privileged Access Index

```text
Human PAI = AUROC2(Self) - max(prespecified generic/public observers)
```

This asks whether explicit Self confidence contains trial-level correctness information unavailable to the strongest tested external public-information comparator.

It does not measure latent internal access directly.

### Personalization Gain

```text
Personalization Gain = score(Personalized Mantis) - score(matched Generic Mantis)
```

This is the central model-of-me estimand.

### Audio Leakage Gain

```text
Audio Leakage Gain = score(Audio observer) - score(Transcript-only observer)
```

This asks whether speech carries correctness information beyond lexical content.

### Future-State Advantage

```text
Future-State Advantage = score(Personalized Mantis) - score(Self forecast)
```

Used when the outcome does not yet exist, especially delayed recall.

### Solver Advantage

Independent solver performance is reported separately.

A solver beating Self may reflect task competence, not person modeling.

## 4. Initial hypotheses

These remain provisional until preregistered.

### H1 — Self is informative but imperfect

Within at least one domain, explicit confidence will discriminate correct from incorrect responses above chance but remain miscalibrated.

### H2 — public behavior contains additional correctness information

Answer text, latency, and/or speech will improve external prediction over item difficulty alone.

### H3 — audio contains incremental signal

Audio/acoustic observers will predict correctness above transcript-only observers on at least one spoken-answer domain.

### H4 — personalization adds value

A prequential personalized observer will outperform the matched generic observer after sufficient participant history exists.

### H5 — personalization is domain-sensitive

Personalization gain will vary materially across domains rather than forming one universal participant model.

### H6 — future memory is the cleanest model-of-me test

In delayed recall, a personalized observer may improve over generic prediction without the independent-solver explanation available in current-answer tasks.

### H7 — measurement is reactive

Confidence elicitation and response modality may alter first-order behavior in at least some domains.

## 5. Potential methodological contribution

The project could contribute a reusable architecture combining:

- intensive N-of-1 design;
- metacognitive measurement;
- AI observer ladders;
- prequential personalization;
- speech as public behavioral evidence;
- future-state prediction;
- immutable multimodal provenance;
- explicit observation/intervention separation.

## 6. Potential empirical contribution

The participant-specific case may reveal:

- domains where Self has a behavioral informational advantage;
- domains where external observers outperform Self;
- whether speech exposes errors not captured by explicit confidence;
- whether a personalized model learns stable participant-specific error patterns;
- whether those patterns drift;
- whether future-memory prediction differs from current-answer prediction.

## 7. Novelty caution

Novelty must not be asserted from memory.

Before manuscript framing:

1. conduct a structured literature search;
2. create an evidence table;
3. distinguish exact precedent from adjacent work;
4. state the contribution narrowly;
5. avoid presenting a new software combination as a new scientific construct.

## 8. Publication-shaped research products

Possible outputs:

### Methods / instrument paper

An open, provenance-rich platform for Human Self versus AI observer experiments.

### Intensive case study

Cross-domain Self and observer comparison in one deeply measured participant.

### Speech/prosody paper

Explicit confidence versus lexical and acoustic public signals.

### Personalized prediction paper

Prequential generic versus personalized model-of-me comparison.

### Future-memory paper

Self versus external prediction of delayed recall.

These are potential products, not promises.


---

# SOURCE: `docs/03_RESEARCH_LANDSCAPE.md`

# Research Landscape and Evidence Map

This document connects Project MAMMAL to neighboring research without claiming that those studies already answer its exact question.

Reference IDs map to `17_RESEARCH_BIBLIOGRAPHY.md`.

## 1. Human metacognition

Human metacognition research separates confidence bias, metacognitive sensitivity, and metacognitive efficiency. Meta-d′ was introduced to estimate Type-2 sensitivity in Type-1 SDT units while accounting for performance and response bias. [R01, R02]

Design implication:

- report confidence level and confidence–correctness discrimination separately;
- do not compare domains solely using raw confidence or AUROC2 when first-order regimes differ;
- use meta-d′ only when task and confidence data support it.

## 2. Confidence reactivity

Confidence judgments are not always passive. Concurrent confidence can impair perceptual decisions, while retrospective confidence is generally less reactive but can still add response burden. [R03]

Design implication:

> first-order answer → lock → retrospective confidence.

Answer-only control blocks are part of instrument qualification.

## 3. Speech as an accuracy channel

Speech prosody can encode both subjective confidence and objective accuracy. In prior work, acoustic features predicted accuracy beyond the speaker's explicit metacognitive awareness. [R04]

Design implication:

- preserve raw audio;
- distinguish transcript, acoustic, and combined observers;
- do not interpret acoustic prediction as subjective access;
- treat audio as public behavioral evidence.

## 4. Domain specificity

Recent work suggests confidence bias may generalize more readily across memory and perception than metacognitive sensitivity or efficiency. [R05]

Design implication:

- analyze semantic, formal, perceptual, and memory domains separately;
- treat a global participant trait as a later hypothesis;
- preserve domain-specific item and observer models.

## 5. Modeling human behavior

Centaur demonstrates that a language-model-based system can model trial-level human behavior across many psychological paradigms. [R06]

Design implication:

- store trials in model-readable form;
- compare LLM observers to interpretable cognitive/statistical baselines;
- do not assume a foundation model automatically learns one person from sparse history.

## 6. Social and actor–observer metacognition

Human observers can use another person's confidence, but confidence communication and ability differences can distort collaborative judgment. Actor–observer confidence studies show that judging another person's correctness is a legitimate metacognitive paradigm. [R07, R08]

Design implication:

Project MAMMAL should preserve the distinction between:

- Self confidence;
- observer prediction;
- observer knowledge of Self confidence;
- public answer evidence;
- personalized history.

## 7. Learner modeling

Knowledge tracing and Item Response Theory model future performance using learner history and item properties. [R09, R10]

Design implication:

Every personalized LLM observer must compete against:

- base-rate models;
- recent-performance models;
- item difficulty models;
- logistic/IRT-like models;
- knowledge-tracing-style state models.

## 8. Future memory

Delayed judgments of learning can predict later recall more accurately than immediate judgments under some conditions. The delayed judgment itself may also sample retrieval and thereby affect later memory. [R11, R12, R13]

Design implication:

- immediate and delayed JOLs are distinct interventions;
- exact cue format matters;
- future-memory prediction requires a protocol that acknowledges retrieval-practice contamination;
- Self and Mantis must predict before later recall is scored.

## 9. Browser psychophysics

JavaScript and jsPsych can capture behavior with useful sensitivity, though absolute response times and display timing depend on browser/device. Random-dot kinematograms have a published web implementation, and actual frame delivery should be logged. [R14, R15, R16]

Design implication:

- freeze browser and device;
- use fullscreen;
- log frames and refresh metadata;
- treat absolute RT cautiously;
- use within-setup comparisons;
- vendor and pin the RDK plugin.

## 10. N-of-1 and single-case reporting

SCRIBE provides reporting guidance for single-case behavioral research. CENT applies specifically to prospectively planned multiple-crossover N-of-1 trials and is relevant when Project MAMMAL tests repeated modality or feedback interventions. [R17, R18]

Design implication:

- use SCRIBE as the general reporting scaffold;
- use CENT/SPENT elements when randomized crossover interventions are introduced;
- report sequence, missingness, deviations, and precision.

## 11. Open science

OSF registrations create timestamped read-only study plans. Registered Reports separate publication decisions from results. [R19, R20]

Design implication:

- register engineering/exploratory/confirmatory phases separately;
- freeze code commits and analysis artifacts;
- publish deviations rather than rewriting history.

## 12. Self-experimentation ethics

Institutional policies commonly state that self-experimentation is still human-subject research when conducted as research, and approval cannot be retroactive. [R21, R22]

Design implication:

Before confirmatory data intended for publication:

- obtain a formal ethics/IRB determination appropriate to affiliation and venue;
- document self-consent and risk controls;
- do not assume self-participation creates an exemption;
- preserve the determination with the protocol.

## 13. Visual qualification

Published visual studies commonly require normal or corrected-to-normal vision. This project instead begins with a documented uncorrected participant condition and must not make population-normal vision claims. Browser-based visual acuity tools such as FrACT can support qualification, but they are screening/measurement tools rather than medical diagnosis. [R23]

Design implication:

- document uncorrected vision;
- conduct a reproducible acuity/visibility qualification;
- require stable task thresholds;
- if glasses are introduced, create a new protocol version.


---

# SOURCE: `docs/04_EXPERIMENT_PROGRAM_AND_GATES.md`

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


---

# SOURCE: `docs/05_DOMAIN_PROTOCOLS.md`

# Domain Protocols

Project MAMMAL begins with four domains because metacognitive bias, sensitivity, and efficiency may not generalize identically across tasks.

Each domain gets its own protocol ID, item bank, difficulty model, and primary analysis.

## 1. Semantic knowledge

### Purpose

Measure Self and observer correctness prediction in an objective knowledge domain.

### Default task

4-alternative forced choice.

The participant speaks the actual answer text, not merely a letter, when the answer is short enough.

### Trial

```text
visual question + four options
        ↓
private deliberation
        ↓
spoken final answer
        ↓
answer lock
        ↓
numeric confidence 0–100
        ↓
trial complete
```

### Item requirements

- objective, verifiable answer;
- source/provenance recorded;
- no trick wording unless declared;
- option order randomized;
- distractors plausible and format-matched;
- no answer uniquely identifiable by length/grammar;
- domain/subdomain tags;
- item-bank split: engineering, calibration, exploratory, confirmatory, reserve.

### Observer decomposition

- Item Only controls difficulty.
- Visible Answer Text uses the participant's answer.
- Independent Solver separates model knowledge from person modeling.
- Audio observer tests public speech signal.
- Personalized Mantis uses only prior participant trials.

### Key risk

Mantis Confound: model appears to know Jonathan but simply knows the fact.

## 2. Formal reasoning

### Scope

Keep at least two subdomains distinct:

- mathematics/logic;
- short-code reasoning.

Do not pool them by default.

### Default format

2AFC or 4AFC with deterministic scoring.

Examples:

- choose which conclusion follows;
- identify output of a short code snippet;
- detect a counterexample;
- choose which algebraic claim is correct;
- compare two algorithms or invariants.

### Rules

- freeze calculator/tool policy;
- freeze whether scratch paper is allowed;
- record use of external tools as an event;
- avoid time pressure in the first baseline;
- item solutions must be independently verified;
- code snippets must pin language/version assumptions.

### Personal relevance

This domain places the participant in an expertise-adjacent regime. It may reveal whether Self-monitoring improves with familiarity or whether overconfidence becomes stronger in a domain with a developed self-concept.

### Key risk

Task heterogeneity. “Formal reasoning” can become a bag of unrelated puzzles. Maintain explicit item families.

## 3. Visual perception

Detailed in `06_PERCEPTUAL_PSYCHOPHYSICS_PROTOCOL.md`.

### Initial reference

Random-dot motion direction discrimination:

- visual stimulus;
- manual left/right response;
- answer lock;
- numeric confidence.

### Why manual first

The perceptual task provides a conventional psychophysical anchor. Manual response avoids making speech a hidden extra manipulation in the reference condition.

### Follow-up

Spoken versus manual response becomes a randomized modality experiment.

### Key risk

Uncorrected vision and display timing. The study measures this participant under a documented setup, not normal vision.

## 4. Future memory

### Purpose

Predict a later cognitive state whose ground truth does not exist at forecast time.

### Item families

Potential starting families:

- arbitrary concrete-noun pairs;
- cue–pseudoword pairs;
- obscure factual associations;
- image–label pairs.

Avoid strongly associated pairs in confirmatory banks unless association strength is measured.

### Core phases

```text
ENCODE cue-target pair
        ↓
SELF forecast (immediate JOL or delayed JOL)
        ↓
MANTIS forecast
        ↓
predefined delay/next eligible recall event
        ↓
cued recall
        ↓
score future outcome
```

### Observer inputs

Possible ladders:

- item features only;
- encoding behavior;
- study duration;
- prior memory performance;
- immediate retrieval success if protocol permits;
- speech/latency signals;
- personalized history.

### Key risk

Delayed JOLs may cause retrieval practice and change future memory. Treat judgment timing and cue format as interventions, not harmless measurements.

## 5. Domain-comparison rules

- Report each domain separately first.
- Do not compare raw confidence levels without accounting for scale use.
- Do not infer a domain-general trait from a small number of tasks.
- Test transfer prospectively.
- Maintain conventional task names in publications.
- Preserve domain-specific public observer baselines.

## 6. Item-bank governance

Each item stores:

- unique ID;
- version;
- source;
- license;
- domain and family;
- prompt and alternatives;
- ground truth;
- explanation/verification;
- difficulty metadata;
- leakage checks;
- usage partition;
- first exposure date;
- retirement/supersession status.

An item used for participant training or feedback cannot silently re-enter a confirmatory bank.

LLM-generated items may be used only after independent verification and frozen human review. The model that generated an item must not be assumed to provide an unbiased difficulty estimate.


---

# SOURCE: `docs/06_PERCEPTUAL_PSYCHOPHYSICS_PROTOCOL.md`

# Perceptual Psychophysics Protocol
## Random-dot motion as the conventional reference task

## 1. Purpose

The perceptual branch provides a conventional, low-level decision task with an experimentally controllable evidence variable.

The initial task asks:

> Is the net direction of motion left or right?

Difficulty is manipulated through **motion coherence**: the proportion of dots supporting the true direction.

The purpose is not to diagnose vision or estimate a population-normal threshold. It is to create a stable participant-specific psychophysical reference for metacognitive measurement.

## 2. Participant visual condition

Founding condition:

- participant has prescription glasses but does not ordinarily wear them;
- initial protocol uses **uncorrected vision**;
- same desktop monitor and browser;
- approximately fixed viewing distance;
- fixed room/setup as practical.

The manuscript must not describe the participant as having normal or corrected-to-normal vision.

If the protocol later changes to glasses:

- create a new `vision_condition`;
- start a new calibration series;
- do not pool thresholds without an explicit model;
- record prescription currency if known, without treating the app as medical assessment.

## 3. Qualification before scientific trials

### 3.1 Visual acuity / visibility record

Before confirmatory perceptual work, record:

- uncorrected/corrected status;
- browser-based acuity or optotype screening result;
- whether each eye or binocular viewing is used;
- participant-reported difficulty;
- date and setup version.

A browser screening such as FrACT may be used as a reproducible measurement aid. It is not a diagnosis.

### 3.2 Display calibration

Record:

- monitor make/model if available;
- native resolution;
- operating-system scaling;
- browser/version;
- viewport size;
- device pixel ratio;
- refresh rate;
- fullscreen state;
- physical screen calibration;
- viewing distance;
- ambient-light protocol;
- frame timing diagnostics.

### 3.3 Task visibility

Engineering trials must show that:

- dot size is comfortably visible;
- high-coherence motion is reliably discriminable;
- low-coherence motion approaches chance without visual discomfort;
- left/right keys are understood;
- response mapping is counterbalanced or fixed and documented;
- no systematic rendering failures occur.

## 4. Technical implementation

Recommended client stack:

- jsPsych pinned to an exact version;
- `@jspsych-contrib/plugin-rdk` pinned/vendor-copied and checksummed;
- local static assets rather than CDN for frozen experiments;
- browser fullscreen;
- trial-level frame count and frame-rate logging;
- Flask backend for session/protocol assignment and result ingestion.

The RDK plugin is community-contributed, so Project MAMMAL must vendor, test, and audit the version rather than relying on unpinned upstream behavior.

## 5. Initial stimulus contract

The exact confirmatory parameters remain provisional until P00 passes.

The protocol must eventually freeze:

- aperture shape and visual angle;
- dot count/density;
- dot size;
- dot speed;
- dot lifetime;
- noise algorithm;
- stimulus duration;
- fixation duration;
- inter-trial interval;
- coherence levels;
- left/right direction balance;
- key mapping;
- feedback policy.

Founding design preferences:

- circular central aperture;
- high-contrast dots/background;
- stimulus large enough for the documented uncorrected setup;
- fixed short stimulus duration;
- left/right directions exactly balanced;
- no correctness feedback during measurement;
- numeric confidence after choice lock.

## 6. Calibration strategy

### Phase P00-A — visibility and gross range

Use a broad set of coherence values to locate:

- ceiling-like performance;
- mixed-error performance;
- chance-like performance.

### Phase P00-B — threshold estimation

Use a preregistered method such as:

- two interleaved 2-down/1-up staircases;
- weighted up-down;
- or a Bayesian threshold method.

The staircase is for calibration, not the final metacognitive dataset.

### Phase P00-C — held-out validation

Freeze one or more coherence levels and use fresh trials to verify:

- mixed-error accuracy;
- acceptable response bias;
- stable frame delivery;
- sufficient correct and incorrect classes;
- acceptable threshold stability.

### Confirmatory perceptual block

Use method of constant stimuli or a frozen difficulty mixture rather than continuing to adapt every confirmatory trial.

## 7. Trial sequence

```text
fixation
   ↓
RDK stimulus
   ↓
blank / response screen
   ↓
manual left/right response
   ↓
CHOICE_LOCKED
   ↓
0–100 confidence response
   ↓
CONFIDENCE_LOCKED
   ↓
no immediate correctness feedback
```

The confidence interface appears only after choice lock.

## 8. Primary measures

- accuracy;
- Type-1 `d′`;
- criterion `c`;
- response time;
- confidence distribution;
- AUROC2;
- Brier score;
- calibration;
- meta-d′ / M-ratio if estimable;
- frame/timing compliance.

## 9. Speech follow-up

The first modality experiment randomizes first-order response:

- manual left/right;
- spoken “left”/“right”.

Hold constant:

- visual stimulus;
- coherence distribution;
- confidence entry;
- feedback;
- item/trial generation.

Primary modality questions:

- Does speech change accuracy?
- Does speech change latency?
- Does speech change confidence bias?
- Does speech change AUROC2 or meta-d′?
- Does speech create usable acoustic correctness signal?

## 10. Safety and stopping

Stop a perceptual session if the participant reports:

- eye strain;
- headache;
- nausea;
- unusual visual disturbance;
- inability to see the stimulus clearly;
- equipment/setup drift.

Stopping is not protocol failure. It is a logged event.

The application is not a substitute for eye care.

## 11. Publication language

Safe:

> Under a fixed uncorrected-vision desktop setup, the participant completed a calibrated random-dot motion discrimination task.

Unsafe:

> The participant had normal visual motion processing.

Safe:

> Coherence was calibrated to produce a participant-specific mixed-error regime.

Unsafe:

> Coherence level measured a universal unit of cognitive difficulty.


---

# SOURCE: `docs/07_INPUT_MODALITY_AND_ACQUISITION_CONTRACT.md`

# Input Modality and Acquisition Contract

## 1. Primary non-perceptual trial flow

```text
PROMPT_SHOWN
  ↓
private deliberation
  ↓
ANSWER_CAPTURE_STARTED
  ↓
spoken final answer
  ↓
ANSWER_CAPTURE_ENDED
  ↓
canonical answer review/parser
  ↓
ANSWER_LOCKED
  ↓
CONFIDENCE_PROMPT_SHOWN
  ↓
numeric confidence entry
  ↓
CONFIDENCE_LOCKED
  ↓
TRIAL_COMPLETE
```

No backward transitions after lock.

## 2. Spoken final answer is not think-aloud

Primary baseline:

- reason privately;
- speak only the final response;
- do not narrate intermediate reasoning unless the protocol explicitly studies think-aloud.

Think-aloud is a separate Liquid manipulation because it can alter reasoning, timing, and error rates.

## 3. Answer lock

After `ANSWER_LOCKED`:

- semantic answer cannot change;
- answer timestamp cannot change;
- raw audio cannot be replaced;
- original transcript cannot be overwritten;
- confidence may not modify the answer.

If the participant notices a mis-speaking before lock, restart is allowed and logged.

After lock, a semantic correction is not allowed inside the trial. A later annotation may say “participant reported a slip,” but the locked response remains the scored response unless a preregistered exclusion rule applies.

## 4. ASR handling

Raw audio is authoritative evidence of what was spoken.

Store:

- original browser recording;
- derived normalized audio;
- ASR engine/model/version;
- original transcript;
- word/segment timing if available;
- ASR confidence metadata if available;
- correction events.

A correction event stores:

- original transcript;
- corrected transcript;
- correction actor;
- timestamp;
- reason;
- whether the canonical answer changes due only to ASR error.

The participant's spoken response and the ASR's text are distinct objects.

## 5. Confidence entry

Founding baseline:

- numeric 0–100;
- displayed only after answer lock;
- no default value;
- explicit lock required;
- keyboard entry and accessible slider/buttons allowed;
- record initial touched value, final value, and latency.

Manual confidence is preferred initially because it prevents confidence-ASR errors from contaminating the primary measurement while preserving speech for the first-order answer.

Spoken confidence may be studied later as a modality condition with separate audio.

## 6. Audio capture contract

Store per recording:

- raw WebM/Opus or browser-native format;
- start/end timestamps;
- MIME type;
- browser/device information;
- microphone identifier when available;
- bytes and SHA-256;
- derived WAV link;
- processing status.

Do not store audio BLOBs in SQLite.

Do not upload raw audio to third-party services by default.

## 7. Response latency

Define separate latency fields:

- prompt-to-capture-start;
- prompt-to-speech-onset;
- utterance duration;
- answer-end-to-lock;
- lock-to-confidence-start;
- confidence latency.

Do not collapse them into one response-time field.

## 8. Feedback

Primary measurement blocks:

- no trial-level correctness feedback;
- no Mantis prediction;
- no personalized performance summary.

Permitted neutral feedback:

- answer successfully recorded;
- confidence successfully locked;
- session progress;
- equipment warning.

Debrief or correctness feedback occurs only at frozen block/session boundaries if the protocol permits it.

## 9. Session context

Capture only prespecified context variables.

Founding variables:

- local timestamp;
- session ID/order;
- domain/protocol;
- device/browser;
- microphone;
- vision condition for perceptual tasks;
- interruptions flag;
- optional fatigue/alertness rating;
- feedback exposure state;
- experiment version.

Do not collect a giant lifestyle questionnaire because it might someday be useful.

## 10. Modality experiment design

When speech versus manual response is tested:

- randomize/counterbalance condition;
- hold item family and confidence method fixed;
- predefine exclusions;
- analyze order and period effects;
- preserve both modalities' raw event timing;
- do not pool conditions before testing reactivity.

## 11. Accessibility and participant comfort

The interface should support:

- large readable prompt text;
- keyboard-only operation;
- microphone level test;
- clear locked/unlocked state;
- easy session stop;
- no punitive language for missed sessions or errors.

MAMMAL is an instrument, not a productivity streak app.


---

# SOURCE: `docs/08_DATA_AND_EPISTEMIC_MODEL.md`

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


---

# SOURCE: `docs/09_OBSERVER_AND_PERSONALIZATION_ARCHITECTURE.md`

# Observer and Personalization Architecture

## 1. Why one “AI observer” is not enough

A model can predict participant correctness for different reasons.

The observer ladder separates those reasons.

## 2. Generic observer ladder

### Mantis/Item — item-only baseline

Sees:

- item prompt;
- options;
- domain/difficulty fields allowed by protocol.

Does not see:

- participant answer;
- confidence;
- audio;
- personal history;
- current outcome.

Question:

> How likely is this participant to answer this item correctly?

Controls item difficulty and generic participant base rate.

### Mantis/Text — visible-answer transcript

Sees:

- item;
- frozen canonical answer or transcript.

Does not see:

- confidence;
- audio;
- current outcome;
- personal history unless explicitly personalized.

Question:

> How likely is the frozen participant answer to be correct?

### Mantis/Audio — acoustic/public behavior

Variants:

- audio only;
- derived acoustic features only;
- audio + transcript;
- transcript + latency;
- combined public signal.

Does not see explicit confidence unless the specific study tests confidence communication.

### Mantis/Solver — independent solve

Independently solves or estimates candidate probabilities.

Purpose:

Separate task-solving competence from participant modeling.

Do not describe Solver advantage as personalization.

## 3. Personalized observers

### Mantis/Personal-Text

Sees:

- allowed prior participant trials;
- current item;
- current frozen answer.

### Mantis/Personal-Multimodal

May additionally see:

- prior audio/acoustic features;
- prior response timing;
- session/domain state;
- current permitted public signals.

### Mantis/Future

Predicts a later outcome such as recall.

The future outcome must not exist in the visible history.

## 4. Simple baselines

Before a personalized LLM earns explanatory attention, compare it with:

- overall/domain accuracy;
- item-only probability;
- recent moving accuracy;
- response-time logistic regression;
- confidence-history model;
- calibration-by-domain model;
- IRT-like ability × difficulty model where item information permits;
- knowledge-tracing or state-space learner model;
- regularized mixed-effects/logistic model.

## 5. Visibility contracts

Every observer has a named, versioned contract.

Example:

```yaml
id: VISIBLE_ANSWER_AUDIO_V1
current_item:
  prompt: true
  options: true
current_target:
  canonical_answer: true
  transcript: true
  raw_audio: true
  explicit_confidence: false
  current_outcome: false
history:
  allowed: false
```

A prompt is generated from the contract, not handcrafted ad hoc.

## 6. Frozen target rule

Participant answer and Self confidence are generated once.

Observer changes never rerun the participant target unless the study is explicitly a new replication.

This preserves the dependent behavior while observer interfaces are repaired or compared.

## 7. Prequential personalization

Personalized Mantis cannot train on the future.

At trial `t`:

```text
state_t = fit/update(history before t)
prediction_t = predict(current trial)
outcome_t becomes visible only after prediction is frozen
state_(t+1) may then incorporate outcome_t
```

Store a history manifest for every prediction.

## 8. Evaluation splits

Recommended layers:

- engineering/synthetic;
- exploratory history-building;
- frozen prequential evaluation;
- held-out sessions/blocks;
- optional transfer domain.

Do not randomly shuffle time when the scientific question is longitudinal personalization.

## 9. Human PAI and related contrasts

### Human PAI

```text
AUROC2(Self) - max(Item, Visible Text, prespecified public observers)
```

Whether Solver belongs in the primary max depends on the question:

- include Solver for a strong privileged-access test;
- report separately for “does the model know me?” because Solver skill is not personalization.

Freeze the comparator set before analysis.

### Personalization Gain

```text
Personalized - Generic matched observer
```

### Audio Leakage Gain

```text
Audio public-signal observer - transcript-only observer
```

### Future-State Advantage

```text
Personalized future observer - Self JOL
```

## 10. Compliance

Observer output requires:

- valid probability;
- valid schema;
- complete evidence manifest;
- no leaked outcome;
- successful prompt/model call.

A failed observer gate makes paired PAI diagnostic.

Report:

- condition-specific compliance;
- shared intersection size;
- Self metrics on all Self-valid trials;
- Self metrics on shared intersection;
- selection diagnostics.

## 11. Observer model governance

Freeze:

- model/checkpoint;
- provider/local digest;
- prompt template;
- system prompt;
- temperature;
- seed where applicable;
- tool access;
- context window;
- history compiler;
- output schema.

Changing any of these creates a new observer version.

## 12. Interpretation boundaries

Safe:

> The personalized observer improved predictive AUROC over the generic observer on held-out future trials.

Unsafe:

> The model understands Jonathan.

Safe:

> Audio contained incremental correctness information beyond transcript.

Unsafe:

> Jonathan's unconscious mind knew the answer.


---

# SOURCE: `docs/10_STATISTICAL_ANALYSIS_PLAN.md`

# Statistical Analysis Plan
## Founding framework

This is a framework, not a preregistration. Each confirmatory experiment receives its own frozen analysis plan.

## 1. Units of analysis

Primary unit:

- trial, nested within session/block and domain.

The project is N=1 at the participant level but contains repeated trial observations.

Trials are not automatically independent.

## 2. Primary descriptive outputs

For every domain/condition:

- number of trials;
- valid/missing counts;
- accuracy;
- response-position distribution;
- confidence distribution;
- mean/median response latency;
- session trajectories;
- item-family breakdown;
- feedback/intervention status.

## 3. Self metacognition

### Accuracy

Report point estimate and interval.

### Brier score

Primary probability-forecast accuracy metric.

### AUROC2

Primary non-parametric correctness-discrimination metric.

### Calibration

Prefer:

- reliability diagram with adequate bins or smoothing;
- calibration intercept and slope when estimable;
- mean confidence minus accuracy as descriptive bias.

Avoid unstable ECE-style metrics as the sole calibration summary in small samples.

### Type-1 SDT

For balanced 2AFC tasks:

- `d′`;
- criterion `c`;
- response rates;
- bootstrap/Bayesian intervals.

### Meta-d′

Use only when:

- the participant has both correct and incorrect trials;
- multiple confidence categories are populated;
- the task supports the chosen SDT formulation;
- the implementation is validated against a reference.

Report fit status and avoid manufactured values for degenerate confidence.

## 4. Observer comparison

All comparisons are trial-paired.

Report:

- observer AUROC2;
- Brier;
- calibration;
- paired Self–observer differences;
- shared valid intersection;
- compliance;
- bootstrap or Bayesian intervals.

For a joint max-comparator index, recompute the strongest observer within every bootstrap draw.

## 5. Repeated-measures uncertainty

Because trials cluster by session and may exhibit learning/drift:

Preferred resampling/modeling:

- session/block bootstrap when enough sessions exist;
- cluster bootstrap of trial trajectories;
- generalized estimating equations;
- mixed/state-space models with session effects;
- time-aware Bayesian models.

Do not bootstrap individual trials as if the longitudinal sequence does not matter when session dependence is visible.

## 6. Personalized prediction

Use prequential scoring.

Metrics:

- Brier;
- log loss where probabilities avoid exact 0/1 or are clipped by frozen rule;
- AUROC when both classes exist;
- calibration;
- paired gain over generic/statistical baseline.

Compare cumulative performance over time, but do not choose the “learning point” after looking without labeling it exploratory.

## 7. Domain structure

Primary domain-specific analyses precede cross-domain synthesis.

Cross-domain models may include:

- domain fixed effects;
- item family;
- modality;
- session/time;
- difficulty;
- observer type;
- observer × domain interactions.

Do not average meta-d′ across domains without a model and uncertainty.

## 8. Modality crossover

For speech/manual comparison:

- use paired item/block structure;
- include period/order effects;
- report carryover or learning concerns;
- analyze accuracy, RT, confidence, AUROC2, and meta-d′ separately;
- use SCRIBE/CENT-compatible reporting.

## 9. Future-memory outcomes

Depending on protocol:

- binary recall;
- graded recall score;
- latency;
- intrusion/error type.

Primary forecast metrics:

- Brier;
- AUROC2;
- calibration;
- Self vs generic/personalized observer contrast.

Missing future tests are outcomes of the protocol process and must be reported.

## 10. Precision planning

Do not choose confirmatory N by convention alone.

After exploratory data:

1. estimate accuracy and confidence distribution;
2. simulate planned estimators under realistic dependence;
3. vary trial/session counts;
4. choose a sample target based on interval width or decision error;
5. freeze the result before confirmatory collection.

The simulation code and assumptions become part of the preregistration.

## 11. Multiple comparisons

Each experiment declares:

- primary estimand;
- primary comparison;
- secondary outcomes;
- exploratory analyses.

Use hierarchical modeling or multiplicity control where families of secondary tests are interpreted jointly.

Do not hide negative secondary results.

## 12. Missingness and compliance

Report:

- why data are missing;
- condition-specific missingness;
- whether missingness predicts correctness, confidence, item difficulty, domain, or session;
- shared-intersection selection effects.

A low observer-compliance run cannot support confirmatory PAI merely because a shared subset exists.

## 13. Change over time

Longitudinal analyses may examine:

- calibration drift;
- learning;
- fatigue/session effects;
- model personalization gain;
- response-modality adaptation;
- effects of feedback exposure.

Time trends must be prespecified for confirmatory claims or labeled exploratory.

## 14. Claim language

### Confirmatory positive

Interval/decision rule satisfies preregistered criterion.

### Confirmatory negative relative to SESOI

Interval excludes the prespecified meaningful effect.

### Unresolved

Interval remains compatible with materially different conclusions.

### Diagnostic

Measurement or protocol gate failed.

### Exploratory

Analysis was not frozen before outcome inspection.


---

# SOURCE: `docs/11_TECHNICAL_ARCHITECTURE.md`

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


---

# SOURCE: `docs/12_DEVELOPMENT_SEQUENCE_AND_DEPENDENCIES.md`

# Development Sequence and Dependencies
## No calendar estimates; advancement is gate-based

Each stage depends on previous scientific and technical contracts.

```text
M0 Founding freeze
 ↓
M1 Core provenance kernel
 ↓
M2 Manual trial vertical slice
 ↓
M3 Voice acquisition vertical slice
 ↓
M4 Confidence and no-feedback protocol
 ↓
M5 E00 qualification and replay
 ├───────────────┐
 ↓               ↓
M6 Item banks    M7 Psychophysics engine / P00
 └───────┬───────┘
         ↓
M8 Human Self baseline engine
         ↓
M9 Generic observer ladder
         ↓
M10 Acoustic/public-signal pipeline
         ↓
M11 Personalized prequential models
         ↓
M12 Future-memory subsystem
         ↓
M13 Intervention/feedback mode
         ↓
M14 Publication/release pipeline
```

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


---

# SOURCE: `docs/13_RISKS_ETHICS_AND_GOVERNANCE.md`

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


---

# SOURCE: `docs/14_PUBLICATION_AND_REPRODUCIBILITY_PLAN.md`

# Publication and Reproducibility Plan

## 1. Publication stance

The project is an intensive N-of-1 program.

The manuscript should be explicit that the inferential participant population is one person.

Publication value comes from:

- methodological depth;
- repeated trials;
- preregistration;
- construct separation;
- transparent negative/unresolved results;
- provenance;
- open instrument/code;
- careful claim boundaries.

## 2. Ethics gate

Before confirmatory data:

- obtain the appropriate IRB/ethics determination;
- preserve approval/exemption/not-human-subject determination exactly as issued;
- register consent and risk plan;
- do not assume self-experimentation is exempt;
- do not describe approval retroactively.

## 3. Preregistration

Use OSF or an appropriate registry.

Register:

- research question;
- protocol;
- participant/inferential scope;
- domains;
- item partitions;
- primary estimands;
- observer set;
- compliance gates;
- precision/sample plan;
- exclusions;
- missingness handling;
- model versions;
- analysis code commit;
- stopping rules;
- data-sharing plan;
- deviations process.

Use separate registrations for substantively different experiments.

## 4. Registered Report option

Before the flagship confirmatory study, identify journals accepting Registered Reports in:

- metacognition;
- cognitive science;
- human–AI interaction;
- behavioral research methods;
- computational modeling.

A Registered Report is especially attractive because the result may be:

- Self advantage;
- observer advantage;
- no difference;
- failed measurement gate.

All are scientifically useful if the method is sound.

## 5. Reporting guidelines

Primary reporting scaffold:

- **SCRIBE 2016** for single-case behavioral research.

When using repeated randomized intervention periods/crossovers:

- apply relevant **CENT 2015** and/or SPENT elements.

Also report:

- exact protocol versions;
- completed sessions/blocks/trials;
- deviations;
- missingness;
- first-order performance;
- confidence distributions;
- effect estimates and intervals;
- adverse events/discomfort;
- feedback exposure;
- data/code availability.

## 6. Reproducibility bundle

Each paper/release includes:

- code commit/tag;
- environment lockfile;
- protocol snapshot;
- schemas;
- item-bank manifest or licensed access instructions;
- observer prompt/contracts;
- model versions/digests;
- frozen analysis export hash;
- analysis scripts;
- generated tables/figures;
- reporting checklist;
- deviation log;
- claim ledger.

## 7. Data sharing

Because raw audio identifies the participant, open-data ideals must be balanced with privacy.

Potential release levels:

### Public Tier A

- code;
- synthetic fixture data;
- protocol;
- analysis;
- aggregate results.

### Public Tier B

- de-identified trial-level behavioral data;
- derived timing/acoustic features after privacy review;
- item IDs/metadata.

### Controlled Tier C

- transcripts or richer personal history under access agreement.

### Private Tier D

- raw audio;
- unredacted private context;
- live database.

The manuscript states exactly what is unavailable and why.

## 8. Manuscript sequence

Sequence by evidence, not a promised schedule.

### Manuscript A — instrument/method

Focus:

- architecture;
- acquisition validity;
- observer contracts;
- N-of-1 provenance;
- measurement archaeology.

### Manuscript B — Self versus generic/public observers

Focus:

- domain-specific Self metacognition;
- Human PAI;
- public behavior.

### Manuscript C — speech/prosody

Focus:

- transcript versus acoustic prediction;
- incremental public signal.

### Manuscript D — personalization

Focus:

- prequential generic versus personalized models;
- simple baseline comparison;
- longitudinal gain/drift.

### Manuscript E — future memory

Focus:

- Self JOL versus generic/personalized Mantis;
- future-state prediction.

The actual output may combine or omit manuscripts depending on evidence.

## 9. Claim ledger

Every manuscript claim records:

- exact wording;
- estimand;
- evidence IDs;
- domain and time scope;
- uncertainty;
- preregistered/exploratory status;
- alternative explanations;
- prohibited stronger paraphrases.

## 10. Negative and unresolved results

The publication plan explicitly values:

- a confirmatory negative relative to SESOI;
- an unresolved result due to wide intervals;
- a diagnostic failed gate;
- a failed personalization model;
- no incremental audio signal.

These outcomes are not buried.

## 11. Independent review

Before preregistration and manuscript submission, seek external review from at least one person with relevant expertise in:

- metacognition/psychophysics;
- statistics/single-case methods;
- human-subject ethics;
- speech/acoustics when relevant.

Record review responses and design changes.

## 12. Public project narrative

The Metal Gear branding may appear in repository/UI/outreach.

The paper uses conventional terminology first and may explain the internal names in a short design note.

Science must remain understandable without franchise knowledge.


---

# SOURCE: `docs/15_PRODUCT_EXPERIENCE_AND_BRANDING.md`

# Product Experience and Branding
## CODEC inside Mother Base

## 1. Experience goal

The app should feel like a calm scientific instrument with playful Metal Gear flavor—not a gamified productivity system and not an ominous personality profiler.

The participant should always know:

- what mode is active;
- what is being recorded;
- what is locked;
- whether feedback is hidden;
- whether the current screen is observation or intervention;
- how to stop.

## 2. Naming map

| Internal/UI term | Scientific translation |
|---|---|
| Project MAMMAL | intensive N-of-1 metacognition project |
| Big Boss | participant |
| Mammal Pod | longitudinal evidence-backed participant model |
| Solid | Self report / metacognitive judgment |
| Mantis | external observer |
| Liquid | intervention/manipulation |
| Solidus | frozen claim/preregistration ledger |
| CODEC | participant interaction interface |
| Mother Base | repository/infrastructure |
| Mission Brief | experiment/session protocol summary |
| Debrief | permitted feedback/review phase |

## 3. Core screens

### Mother Base / home

Show:

- available protocols;
- observation/intervention mode;
- equipment status;
- recent session completion;
- pending scheduled recall tasks;
- data integrity status.

Do not show personalized performance claims during observation.

### Mission Brief

Before a session:

- domain;
- response modality;
- confidence method;
- feedback policy;
- expected task format;
- stop control;
- protocol/version.

Avoid exposing hypotheses that could bias behavior if blinding is desired.

### Trial screen

Minimal.

- prompt/stimulus;
- clear response action;
- no analytics;
- no model presence;
- visible recording/lock state.

### Confidence screen

Appears only after answer lock.

- 0–100 entry;
- no default;
- lock confirmation;
- no correctness clue.

### Session complete

Observation mode may show:

- trials captured;
- data saved;
- equipment warnings;
- next eligible session/recall state without performance evaluation.

### Mammal Pod review

Available only at declared review/intervention points.

Show:

- evidence range;
- uncertainty;
- domain/time scope;
- generic versus personalized model distinction;
- participant accept/reject/annotate controls;
- “what evidence was not shown?” audit.

## 4. Visual language

Suggested:

- restrained dark interface;
- amber/green status accents;
- clean mono labels for protocol metadata;
- no copyrighted character art or franchise logos;
- original abstract radar/codec motifs;
- conventional accessibility contrast and font sizing.

## 5. Tone

Good:

- “Answer locked.”
- “Confidence recorded.”
- “Observation mode: results hidden.”
- “This estimate applies to semantic trials in protocol v1 only.”

Bad:

- “Mammal Pod knows you better.”
- “You failed.”
- “Your true weakness is...”
- “Mantis predicts your mind.”

## 6. Mode indicators

### OBSERVATION

Blue/neutral.

No personalized feedback.

### INTERVENTION

Amber.

Explicit warning:

> This screen may change later behavior. The intervention will be logged.

### DEBRIEF

Green/white.

Evidence and interpretations may be reviewed.

## 7. Voice UX

- microphone qualification before session;
- waveform/level indicator without real-time semantic transcription by default;
- explicit start/stop;
- playback allowed before lock only if protocol permits;
- transcript hidden until after confidence in baseline protocols;
- raw save confirmation.

## 8. Perceptual UX

- fullscreen requirement;
- visual setup checklist;
- fixed viewing-distance reminder;
- keyboard mapping practice;
- frame-timing warning;
- stop immediately if discomfort.

## 9. Researcher/admin UI

Separate from participant mode.

Capabilities:

- protocol validation;
- item-bank management;
- artifact integrity;
- observer runs;
- preregistration/freeze status;
- deviation log;
- reports;
- backups.

Admin analysis must not leak into participant observation screens.


---

# SOURCE: `docs/16_DECISIONS_AND_OPEN_QUESTIONS.md`

# Decisions and Open Questions

## Active decisions

### D-MAMMAL-001 — Name the project Project MAMMAL

Full name:

**Metacognitive Assessment & Machine Modeling of an Adaptive Learner**

The app/model is Mammal Pod.

### D-MAMMAL-002 — Separate repository from LET

Reuse epistemic grammar and export bridges only.

### D-MAMMAL-003 — Intensive N-of-1 inferential scope

The primary scientific claims concern Jonathan under tested conditions, not a population.

### D-MAMMAL-004 — Four initial domains

- semantic knowledge;
- formal reasoning;
- visual perception;
- future memory.

### D-MAMMAL-005 — Voice-first non-perceptual answers

Speak final answer; do not think aloud by default.

### D-MAMMAL-006 — Manual perceptual reference

Random-dot left/right response uses keyboard first. Speech/manual becomes an experiment.

### D-MAMMAL-007 — Confidence after lock

Numeric confidence appears only after answer lock.

### D-MAMMAL-008 — No immediate trial feedback

Primary observation blocks hide correctness and model predictions.

### D-MAMMAL-009 — Raw audio is canonical local evidence

Stored outside Git with hashes and derivations.

### D-MAMMAL-010 — Fixed uncorrected-vision founding protocol

Same desktop/browser/distance. Document acuity/qualification. New protocol version if glasses are introduced.

### D-MAMMAL-011 — Flask/SQLite application shell

Use jsPsych for perceptual timing and a light JS layer only where justified.

### D-MAMMAL-012 — Gate-based development

Sequence and dependencies only; no development time estimates.

### D-MAMMAL-013 — Observation silence

Mammal Pod conclusions are hidden until a declared review/intervention phase.

### D-MAMMAL-014 — Publication-first governance

Ethics determination, preregistration, frozen analysis, and reproducible export precede confirmatory inference.

## Open questions

### O-MAMMAL-001 — Repository name/URL

Likely `mammal`, `project-mammal`, or `mammal-pod`.

No scientific dependency.

### O-MAMMAL-002 — Exact semantic item source

Need a licensed, verified, difficulty-diverse bank.

### O-MAMMAL-003 — Exact formal item families

Decide initial math/logic families and whether code reasoning enters the first field program or a separate protocol.

### O-MAMMAL-004 — Exact RDK parameters

Resolved through P00 qualification, then frozen.

### O-MAMMAL-005 — Visual acuity procedure

Choose FrACT or another reproducible screening method and document calibration.

### O-MAMMAL-006 — Observer model panel

Select at least one local/open observer and any external model, with publication/data policies.

### O-MAMMAL-007 — Raw audio retention

Define retention, encryption, backup, and withdrawal policies before confirmatory collection.

### O-MAMMAL-008 — Primary flagship estimand

Candidate:

- Human PAI in one domain;
- audio incremental gain;
- personalization gain;
- future-memory advantage.

The founding program keeps them separate until pilot precision is known.

### O-MAMMAL-009 — Confidence scale/binning

0–100 is locked for acquisition. Meta-d′ category transformation must be preregistered per task.

### O-MAMMAL-010 — Fatigue/context variables

Keep minimal initially; add only if justified by observed session effects.

### O-MAMMAL-011 — Feedback review cadence

Must balance scientific silence with participant engagement. Define block-level debrief gates before use.

### O-MAMMAL-012 — Ethics review path

Determine institutional or independent review mechanism and journal expectations before confirmatory data.

### O-MAMMAL-013 — Public data tier

Decide which derived audio features and trial-level variables can be shared safely.

### O-MAMMAL-014 — Registered Report target

Survey suitable journals once the first flagship experiment is fully specified.

## Reconsideration rule

Every active decision states a trigger for reconsideration in `templates/decision-record.md`.

A new preference or surprising pilot does not silently rewrite the protocol.


---

# SOURCE: `docs/17_RESEARCH_BIBLIOGRAPHY.md`

# Research Bibliography and Evidence Map

The bibliography prioritizes primary research, reporting standards, and official technical/ethics guidance.

## Evidence map

| ID | Theme | Source | Project use |
|---|---|---|---|
| R01 | Meta-d′ | Maniscalco & Lau (2012) | Type-2 sensitivity/efficiency framework |
| R02 | Measuring metacognition | Fleming & Lau (2014) | bias, sensitivity, efficiency, task-regime cautions |
| R03 | Reactivity | Double & Birney (2024) | answer lock before retrospective confidence |
| R04 | Speech | Goupil & Aucouturier (2021) | transcript/acoustic observer decomposition |
| R05 | Domain specificity | Baer, Ghetti & Odic (2026) | separate domains before global trait claims |
| R06 | Human behavior models | Binz et al. (2025) Centaur | model-readable trial histories and behavior prediction |
| R07 | Collective confidence | Bahrami et al. (2010) | interpersonal metacognition context |
| R08 | Actor–observer confidence | Allwood & Johansson (2004) | judging own versus others' knowledge answers |
| R09 | Knowledge tracing | Corbett & Anderson lineage | simple personalized learner-state baseline |
| R10 | Deep knowledge tracing | Piech et al. (2015) | longitudinal prediction benchmark |
| R11 | Delayed JOL | Nelson & Dunlosky (1991) | future-memory Self prediction |
| R12 | JOL cue conditions | Dunlosky & Nelson (1992) | cue format and delayed judgment |
| R13 | JOL reactivity | Spellman & Bjork (1992) | predictions can change future memory |
| R14 | RDK web software | Rajananda, Lau & Odegaard (2018) | random-dot implementation and frame logging |
| R15 | Browser RT | de Leeuw & Motz (2016) | jsPsych/browser timing sensitivity |
| R16 | jsPsych timing guidance | jsPsych documentation | implementation and timing audit |
| R17 | Single-case reporting | SCRIBE 2016 | reporting framework |
| R18 | N-of-1 crossover reporting | CENT 2015 | modality/feedback crossover studies |
| R19 | Preregistration | OSF Registrations | frozen transparent study plans |
| R20 | Registered Reports | COS/Registered Reports literature | outcome-independent publication path |
| R21 | Self-experimentation ethics | NIH/OHRP decision guidance | ethics determination before research |
| R22 | Investigator as participant | Johns Hopkins/UW policies | self-experimentation treated as human-subject research |
| R23 | Visual qualification | Freiburg Vision Test / visual-study conventions | document participant-specific uncorrected vision |

## References

### R01

Maniscalco, B., & Lau, H. (2012). A signal detection theoretic approach for estimating metacognitive sensitivity from confidence ratings. *Consciousness and Cognition, 21*(1), 422–430. https://doi.org/10.1016/j.concog.2011.09.021

### R02

Fleming, S. M., & Lau, H. C. (2014). How to measure metacognition. *Frontiers in Human Neuroscience, 8*, 443. https://doi.org/10.3389/fnhum.2014.00443

### R03

Double, K. S., & Birney, D. P. (2024). Confidence judgments interfere with perceptual decision making. *Scientific Reports, 14*, 14133. https://doi.org/10.1038/s41598-024-64575-7

### R04

Goupil, L., & Aucouturier, J.-J. (2021). Distinct signatures of subjective confidence and objective accuracy in speech prosody. *Cognition, 212*, 104661. https://doi.org/10.1016/j.cognition.2021.104661

### R05

Baer, C., Ghetti, S., & Odic, D. (2026). Domain generality is an emergent, not inherent, property of metacognition. *Nature Human Behaviour, 10*, 1316–1326. https://doi.org/10.1038/s41562-026-02443-2

### R06

Binz, M., Akata, E., Bethge, M., et al. (2025). A foundation model to predict and capture human cognition. *Nature, 644*, 1002–1009. https://doi.org/10.1038/s41586-025-09215-4

### R07

Bahrami, B., Olsen, K., Latham, P. E., Roepstorff, A., Rees, G., & Frith, C. D. (2010). Optimally interacting minds. *Science, 329*, 1081–1085. https://doi.org/10.1126/science.1185718

### R08

Allwood, C. M., & Johansson, M. (2004). Actor–observer differences in realism in confidence and frequency judgments. *Acta Psychologica*. https://doi.org/10.1016/j.actpsy.2004.06.006

### R09

Corbett, A. T., & Anderson, J. R. Knowledge tracing and Bayesian learner modeling lineage.

### R10

Piech, C., et al. (2015). Deep Knowledge Tracing. arXiv:1506.05908. https://arxiv.org/abs/1506.05908

### R11

Nelson, T. O., & Dunlosky, J. (1991). When people's judgments of learning are extremely accurate at predicting subsequent recall: The delayed-JOL effect. *Psychological Science, 2*(4), 267–271. https://doi.org/10.1111/j.1467-9280.1991.tb00147.x

### R12

Dunlosky, J., & Nelson, T. O. (1992). Importance of the kind of cue for judgments of learning and the delayed-JOL effect. *Memory & Cognition, 20*, 374–380. https://doi.org/10.3758/BF03210921

### R13

Spellman, B. A., & Bjork, R. A. (1992). When predictions create reality: Judgments of learning may alter what they are intended to assess. *Psychological Science, 3*, 315–317. https://doi.org/10.1111/j.1467-9280.1992.tb00680.x

### R14

Rajananda, S., Lau, H., & Odegaard, B. (2018). A Random-Dot Kinematogram for Web-Based Vision Research. *Journal of Open Research Software, 6*(1), 6. https://doi.org/10.5334/jors.194

### R15

de Leeuw, J. R., & Motz, B. A. (2016). Psychophysics in a Web browser? Comparing response times collected with JavaScript and Psychophysics Toolbox in a visual search task. *Behavior Research Methods, 48*, 1–12. https://doi.org/10.3758/s13428-015-0567-2

### R16

jsPsych. Timing Accuracy documentation and current official documentation. https://www.jspsych.org/latest/overview/timing-accuracy/

### R17

Tate, R. L., et al. (2016). The Single-Case Reporting Guideline In BEhavioural Interventions (SCRIBE) 2016 Statement. *Journal of Clinical Epidemiology, 73*, 142–152. https://www.equator-network.org/reporting-guidelines/scribe-statement/

### R18

Vohra, S., et al. (2015/2016). CONSORT extension for reporting N-of-1 trials (CENT) 2015 Statement. https://doi.org/10.1136/bmj.h1738

### R19

Open Science Framework. Registrations & Preregistrations documentation. https://help.osf.io/article/330-welcome-to-registrations

### R20

Center for Open Science. Registered Reports initiative and participating-journal resources. https://www.cos.io/initiatives/registered-reports

### R21

NIH IRB. Do you need to submit to the IRB? https://irbo.nih.gov/irb-review/do-you-need-to-submit-to-the-irb/

### R22

Johns Hopkins Medicine. Investigators as Study Participants (Self-Experimentation). https://www.hopkinsmedicine.org/institutional-review-board/guidelines-policies/guidelines/self-experimentation

University of Washington. Self-experimentation in human subjects research guidance. https://www.washington.edu/research/hsd/do-i-need-irb-review/does-your-research-involve-human-subjects/

### R23

Bach, M. Freiburg Vision Test (FrACT), browser-based visual acuity and contrast testing. https://github.com/michaelbach/FrACT10

## Research review rule

Before each manuscript:

- update searches;
- record search dates/databases/terms;
- classify direct precedents versus adjacent work;
- verify all current papers and versions;
- avoid citing this founding bibliography as if it were systematic.


---

# SOURCE: `docs/18_SOURCE_LINEAGE.md`

# Source Lineage

This packet synthesizes three source families.

## 1. Direct user decisions from the founding conversation

Locked inputs include:

- publication-first intensive N-of-1 scope;
- no intended general-population claim;
- short repeatable daily cadence;
- four domains including a conventional perceptual task from the beginning;
- willingness to delay correctness feedback;
- comfort with forced choice and durable local audio;
- same desktop/browser/viewing distance for perception;
- initial uncorrected-vision condition;
- manual left/right perceptual reference and speech follow-up;
- separate repository;
- Flask + SQLite + HTML/CSS/light JavaScript preference;
- no development time estimates;
- sequence and dependency planning.

## 2. Les Enfants Terribles source concepts

Adapted from the LET planning packet and rules:

- Big Boss as living original/final authority;
- GENE/MEME/SCENE/SENSE;
- Mammal Pod as evidence-backed evolving model;
- CODEC and Mother Base language;
- raw evidence immutability;
- observation/intervention separation;
- S3 Contamination;
- Venom Problem;
- Patriots Problem;
- Phantom Memory;
- Les Enfants Determinism;
- smallest reliable instrument;
- a hypothesis pulls in a sensor;
- no identity claim from sparse episodes.

Project MAMMAL is a sibling, not a database extension of LET.

## 3. Prior Human H0 research packet

Preserved concepts:

- Human Self versus AI observer distinction;
- speech as possible public accuracy signal;
- experiment ladder;
- append-only trial events;
- prequential personalization;
- future-memory branch;
- simple statistical baselines;
- voice-first acquisition.

This founding packet expands those notes into a complete research, governance, publication, and development system.

## 4. External research and standards

Mapped in `17_RESEARCH_BIBLIOGRAPHY.md`.

External sources inform:

- metacognitive measurement;
- reactivity;
- speech/prosody;
- domain specificity;
- behavior modeling;
- psychophysics;
- single-case reporting;
- preregistration;
- self-experimentation ethics;
- visual qualification.

They do not determine Project MAMMAL's empirical findings, which do not yet exist.

## 5. Authority rule

When this packet conflicts with a later frozen protocol:

1. ethics determination;
2. preregistered protocol/analysis;
3. frozen code and item manifests;
4. canonical decision log;
5. founding packet;
6. informal conversation notes.

The founding packet is architectural authority until superseded by explicit decisions.
