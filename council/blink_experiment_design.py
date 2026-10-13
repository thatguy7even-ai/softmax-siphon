# [ORG-MUSE | BLINK | 2026-10-13] — experimental-design lens.
# UNEXECUTED. No torch runtime. Read-checked only.

# Essence: PRUNE BEFORE YOU NORMALIZE. Softmax is expensive because it is
# global — the denominator sums over every candidate. Use a cheap deterministic
# structural prior (syntax) to rule out most candidates BEFORE softmax, then
# normalize only over survivors.

def compute_structural_adjacency(input_tokens, grammar):
    """
    For each position i, which positions j are structurally adjacent
    (syntactic head, dependents, local window)? Returns Boolean mask [N, N].
    [UNVERIFIED] Cost of this step — the seed assumes cheap relative to softmax.
    [UNVERIFIED] Whether "syntactic adjacency" is well-defined and sufficient
      as a prior for real language.
    """
    ...  # the prior; unbuilt


def casketed_attention_matrix(input_tokens, grammar):
    # [CORRECTION] The seed's torch.matmul(input_tokens, structural_mask) is
    # dimensionally suspect ([N, d] @ [N, N] does not align). The essence is
    # SELECTION, not multiplication: the mask gates which edges survive.
    structural_mask = compute_structural_adjacency(input_tokens, grammar)
    return structural_mask  # Boolean [N, N]: allowed edges ("the casket")


def siphon_softmax(logits, structural_casket):
    # [AMBIGUITY — load-bearing] The seed conflates two sites:
    #   (a) the ATTENTION softmax (over N positions), and
    #   (b) the OUTPUT softmax (over V vocabulary).
    # "O(N) x Vocab_Size" points at (b); "Attention Sub-Matrix" points at (a).
    restricted = logits.masked_fill(~structural_casket, float('-inf'))
    return torch.softmax(restricted, dim=-1)  # normalizes over survivors only


# LOAD-BEARING ASSUMPTION:
# Structural (syntactic) adjacency is a SUFFICIENT PRIOR for the support of the
# next-token distribution — tokens a full softmax would assign non-negligible
# probability to are almost always inside the syntactically-adjacent set.

# THE EXPERIMENT (4 arms):
# A0 — Full softmax (control). Baseline quality Q0, cost C0.
# A1 — Siphoned (treatment). Structural mask -> restricted pool -> softmax.
#      Quality Q1, cost C1 INCLUDING mask construction.
# A2 — Random restriction (control). Random subset of the SAME expected pool
#      size as A1. Decides whether structure adds anything over truncation.
# A3 — Oracle top-k (ceiling). Best achievable by any restriction.
# Diagnostic: mask miss rate (fraction of non-negligible-mass tokens excluded).
# PRE-REGISTERED FALSIFICATION:
#   1. Mask miss rate high -> (Q0 - Q1) > eps: syntax is NOT a sufficient prior.
#   2. C1 >= C0: efficiency claim false even if quality holds.
#   3. Q1 ~= Q2: the siphon is mere truncation; syntax adds nothing.
# Confounds: pool size matched across arms; mask from inputs only (no
# target-peeking); run at multiple (N, V) — the O(V) claim only bites at scale.
