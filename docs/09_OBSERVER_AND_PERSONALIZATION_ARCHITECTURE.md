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
