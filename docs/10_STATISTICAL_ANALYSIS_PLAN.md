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
