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
