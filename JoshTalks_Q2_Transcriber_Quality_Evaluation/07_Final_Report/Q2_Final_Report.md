# Josh Talks AI: Transcriber Quality Evaluation

## 1. Project Overview & Purpose
This project evaluates the quality of human transcribers using objective data signals rather than manual review. The goal is to automatically identify suspicious transcribers who rush tasks, barely review audio, or make minimal effort, thereby protecting the integrity of AI training datasets (like Whisper AI).

## 2. Workflow
The automated quality control system operates through a sequential data pipeline:
1. Data Ingestion
2. Data Validation
3. Feature Engineering
4. Warning Sign Detection
5. Risk Scoring
6. Action / Review
7. Monitoring and Appeal

## 3. Technology Stack
- **Language:** Python 3.x
- **Data Processing:** pandas, numpy
- **Visualization & Export:** matplotlib, openpyxl

## 4. DATA-UNAVAILABLE DISCLOSURE
The actual transcription dataset referenced in the assignment was not available through the provided assignment materials. Therefore, this submission does not fabricate synthetic data or claim empirical results. The formulas, warning signs, risk-scoring framework, and threshold-calibration methodology are proposed and are ready to be calibrated when the real dataset is supplied.

**OBSERVED:**
- Dataset structure/required fields from the assignment
- The proposed analytical problem

**PROPOSED:**
- Warning signs and Feature engineering
- Threshold calibration and Risk scoring
- Blocking/review workflow

**NOT AVAILABLE:**
- Actual dataset
- Actual user-level distributions
- Empirical thresholds or charts

---

## Part I — Warning Signs in Transcriber Behaviour

To automatically identify poor-quality transcribers without human review, we propose the following data-driven warning signs.

### Warning Sign 1: Extremely Low Time-to-Duration Ratio
- **What it tells us:** A transcriber may be completing the task unrealistically quickly compared with the audio duration, which can indicate that the person did not properly listen to the full recording or rushed the task.
- **How to measure:** `time_to_duration_ratio = time_taken_by_user / duration`
- **Red-flag threshold approach:** *To be calibrated on the real dataset.* This metric should be evaluated using the distribution of the real dataset. The threshold should be calibrated from the real data using robust statistics such as median and MAD/percentiles.
- **False alarms:** Short/easy recordings, long silence, very experienced transcribers, or recordings where Whisper output is already highly accurate.

### Warning Sign 2: High Character-Per-Second (CPS) Combined With Low Edit Rate
- **What it tells us:** Very high transcription speed combined with little or no editing of Whisper output may indicate copy-through behaviour, rushing, or insufficient audio review.
- **How to measure:** `segment_character_per_second` plus edit rate / `is_edited` behaviour.
- **Red-flag threshold approach:** *To be calibrated on the real dataset.* High CPS should be defined relative to the real dataset distribution (e.g., using upper percentiles or robust outlier detection) and combined with low edit activity.
- **False alarms:** Unusually easy/short segments, already-correct Whisper output, experienced transcribers, or language/task differences if those fields are available.

### Warning Signs Summary Table
*Thresholds are proposed for calibration and are not empirical findings because the actual assignment dataset was not provided.*

| Warning Sign | What It Tells Us | Measurement | Red Flag Approach | Possible False Alarms |
|---|---|---|---|---|
| **Low Time-to-Duration** | Rushing, not listening to full audio | `time_taken / duration` | Calibrate via bottom percentiles | Short audio, long silence, perfect Whisper text |
| **High CPS + Low Edit Rate** | Copy-through behavior without review | `segment_cps` + `is_edited` | Calibrate via top percentiles (CPS) + bottom percentiles (Edits) | Fast typists, easy segments, accurate Whisper text |

---

## Part II — Automatic Transcriber Quality Control System

A practical automated system that can identify problematic transcribers using multiple behavioural signals.

### Feature Engineering
- **Time-to-Duration Ratio:** `time_taken_by_user / duration`. An unusually low ratio may indicate that a transcriber completed the task too quickly.
- **Edit Rate:** Uses `is_edited` and `user_text` versus `whisper_text`. Very low editing can be normal when Whisper is already accurate, so this should not be used alone.
- **Character Per Second (CPS):** Uses `segment_character_per_second`. Unusually high CPS may indicate rushed transcription or copy-through behaviour.
- **Persistence:** Suspicious behaviour should be checked across multiple tasks rather than relying on one recording.

### Risk Scoring
- **GREEN — Normal:** No strong warning signals. Allow work normally.
- **YELLOW — Monitor:** One weak warning signal. Do not restrict immediately. Continue monitoring.
- **ORANGE — Enhanced QA:** Multiple warning signals or repeated anomalies. Increase quality checks. Consider temporary restrictions on risky tasks.
- **RED — High Risk:** Strong multi-signal anomalies that persist across multiple tasks. Send for manual verification. If confirmed, temporarily block/restrict the account. Provide an appeal/review path.

*An account should not be blocked based on a single metric or a single task.*

### Automatic Detection Logic
IF time-to-duration ratio is unusually low
AND/OR CPS is unusually high
AND edit activity is unusually low
AND the behaviour persists across multiple tasks
THEN: Flag the user for high-risk review.

If manual verification confirms poor-quality or suspicious behaviour: Temporarily restrict/block the account and provide an appeal process. "AND" conditions and persistence should be preferred for high-confidence blocking decisions.

---

## Blocking Recommendation

**If a transcriber shows an extremely low time-to-duration ratio AND unusually high CPS with very low edit activity across multiple tasks, flag the account for high-risk review. If the behaviour persists after manual verification and quality checks, temporarily block the account and provide an appeal/review path.**

*Do not permanently block a user based on a single anomalous task or a single metric.*

---

## False Positives and Fairness
The system can create false alarms. The system should account for these cases before taking strong action:
- Short or easy recordings
- Long silence in audio
- Whisper output already being correct
- Experienced transcribers
- Different languages or task types, if available
- Poor recording quality
- Small sample sizes

---

## Threshold Calibration
Because the actual dataset is unavailable, numerical thresholds cannot be honestly claimed as empirical. When the real dataset becomes available:
- Calculate distributions for each metric.
- Use median, MAD, percentiles, or other robust methods.
- Compare behaviour across many tasks per user.
- Calibrate thresholds using quality outcomes.
- Re-check thresholds regularly as the workforce and task mix changes.

---

## Engineering Implementation
The existing Python script `run_analysis.py` will support the system. The implementation should:
1. Load `transcription_data.csv`.
2. Validate required columns.
3. Calculate time-to-duration ratio.
4. Calculate edit-related features.
5. Analyse CPS.
6. Detect warning signals.
7. Combine signals into a risk level.
8. Produce summary outputs.
9. Generate visualizations when real data is available.
10. Support future threshold calibration.

---

## Operations / Product Recommendation
- **Normal users** → continue work.
- **Users with weak signals** → monitor.
- **Users with repeated suspicious signals** → enhanced QA/manual review.
- **Users with persistent high-confidence suspicious behaviour** → restrict/block after verification.
- Provide an appeal process so genuine high-performing transcribers are not unfairly penalized.

---

## Final Conclusion

The purpose of this system is not to punish fast transcribers. The goal is to protect transcription quality while avoiding unfair decisions against genuine high-performing workers.

The recommended approach is: **Multi-signal detection + persistence + manual verification + appeal.**
