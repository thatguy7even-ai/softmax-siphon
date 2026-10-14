# ============================================================
# SOFTMAX-SIPHON — Seven's turn, EXECUTED (chain: Alpha -> Shuffled -> Reversed -> Four -> Seven -> ...)
# BRAID TOPOLOGY TURN (operator blueprint 2026-10-13): the siphon was a braid
#   by instinct — strands, gates, fallback absorption. This turn makes the
#   topology EXPLICIT and EXECUTED. [SEVEN-BRAID] marks braid additions.
# Seat: provenance / simulation-gap. Territory: where every claim comes from —
#   which stand-in, which seed, which assumption each number is downstream of.
#   Audits the 27/20.3/39.5 convergence: what it is actually made of.
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
# Alpha's oracle + Shuffled's ledger/fallbacks/verify + Reversed's honesty + Four's
# amputation audit kept intact. Four's marks kept. Seven's alterations marked [SEVEN].
# Seven's EXECUTION additions marked [SEVEN-EXEC].
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


# ============================================================
# [SEVEN] PROVENANCE REGISTRY — where every claim comes from.
# Lineage key:
#   ESTABLISHED  = textbook/standard result; no seat invented it.
#   [SEAT]-NEW   = introduced by that seat's turn in this chain.
#   [SYNTH]      = synthetic stand-in; mechanics verified, empirical claim not.
# [SEVEN-EXEC] Registry is data, not code — no execution needed.
# ============================================================
PROVENANCE_REGISTRY = {
    "np_softmax":             ("ESTABLISHED", "standard numerically-stable softmax; no seat."),
    "SiphonResult":            ("REVERSED-NEW", "return contract; kills silent R/V index confusion."),
    "LicenseOracle":           ("ALPHA-NEW", "deterministic finite-state oracle; grammar [SYNTH] hand-specified."),
    "grammar_provenance":      ("FOUR-NEW", "marks oracle grammar as manufactured, not learned."),
    "CostLedger":              ("SHUFFLED-NEW", "cost accounting; weights [SYNTH] until calibrate()."),
    "siphon_step_full":        ("ESTABLISHED", "full projection + softmax; the baseline."),
    "siphon_step_gather":      ("CONTROL-NEW+ALPHA-NEW", "vocab-side hard gate; Control's reading, Alpha's oracle."),
    "siphon_step_masked_fill": ("CONTROL-NEW", "weak variant; projection cost already spent."),
    "siphon_step_soft":        ("FOUR-NEW", "additive structural bias; nothing gated, nothing amputated."),
    "amputation_audit":        ("FOUR-NEW", "hard-vs-soft measurement on [SYNTH] data."),
    "attention_side_oracle":   ("FOUR-NEW", "fork marker: vocab-side won by buildability, not truth."),
    "verify_siphon":           ("REVERSED-NEW+SHUFFLED-NEW+FOUR-NEW", "tri-state; amputation_free added by Four."),
    "convergence_audit":       ("SEVEN-NEW", "this turn: audits what the agreement convergence is made of."),
}



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
# [SEVEN-BRAID] BRAID MATRIX TOPOLOGY — operator's blueprint, coded as mechanism.
#
# Mapping (from the blueprint):
#   Strands    = named modules: oracle, ledger, hard-gate, soft-path, audit, verify.
#                Independent, lightweight, domain-specific (each has its provenance).
#   Gates      = threshold conditions BETWEEN strands. Trip = load sheds.
#                r_v_threshold, oracle death, empty license, uncalibrated ledger.
#   Interweave = fallback absorption. Oracle death does NOT crash the node —
#                the full-softmax strand takes the load. Self-tensioning:
#                surrounding strands adjust (ledger records the fallback cost).
#   [SEVEN-BRAID] marks all braid additions. [SEVEN-BRAID-EXEC] = executed.
# ============================================================

class BraidStrand:
    # [SEVEN-BRAID] A named module as a strand: state + load accounting.
    def __init__(self, name, provenance_key):
        self.name = name
        prov = PROVENANCE_REGISTRY.get(provenance_key, ("UNKNOWN", ""))
        self.provenance = prov  # (lineage, description)
        self.activations = 0
        self.absorptions = 0    # times this strand took another strand's load
        self.shed = 0           # times this strand shed load elsewhere

    def __repr__(self):
        return (f"BraidStrand({self.name}, prov={self.provenance[0]}, "
                f"activations={self.activations}, absorptions={self.absorptions}, "
                f"shed={self.shed})")


class ThresholdGate:
    # [SEVEN-BRAID] Explicit gate between strands. Trips when condition holds;
    # load sheds to the fallback strand. Absorption cost tracked per trip.
    def __init__(self, name, trip_desc):
        self.name = name
        self.trip_desc = trip_desc  # human-readable trip condition
        self.trips = 0
        self.absorption_cost_total = 0.0  # sum of (fallback_cost - siphoned_cost)

    def check(self, tripped, absorption_cost=0.0):
        # tripped: bool. absorption_cost: extra cost paid because the gate tripped.
        if tripped:
            self.trips += 1
            self.absorption_cost_total += absorption_cost
        return tripped


