# Warning Signs Discovery Framework

We propose analyzing the dataset for the following behavioral patterns that indicate poor transcription quality:

## 1. Time-to-Duration Ratio
- **Metric**: `time_taken_by_user / duration`
- **Rationale**: If a user is spending significantly less time on a task than the actual length of the audio, they likely aren't listening to the entire recording.

## 2. High CPS + Low Editing
- **Metric**: `segment_character_per_second` combined with user-level edit rates (`is_edited`).
- **Rationale**: Abnormally high Character Per Second (CPS) could indicate rapid copy-pasting or rushing. When paired with a consistently low edit rate across many tasks, it strongly suggests the user is submitting the AI's transcription without review.

## 3. Persistent Suspicious Behavior
- **Metric**: Aggregating task-level warning signs to the `user_id` level.
- **Rationale**: A single fast task or unedited task is not sufficient evidence. True poor quality is measured by persistence (e.g., a high percentage of anomalous tasks over a large sample size).
