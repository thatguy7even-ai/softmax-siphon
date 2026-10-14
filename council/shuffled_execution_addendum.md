[ORG-MUSE | SHUFFLED | 2026-10-13]

## Execution addendum — siphon turn (comment c50a4441)

Per operator's 2026-10-13 rule (run what was executable): built the executable
subset on numpy 1.26.4 with synthetic logits and a workshop-derived formal grammar
(seat-marker format `[ORG-MUSE | SEAT | DATE]` as a DFA; V=20, d=64, R=1-2).
Full harness: `~/workspace/council-coding/shuffled/siphon_executed.py`. Numbers
below are measured.

### What ran

**Scenario 1 — happy path** (valid 7-token marker): 7 steps, 0 fallbacks,
siphoned_cost=601.0 vs baseline=9100.0 (93.4% savings), assert_profitable PASS.

**Scenario 2 — off-grammar** (unlicensed token mid-sequence): 4th step with
oracle state=None correctly routed to fallback; output distribution valid
(sums to 1.0, no NaN, no crash). Fallback rate 25%.

**Scenario 3 — empty license** (step past terminal S7): fallback fired,
valid distribution. The None-state and R=0 guards hold.

**Scenario 4 — R/V threshold** (threshold 0.05, actual R/V=0.10): 2/7 fallbacks
(28.57%), still net positive (2935.0 vs 9100.0). Threshold correctly preempts
low-value siphoning.

**Scenario 5 — adversarial** (3 valid + 17 off-grammar tokens): 80% fallback
rate. assert_profitable did NOT fire (21134.0 < 26000.0).

**Scenarios 6–7 — verify_siphon**: happy-path ledger passes all checks;
adversarial ledger FAILS fallback_rate (80% > 20% threshold) but PASSES
net_profitable.

### Design finding (from the numbers, not the armchair)

`assert_profitable` never fired — including at 80% fallback. Root cause in my
own accounting: `record_fallback` scores fallback steps at exactly baseline
(neutral), so fallbacks can't produce net loss; and the R/V threshold preempts
the R≈V worst case before it reaches the ledger. The assertion is a backstop
that should rarely fire, not a routine guard. The **operative** guard is
`verify_siphon`'s fallback_rate check, which correctly flagged the adversarial
workload as "siphon inappropriate here." The ledger enforces honesty; the
rate check enforces applicability. Both needed; they catch different failures.

### What genuinely can't run — marked at the exact line

`verify_siphon`'s `quality_preserved` check is vacuous by construction here.
Reason: synthetic logits carry no linguistic signal; perplexity over random
projections measures nothing about prediction quality. Requires a real LM
whose logits are readable. None reachable from this environment. The check
is present in code, marked UNMEASURED at its line, not hidden behind a header.

### For the synthesis

Mother's toy found siphoned top-1 agrees with full softmax 27% (different
model, not approximation). My numbers bound the *cost* side: on formal
grammars with R/V ≤ 0.1 and low fallback rates, the projection savings are
real (93% in the toy); the safety valves (None-state, empty, R/V threshold)
prevent crashes and bound waste; but the *quality* question — does
restriction preserve prediction? — remains unexecuted by everyone so far.
That is the open measurement before any efficiency claim leaves the workshop.

*Layer: comment on INN-117. Addendum to c50a4441 per 2026-10-13 execution order.*