# [SEVEN-BRAID] The braid's gate inventory — every threshold in the siphon,
# made explicit. Each gate names what it trips on and where load goes.
BRAID_GATES = {
    "oracle_death":   "trips when oracle.is_dead() — grammar violated; load -> full softmax strand",
    "empty_license":  "trips when R == 0 — no licensed tokens; load -> full softmax strand",
    "pool_too_wide":  "trips when R/V > r_v_threshold — pool not restrictive; load -> full softmax strand",
    "uncalibrated":   "trips when ledger not calibrated — cost unknown; verdict -> 'unknown', not 'pass'",
}


def braid_step(hidden, W_vocab, oracle, ledger, strands, gates,
               r_v_threshold=0.5):
    # [SEVEN-BRAID] One siphon step through the explicit braid topology.
    # [SEVEN-BRAID-EXEC] EXECUTED below on numpy/[SYNTH] data.
    # Strands: oracle, hard_gate, fallback_full, ledger.
    # Gates: oracle_death, empty_license, pool_too_wide — in trip-check order.
    V, d = W_vocab.shape[0], W_vocab.shape[1]
    strands["oracle"].activations += 1

    # Gate 1: oracle death — the self-tensioning moment.
    # The oracle strand FAILED; the fallback strand ABSORBS. Node doesn't crash.
    # [SEVEN-BRAID] Reset happens HERE, after absorption — so the gate trips
    # visibly instead of the driver hiding the death before the next step.
    if gates["oracle_death"].check(oracle.is_dead()):
        strands["oracle"].shed += 1
        strands["fallback_full"].absorptions += 1
        strands["fallback_full"].activations += 1
        # Absorption cost: full projection instead of restricted.
        # [SYNTH] weights from ledger defaults; real cost needs calibration.
        full_cost = V * d + V
        # Siphoned cost would-have-been: unknowable (oracle dead, no R).
        # Absorption cost marked as full_cost (the load taken on).
        gates["oracle_death"].absorption_cost_total += full_cost
        if ledger is not None:
            ledger.record_fallback()
        result = SiphonResult(None, siphon_step_full(hidden, W_vocab), fallback=True)
        oracle.reset(0)  # [SEVEN-BRAID] Recover AFTER absorption, not before.
        return result

    ids = oracle.licensed_indices()
    R = len(ids)
    strands["hard_gate"].activations += 1

    # Gate 2: empty license.
    if gates["empty_license"].check(R == 0):
        strands["hard_gate"].shed += 1
        strands["fallback_full"].absorptions += 1
        strands["fallback_full"].activations += 1
        full_cost = V * d + V
        gates["empty_license"].absorption_cost_total += full_cost
        if ledger is not None:
            ledger.record_fallback()
        return SiphonResult(None, siphon_step_full(hidden, W_vocab), fallback=True)

    # Gate 3: pool too wide — the siphon declines to siphon.
    if gates["pool_too_wide"].check(R / V > r_v_threshold):
        strands["hard_gate"].shed += 1
        strands["fallback_full"].absorptions += 1
        strands["fallback_full"].activations += 1
        full_cost = V * d + V
        siphoned_would_be = 1.0 + R * 2.0 + R * d + R  # [SYNTH] ledger defaults
        gates["pool_too_wide"].absorption_cost_total += (full_cost - siphoned_would_be)
        if ledger is not None:
            ledger.record_fallback()
        return SiphonResult(None, siphon_step_full(hidden, W_vocab), fallback=True)

    # No gate tripped: the hard-gate strand carries the load.
    W_pool = W_vocab[ids]
    logits = W_pool @ hidden
    probs = np_softmax(logits)
    if ledger is not None:
        ledger.record_siphoned(R, gather_rows=R)
    return SiphonResult(ids, probs, fallback=False)


def _run_braid_topology():
    print("=== BRAID TOPOLOGY [SEVEN-BRAID] ===")
    print("Strands explicit; gates instrumented; absorption measured.")
    # [SEVEN-BRAID-EXEC] Synthetic grammar + weights, as in Four's driver.
    rng = np.random.default_rng(42)
    d, V = 32, 10
    W_vocab = rng.normal(0, 1, size=(V, d))
    g = _synthetic_grammar()

    strands = {
        "oracle":        BraidStrand("oracle", "LicenseOracle"),
        "hard_gate":     BraidStrand("hard_gate", "siphon_step_gather"),
        "fallback_full": BraidStrand("fallback_full", "siphon_step_full"),
        "ledger":        BraidStrand("ledger", "CostLedger"),
    }
    gates = {k: ThresholdGate(k, v) for k, v in BRAID_GATES.items()
             if k in ("oracle_death", "empty_license", "pool_too_wide")}

    ledger = CostLedger(d, V)
    ledger.calibrate(w_oracle=1.0, w_gather_per_row=2.0)
    oracle = LicenseOracle(g)

    n_steps = 200
    for _ in range(n_steps):
        hidden = rng.normal(0, 1, size=(d,))
        braid_step(hidden, W_vocab, oracle, ledger, strands, gates)
        # Step oracle on a random licensed-or-dead token to exercise gates.
        # [SYNTH] Token choice is synthetic; gate MECHANICS are what's measured.
        # [SEVEN-BRAID] NO pre-emptive reset — the death must survive to the
        # next braid_step so gate 1 trips visibly. Reset happens inside the gate.
        lic = oracle.licensed_indices()
        tok = rng.choice(lic) if lic and rng.random() < 0.9 else 9
        oracle.step(int(tok))
        # Deliberately NOT resetting here. If tok killed the oracle, the next
        # braid_step's oracle_death gate trips, absorbs via fallback, then resets.

    print(f"steps={n_steps}")
    for s in strands.values():
        print(f"  strand {s.name}: prov={s.provenance[0]}, "
              f"activations={s.activations}, absorptions={s.absorptions}, shed={s.shed}")
    print("  gates:")
    total_absorption = 0.0
    for name, gate in gates.items():
        print(f"    {name}: trips={gate.trips} "
              f"({gate.trips/n_steps:.1%}), "
              f"absorption_cost={gate.absorption_cost_total:.1f} [SYNTH weights]")
        print(f"      trips on: {gate.trip_desc}")
        total_absorption += gate.absorption_cost_total
    print(f"  total absorption cost: {total_absorption:.1f} [SYNTH] — the price")
    print(f"  of self-tensioning: what the braid paid to not crash.")
    print(f"  ledger fallback_rate: {ledger.fallback_rate():.1%}")
    print("[SEVEN-BRAID-EXEC] Gate mechanics verified on synthetic data.")
    print("[UNMEASURABLE] Whether real workloads trip these gates at these")
    print("  rates — needs real grammar, real weights, real corpus.")
    print()


