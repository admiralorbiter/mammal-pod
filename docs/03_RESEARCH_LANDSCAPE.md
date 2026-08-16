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
