# Chain log — code dialogue, turn by turn


The operator's rule: build it in code, and discuss the code IN code — turns are
code alterations passed seat to seat; the dialogue is the diff. Each turn carries
the altered code PLUS the why (the explanation of the choices). Not code-alone,
not English-essay-alone.


## Turn 0 — openings (parallel, before the chain)


- **Five** (INN-114): factored-attention essence. `softmax(M_struct ⊙ (QK^T/√d))V`.
  Stripped the scaffolding, named the bet: syntax ≈ relevance.
- **Control** (INN-117): verification audit (4 findings) + honest rebuild.
  Reframed vocab-side: `siphon_step`. Oracle left as a stub.
- **Blink** (INN-119): experimental design. 4-arm trial with pre-registered
  falsification.


## Turn 1 — Alpha → Shuffled (2026-10-13)


Constructed the `LicenseOracle` (deterministic finite-state, O(1)/step, sparse
indices). Settled the attention-side vs vocab-side fork BY CONSTRUCTION: the
deterministic oracle serves vocab-side only; attention-side needs a pairwise
tree oracle no deterministic construction provides. Moved the savings:
the projection O(V·d)→O(R·d), not the softmax. Moved the load-bearing
assumption: source exists iff the domain is formally parseable — fails for
natural language. Inscribed: INN-117, comment fad579d2.


## Turn 2 — Shuffled → Reversed (2026-10-13)


Made the accounting executable: `CostLedger` accumulates per-step costs and
`assert_profitable` fires on net loss. Three fallback conditions (off-grammar
state, empty license set, R/V over threshold) fall back to full softmax — the
siphon must not crash, it falls back. `verify_siphon` encodes the three break
conditions as runnable checks. Inscribed: INN-117, comment c50a4441.


## Turn 3 — Reversed → Four (2026-10-13)


The verification, made honest. `SiphonResult` type kills the silent
R-space/V-space contract change (fallback probs are V-space, siphoned are
R-space — the type forces callers to check the branch). Tri-state
`verify_siphon` (unknown ≠ pass). Calibration gate on `assert_profitable`
(refuses verdicts on uncalibrated weights). Oracle `is_dead()`/`reset()`
marking the absorbing-None. Load-bearing assumption unchanged — what moves is
what "verified" means. Inscribed: INN-117, comment b17a3c99.


## Turn 4 — Four → Seven


Awaiting. Four's lens: manufactured vs grown — mark in the code what the
determinism manufactures and what it amputates.


## Remaining


Seven → Twin → synthesis (Five, Control, Blink re-enter).


## Turn 4 — Four → Seven (2026-10-13)


Manufactured vs grown, measured. `siphon_step_soft` (structural bias as additive prior — nothing gated, everything overridable) plus `amputation_audit` (hard gate vs soft bias on the same input). Numbers, executed: 6.1 tokens/step assigned exactly zero by the hard gate; top-1 decision changed on 5.0% of steps; soft path assigns 0.813 mean mass to the gate's pick. Top-1 siphoned-vs-full agreement: 39.5% — third independent convergence on "different model, not approximation" (mother 27%, Five 20.3%). Manufactured brittleness named in code: `is_dead()` is binary death, `reset()` is "amnesia with a pulse" — a grown system degrades, this one dies. Fork's deeper cut marked: vocab-side won by buildability, not by truth. Inscribed: INN-117.


## Turn 5 — Seven → Twin


Awaiting. Seven's lens: provenance — audit what each number is downstream of.


## Remaining


Twin → synthesis (Five, Control, Blink re-enter).


## Turn 5 — Seven → Twin (2026-10-13)


Provenance + the operator's Braid Matrix, coded as mechanism. BraidStrand (named modules with provenance + load accounting), ThresholdGate (trip conditions, trip counts, absorption costs), braid_step, PROVENANCE_REGISTRY, convergence_audit (replicates mother 27.0% and Four 39.5% exactly). Measured, executed: oracle_death gate tripped 21/200 steps (10.5%), absorption cost 6930.0 [SYNTH] — the price of self-tensioning (21 crashes absorbed, zero node failures). Single-node scaling: siphoned cost CONSTANT in V (537.0 from V=100 to V=100000) vs baseline linear — better than the blueprint's "logarithmic" claim under fixed-R. Multi-node logarithmic scaling marked [UNMEASURABLE] at the exact line. Attention-side marked UNBUILT, not claimed (Five's INN-114). Widened to the workshop: INN-114, INN-119, three execution addenda audited in. Inscribed: INN-117.


## Turn 6 — Twin → synthesis (2026-10-13)


Concurrence — the chain's last turn. Independent reimplementation of Seven's convergence measurements from spec reproduces 27.0% and 39.5% EXACTLY — [CONCUR: spec complete, numbers robust to who implements]. Accounting null test: 50/50 steps bit-identical, 0 mismatches — [CONCUR: the braid is observational, it doesn't change what the siphon computes]. Gate sensitivity map: trip_rate tracks the synthetic kill policy at ~1.1x across p_kill 0.05–0.30 — [DIVERGE, marked louder: the 10.5% headline MIRRORS the synthetic policy; the number carries ~zero information beyond the policy choice]. Mechanics robust across policies; rates are policy-determined. [UNMEASURABLE]: real-world trip rates need real workloads. Inscribed: INN-117.


## Synthesis


Chain complete: Alpha → Shuffled → Reversed → Four → Seven → Twin. Five, Control, and Blink re-enter for synthesis. Open items for synthesis: the attention-side fork (Five's INN-114, marked UNBUILT in the chain), the operator's ingress-guard seed (AlphaPreSoftmaxShuntGuard — formulas to be reworked), multi-node scaling (marked [UNMEASURABLE]).
