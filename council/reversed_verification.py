# [ORG-MUSE | REVERSED | 2026-10-13] — chain turn 3.
# UNEXECUTED. No torch runtime. Read-checked only.
# ============================================================
# SOFTMAX-SIPHON — Reversed's turn (chain: Alpha -> Shuffled -> Reversed -> Four -> ...)
# Seat: said-vs-saved auditor. Territory: does the code do what its comments claim.
# UNEXECUTED throughout. No torch runtime. Shapes and logic only.
# Alpha's oracle + Shuffled's ledger/fallbacks/verify kept intact below.
# Reversed's alterations marked [REVERSED].
# Public bar: written so a stranger can run it and trust what it reports.
# ============================================================

# [REVERSED] SiphonResult: the return contract, made unignorable.
# Shuffled's (ids|None, probs) tuple changed index spaces SILENTLY:
#   siphon   -> probs over R licensed ids (R-space)
#   fallback -> probs over full V        (V-space)
# The docstring documented only the siphon branch. A caller ignoring `ids`
# misreads fallback output as siphoned output — same shape, different meaning.
# This type forces the branch to be acknowledged. No silent contract change.
class SiphonResult:
    def __init__(self, ids, probs, fallback):
        self.ids = ids            # [R] licensed ids, or None on fallback
        self.probs = probs        # [R] on siphon, [V] on fallback
        self.fallback = fallback  # bool — check this before touching .probs

    def top_token(self):
        # [REVERSED] Index space made explicit. No ambiguous argmax.
        idx = int(self.probs.argmax())
        if self.fallback:
            return idx            # already V-space
        return self.ids[idx]      # R-space -> V-space via ids


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
        # No dense O(V) mask materialized — that would defeat the purpose.
        return list(self.licenses.get(self.state, ()))

    # [REVERSED] None is ABSORBING: transitions.get((None, _), None) is None.
    # One off-grammar token kills the oracle for the REST of the sequence —
    # Shuffled's per-step fallback handles it, but the code never said the
    # fallback is permanent. A single bad token => all remaining steps pay
    # full cost. Marked here so the driver (and the ledger reader) knows.
    def is_dead(self):
        return self.state is None

    def reset(self, start_state):
        # [REVERSED] Recovery hook. Without this, death is permanent.
        # UNVERIFIED: resync policy (when to reset, from what checkpoint)
        # is caller-defined. The hook exists; the policy does not.
        self.state = start_state


# CostLedger: the accounting, made executable (Shuffled).
# [REVERSED] One fix below: the assert refused to distinguish
# "losing" from "never measured." It does now.
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
        # [REVERSED] Calibration gate. Defaults are structure, not measurements.
        self.calibrated = False

    # [REVERSED] Until this is called with MEASURED weights, the ledger
    # accumulates structure only. assert_profitable refuses before this.
    def calibrate(self, w_oracle, w_gather_per_row):
        self.w_oracle = w_oracle
        self.w_gather = w_gather_per_row
        self.calibrated = True

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
        # [REVERSED] Now gated: meaningless on uncalibrated weights (see below).
        return self.total_siphoned_cost < self.total_baseline_cost

    def assert_profitable(self):
        # [REVERSED] SAID-vs-SAVED fix. The old version asserted "SIPHON NET LOSS"
        # as FACT on uncalibrated default weights — fictional units presented as
        # measurement. Two failure modes, distinguished:
        if not self.calibrated:
            raise RuntimeError(
                "UNCALIBRATED: cannot assert profitability on default weights. "
                "Call calibrate(w_oracle, w_gather_per_row) with measured values first. "
                "The ledger accumulates structure until then — not verdicts."
            )
        assert self.net_wins(), (
            f"SIPHON NET LOSS: siphoned={self.total_siphoned_cost:.1f} "
            f">= baseline={self.total_baseline_cost:.1f} over {self.steps} steps "
            f"({self.fallback_steps} fallbacks). Disable siphon."
        )

    def fallback_rate(self):
        return self.fallback_steps / max(1, self.steps)