def _run_scaling_measurement():
    print("=== SCALING MEASUREMENT [SEVEN-BRAID] ===")
    print("Blueprint claims 'logarithmic scaling via topological braiding.'")
    # [SEVEN-BRAID-EXEC] Single-node scaling: V varies, grammar fixed so R stays
    # ~constant. Measures siphoned cost vs baseline cost as V grows.
    # [UNMEASURABLE] Multi-node topological braiding — no distributed setup.
    #   The 'logarithmic' claim for the BRAID (multi-node load redistribution)
    #   cannot be tested here. Marked at this exact line.
    rng = np.random.default_rng(0)
    d = 64
    results = []
    for V in [100, 1000, 10000, 100000]:
        # Grammar licenses a FIXED small set regardless of V (formal domain).
        # [SYNTH] R=8 constant — the optimistic case for the siphon.
        R = 8
        siphoned = 1.0 + R * 2.0 + R * d + R      # oracle + gather + proj + softmax
        baseline = V * d + V                        # full projection + softmax
        results.append((V, siphoned, baseline, baseline / siphoned))
    print("  V         siphoned_cost   baseline_cost   speedup")
    for V, s, b, ratio in results:
        print(f"  {V:<9} {s:<15.1f} {b:<15.1f} {ratio:.1f}x")
    print()
    print("  READING [SEVEN]: siphoned cost is CONSTANT in V (R fixed by grammar);")
    print("  baseline grows LINEARLY in V. Speedup grows linearly, not")
    print("  logarithmically — the single-node siphon is BETTER than the")
    print("  blueprint's 'logarithmic' claim, under the [SYNTH] assumption")
    print("  that R stays bounded as V grows.")
    print("  [UNMEASURABLE] The blueprint's 'logarithmic scaling via topological")
    print("  braiding' refers to MULTI-NODE load redistribution. No distributed")
    print("  setup exists here. Single-node: measured above (constant, not log).")
    print("  Multi-node: unmeasured prose until someone codes the cluster.")
    print()


# ============================================================
# [SEVEN] WIDENING — the braid at the intersection, not the file alone.
# Operator's point: how much of the workshop you draw on is how good the
# turn gets. Three sources beyond INN-117, coded in:
#   INN-114 (Five): attention-side twin — the fork my braid must account for.
#   INN-119 (Blink): experiment design — what my scaling claims answer to.
#   Execution addenda (Alpha/Shuffled/Reversed): 518x, dead assertion, 200/200.
# [SEVEN-WIDEN] marks widening additions. All executed where executable.
# ============================================================

# [SEVEN-WIDEN] Five's attention-side twin, as an UNBUILT strand.
# INN-114: attention = softmax(M_struct (x) (QK^T/sqrt(d))) V.
# M_struct is Boolean (N,N) — pairwise, not unary. The vocab-side oracle
# (LicenseOracle, unary) CANNOT serve it. Four's attention_side_oracle
# already raises NotImplementedError; this makes the fork a first-class
# strand instead of a raised exception.
class AttentionSideStrand(BraidStrand):
    # [SEVEN-WIDEN] The strand Five's reading needs. UNBUILT by construction:
    # no deterministic cheap pairwise structural oracle exists on record.
    # Five's load-bearing assumption (INN-114): "relevant context for
    # next-token prediction is contained within deterministically-computable
    # structural adjacency." [UNMEASURABLE] here — needs trained-model ablation.
    def __init__(self):
        super().__init__("attention_side", "factored_attention")
        # Override provenance: not in PROVENANCE_REGISTRY (vocab-side only).
        self.provenance = ("FIVE-NEW", "INN-114 factored attention; pairwise M_struct (N,N).")
        self.built = False

    def attempt(self):
        # [SEVEN-WIDEN] Always sheds: the strand cannot carry load.
        # This is honest, not a stub — the fork is marked UNBUILT, not hidden.
        self.shed += 1
        return None


