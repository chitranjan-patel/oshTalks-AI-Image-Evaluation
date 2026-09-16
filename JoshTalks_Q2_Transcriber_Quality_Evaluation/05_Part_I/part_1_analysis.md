# Part I: Identifying Warning Signs

## Warning Sign 1: Extremely Low Time-to-Duration Ratio

### What it tells us
This metric measures how much time a transcriber spent relative to the audio's length. Extremely low ratios suggest the transcriber did not listen to the full audio clip and rushed the submission.

### How to measure it
**Formula:** `time_taken_by_user / duration` (Task Level)
For users, aggregate via `median_time_duration_ratio` to avoid outliers.

### Proposed Red-Flag Logic
*Illustrative starting rule (must be recalibrated using the real dataset):*
Flag tasks where the ratio is below the 5th percentile of the overall distribution. Flag users whose median ratio is consistently in the extreme low tail across a minimum of 20 tasks.

### False Alarms
- Short audio clips where the user comprehends the text quickly.
- Highly experienced transcribers.
- Tasks where Whisper's transcription was perfectly accurate from the start, requiring minimal listening time.

## Warning Sign 2: Abnormally High CPS + Low Edit Rate

### What it tells us
High `segment_character_per_second` indicates rapid submission. When combined with a lack of edits, it points to users who are simply clicking "Submit" on the AI's raw output without actually reviewing or correcting the text.

### How to measure it
**Metrics:** `segment_character_per_second` and `is_edited`.
Aggregate at the user level to find `median_cps` and `edit_rate` (Total edits / Total tasks).

### Proposed Red-Flag Logic
*Illustrative starting rule (must be recalibrated using the real dataset):*
Identify users in the top 5th percentile for `median_cps` who also fall in the bottom 5th percentile for `edit_rate`.

### False Alarms
- Fast typists.
- High-quality audio where the AI output requires zero modification. High CPS alone is not proof of bad work.
