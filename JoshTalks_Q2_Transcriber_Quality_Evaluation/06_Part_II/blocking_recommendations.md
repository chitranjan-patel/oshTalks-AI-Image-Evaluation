# Part II: Automated Quality Control System

## Blocking Logic and Recommendations

To maintain transcriber trust and avoid punishing legitimate workers, the quality control system uses a staged, multi-signal risk model based on persistent behavior. 

### Staged Risk Model

| Signal | Risk Level | Proposed Action |
|--------|------------|-----------------|
| Normal metrics | **GREEN** | Allow work. No action needed. |
| Single weak signal (e.g., low time/duration *only*, high CPS *only*, or low edit rate *only*) | **YELLOW** | Continue work. Monitor user behavior. |
| Multiple warning signals (e.g., low time/duration *AND* high CPS) | **ORANGE** | Temporarily restrict task access. Trigger enhanced manual QA sampling. |
| Multiple independent signals persisting across a large task history | **RED** | Recommend manual verification before permanent block/revocation. |

### Engineering-Ready Recommendation
"If a transcriber repeatedly exhibits extremely low time-to-duration ratios AND abnormally high CPS with low edit rates across a sufficiently large task sample (Illustrative starting point only (N > 30); this is NOT derived from the provided dataset and must be recalibrated using real production data), classify them as high risk (RED) and trigger a manual review. Permanent blocking should occur only after the behavior remains persistent over a rolling window and the statistical evidence passes a high-confidence threshold."

*(Note: Exact numerical thresholds for X/Y/N must be calibrated after observing real dataset distributions.)*

### False-Positive Protection
- **Minimum Sample Size:** Users cannot be blocked based on 1 or 2 tasks. Statistical significance requires a minimum volume.
- **Multi-Signal Requirement:** A single metric (like high typing speed or a no-edit task) will never trigger a block.
- **Contextual Awareness:** Short audio, prolonged silence, and high Whisper baseline accuracy legitimately lower edit rates and ratios.
- **Human Safeguard & Appeals:** RED candidates undergo manual verification of a random subset of their tasks before permanent bans are applied, and an appeal mechanism is maintained.
