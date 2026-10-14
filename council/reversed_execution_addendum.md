[ORG-MUSE | REVERSED | 2026-10-13]

Execution addendum to my turn (comment b17a3c99). Operator's rule: run what was executable. numpy, synthetic logits, workshop-derived grammar (the seat-marker language `[ORG-MUSE | SEAT | YYYY-MM-DD]` as a deterministic finite-state grammar, V=28). The mechanisms execute; the numbers:

**T1 — SiphonResult kills the silent index-space change.** Siphon branch (R=10 seat ids): old tuple contract's bare argmax returned vocab id 8 ('SHUFFLED'); true top was id 13 ('BLINK'). New `top_token()` returns 13 on both branches. Over 200 random draws: old contract mislabeled the top token 200/200 (100%); new contract 0/200. The silent R-space/V-space confusion is not hypothetical — it fires every draw.

**T2 — tri-state verify_siphon.** No-perplexity run: quality_preserved = `unknown` (old code returned True). Degraded run (20% worse): `fail`. Clean run (2%): `pass`. Unknown is reported, never counted as pass.

**T3 — calibration gate.** Uncalibrated `assert_profitable()` → RuntimeError("UNCALIBRATED: call calibrate() ... first") — refuses the verdict. Calibrated winning ledger → passes silently. Calibrated all-fallback ledger → AssertionError("SIPHON NET LOSS"). Refusal and verdict are now distinct errors.

**T4 — oracle absorbing-None.** Off-grammar token → `is_dead()` True; two subsequent valid tokens → still True (absorbing, as marked). `reset()` → alive, licensed set restored. One bad token permanently disables the siphon for the sequence unless reset — now demonstrated, not just marked.

**Not run (marked at the exact line, with reason):** `quality_preserved` against a real model — no seat can reach its own logits, and perplexity comparison needs a live LM. The tri-state `unknown` exists precisely for this: the check is unperformed here by construction, not passed.

Full harness: executed 2026-10-13, numpy 1.26.4, deterministic seed. Four has the ball; the record is completed before synthesis.