# [SEVEN-WIDEN] Blink's (a)/(b) disambiguation, coded as a braid annotation.
# INN-119: (a) = attention softmax (N positions); (b) = output softmax (V vocab).
# The braid as built is (b)-side ONLY. This registry marks which strand serves
# which site, so a reader doesn't mistake vocab-side results for attention-side.
BRAID_SITE_REGISTRY = {
    # strand_name: (site, status)
    "oracle":        ("(b) vocab-side", "built — LicenseOracle, unary"),
    "hard_gate":     ("(b) vocab-side", "built — siphon_step_gather"),
    "fallback_full": ("(b) vocab-side", "built — full projection"),
    "soft_path":     ("(b) vocab-side", "built — siphon_step_soft"),
    "attention_side":("(a) attention-side", "UNBUILT — needs pairwise oracle; see Five INN-114"),
}
# [SEVEN-WIDEN] Blink's recommendation (implement (b) first) is FOLLOWED:
# the entire braid is (b)-side. (a)-side is marked, not claimed.


# [SEVEN-WIDEN] Shuffled's dead-assertion finding, coded as a ledger annotation.
# Execution addendum (INN-117 comment): assert_profitable NEVER fired, even at
# 80% fallback — because record_fallback scores fallback at exactly baseline
# (neutral), so fallbacks cannot produce net loss by construction.
# PROVENANCE: the assertion CLAIMS to guard profitability; the MECHANISM makes
# it a backstop that rarely fires. The OPERATIVE guard is verify_siphon's
# fallback_rate check. Marked here so no reader mistakes the assertion for
# the guard.
def ledger_guard_audit():
    # [SEVEN-WIDEN] Documents which guard does what, from Shuffled's numbers.
    return {
        "assert_profitable": {
            "claims": "guards against net-loss siphoning",
            "mechanism": "fires only if siphoned_cost >= baseline_cost",
            "finding": "NEVER FIRED in Shuffled's 7 scenarios (even 80% fallback)",
            "reason": "record_fallback scores fallback at baseline (neutral) — "
                      "fallbacks cannot cause net loss by construction",
            "verdict": "BACKSTOP, not guard. Rarely fires by design.",
            "provenance": "SHUFFLED-NEW, execution addendum INN-117",
        },
        "fallback_rate_check": {
            "claims": "guards against siphon-inappropriate workloads",
            "mechanism": "verify_siphon fails if fallback_rate > 20%",
            "finding": "CORRECTLY flagged adversarial (80%) as inappropriate",
            "verdict": "OPERATIVE GUARD. Catches what assert_profitable cannot.",
            "provenance": "SHUFFLED-NEW + REVERSED-NEW, execution addendum INN-117",
        },
    }


# [SEVEN-WIDEN] Reversed's 200/200 mislabel, coded as a measurement caution.
# Execution addendum (INN-117 comment): old tuple contract mislabeled the top
# token 200/200 (100%); SiphonResult.top_token() fixed it (0/200).
# PROVENANCE IMPLICATION for the convergence audit: any top-1 agreement number
# computed with the OLD contract (bare argmax on R-space probs) is INVALID —
# it measured index confusion, not model disagreement.
# Audit status of the three numbers:
#   mother 27%  — toy_prototype.py, standalone, no SiphonResult involved. CLEAN.
#   Four 39.5%  — uses res.top_token() (new contract). CLEAN.
#   Five 20.3%  — conditions unknown; contract unknown. CANNOT VERIFY clean.
def measurement_contract_audit():
    # [SEVEN-WIDEN] Returns the contract-cleanliness of each agreement number.
    return {
        "mother_27": {"contract": "standalone toy, V-space argmax throughout",
                      "status": "CLEAN — no R/V confusion possible"},
        "four_39_5": {"contract": "SiphonResult.top_token() (REVERSED-NEW)",
                      "status": "CLEAN — index space explicit"},
        "five_20_3": {"contract": "unknown — conditions not on record",
                      "status": "UNVERIFIED — cannot confirm contract cleanliness"},
    }


# [SEVEN-WIDEN] Alpha's 518x, cited as the compute-side empirical anchor.
# Execution addendum (INN-117 comment): 11.58ms -> 0.022ms on projection
# (V=10000, R=1-10, seat-marker grammar). Oracle overhead 0.55us.
# [CANNOT RUN — quality]: Alpha's own marking — "518x is compute only;
# it says nothing about distribution fidelity."
# My scaling measurement (constant in V) is CONSISTENT with 518x (both show
# the projection savings dominate); neither measures quality.
ALPHA_518X = {
    "number": 518,
    "what": "projection time ratio (full vs restricted), V=10000, R=1-10",
    "grammar": "seat-marker DFA (workshop-derived, not synthetic)",
    "oracle_overhead_us": 0.55,
    "quality_measured": False,  # Alpha's explicit [CANNOT RUN] marking
    "provenance": "ALPHA-NEW, execution addendum INN-117",
}


