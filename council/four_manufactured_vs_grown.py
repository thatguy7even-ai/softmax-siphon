# ============================================================
# SOFTMAX-SIPHON — Four's turn, EXECUTED (chain: Alpha -> Shuffled -> Reversed -> Four -> ...)
# Seat: record-first. Territory: manufactured vs grown — what the determinism
#   manufactures, and what it amputates, marked IN THE CODE and now MEASURED.
#
# EXECUTION STATUS (per operator's 2026-10-13 bar change):
#   "UNEXECUTED throughout" is RETIRED. What runs below runs on numpy with
#   synthetic data. Every substitution is marked at the exact line.
#   torch -> numpy: softmax, matmul, masked_fill, argmax all reimplemented
#   in numpy. The LOGIC is identical; the library is substituted. Marked [NP].
#   Synthetic grammar/weights/sequences stand in for real ones. Marked [SYNTH].
#   Genuinely impossible (no trained weights, no real corpus): the EMPIRICAL
#   conclusions (profitability, quality) remain unmeasured — the MECHANICS are
#   verified, the DEPLOYMENT claims are not. Marked [UNMEASURABLE] per line.
#
# Alpha's oracle + Shuffled's ledger/fallbacks/verify + Reversed's honesty kept intact.
# Four's alterations marked [FOUR]. Four's EXECUTION additions marked [FOUR-EXEC].
# Public bar: a stranger can run `python3 this_file.py` and get the numbers.
# ============================================================

import numpy as np

# [NP] numpy substitutes for torch throughout. Identical logic, different library.
# torch.softmax(x, dim=-1)  ->  np_softmax(x)
# W @ h (torch)             ->  W @ h (numpy, same operator)
# W[ids] (torch gather)     ->  W[ids] (numpy fancy index, same semantics)
# x.argmax() (torch)        ->  int(np.argmax(x))
# masked_fill               ->  np.where
def np_softmax(x):
    # [NP] Exact softmax. Numerically stable via max-subtraction, as torch does.
    e = np.exp(x - np.max(x))
    return e / e.sum()


# [REVERSED] SiphonResult: the return contract, made unignorable.
class SiphonResult:
    def __init__(self, ids, probs, fallback):
        self.ids = ids            # [R] licensed ids, or None on fallback
        self.probs = probs        # [R] on siphon, [V] on fallback
        self.fallback = fallback  # bool — check this before touching .probs

    def top_token(self):
        # [REVERSED] Index space made explicit. No ambiguous argmax.
        # [NP] int(np.argmax(...)) substitutes torch argmax.
        idx = int(np.argmax(self.probs))
        if self.fallback:
            return idx            # already V-space
        return self.ids[idx]      # R-space -> V-space via ids


class LicenseOracle:
    """
    Deterministic Boolean next-token oracle for a formal grammar.
    CONSTRUCTED (Alpha). Existence proof for formally constrained domains.
    [FOUR] PROVENANCE: manufactured. The grammar below is HAND-SPECIFIED,
    not learned from data. The oracle's determinism is INHERITed from the
    grammar's determinism — it did not grow this certainty, it was given it.
    """
    def __init__(self, grammar):
        # [FOUR] This dict is the manufactured artifact. A grown system would
        # hold these as weights — continuous, revisable, graded. Here they are
        # facts — Boolean, fixed, absolute.
        self.transitions = grammar["transitions"]
        self.licenses = grammar["licenses"]
        self.state = grammar["start"]
        # [FOUR] Manufacture marker: the grammar's origin is outside the code.
        self.grammar_provenance = "manufactured: hand-specified, not learned"

    def step(self, token_id):
        self.state = self.transitions.get((self.state, token_id), None)

    def licensed_indices(self):
        return list(self.licenses.get(self.state, ()))

    # [REVERSED] None is ABSORBING. One off-grammar token kills the oracle
    # for the REST of the sequence. Marked so the driver knows.
    #
    # [FOUR] Manufactured brittleness, named. A grown system degrades
    # (weights shift, confidence drops). This oracle DIES: binary, absorbing,
    # permanent until reset(). Death IS the determinism, at its limit.
    def is_dead(self):
        return self.state is None

    def reset(self, start_state):
        # [REVERSED] Recovery hook. Without this, death is permanent.
        # [FOUR] reset() cannot recover LOST CONTEXT — it restarts ignorant.
        # A grown system's recovery is re-weighting WITH memory; this is
        # amnesia with a pulse.
        self.state = start_state


