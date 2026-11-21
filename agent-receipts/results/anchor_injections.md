# Anchor tamper cases: results

Expected verdicts frozen before the anchoring code. Unreviewed departures: **0**.

Attacks caught: anchored **10/11**, v0 without an anchor 0/11. Attacks needing the signing key: anchored **3/4**, v0 0/4.

Run against a local stand-in for Rekor, because the public log is unreachable from the machine that built this.

| case | needs key | anchored | v0, no anchor |
| --- | --- | --- | --- |
| clean | no | pass  | pass  |
| holder_rewrite | yes | **FAIL** anchor_bad_signature, anchor_mismatch | pass  |
| holder_rewrite_edits_bundle | yes | **FAIL** anchor_inclusion_invalid, anchor_set_invalid | pass  |
| holder_rewrite_reanchor_later | yes | **FAIL** anchor_late | pass  |
| holder_rewrite_shift_and_reanchor | yes | pass  | pass  |
| forged_log | no | **FAIL** anchor_untrusted_log | pass  |
| inclusion_hash_flipped | no | **FAIL** anchor_inclusion_invalid | pass  |
| checkpoint_sig_flipped | no | **FAIL** anchor_checkpoint_invalid | pass  |
| set_flipped | no | **FAIL** anchor_set_invalid | pass  |
| anchor_of_other_session | no | **FAIL** anchor_bad_signature, anchor_mismatch | pass  |
| anchor_by_other_key | no | **FAIL** anchor_key_mismatch | pass  |
| missing_but_required | no | **FAIL** anchor_missing | pass  |

`holder_rewrite_shift_and_reanchor` passing is the expected blind spot: a key holder who rewrites, moves every timestamp and anchors the rewrite. Only an online search of the log for the key's other entries finds it.