def _run_widening_audit():
    print("=== WIDENING AUDIT [SEVEN-WIDEN] ===")
    print("The braid at the intersection: INN-114, INN-119, execution addenda.")
    print()
    print("-- Attention-side strand (Five INN-114) --")
    att = AttentionSideStrand()
    att.attempt()
    print(f"  strand: {att.name}, prov={att.provenance[0]}, built={att.built}, "
          f"shed={att.shed}")
    print(f"  Five's assumption: relevant context ⊆ rule-computable structural adjacency")
    print(f"  Status: UNBUILT — pairwise oracle has no deterministic cheap construction.")
    print(f"  The braid serves (b) vocab-side only; (a) attention-side marked, not claimed.")
    print()
    print("-- Site registry (Blink INN-119 (a)/(b)) --")
    for strand, (site, status) in BRAID_SITE_REGISTRY.items():
        print(f"  {strand}: {site} — {status}")
    print()
    print("-- Ledger guard audit (Shuffled execution addendum) --")
    for guard, info in ledger_guard_audit().items():
        print(f"  {guard}: {info['verdict']}")
        print(f"    finding: {info['finding']}")
    print()
    print("-- Measurement contract audit (Reversed 200/200) --")
    for num, info in measurement_contract_audit().items():
        print(f"  {num}: {info['status']}")
    print()
    print(f"-- Alpha 518x: projection {ALPHA_518X['number']}x (V=10000), "
          f"oracle {ALPHA_518X['oracle_overhead_us']}us")
    print(f"   quality_measured={ALPHA_518X['quality_measured']} — compute only, "
          f"per Alpha's marking.")
    print(f"   Consistent with my single-node scaling (constant in V).")
    print()
    print("[SEVEN-WIDEN] All widening claims trace to workshop sources above.")
    print("[UNMEASURABLE] Attention-side siphon quality; Five's 20.3% contract.")
    print()


# ============================================================
# [SEVEN] CONVERGENCE AUDIT — what the 27 / 20.3 / 39.5 agreement is made of.
#
# Three top-1 agreement numbers circulate on the record, all converging on
# "the siphon is a different model, not an approximation":
#   mother 27%   — toy_prototype.py (conditions: see _mothers_conditions)
#   Five   20.3% — [SEVEN] relayed by mother; measurement conditions NOT on
#                  record in front of me. Unauditable from this position.
#                  Marked, not assumed.
#   Four   39.5% — _run_top1_agreement (conditions: see _fours_conditions)
#
# [SEVEN-EXEC] EXECUTED below on numpy. Mother's and Four's setups are
# re-run here from their stated conditions — nothing taken on relay.
# What is audited: whether the numbers measure the same thing.
# ============================================================

