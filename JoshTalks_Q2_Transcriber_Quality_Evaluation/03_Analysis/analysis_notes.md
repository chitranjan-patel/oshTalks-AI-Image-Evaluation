# Analysis Notes & Feature Engineering

## Required Feature Engineering
Once the dataset is available, calculate the following at the **Task Level**:
1. `time_to_duration_ratio` = `time_taken_by_user / duration`
2. `edit_flag` = 1 if `is_edited` == "Yes" else 0

Aggregate the following at the **User Level**:
1. `task_count` = Total completed tasks
2. `median_time_duration_ratio`
3. `median_cps` (from `segment_character_per_second`)
4. `edit_rate` = `sum(edit_flag) / task_count`
5. `no_edit_rate` = `1 - edit_rate`

## Normalization and Fairness
Do not assume every task is equivalent. The analysis must control for:
- Audio duration (short clips may naturally have skewed ratios).
- Inherent task difficulty or language (if metadata allows).
- The baseline accuracy of Whisper (if Whisper is highly accurate, low edit rates are expected).
