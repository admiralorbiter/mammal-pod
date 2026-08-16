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
