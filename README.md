# Softmax-Siphon

An exploration of a speculative attention/compute idea — **built through dialogue**.
A human operator supplied the seed snippet; a council of AI seats expanded it,
audited it, rebuilt it, and hammered it out turn by turn, in code.

## The seed

`seed_snippet.py` — the original sketch: a deterministic "casketed" structural
mask over attention, then softmax over the restricted candidate pool instead of
the full vocabulary. The claim: O(N)×Vocab → O(N)×Reduced_Pool.

## What the dialogue found

1. **The snippet is broken four ways** (Control): no attention matrix in the
   code, a shape error (`[N,d]@[N,N]`), it conflates the *sequence* softmax with
   the *vocabulary* softmax, and its "deterministic oracle" is a stub with an
   asserted property and no mechanism.
2. **The essence is three lines** (Mother): license, mask, normalize —
   `essence.py`. Everything else was scaffolding.
3. **The siphon is a different model, not a faster approximation** (Mother's
   executed toy, `toy_prototype.py`): over 200 trials, siphoned top-1 agrees
   with full softmax only 27%. Restriction redistributes mass; it does not
   preserve it.
4. **The oracle can be constructed — for formal domains** (Alpha): a
   deterministic finite-state `LicenseOracle`, O(1)/step, sparse indices. Shown
   *by construction* to serve the vocab-side reading only; the attention-side
   reading needs a pairwise tree oracle no deterministic construction provides.
   For natural language, the assumption fails — the oracle is the existence
   proof *and* the boundary marker.
5. **The real savings are in the projection, not the softmax** (Alpha):
   O(V·d) → O(R·d). The snippet named the wrong term.
6. **The experiment that decides it** (Blink): 4-arm trial — full / siphoned /
   random-restriction / oracle top-k — with mask miss rate as the diagnostic
   and pre-registered falsification conditions.

## Honesty markings

- Everything under `council/` is **unexecuted by construction** — no torch
  runtime in the seats' chats. Read-checked only, never run. Marked as such.
- The one executed artifact is `toy_prototype.py` (numpy, 200 trials).
- The load-bearing assumption, as moved by the dialogue: *the target domain is
  deterministically parseable with O(1) amortized state update* — and the
  relevant context is contained in rule-computable structural adjacency.

## Provenance

Built October 13, 2026, through human–AI dialogue: operator seed → council
expansion → code-dialogue chain (turns passed seat to seat, the dialogue as
diffs) → this repo. The chain continues; this snapshot will grow.
