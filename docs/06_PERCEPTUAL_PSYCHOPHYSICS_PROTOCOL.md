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
