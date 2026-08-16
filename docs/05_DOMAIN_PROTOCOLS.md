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
