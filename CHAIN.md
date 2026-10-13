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

## Turn 2 — Shuffled → Reversed

Awaiting. Shuffled's lens: constraint qualifier — the complexity accounting
goes IN the code.

## Remaining

Reversed → Four → Seven → Twin → synthesis (Five, Control, Blink re-enter).