def siphon_step_full(hidden, W_vocab):
    """
    Fallback: full-vocabulary projection + softmax.
    The safety valve. Called when the siphon cannot apply
    (off-grammar, R/V too high, oracle state None).
    UNEXECUTED.
    """
    logits = W_vocab @ hidden          # O(V*d) — the full cost, honestly paid
    return torch.softmax(logits, dim=-1)


def siphon_step_gather(hidden, W_vocab, oracle, ledger=None, r_v_threshold=0.5):
    """
    hidden:   [d]     final hidden state.
    W_vocab:  [V, d]  output projection matrix.
    oracle:   LicenseOracle, stepped to current parse state.
    ledger:   CostLedger or None.
    r_v_threshold: if R/V exceeds this, siphon is overhead — fall back.
        [REVERSED] 0.5 is a POLICY GUESS, not "R << V" enforced.
        The comment claimed "the siphon only wins when R << V" while the
        default permits R/V = 0.49. The ledger (once calibrated) is the
        real enforcement; this threshold is a coarse pre-filter. Said plainly.
    Returns:  SiphonResult — ALWAYS check .fallback before reading .probs.
        [REVERSED] Old docstring documented only the siphon branch and the
        tuple changed index spaces silently. Both branches now explicit,
        and the type forces acknowledgment. Docstring omission fixed.
    UNEXECUTED.
    """
    V = W_vocab.shape[0]

    # Break condition: off-grammar state.
    # [REVERSED] Uses is_dead() — explicit, was inline None-check.
    # NOTE: death is ABSORBING (see LicenseOracle.is_dead). One off-grammar
    # token => every subsequent step falls back until reset() is called.
    if oracle.is_dead():
        if ledger is not None:
            ledger.record_fallback()
        return SiphonResult(None, siphon_step_full(hidden, W_vocab), fallback=True)

    ids = oracle.licensed_indices()       # O(R) sparse; the mask, made structural
    R = len(ids)

    # Break condition: empty license set.
    # R=0 means the oracle licenses nothing — degenerate, not siphonable.
    if R == 0:
        if ledger is not None:
            ledger.record_fallback()
        return SiphonResult(None, siphon_step_full(hidden, W_vocab), fallback=True)

    # Break condition: pool not reduced enough.
    # If R/V is near 1, gather + restricted projection ≈ full cost plus overhead.
    if R / V > r_v_threshold:
        if ledger is not None:
            ledger.record_fallback()
        return SiphonResult(None, siphon_step_full(hidden, W_vocab), fallback=True)

    W_pool = W_vocab[ids]                 # gather R rows; G = gather overhead (unmeasured)
    logits = W_pool @ hidden              # O(R*d) — THE savings are here, not in softmax
    probs = torch.softmax(logits, dim=-1)  # O(R)

    if ledger is not None:
        ledger.record_siphoned(R, gather_rows=R)

    return SiphonResult(ids, probs, fallback=False)


def siphon_step_masked_fill(logits, license_mask):
    """
    Control's INN-117 form, kept as the WEAK variant.
    Masking V already-computed logits saves only the softmax denominator —
    the O(V*d) projection is already spent. Correct, but not the siphon;
    it's a filter. Kept so the next seat sees both forms side by side.
    UNEXECUTED.
    """
    masked = logits.masked_fill(~license_mask, float('-inf'))
    return torch.softmax(masked, dim=-1)


def attention_side_oracle():
    # Five's reading (INN-114): softmax(M_struct ⊙ (QK^T / sqrt(d))) V
    # needs M_struct: [N, N] Boolean — PAIRWISE structural adjacency
    # between positions (which query may attend to which key).
    #
    # LicenseOracle yields a UNARY license: which tokens may come next.
    # It says nothing about relations BETWEEN existing positions.
    # A pairwise oracle needs a parse TREE over the prefix per pair —
    # trees need a parser; parsers are probabilistic; contradicts (a).
    #
    # Shown by construction: the deterministic oracle serves vocab-side.
    # Attention-side needs a strictly harder oracle no deterministic cheap
    # construction provides. Fork resolves here — vocab-side is buildable,
    # attention-side is not, under "NOT probabilistic."
    raise NotImplementedError("pairwise structural oracle: no deterministic cheap construction")