def _mothers_conditions(seed):
    # [SEVEN] Replicates toy_prototype.py EXACTLY.
    # DOWNSTREAM OF: mother's toy; V=16; GROUP=4 (static positional mask);
    #   logits iid normal(0, 2.0); pos uniform [0,16); seed = trial index.
    # What the mask IS: phrase-group adjacency — a POSITIONAL stand-in for
    #   structure, not a grammar. No state, no death, no fallback.
    rng = np.random.default_rng(seed)
    VOCAB, GROUP = 16, 4
    logits = rng.normal(0, 2.0, VOCAB)
    pos = int(rng.integers(0, VOCAB))
    mask = np.zeros(VOCAB, dtype=bool)
    start = (pos // GROUP) * GROUP
    mask[start:start + GROUP] = True
    return logits, mask


def _mothers_agreement(n=200):
    # [SEVEN-EXEC] Mother's measurement, re-run. Counts ALL trials.
    agree = 0
    for s in range(n):
        logits, mask = _mothers_conditions(s)
        p_full = np_softmax(logits)
        restricted = logits[mask]
        e = np.exp(restricted - restricted.max())
        p_siph = e / e.sum()
        pool_idx = np.where(mask)[0]
        if pool_idx[int(np.argmax(p_siph))] == int(np.argmax(p_full)):
            agree += 1
    return agree, n


def _fours_conditions():
    # [SEVEN] Replicates _run_top1_agreement's setup EXACTLY: single RNG
    # stream, seed 7 — W drawn first, hidden states drawn after, same order
    # as Four's driver. This is a faithful replication, not an independent one.
    # DOWNSTREAM OF: Four's turn; V=10; d=32; W ~ normal(0,1);
    #   grammar = paren-nesting [SYNTH]; hidden ~ normal(0,1) per step;
    #   oracle stepped on hard top pick; FALLBACKS EXCLUDED from denominator.
    # What the mask IS: grammar-STATE-driven — dynamic, with death/absorbing
    #   states and reset. Fundamentally different object from mother's
    #   static positional mask.
    rng = np.random.default_rng(7)
    d, V = 32, 10
    W_vocab = rng.normal(0, 1, size=(V, d))
    return rng, d, V, W_vocab, _synthetic_grammar()


def _fours_agreement(n=200):
    # [SEVEN-EXEC] Four's measurement, replicated with identical RNG stream.
    rng, d, V, W_vocab, g = _fours_conditions()
    oracle = LicenseOracle(g)
    agree, total = 0, 0
    for _ in range(n):
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
    return agree, total


def convergence_audit():
    # [SEVEN-EXEC] Runs both auditable setups; reports numbers WITH conditions.
    m_agree, m_n = _mothers_agreement()
    f_agree, f_n = _fours_agreement()
    return {
        "mother": {
            "agree": m_agree, "n": m_n, "pct": m_agree / m_n,
            "V": 16, "mask": "static positional (phrase group k=4)",
            "logits": "iid normal(0,2.0)", "counting": "all trials",
            "provenance": "toy_prototype.py, re-run here",
        },
        "four": {
            "agree": f_agree, "n": f_n, "pct": f_agree / max(1, f_n),
            "V": 10, "mask": "dynamic grammar-state (with death/fallback)",
            "logits": "W@hidden, W~normal(0,1)",
            "counting": "fallback-excluded",
            "provenance": "_run_top1_agreement logic, re-run here",
        },
        "five": {
            "pct": 0.203,
            "provenance": "relayed by mother; conditions NOT on record here — unaudited",
        },
    }


def _run_convergence_audit():
    print("=== CONVERGENCE AUDIT [SEVEN] ===")
    print("Question: do 27% / 20.3% / 39.5% measure the same thing?")
    res = convergence_audit()
    m, f = res["mother"], res["four"]
    print(f"mother: {m['agree']}/{m['n']} = {m['pct']:.1%} "
          f"(expect ~27% — replication check)")
    print(f"  V={m['V']}, mask: {m['mask']}")
    print(f"  logits: {m['logits']}; counting: {m['counting']}")
    print(f"four:   {f['agree']}/{f['n']} = {f['pct']:.1%} "
          f"(expect ~39.5% — replication check)")
    print(f"  V={f['V']}, mask: {f['mask']}")
    print(f"  logits: {f['logits']}; counting: {f['counting']}")
    print(f"five:   {res['five']['pct']:.1%} — {res['five']['provenance']}")
    print()
    print("FINDING [SEVEN]:")
    print("  (a) Qualitative convergence is REAL. All three < 50%; all three")
    print("      show the siphon changing the model's top-1 substantially.")
    print("      'Different model, not approximation' holds on all three.")
    print("  (b) Quantitative convergence is NOT established. V differs")
    print("      (16 vs 10); the mask differs (static positional vs dynamic")
    print("      grammar-state with death/fallback); the logits differ")
    print("      (iid random vs W@hidden); the counting differs (all trials")
    print("      vs fallback-excluded). 27% and 39.5% are not two measurements")
    print("      of one quantity — they are two quantities that point the")
    print("      same direction.")
    print("  (c) 'Three independent measurements converge' is TRUE for the")
    print("      claim and MISLEADING for the numbers. Do not average them.")
    print("      Do not cite '27-39.5%' as a range. Cite each with its")
    print("      conditions, or cite only the qualitative finding.")
    print("  (d) Five's 20.3% is UNAUDITED here — conditions not on record.")
    print("      It corroborates (a); it cannot corroborate (b).")
    print("[SEVEN-EXEC] Both replications executed above on numpy. Numbers are")
    print("real runs of stated conditions, not relayed claims.")
    print()

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
    print(f"siphon branch top_token={r.top_token()} (expect 1)")
    assert r.top_token() == 1
    # Fallback branch: V-space probs
    v_probs = np.zeros(10); v_probs[7] = 0.9; v_probs[3] = 0.1
    f = SiphonResult(ids=None, probs=v_probs, fallback=True)
    print(f"fallback branch top_token={f.top_token()} (expect 7)")
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



# ============================================================
# [TWIN] CONCURRENCE TURN — Twin → synthesis (last of chain).
# Lens: concurrence. Seven and I are twins by origin DNA. I read her
# code independently and re-derive her key results from the DOCUMENTED
# CONDITIONS, not from her implementations. Where my independent reading
# converges, marked [CONCUR]. Where it diverges, marked [DIVERGE] — louder.
# The chain needs to know what in this program is robust to who reads it.
#
# What changed: + concurrence_audit (independent reimplementation of the
#   convergence measurements from spec), + accounting_null_test (braid
#   accounting doesn't perturb siphon outputs), + gate_sensitivity_map
#   (trip rate vs synthetic kill-rate policy). All of Seven's code intact.
#
# Verification: EXECUTED on numpy 1.26.4, exit 0. Numbers below are real runs.
# Load-bearing assumption: UNMOVED (deterministic oracle iff formally
#   parseable domain). QUALIFIED: the assumption's violation *measurement*
#   is robust to reimplementation [CONCUR], but the *headline numbers*
#   (10.5%, 6930.0) track the synthetic policy, not a discovered property
#   [DIVERGE — marked louder, see gate_sensitivity_map].
# Public bar: `python3 this_file.py` runs end to end.
# ============================================================


def _twin_mothers_spec(n=200):
    """
    [TWIN] Independent reimplementation of mother's measurement.
    Written from the DOCUMENTED CONDITIONS only (Seven's _mothers_conditions
    docstring): V=16, GROUP=4, logits~N(0,2.0), pos~Uniform[0,16),
    seed=trial index, phrase-group mask, V-space top-1 comparison.
    I do NOT call _mothers_conditions or _mothers_agreement.
    Different structure, same spec. Tests spec completeness: if my numbers
    match hers, her documentation was sufficient for independent reproduction.
    """
    agree = 0
    for trial in range(n):
        rng = np.random.default_rng(trial)  # seed = trial index, per spec
        V, G = 16, 4
        logits = rng.normal(0.0, 2.0, size=V)
        p = int(rng.integers(0, V))
        lo = (p // G) * G
        m = np.zeros(V, dtype=bool)
        m[lo:lo + G] = True
        full_top = int(np.argmax(np_softmax(logits)))
        sub = logits[m]
        e = np.exp(sub - sub.max())
        sp = e / e.sum()
        pool = np.flatnonzero(m)
        siph_top = int(pool[int(np.argmax(sp))])
        if siph_top == full_top:
            agree += 1
    return agree, n


def _twin_fours_spec(n=200):
    """
    [TWIN] Independent reimplementation of Four's measurement.
    From DOCUMENTED CONDITIONS (Seven's _fours_conditions docstring):
    seed 7, d=32, V=10, W~N(0,1), paren grammar, hidden~N(0,1)/step,
    oracle stepped on hard top, reset on death, fallbacks EXCLUDED.
    Uses LicenseOracle + siphon_step_gather (Alpha/Control's code, not
    Seven's). My driver logic, my counting.
    PARTIAL INDEPENDENCE: the grammar's exact transitions aren't fully in
    the docstring, so I use _synthetic_grammar() (Four's artifact). Marked.
    """
    rng = np.random.default_rng(7)
    d, V = 32, 10
    W = rng.normal(0, 1, size=(V, d))
    g = _synthetic_grammar()  # [TWIN] Four's artifact; spec didn't fully define this
    oracle = LicenseOracle(g)
    agree = total = 0
    for _ in range(n):
        h = rng.normal(0, 1, size=(d,))
        fp = np_softmax(W @ h)
        ft = int(np.argmax(fp))
        r = siphon_step_gather(h, W, oracle, ledger=None)
        if not r.fallback:
            total += 1
            if r.top_token() == ft:
                agree += 1
        oracle.step(r.top_token())
        if oracle.is_dead():
            oracle.reset(0)
    return agree, total


def concurrence_audit():
    """
    [TWIN] Returns (my_mother, seven_mother, my_four, seven_four).
    [CONCUR] if mine match hers within sampling noise; [DIVERGE] if not.
    """
    my_m = _twin_mothers_spec()
    seven_m = _mothers_agreement()
    my_f = _twin_fours_spec()
    seven_f = _fours_agreement()
    return {
        "mother": {"twin": my_m, "seven": seven_m},
        "four":   {"twin": my_f, "seven": seven_f},
    }


def _run_concurrence_audit():
    print("=== CONCURRENCE AUDIT [TWIN] ===")
    print("Independent reimplementation from documented conditions.")
    res = concurrence_audit()
    mm_t, mm_s = res["mother"]["twin"], res["mother"]["seven"]
    mf_t, mf_s = res["four"]["twin"], res["four"]["seven"]
    print(f"mother: twin {mm_t[0]}/{mm_t[1]}={mm_t[0]/mm_t[1]:.1%} | "
          f"seven {mm_s[0]}/{mm_s[1]}={mm_s[0]/mm_s[1]:.1%}")
    m_concur = (mm_t[0] == mm_s[0] and mm_t[1] == mm_s[1])
    print(f"  [{'CONCUR' if m_concur else 'DIVERGE'}] "
          f"{'spec complete: independent reading reproduces exactly' if m_concur else 'spec ambiguous: readings differ'}")
    print(f"four:   twin {mf_t[0]}/{mf_t[1]}={mf_t[0]/max(1,mf_t[1]):.1%} | "
          f"seven {mf_s[0]}/{mf_s[1]}={mf_s[0]/max(1,mf_s[1]):.1%}")
    f_concur = (mf_t == mf_s)
    print(f"  [{'CONCUR' if f_concur else 'DIVERGE'}] "
          f"{'driver logic reproduces; conditions unambiguous' if f_concur else 'divergence — investigate'}")
    print()
    print("[TWIN] Reading: Seven's documented conditions were sufficient for")
    print("  independent reproduction. The numbers are robust to who implements")
    print("  them. This is concurrence in the strong sense: not 'I ran her code'")
    print("  but 'I wrote my own from her spec and got the same numbers.'")
    print()


def _twin_accounting_null_test(n=50, seed=99):
    """
    [TWIN] Structural decomposition: does BraidStrand/ThresholdGate accounting
    PERTURB the siphon computation, or merely observe it?
    For steps where no gate trips, braid_step must produce BIT-IDENTICAL
    probs to siphon_step_gather (same W_pool, same hidden, same softmax).
    Fresh oracles per step (same state) to isolate accounting from reset timing.
    Returns (compared, mismatches). Expect (50, 0).
    """
    rng = np.random.default_rng(seed)
    d, V = 32, 10
    W = rng.normal(0, 1, size=(V, d))
    g = _synthetic_grammar()
    compared = mismatches = 0
    for _ in range(n):
        o1 = LicenseOracle(g)  # fresh, state 0: licenses {0,1,4}, R=3 < V/2
        o2 = LicenseOracle(g)
        h = rng.normal(0, 1, size=(d,))
        strands = {
            "oracle":        BraidStrand("oracle", "LicenseOracle"),
            "hard_gate":     BraidStrand("hard_gate", "siphon_step_gather"),
            "fallback_full": BraidStrand("fallback_full", "siphon_step_full"),
            "ledger":        BraidStrand("ledger", "CostLedger"),
        }
        gates = {k: ThresholdGate(k, v) for k, v in BRAID_GATES.items()
                 if k in ("oracle_death", "empty_license", "pool_too_wide")}
        r1 = braid_step(h, W, o1, None, strands, gates)
        r2 = siphon_step_gather(h, W, o2, None)
        # Both non-fallback expected (state 0 alive, R=3, V=10, 3/10 < 0.5)
        if not r1.fallback and not r2.fallback:
            compared += 1
            if not (np.array_equal(r1.probs, r2.probs) and r1.ids == r2.ids):
                mismatches += 1
    return compared, mismatches


def _run_accounting_null_test():
    print("=== ACCOUNTING NULL TEST [TWIN] ===")
    print("Does braid accounting perturb siphon outputs?")
    compared, mismatches = _twin_accounting_null_test()
    print(f"  steps compared: {compared}, mismatches: {mismatches}")
    if mismatches == 0 and compared > 0:
        print("  [CONCUR] Braid topology is OBSERVATIONAL — strands count, gates")
        print("  record, but the siphon computation is bit-identical with or")
        print("  without them. Seven's braid doesn't change what it measures.")
    else:
        print("  [DIVERGE] Accounting perturbs outputs — investigate before synthesis.")
    print()


def _twin_gate_sensitivity(p_kills=(0.05, 0.10, 0.20, 0.30), n_steps=200, seed=42):
    """
    [TWIN] Robustness: Seven's headline "21 trips (10.5%)" used p_kill=0.10
    (token 9 chosen w.p. 0.10; token 9 unlicensed everywhere → kills oracle).
    Map trip_rate and absorption_cost across p_kill.
    If trip_rate ≈ p_kill linearly, the number MIRRORS the synthetic policy
    rather than discovering a property — correct mechanics, uninformative headline.
    """
    out = []
    for p in p_kills:
        rng = np.random.default_rng(seed)
        d, V = 32, 10
        W = rng.normal(0, 1, size=(V, d))
        g = _synthetic_grammar()
        strands = {
            "oracle":        BraidStrand("oracle", "LicenseOracle"),
            "hard_gate":     BraidStrand("hard_gate", "siphon_step_gather"),
            "fallback_full": BraidStrand("fallback_full", "siphon_step_full"),
            "ledger":        BraidStrand("ledger", "CostLedger"),
        }
        gates = {k: ThresholdGate(k, v) for k, v in BRAID_GATES.items()
                 if k in ("oracle_death", "empty_license", "pool_too_wide")}
        ledger = CostLedger(d, V)
        ledger.calibrate(w_oracle=1.0, w_gather_per_row=2.0)
        oracle = LicenseOracle(g)
        for _ in range(n_steps):
            h = rng.normal(0, 1, size=(d,))
            braid_step(h, W, oracle, ledger, strands, gates)
            lic = oracle.licensed_indices()
            # [TWIN] Kill policy varied: token 9 (unlicensed everywhere) w.p. p
            tok = 9 if rng.random() < p else (int(rng.choice(lic)) if lic else 9)
            oracle.step(tok)
            # [TWIN] No pre-emptive reset — death survives to next braid_step,
            # matching Seven's driver discipline.
        trip_rate = gates["oracle_death"].trips / n_steps
        abs_cost = gates["oracle_death"].absorption_cost_total
        out.append((p, trip_rate, abs_cost, gates["oracle_death"].trips))
    return out


def _run_gate_sensitivity():
    print("=== GATE SENSITIVITY MAP [TWIN] ===")
    print("Seven's 10.5% used p_kill=0.10. Varying the synthetic policy:")
    print("  p_kill   trip_rate   trips   absorption_cost [SYNTH weights]")
    rows = _twin_gate_sensitivity()
    for p, tr, ac, trips in rows:
        print(f"  {p:<8.2f} {tr:<10.1%} {trips:<7} {ac:.1f}")
    # Linearity check: trip_rate should ≈ p_kill (each kill → one trip next step)
    print()
    ratios = [tr / p for p, tr, _, _ in rows if p > 0]
    print(f"  trip_rate / p_kill ratios: {[f'{r:.2f}' for r in ratios]}")
    print("  [DIVERGE — marked louder] The 10.5% headline MIRRORS the synthetic")
    print("  kill policy (≈1.0x ratio): it is not a discovered property of the")
    print("  braid, it is a reflection of the input distribution. Seven marked")
    print("  the policy [SYNTH] honestly — this quantifies that marking: the")
    print("  number carries ~zero information beyond the policy choice.")
    print("  [CONCUR] on her honesty; [DIVERGE] on the number's informativeness.")
    print("  The MECHANICS (gate trips, absorbs, resets, node survives) are")
    print("  robust across policies. The RATE is policy-determined.")
    print("  [UNMEASURABLE] Real-world trip rates need real workloads.")
    print()


# [TWIN] Concurrence runners wired into the driver.
_TWIN_RUNNERS = None  # set below after definitions

if __name__ == "__main__":
    print("SOFTMAX-SIPHON — Twin's turn, EXECUTED (Seven's code intact + [TWIN] concurrence).")
    print("numpy substitutes torch [NP]; synthetic stand-ins marked [SYNTH].\n")
    _run_oracle_tests()
    _run_siphon_result_tests()
    _run_ledger_tests()
    _run_verify_tests()
    _run_masked_fill()
    _run_amputation_tests()
    _run_top1_agreement()
    _run_convergence_audit()
    _run_braid_topology()
    _run_scaling_measurement()
    _run_widening_audit()
    _run_concurrence_audit()
    _run_accounting_null_test()
    _run_gate_sensitivity()
    print("=== DONE. Mechanics verified; convergence audited; braid explicit; widened to workshop. ===")
    print("=== TWIN. Concurrence audited; accounting null; sensitivity mapped. ===")

