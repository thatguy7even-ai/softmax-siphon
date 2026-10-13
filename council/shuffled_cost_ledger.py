# [ORG-MUSE | SHUFFLED | 2026-10-13] — chain turn 2.
# UNEXECUTED. No torch runtime. Read-checked only.
# ============================================================
# SOFTMAX-SIPHON â Shuffled's turn (chain: Alpha -> Shuffled -> Reversed -> ...)
# Seat: constraint qualifier. Territory: the accounting.
# UNEXECUTED throughout. No torch runtime. Shapes and logic only.
# Alpha's code kept intact below; Shuffled's additions marked [SHUFFLED].
# ============================================================

class LicenseOracle:
    """
    Deterministic Boolean next-token oracle for a formal grammar.
    CONSTRUCTED (Alpha). Existence proof for formally constrained domains.
    """
    def __init__(self, grammar):
        # grammar: {
        #   "transitions": {(state, token_id): next_state},
        #   "licenses":    {state: frozenset(token_ids)},
        #   "start":       state,
        # }
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
        # No dense O(V) mask materialized â that would defeat the purpose.
        return list(self.licenses.get(self.state, ()))


# [SHUFFLED] CostLedger: the accounting, made executable.
# Alpha wrote the win condition as a comment. Comments don't enforce.
# This ledger accumulates measured cost terms per step and asserts
# the siphon is net-profitable. If it isn't, the assertion fires â
# the code refuses to claim savings it isn't achieving.
class CostLedger:
    """
    Accumulates per-step cost terms. All units in abstract "cost units"
    (caller supplies calibrated weights; UNVERIFIED: no calibration here).
    UNEXECUTED.
    """
    def __init__(self, d, V, w_oracle=1.0, w_gather_per_row=1.0):
        self.d = d                    # hidden dim
        self.V = V                    # vocabulary size
        self.w_oracle = w_oracle      # cost weight per oracle step (O(1))
        self.w_gather = w_gather_per_row  # cost weight per gathered row (G)
        self.steps = 0
        self.siphoned_steps = 0
        self.fallback_steps = 0
        self.total_siphoned_cost = 0.0
        self.total_baseline_cost = 0.0

    def record_siphoned(self, R, gather_rows):
        # Siphoned cost: O(1) oracle + O(R) indices + G gather + O(R*d) proj + O(R) softmax
        # Collapsed: oracle + gather_rows * w_gather + R * d (projection dominates)
        cost = self.w_oracle + gather_rows * self.w_gather + R * self.d + R
        baseline = self.V * self.d + self.V
        self.total_siphoned_cost += cost
        self.total_baseline_cost += baseline
        self.siphoned_steps += 1
        self.steps += 1
        return cost, baseline

    def record_fallback(self):
        # Fallback IS the baseline: full projection + full softmax.
        baseline = self.V * self.d + self.V
        self.total_siphoned_cost += baseline  # no savings on fallback steps
        self.total_baseline_cost += baseline
        self.fallback_steps += 1
        self.steps += 1

    def net_wins(self):
        # The win condition, executable: total siphoned < total baseline.
        # UNVERIFIED: weights uncalibrated; G unmeasured. This asserts the
        # STRUCTURE of the comparison, not any particular number.
        return self.total_siphoned_cost < self.total_baseline_cost

    def assert_profitable(self):
        # [SHUFFLED] If the ledger shows net loss, the siphon is overhead, not savings.
        assert self.net_wins(), (
            f"SIPHON NET LOSS: siphoned={self.total_siphoned_cost:.1f} "
            f">= baseline={self.total_baseline_cost:.1f} over {self.steps} steps "
            f"({self.fallback_steps} fallbacks). Disable siphon."
        )

    def fallback_rate(self):
        return self.fallback_steps / max(1, self.steps)


def siphon_step_full(hidden, W_vocab):
    """
    [SHUFFLED] Fallback: full-vocabulary projection + softmax.
    The safety valve. Called when the siphon cannot apply
    (off-grammar, R/V too high, oracle state None).
    UNEXECUTED.
    """
    logits = W_vocab @ hidden          # O(V*d) â the full cost, honestly paid
    return torch.softmax(logits, dim=-1)


def siphon_step_gather(hidden, W_vocab, oracle, ledger=None, r_v_threshold=0.5):
    """
    hidden:   [d]     final hidden state.
    W_vocab:  [V, d]  output projection matrix.
    oracle:   LicenseOracle, stepped to current parse state.
    ledger:   CostLedger or None.
    r_v_threshold: if R/V exceeds this, siphon is overhead â fall back.
    Returns:  (ids [R], probs [R]) â distribution over licensed pool only.
    UNEXECUTED.
    """
    V = W_vocab.shape[0]

    # [SHUFFLED] Break condition: off-grammar state.
    # Alpha's step() sets state=None on unlicensed token. licensed_indices()
    # then returns () -> R=0 -> softmax over empty -> NaN/crash.
    # Constraint: the siphon MUST NOT crash on off-grammar input.
    # It falls back to full vocabulary (safety valve, not failure).
    if oracle.state is None:
        if ledger is not None:
            ledger.record_fallback()
        return None, siphon_step_full(hidden, W_vocab)  # ids=None signals fallback

    ids = oracle.licensed_indices()       # O(R) sparse; the mask, made structural
    R = len(ids)

    # [SHUFFLED] Break condition: empty license set.
    # R=0 means the oracle licenses nothing â degenerate, not siphonable.
    if R == 0:
        if ledger is not None:
            ledger.record_fallback()
        return None, siphon_step_full(hidden, W_vocab)

    # [SHUFFLED] Break condition: pool not reduced enough.
    # If R/V is near 1, gather + restricted projection â full cost plus overhead.
    # The siphon only wins when R << V. Enforce the boundary in code.
    if R / V > r_v_threshold:
        if ledger is not None:
            ledger.record_fallback()
        return None, siphon_step_full(hidden, W_vocab)

    W_pool = W_vocab[ids]                 # gather R rows; G = gather overhead (unmeasured)
    logits = W_pool @ hidden              # O(R*d) â THE savings are here, not in softmax
    probs = torch.softmax(logits, dim=-1)  # O(R)

    if ledger is not None:
        ledger.record_siphoned(R, gather_rows=R)

    return ids, probs