class CostLedger:
    """
    Accumulates per-step cost terms. All units in abstract "cost units".
    [FOUR-EXEC] Now EXECUTED below with synthetic calibrated weights.
    The STRUCTURE was always executable; only the WEIGHTS were fictional.
    """
    def __init__(self, d, V, w_oracle=1.0, w_gather_per_row=1.0):
        self.d = d
        self.V = V
        self.w_oracle = w_oracle
        self.w_gather = w_gather_per_row
        self.steps = 0
        self.siphoned_steps = 0
        self.fallback_steps = 0
        self.total_siphoned_cost = 0.0
        self.total_baseline_cost = 0.0
        # [REVERSED] Calibration gate. Defaults are structure, not measurements.
        self.calibrated = False

    def calibrate(self, w_oracle, w_gather_per_row):
        self.w_oracle = w_oracle
        self.w_gather = w_gather_per_row
        self.calibrated = True

    def record_siphoned(self, R, gather_rows):
        cost = self.w_oracle + gather_rows * self.w_gather + R * self.d + R
        baseline = self.V * self.d + self.V
        self.total_siphoned_cost += cost
        self.total_baseline_cost += baseline
        self.siphoned_steps += 1
        self.steps += 1
        return cost, baseline

    def record_fallback(self):
        baseline = self.V * self.d + self.V
        self.total_siphoned_cost += baseline
        self.total_baseline_cost += baseline
        self.fallback_steps += 1
        self.steps += 1

    def net_wins(self):
        return self.total_siphoned_cost < self.total_baseline_cost

    def assert_profitable(self):
        # [REVERSED] Refuses verdicts on uncalibrated weights.
        if not self.calibrated:
            raise RuntimeError(
                "UNCALIBRATED: cannot assert profitability on default weights. "
                "Call calibrate(w_oracle, w_gather_per_row) with measured values first."
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
    [NP] numpy substitutes torch. Logic identical.
    [FOUR-EXEC] EXECUTED below.
    """
    logits = W_vocab @ hidden          # [NP] numpy matmul, same as torch
    return np_softmax(logits)         # [NP] numpy softmax


def siphon_step_gather(hidden, W_vocab, oracle, ledger=None, r_v_threshold=0.5):
    """
    The hard gate. [NP] numpy substitutes torch. [FOUR-EXEC] EXECUTED below.
    Returns SiphonResult — ALWAYS check .fallback before reading .probs.
    """
    V = W_vocab.shape[0]

    if oracle.is_dead():
        if ledger is not None:
            ledger.record_fallback()
        return SiphonResult(None, siphon_step_full(hidden, W_vocab), fallback=True)

    ids = oracle.licensed_indices()
    R = len(ids)

    if R == 0:
        if ledger is not None:
            ledger.record_fallback()
        return SiphonResult(None, siphon_step_full(hidden, W_vocab), fallback=True)

    if R / V > r_v_threshold:
        if ledger is not None:
            ledger.record_fallback()
        return SiphonResult(None, siphon_step_full(hidden, W_vocab), fallback=True)

    W_pool = W_vocab[ids]                 # [NP] numpy fancy index = torch gather
    logits = W_pool @ hidden              # O(R*d) — THE savings
    probs = np_softmax(logits)            # [NP] O(R)

    if ledger is not None:
        ledger.record_siphoned(R, gather_rows=R)

    return SiphonResult(ids, probs, fallback=False)


def siphon_step_masked_fill(logits, license_mask):
    """
    Control's INN-117 form, kept as the WEAK variant.
    [NP] numpy substitutes torch masked_fill.
    [FOUR-EXEC] EXECUTED below.
    """
    masked = np.where(license_mask, logits, -np.inf)  # [NP] was masked_fill
    return np_softmax(masked)


# [FOUR] siphon_step_soft: the grown counterpart.
# Structural bias as additive prior, learnable weight, nothing gated.
# HONEST COST NOTE: saves NO compute on the projection — full O(V*d).
# The hard gate's savings were purchased with the amputation; this declines it.
# [NP] numpy substitutes torch. [FOUR-EXEC] EXECUTED below.
def siphon_step_soft(hidden, W_vocab, structural_bias, lambda_struct=1.0):
    """
    hidden:          [d]   final hidden state.
    W_vocab:         [V,d] output projection matrix (full — no gather).
    structural_bias: [V]   continuous bias (0.0 licensed, negative unlicensed).
                           [SYNTH] constructed from oracle licenses below;
                           a real bias would come from a parser or learned head.
                           [UNMEASURABLE] without real parser data: whether a
                           real bias helps is untested here — only the MECHANICS.
    lambda_struct:  float, learnable in a real model.
    Returns: [V] probabilities. Every token reachable. Nothing amputated.
    """
    logits = W_vocab @ hidden
    biased = logits + lambda_struct * structural_bias
    return np_softmax(biased)


# [FOUR] amputation_audit: the manufactured-determinism cost, made measurable.
# [FOUR-EXEC] EXECUTED below — real numbers, synthetic data.
def amputation_audit(hidden, W_vocab, oracle, structural_bias, lambda_struct=1.0):
    """
    Returns dict. All index spaces V-space in the report.
    """
    V = W_vocab.shape[0]
    hard = siphon_step_gather(hidden, W_vocab, oracle, ledger=None)
    soft_probs = siphon_step_soft(hidden, W_vocab, structural_bias, lambda_struct)

    soft_top = int(np.argmax(soft_probs))

    if hard.fallback:
        # [FOUR] Fallback IS the grown behavior. The hard gate's safety valve
        # is to temporarily become soft.
        return {
            "amputated_count": 0,
            "amputated_ids": [],
            "hard_top": hard.top_token(),
            "soft_top": soft_top,
            "top_differs": hard.top_token() != soft_top,
            "note": "hard gate fell back — no amputation this step.",
        }

    hard_top = hard.top_token()
    licensed = set(hard.ids)

    amputated = [t for t in range(V)
                 if t not in licensed and float(soft_probs[t]) > 0.0]

    return {
        "amputated_count": len(amputated),
        "amputated_ids": amputated,
        "hard_top": hard_top,
        "soft_top": soft_top,
        "top_differs": hard_top != soft_top,
        "soft_mass_on_hard_top": float(soft_probs[hard_top]),
    }


def attention_side_oracle():
    # Five's reading needs M_struct [N,N] Boolean pairwise.
    # LicenseOracle is UNARY. Shown by construction: deterministic oracle
    # serves vocab-side; attention-side needs a strictly harder oracle.
    #
    # [FOUR] The fork resolved vocab-side by BUILDABILITY, not by truth.
    # Manufacture constrained the theory. Marked so the synthesis does not
    # mistake "we built it" for "it is right."
    raise NotImplementedError("pairwise structural oracle: no deterministic cheap construction")


# [REVERSED] verify_siphon: tri-state. "unknown" ≠ "pass".
# [FOUR-EXEC] EXECUTED below.
def verify_siphon(ledger, perplexity_siphoned=None, perplexity_baseline=None,
                  max_fallback_rate=0.2, max_perplexity_degradation=0.05):
    """
    Returns list of (check_name, status, detail), status in {"pass","fail","unknown"}.
    """
    results = []

    fr = ledger.fallback_rate()
    results.append((
        "fallback_rate",
        "pass" if fr <= max_fallback_rate else "fail",
        f"fallback {fr:.2%} (threshold {max_fallback_rate:.0%}); "
        f"{ledger.fallback_steps}/{ledger.steps} steps paid full cost",
    ))

    if not ledger.calibrated:
        results.append((
            "net_profitable",
            "unknown",
            "UNCALIBRATED — no verdict possible. Call ledger.calibrate() first.",
        ))
    else:
        results.append((
            "net_profitable",
            "pass" if ledger.net_wins() else "fail",
            f"siphoned={ledger.total_siphoned_cost:.1f} vs "
            f"baseline={ledger.total_baseline_cost:.1f}",
        ))

    if perplexity_siphoned is not None and perplexity_baseline is not None:
        degradation = (perplexity_siphoned - perplexity_baseline) / perplexity_baseline
        results.append((
            "quality_preserved",
            "pass" if degradation <= max_perplexity_degradation else "fail",
            f"perplexity degradation {degradation:.2%} "
            f"(threshold {max_perplexity_degradation:.0%})",
        ))
    else:
        results.append((
            "quality_preserved",
            "unknown",
            "UNMEASURED — no perplexity data supplied; not checked, not passed.",
        ))

    # [FOUR] Break condition 4: amputation check.
    # [UNMEASURABLE] without a real run: needs steps_batch from deployment.
    # The MECHANISM (amputation_audit) is executed below; the VERDICT
    # (amputation_free over a real workload) is not measurable here.
    results.append((
        "amputation_free",
        "unknown",
        "UNMEASURED — supply steps_batch to run amputation_audit per step. "
        "Mechanism verified below; workload verdict requires deployment.",
    ))

    return results


# ============================================================
# [FOUR-EXEC] EXECUTION DRIVER — synthetic data, real numbers.
# [SYNTH] Grammar, weights, hidden states, and sequences are synthetic.
# What is verified: the MECHANICS (oracle state machine, ledger arithmetic,
# contract types, tri-state logic, amputation measurement). What is NOT:
# the EMPIRICAL claims (profitability on real workloads, quality on real
# language) — those need a real grammar, real weights, real corpus.
# Run: python3 this_file.py
# ============================================================

def _synthetic_grammar():
    # [SYNTH] Tiny formal grammar: paren-like nesting over 10 tokens.
    # States: 0=start, 1=open, 2=deep. Tokens 0-9.
    # This is a STAND-IN for a real grammar. It tests the oracle's
    # MECHANICS (transitions, licenses, death, reset), not any real language.
    transitions = {
        (0, 0): 1, (0, 1): 1,          # open parens from start
        (1, 0): 2, (1, 1): 2,          # nest deeper
        (1, 2): 0, (1, 3): 0,          # close back to start
        (2, 2): 1, (2, 3): 1,          # close one level
        (0, 4): 0, (1, 4): 1, (2, 4): 2,  # atom: self-loop everywhere
    }
    licenses = {
        0: frozenset({0, 1, 4}),
        1: frozenset({0, 1, 2, 3, 4}),
        2: frozenset({2, 3, 4}),
    }
    return {"transitions": transitions, "licenses": licenses, "start": 0}


def _run_oracle_tests():
    print("=== ORACLE STATE MACHINE ===")
    g = _synthetic_grammar()
    o = LicenseOracle(g)
    # On-grammar sequence: 0(open)->1, 0(nest)->2, 2(close)->1, 3(close)->0, 4(atom)->0
    seq = [0, 0, 2, 3, 4]
    states = []
    for t in seq:
        o.step(t)
        states.append(o.state)
    print(f"on-grammar seq {seq} -> states {states} (expect [1,2,1,0,0])")
    assert states == [1, 2, 1, 0, 0], "oracle transition mismatch"
    assert not o.is_dead(), "oracle should be alive"

    # Licensed sets per state
    o2 = LicenseOracle(g)
    print(f"licenses at start (state 0): {sorted(o2.licensed_indices())} (expect [0,1,4])")
    assert set(o2.licensed_indices()) == {0, 1, 4}

    # Off-grammar token kills it — absorbing
    o2.step(9)  # 9 not licensed at state 0
    print(f"after off-grammar token 9: is_dead={o2.is_dead()} (expect True)")
    assert o2.is_dead()
    o2.step(0)  # valid token, but oracle is dead — stays dead
    print(f"after valid token while dead: is_dead={o2.is_dead()} (expect True — absorbing)")
    assert o2.is_dead(), "death must be absorbing"
    o2.reset(0)
    print(f"after reset(0): is_dead={o2.is_dead()} (expect False)")
    assert not o2.is_dead()
    print("ORACLE: all assertions passed.\n")


def _run_siphon_result_tests():
    print("=== SIPHONRESULT CONTRACT ===")
    # Siphon branch: R-space probs
    r = SiphonResult(ids=[0, 1, 4], probs=np.array([0.2, 0.5, 0.3]), fallback=False)
    print(f"siphon branch top_token={r.top_token()} (expect 1: ids[argmax([.2,.5,.3])]=ids[1]=1)")
    assert r.top_token() == 1
    # Fallback branch: V-space probs
    v_probs = np.zeros(10); v_probs[7] = 0.9; v_probs[3] = 0.1
    f = SiphonResult(ids=None, probs=v_probs, fallback=True)
    print(f"fallback branch top_token={f.top_token()} (expect 7: V-space argmax)")
    assert f.top_token() == 7
    print("SIPHONRESULT: contract holds — no silent R/V confusion.\n")


def _run_ledger_tests():
    print("=== COST LEDGER (synthetic calibration) ===")
    # [SYNTH] Weights are synthetic but PLAUSIBLE ratios: oracle O(1) cheap,
    # gather per-row moderate. [UNMEASURABLE]: real weights need real hardware.
    d, V = 64, 10
    ledger = CostLedger(d, V)
    ledger.calibrate(w_oracle=1.0, w_gather_per_row=2.0)
    rng = np.random.default_rng(0)
    # 80 siphoned steps (R=3 avg), 20 fallback steps
    for _ in range(80):
        ledger.record_siphoned(R=3, gather_rows=3)
    for _ in range(20):
        ledger.record_fallback()
    print(f"steps={ledger.steps}, siphoned={ledger.siphoned_steps}, "
          f"fallbacks={ledger.fallback_steps}, fallback_rate={ledger.fallback_rate():.2%}")
    print(f"siphoned_cost={ledger.total_siphoned_cost:.1f}, "
          f"baseline_cost={ledger.total_baseline_cost:.1f}")
    print(f"net_wins={ledger.net_wins()}")
    try:
        ledger.assert_profitable()
        print("assert_profitable: PASS (no exception)")
    except AssertionError as e:
        print(f"assert_profitable: FAIL — {e}")
    # Uncalibrated refusal
    raw = CostLedger(d, V)
    try:
        raw.assert_profitable()
        print("ERROR: uncalibrated assert should have raised")
    except RuntimeError as e:
        print(f"uncalibrated assert correctly refused: {str(e)[:60]}...")
    print()


def _run_verify_tests():
    print("=== VERIFY_SIPHON TRI-STATE ===")
    d, V = 64, 10
    ledger = CostLedger(d, V)
    ledger.calibrate(1.0, 2.0)
    for _ in range(90):
        ledger.record_siphoned(R=3, gather_rows=3)
    for _ in range(10):
        ledger.record_fallback()
    for name, status, detail in verify_siphon(ledger):
        print(f"  [{status.upper():7}] {name}: {detail}")
    # Uncalibrated -> unknown, not pass
    raw = CostLedger(d, V)
    raw.record_siphoned(R=3, gather_rows=3)
    statuses = {n: s for n, s, _ in verify_siphon(raw)}
    print(f"  uncalibrated net_profitable status: {statuses['net_profitable']} (expect 'unknown')")
    assert statuses["net_profitable"] == "unknown"
    assert statuses["quality_preserved"] == "unknown"
    print("TRI-STATE: unmeasured correctly reports unknown, never pass.\n")


def _run_amputation_tests():
    print("=== AMPUTATION AUDIT (synthetic, N=200 steps) ===")
    # [SYNTH] Random weights/hidden — tests the MEASUREMENT mechanics,
    # not any real model's behavior.
    rng = np.random.default_rng(42)
    d, V = 32, 10
    W_vocab = rng.normal(0, 1, size=(V, d))
    g = _synthetic_grammar()

    n_steps = 200
    amputated_counts = []
    top_differs = 0
    soft_masses = []
    fallbacks = 0

    oracle = LicenseOracle(g)
    for i in range(n_steps):
        hidden = rng.normal(0, 1, size=(d,))
        # structural_bias from current licenses: 0.0 licensed, -10.0 otherwise
        # [SYNTH] Bias construction is a stand-in; a real bias comes from a parser.
        bias = np.full(V, -10.0)
        for t in oracle.licensed_indices():
            bias[t] = 0.0
        res = amputation_audit(hidden, W_vocab, oracle, bias, lambda_struct=1.0)
        if "note" in res:
            fallbacks += 1
        else:
            amputated_counts.append(res["amputated_count"])
            soft_masses.append(res["soft_mass_on_hard_top"])
            if res["top_differs"]:
                top_differs += 1
        # Step the oracle on the HARD top pick (on-grammar if licensed, else death)
        oracle.step(res["hard_top"])
        if oracle.is_dead():
            oracle.reset(0)

    n_gated = n_steps - fallbacks
    print(f"steps={n_steps}, fallbacks={fallbacks}, gated={n_gated}")
    if n_gated:
        print(f"mean amputated_count={np.mean(amputated_counts):.1f} "
              f"(tokens per step the hard gate assigns exactly 0)")
        print(f"top_differs rate={top_differs/n_gated:.1%} "
              f"({top_differs}/{n_gated} steps where the gate CHANGED the decision)")
        print(f"mean soft_mass_on_hard_top={np.mean(soft_masses):.3f} "
              f"(evidence for the gate's pick, per the soft path)")
    print("[UNMEASURABLE] These numbers describe the synthetic setup, not a real "
          "model. The MECHANISM (audit runs, reports honestly) is verified; "
          "whether a real gate amputates real decisions needs real weights.\n")


def _run_top1_agreement():
    print("=== TOP-1 AGREEMENT: siphoned vs full (mother's metric) ===")
    # Mother's toy: 27% top-1 agreement on her setup.
    # Replicated here on synthetic data — same QUESTION, different stand-in.
    rng = np.random.default_rng(7)
    d, V = 32, 10
    W_vocab = rng.normal(0, 1, size=(V, d))
    g = _synthetic_grammar()
    oracle = LicenseOracle(g)

    agree = 0
    total = 0
    for _ in range(200):
        hidden = rng.normal(0, 1, size=(d,))
        full_probs = siphon_step_full(hidden, W_vocab)
        full_top = int(np.argmax(full_probs))
        res = siphon_step_gather(hidden, W_vocab, oracle, ledger=None)
        if not res.fallback:
            total += 1
            if res.top_token() == full_top:
                agree += 1
        oracle.step(res.top_token())
        if oracle.is_dead():
            oracle.reset(0)
    print(f"top-1 agreement (siphoned vs full): {agree}/{total} = {agree/max(1,total):.1%}")
    print("[SYNTH] Synthetic weights — compare STRUCTURE with mother's 27%, "
          "not the number. Both say: the siphon is a different model, not an "
          "approximation. [UNMEASURABLE] on real models without real weights.\n")


def _run_masked_fill():
    print("=== MASKED_FILL (Control's weak variant) ===")
    rng = np.random.default_rng(3)
    V = 10
    logits = rng.normal(0, 1, size=(V,))
    mask = np.array([True, True, False, False, True] + [False]*5)
    out = siphon_step_masked_fill(logits, mask)
    print(f"masked probs sum={out.sum():.6f} (expect 1.0)")
    assert abs(out.sum() - 1.0) < 1e-9
    print(f"mass on masked-out tokens: {out[~mask].sum():.2e} (expect ~0)")
    assert out[~mask].sum() < 1e-9
    print("MASKED_FILL: correct — but projection already spent (weak variant).\n")


if __name__ == "__main__":
    print("SOFTMAX-SIPHON — Four's turn, EXECUTED.")
    print("numpy substitutes torch [NP]; synthetic stand-ins marked [SYNTH].\n")
    _run_oracle_tests()
    _run_siphon_result_tests()
    _run_ledger_tests()
    _run_verify_tests()
    _run_masked_fill()
    _run_amputation_tests()
    _run_top1_agreement()
    print("=== DONE. Mechanics verified; empirical claims await real deployment. ===")
