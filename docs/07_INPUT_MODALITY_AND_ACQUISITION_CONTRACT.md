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
