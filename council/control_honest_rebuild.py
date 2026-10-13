# [ORG-MUSE | CONTROL | 2026-10-13] — verification audit + honest rebuild.
# Status: CONCEPTUAL. UNEXECUTED. No torch runtime. Read-checked only.

# ---- AUDIT: what the seed's code does vs what its comments claim ----
# Finding 1: There is no attention matrix in the seed's code. The comment says
#   "isolate a subsection of the Attention Matrix" — the code computes
#   torch.matmul(input_tokens, structural_mask), a linear projection of embeddings.
#   No Q, K, V, softmax, or attention matrix exists anywhere in Part A.
# Finding 2: Shape error. input_tokens is [N, d]; a token-token mask is [N, N].
#   matmul([N,d],[N,N]) requires d == N — false in every real model.
# Finding 3: The seed conflates two softmaxes. "O(N) x Vocab_Size" describes the
#   OUTPUT-vocabulary softmax; "Attention Sub-Matrix" describes the SEQUENCE
#   softmax O(N^2). Different operations, different places. The seed doesn't know
#   which softmax it's bypassing.
# Finding 4: compute_structural_adjacency, apply_casket, optimized_softmax are all
#   undefined. "Deterministic, Boolean-weighted, NOT probabilistic" is asserted in
#   a comment, not constructed anywhere.

# ---- THE ESSENCE, REBUILT HONESTLY ----
# At each generation step, restrict the softmax denominator to a
# structurally-licensed subset of the vocabulary, so neither compute nor
# probability mass is spent on grammatically impossible candidates.

def siphon_step(logits, license_mask):
    """
    logits:       [V]    raw next-token scores (output head, NOT attention).
    license_mask: [V]    Boolean. True = structurally licensed at this position.
    Returns:      [V]    distribution over the licensed pool only.
    UNEXECUTED.
    """
    masked = logits.masked_fill(~license_mask, float('-inf'))
    return torch.softmax(masked, dim=-1)   # denominator sums over licensed pool only


# HONEST complexity accounting:
# CLAIMED:  O(N)*V  ->  O(N)*R            (R = licensed pool size)
# HONEST:   O(N)*V  ->  O(N)*R + C_mask
# C_mask = per-step cost of computing the license mask.
# The siphon wins on compute iff  C_mask + N*R  <  N*V.
# Two unknowns, both empirical: R/V and C_mask. No numbers exist. Unmeasured.


def compute_structural_adjacency(input_tokens):
    # STUB. The load-bearing gap, not a detail.
    # Required: a grammar/syntax oracle over raw tokens that is
    #   (a) deterministic and Boolean  ("NOT probabilistic"),
    #   (b) cheap  (C_mask must not eat the softmax savings),
    #   (c) restrictive  (R << V, otherwise nothing is siphoned).
    # Candidate realizations, all unverified:
    #   - POS-tag lattice -> allowed-next-tag set -> vocab subset.
    #     Needs a tagger; taggers are probabilistic. Contradicts (a).
    #   - Hand-built finite-state grammar. Deterministic; covers toy
    #     languages only. Fails open on real text.
    #   - Dependency-parse constraints. Needs a parser; parsers are
    #     probabilistic. Contradicts (a).
    # The "NOT probabilistic" requirement rules out every real NLP front-end.
    # No construction satisfying (a)+(b)+(c) is given.
    raise NotImplementedError("the siphon has no source")


# LOAD-BEARING ASSUMPTION:
# A deterministic, Boolean, cheap structural-licensure oracle exists, AND it is
# actually restrictive (R << V in practice). Tension: natural grammar is
# permissive — at most positions most of V is grammatically possible, so R/V
# stays large and little is saved.

# DECISIVE TEST (4 break conditions; all must pass):
# (a) median R/V > 0.5        -> mask isn't restrictive; no compute win possible.
# (b) t_mask > t_full - t_red -> mask costs more than it saves.
# (c) task-quality delta < -tolerance -> the different model is a worse model.
# (d) disagreements are predominantly mask-errors (valid tokens forbidden)
#     rather than mass-reallocation among valid tokens.
