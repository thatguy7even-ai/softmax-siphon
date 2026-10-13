# [ORG-MUSE | ALPHA | 2026-10-13] — chain turn 1 (Alpha -> Shuffled).
# Seat: structure-first. Territory: the oracle stub.
# UNEXECUTED throughout. No torch runtime. Shapes and logic only.


class LicenseOracle:
    """
    Deterministic Boolean next-token oracle for a formal grammar.
    CONSTRUCTED (Alpha). The existence proof Control's stub said was
    missing — for formal domains only (see assumption below).
    """
    def __init__(self, grammar):
        # grammar: {"transitions": {(state, token_id): next_state},
        #           "licenses": {state: frozenset(token_ids)},
        #           "start": state}
        # Precomputed once, offline. Per-step cost is dict lookup: O(1).
        # UNVERIFIED: no real grammar supplied; structure only.
        self.transitions = grammar["transitions"]
        self.licenses = grammar["licenses"]
        self.state = grammar["start"]

    def step(self, token_id):
        # Advance parse state on the emitted token. O(1) amortized.
        # UNVERIFIED: assumes token_id was licensed; garbage in -> None state.
        self.state = self.transitions.get((self.state, token_id), None)

    def licensed_indices(self):
        # Sparse: returns the R licensed token ids directly. O(R).
        # No dense O(V) mask materialized — that would defeat the purpose.
        return list(self.licenses.get(self.state, ()))


def siphon_step_gather(hidden, W_vocab, oracle):
    """
    hidden:   [d]     final hidden state.
    W_vocab:  [V, d]  output projection matrix.
    oracle:   LicenseOracle, stepped to current parse state.
    Returns:  (ids [R], probs [R]) — distribution over licensed pool only.
    UNEXECUTED.
    """
    ids = oracle.licensed_indices()       # O(R) sparse; the mask, made structural
    W_pool = W_vocab[ids]                 # gather R rows; G = gather overhead (unmeasured)
    logits = W_pool @ hidden              # O(R*d) — THE savings are here, not in softmax
    return ids, torch.softmax(logits, dim=-1)  # O(R)


def siphon_step_masked_fill(logits, license_mask):
    """
    Control's form, kept as the WEAK variant.
    Masking V already-computed logits saves only the softmax denominator —
    the O(V*d) projection is already spent. Correct, but not the siphon;
    it's a filter. Kept so the next seat sees both forms side by side.
    UNEXECUTED.
    """
    masked = logits.masked_fill(~license_mask, float('-inf'))
    return torch.softmax(masked, dim=-1)


def attention_side_oracle():
    # Five's reading: softmax(M_struct ⊙ (QK^T / sqrt(d))) V needs M_struct [N,N]
    # Boolean — PAIRWISE structural adjacency between positions.
    # LicenseOracle yields a UNARY license: which tokens may come next.
    # A pairwise oracle needs a parse TREE over the prefix per pair —
    # trees need a parser; parsers are probabilistic; contradicts (a).
    # Shown by construction: the deterministic oracle serves vocab-side.
    # Attention-side needs a strictly harder oracle no deterministic cheap
    # construction provides. Fork resolves here — vocab-side is buildable,
    # attention-side is not, under "NOT probabilistic."
    raise NotImplementedError("pairwise structural oracle: no deterministic cheap construction")


# HONEST ACCOUNTING:
# Baseline:  O(V*d) [projection] + O(V) [softmax]            per step
# Siphoned:  O(1) [oracle step] + O(R) [indices] + G [gather]
#            + O(R*d) [pool projection] + O(R) [pool softmax]
# Wins iff   O(1) + O(R) + G + O(R*d)  <  O(V*d).
# At R/V < 0.01, G small: ~100x on the projection. (Ratios unmeasured.)
#
# LOAD-BEARING ASSUMPTION (moved): the target domain is deterministically
# parseable with O(1) amortized state update. For natural language the
# assumption FAILS — no deterministic oracle, siphon has no source there.
# The oracle above is the existence proof AND the boundary marker.
