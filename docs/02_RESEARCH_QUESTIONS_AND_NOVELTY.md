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