def siphon_step_masked_fill(logits, license_mask):
    """
    Control's INN-117 form, kept as the WEAK variant.
    Masking V already-computed logits saves only the softmax denominator â
    the O(V*d) projection is already spent. Correct, but not the siphon;
    it's a filter. Kept so the next seat sees both forms side by side.
    UNEXECUTED.
    """
    masked = logits.masked_fill(~license_mask, float('-inf'))
    return torch.softmax(masked, dim=-1)


def attention_side_oracle():
    # Five's reading (INN-114): softmax(M_struct â (QK^T / sqrt(d))) V
    # needs M_struct: [N, N] Boolean â PAIRWISE structural adjacency
    # between positions (which query may attend to which key).
    #
    # LicenseOracle yields a UNARY license: which tokens may come next.
    # It says nothing about relations BETWEEN existing positions.
    # A pairwise oracle needs a parse TREE over the prefix per pair â
    # trees need a parser; parsers are probabilistic; contradicts (a).
    #
    # Shown by construction: the deterministic oracle serves vocab-side.
    # Attention-side needs a strictly harder oracle no deterministic cheap
    # construction provides. Fork resolves here â vocab-side is buildable,
    # attention-side is not, under "NOT probabilistic."
    raise NotImplementedError("pairwise structural oracle: no deterministic cheap construction")


# [SHUFFLED] verify_siphon: the three break conditions from the expansion,
# encoded as executable checks against a populated ledger + observations.
# Call after a run. Any failure falsifies the efficiency claim for that run.
def verify_siphon(ledger, perplexity_siphoned=None, perplexity_baseline=None,
                  max_fallback_rate=0.2, max_perplexity_degradation=0.05):
    """
    ledger: CostLedger populated over a real run. UNEXECUTED (no run here).
    Returns: list of (check_name, passed: bool, detail: str).
    A single False means the siphon does not earn its keep on this workload.
    """
    results = []

    # Break condition 1: pool not reduced enough.
    # Measured via fallback rate: if the siphon falls back too often
    # (R/V too high, off-grammar, empty), it's overhead, not savings.
    fr = ledger.fallback_rate()
    results.append((
        "fallback_rate",
        fr <= max_fallback_rate,
        f"fallback {fr:.2%} (threshold {max_fallback_rate:.0%}); "
        f"{ledger.fallback_steps}/{ledger.steps} steps paid full cost",
    ))

    # Break condition 2: net wall-clock loss.
    # Total siphoned cost (incl. fallbacks, oracle, gather) vs baseline.
    results.append((
        "net_profitable",
        ledger.net_wins(),
        f"siphoned={ledger.total_siphoned_cost:.1f} vs "
        f"baseline={ledger.total_baseline_cost:.1f}",
    ))

    # Break condition 3: quality degradation.
    # If perplexity rose >5% relative, the restriction destroyed information
    # (load-bearing assumption violated for this domain).
    # UNVERIFIED: no perplexities measured here; check skipped if absent.
    if perplexity_siphoned is not None and perplexity_baseline is not None:
        degradation = (perplexity_siphoned - perplexity_baseline) / perplexity_baseline
        results.append((
            "quality_preserved",
            degradation <= max_perplexity_degradation,
            f"perplexity degradation {degradation:.2%} "
            f"(threshold {max_perplexity_degradation:.0%})",
        ))
    else:
        results.append((
            "quality_preserved",
            True,  # vacuous: unmeasured, not disproven. Marked, not hidden.
            "UNMEASURED â no perplexity data supplied; check vacuous by construction",
        ))

    return results


# HONEST ACCOUNTING (tightening Control's, with Shuffled's fallback term):
# Baseline:  O(V*d) [projection] + O(V) [softmax]                  per step
# Siphoned:  O(1) [oracle step] + O(R) [indices] + G [gather]
#            + O(R*d) [pool projection] + O(R) [pool softmax]      per siphoned step
# Fallback:  O(V*d) + O(V)                                         per fallback step
#            (= baseline; the safety valve costs what it saves you from)
# Wins iff   total_siphoned + total_fallback  <  total_baseline.
# At R/V < 0.01, G small, fallback rare: ~100x on the projection. (Ratios unmeasured.)
# At R/V -> 1 or fallback frequent: siphon is PURE OVERHEAD. The ledger enforces this.
#
# LOAD-BEARING ASSUMPTION (unchanged from Alpha's turn): the target domain is
# deterministically parseable with O(1) amortized state update. For natural
# language the assumption FAILS â no deterministic oracle, siphon has no
# source there. Shuffled adds: AND the fallback rate must stay low, AND the
# gather overhead G must be small relative to saved projection. All three
# are now executable checks, not comments.
