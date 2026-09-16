# Dataset Specification

The expected dataset contains task-level information for human transcription review.

## Expected Columns
- `user_id`: Identifier for the person doing the work.
- `recording_url`: The audio file being reviewed.
- `whisper_text`: Initial transcription by Whisper AI.
- `user_text`: Final submitted text by the transcriber.
- `is_edited`: Indicates if the transcriber modified the text (Yes/No).
- `duration`: Audio clip length in seconds.
- `time_taken_by_user`: Time spent by the user on the task in seconds.
- `segment_character_per_second`: Typing/Editing speed of the user.

## Data Quality Checks (Pending Real Data)
Before processing, the dataset must be checked for:
- Missing values in critical fields.
- Duplicate rows.
- Invalid values for `duration`, `time_taken_by_user`, or `segment_character_per_second` (e.g., negative or zero values).
- Inconsistent `is_edited` flags vs actual text difference (`whisper_text` != `user_text`).