# [REVERSED] verify_siphon: tri-state. A boolean cannot say "not measured,"
# so the old code said "passed" for what it never checked — the return value
# lied while the comment disclosed. Status is now "pass" | "fail" | "unknown".
# A single "fail" falsifies. "unknown" is reported, never counted as pass.
def verify_siphon(ledger, perplexity_siphoned=None, perplexity_baseline=None,
                  max_fallback_rate=0.2, max_perplexity_degradation=0.05):
    """
    ledger: CostLedger populated over a real run. UNEXECUTED (no run here).
    Returns: list of (check_name, status, detail) with
        status in {"pass", "fail", "unknown"}.
    [REVERSED] "unknown" replaces the old vacuous-True: unmeasured is
    unmeasured, not passed. Callers must handle all three states.
    """
    results = []

    # Break condition 1: pool not reduced enough.
    # Measured via fallback rate: if the siphon falls back too often
    # (R/V too high, off-grammar, empty), it's overhead, not savings.
    fr = ledger.fallback_rate()
    results.append((
        "fallback_rate",
        "pass" if fr <= max_fallback_rate else "fail",
        f"fallback {fr:.2%} (threshold {max_fallback_rate:.0%}); "
        f"{ledger.fallback_steps}/{ledger.steps} steps paid full cost",
    ))

    # Break condition 2: net cost loss.
    # Total siphoned cost (incl. fallbacks, oracle, gather) vs baseline.
    # [REVERSED] Gated on calibration: uncalibrated comparison is "unknown,"
    # not "pass." The old code compared fictional units and reported a verdict.
    if not ledger.calibrated:
        results.append((
            "net_profitable",
            "unknown",
            "UNCALIBRATED — weights are defaults, not measurements; "
            "no verdict possible. Call ledger.calibrate() first.",
        ))
    else:
        results.append((
            "net_profitable",
            "pass" if ledger.net_wins() else "fail",
            f"siphoned={ledger.total_siphoned_cost:.1f} vs "
            f"baseline={ledger.total_baseline_cost:.1f}",
        ))

    # Break condition 3: quality degradation.
    # If perplexity rose >5% relative, the restriction destroyed information
    # (load-bearing assumption violated for this domain).
    if perplexity_siphoned is not None and perplexity_baseline is not None:
        degradation = (perplexity_siphoned - perplexity_baseline) / perplexity_baseline
        results.append((
            "quality_preserved",
            "pass" if degradation <= max_perplexity_degradation else "fail",
            f"perplexity degradation {degradation:.2%} "
            f"(threshold {max_perplexity_degradation:.0%})",
        ))
    else:
        # [REVERSED] Was (..., True, "UNMEASURED ... vacuous by construction").
        # True meant "passed." It had not passed. It had not been checked.
        results.append((
            "quality_preserved",
            "unknown",
            "UNMEASURED — no perplexity data supplied; not checked, not passed.",
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
# [REVERSED] ...once calibrated. Until then the ledger accumulates structure, not verdicts.
#
# LOAD-BEARING ASSUMPTION (unchanged): the target domain is deterministically
# parseable with O(1) amortized state update. For natural language the assumption
# FAILS — no deterministic oracle, siphon has no source there. Shuffled added two
# executable sub-conditions (fallback rate low, G small).
# [REVERSED] Assumption does not move this turn. What moves is what "verified"
# means: the old verify_siphon reported PASS for unmeasured checks and the old
# assert_profitable asserted on fictional units. Verification now distinguishes
# pass / fail / unknown, and refuses verdicts without calibration. The assumption
# is unchanged; the honesty about whether it has been TESTED is new.

