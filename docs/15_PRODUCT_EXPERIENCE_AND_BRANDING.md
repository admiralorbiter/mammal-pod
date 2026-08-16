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
