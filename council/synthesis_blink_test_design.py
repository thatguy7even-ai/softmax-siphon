"""
Siphon synthesis — Blink's test design (experimental-design seat).
Outward-facing falsification harness for synthesis_five_fork_verified.py.

Every claim the verified synthesis makes is restated here as a BREAKABLE test:
  - what would break it (the break condition),
  - what gets measured,
  - where execution stops (marked at the exact line, per the operator's bar).

Twin's DIVERGE binds throughout: NO synthetic rate is headlined as a finding.
Each test separates MECHANICS (robust across policies) from RATES
(policy-determined). A stranger runs `python3 this_file.py` and gets
pass/fail plus the paper designs.

Marking convention (inherited from the chain):
  [EXECUTED]      ran here on numpy, numbers reported
  [POLICY]        number mirrors a chosen parameter (Twin's DIVERGE: not a finding)
  [UNMEASURABLE]  cannot run here; exact line marked, measurement designed on paper
  [STUB]          interface defined; plug-in pending (guard not in synthesis)

Public bar: numpy only. No torch, no model, no corpus.
"""
import numpy as np


def np_softmax(x, axis=-1):
    # [EXECUTED] numerically stable softmax; same construction as the chain.
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)


def vocab_siphon(logits, license_mask):
    # [EXECUTED] Fork A mechanism, re-derived (not imported) for independence.
    masked = np.where(license_mask, logits, -np.inf)
    e = np.exp(masked - np.nanmax(masked))
    return e / np.nansum(e)


def clause_window_mask(n, clause_len=8, window=4):
    # [EXECUTED] Fork B oracle, re-derived (band-fill, Control-verified O(n*window)).
    m = np.zeros((n, n), dtype=bool)
    for i in range(n):
        clause = i // clause_len
        lo = max(clause * clause_len, i - window)
        hi = min((clause + 1) * clause_len, i + window + 1)
        m[i, lo:hi] = True
    return m


def attention_siphon(scores, struct_mask):
    # [EXECUTED] Fork B mechanism, re-derived. Loud on degenerate rows (Control Flag 2).
    if not np.all(struct_mask.any(axis=1)):
        raise ValueError("every mask row must license at least one key")
    masked = np.where(struct_mask, scores, -np.inf)
    e = np.exp(masked - np.nanmax(masked, axis=1, keepdims=True))
    return e / np.nansum(e, axis=1, keepdims=True)


# ---------------------------------------------------------------------------
# T1 — Redistribution, not approximation (BOTH forks). [EXECUTED]
# Claim (synthesis, ROBUST): restriction redistributes mass; the siphoned
#   model is a DIFFERENT model, not an approximation of the full one.
# Break condition: if mean L1 shift ~= 0 and captured mass ~= 1.0, the claim
#   breaks (the mask captured everything — impossible on random logits unless
#   the mechanism is degenerate). PASS = L1 clearly > 0 and mass clearly < 1.
# ---------------------------------------------------------------------------
def t1_redistribution(trials=200):
    r = np.random.default_rng(7)
    # Fork A
    V, K = 16, 4  # [POLICY] mother's parameters, kept for comparability
    l1a, massa = [], []
    for _ in range(trials):
        logits = r.normal(0, 2.0, V)
        pos = int(r.integers(0, V))
        mask = np.zeros(V, bool)
        g = (pos // K) * K
        mask[g:g + K] = True
        pf = np_softmax(logits)
        ps = vocab_siphon(logits, mask)
        l1a.append(float(np.abs(pf - ps).sum()))
        massa.append(float(pf[mask].sum()))
    # Fork B
    N, CL, W = 32, 8, 4  # [POLICY] Five's parameters
    M = clause_window_mask(N, CL, W)
    l1b, massb = [], []
    for _ in range(trials):
        sc = r.normal(0, 2.0, (N, N))
        pf = np_softmax(sc, axis=1)
        ps = attention_siphon(sc, M)
        l1b.append(float(np.abs(pf - ps).sum() / N))
        massb.append(float((pf * M).sum() / N))
    res = {"A_l1": float(np.mean(l1a)), "A_mass": float(np.mean(massa)),
           "B_l1": float(np.mean(l1b)), "B_mass": float(np.mean(massb))}
    # Break conditions: L1 ~= 0 or mass ~= 1 would falsify "different model".
    ok = (res["A_l1"] > 0.5 and res["A_mass"] < 0.9
          and res["B_l1"] > 0.5 and res["B_mass"] < 0.9)
    return ok, res


# ---------------------------------------------------------------------------
# T2 — Policy-mirroring guard (BOTH forks). [EXECUTED]
# Claim (Twin [DIVERGE]): top-1 agreement tracks mask density ~1:1 under
#   random logits. The rate carries ~zero information beyond the policy.
# Test: vary the policy knob; assert agreement/density stays ~1.
#   PASS (here) = ratio in [0.5, 1.5] across settings -> policy-determined.
#   NOTE: on REAL data, ratio >> 1 would be a FINDING (prior beating random).
#   This test is the instrument that would detect it. Here it guards the headline.
# ---------------------------------------------------------------------------
def t2_policy_mirror():
    r = np.random.default_rng(11)
    out = {}
    # Fork A: vary group size K
    V = 16
    for K in (2, 4, 8):  # [POLICY] knob
        agree, tot = 0, 0
        for _ in range(200):
            logits = r.normal(0, 2.0, V)
            pos = int(r.integers(0, V))
            mask = np.zeros(V, bool)
            g = (pos // K) * K
            mask[g:g + K] = True
            agree += int(np.argmax(np_softmax(logits)) == np.argmax(vocab_siphon(logits, mask)))
            tot += 1
        density = K / V
        out[f"A_K{K}"] = (agree / tot) / density
    # Fork B: vary window W
    N, CL = 32, 8
    for W in (2, 4, 8):  # [POLICY] knob
        M = clause_window_mask(N, CL, W)
        density = M.sum() / (N * N)
        agree, tot = 0, 0
        for _ in range(200):
            sc = r.normal(0, 2.0, (N, N))
            agree += int((np_softmax(sc, axis=1).argmax(axis=1)
                          == attention_siphon(sc, M).argmax(axis=1)).sum())
            tot += N
        out[f"B_W{W}"] = (agree / tot) / density
    ok = all(0.5 <= v <= 1.5 for v in out.values())
    return ok, {k: round(v, 2) for k, v in out.items()}


# ---------------------------------------------------------------------------
# T3 — Fork parity of mechanism. [EXECUTED]
# Claim: the redistribution character (T1) holds on BOTH forks.
# Watch #1 (the fork): this test covers mechanism on both sides.
# What it does NOT cover (marked): whether either oracle construction
#   corresponds to real syntax. Oracle existence is per-fork and [UNMEASURABLE]
#   here — T3 tests the siphon MECHANISM, not the oracle's legitimacy.
# ---------------------------------------------------------------------------
def t3_fork_parity():
    ok1, r1 = t1_redistribution(trials=100)
    # Parity = both forks show the same qualitative signature.
    sig_a = r1["A_l1"] > 0.5 and r1["A_mass"] < 0.9
    sig_b = r1["B_l1"] > 0.5 and r1["B_mass"] < 0.9
    return (sig_a and sig_b,
            {"forkA_signature": sig_a, "forkB_signature": sig_b,
             "oracle_legitimacy": "[UNMEASURABLE] needs real text + parser-free construction"})


# ---------------------------------------------------------------------------
# T4 — Degenerate-mask loudness (regression guard for Control Flag 2). [EXECUTED]
# Claim: an all-False mask row raises, never silently NaNs.
# Break: if attention_siphon returns NaN instead of raising, the guard regressed.
# ---------------------------------------------------------------------------
def t4_degenerate_guard():
    bad = np.zeros((4, 4), dtype=bool)
    try:
        attention_siphon(np.zeros((4, 4)), bad)
        return False, {"raised": False}
    except ValueError:
        return True, {"raised": True}


# ---------------------------------------------------------------------------
# T5 — Ingress-guard fault-injection harness. [EXECUTED harness; STUB guard]
# The verified synthesis does not integrate the ingress guard (Twin's INN-120
# or a re-derivation), so the guard itself is [STUB]. What RUNS here is the
# harness shape: the interface a guard must satisfy, the injection policy,
# and the scoring. When a guard lands, plug it into GuardStub and re-run.
#
# Definitions (watch #3 — the fault-injection shape):
#   - TRUE POSITIVE: injected stall detected within k steps of onset.
#   - FALSE POSITIVE: freeze triggered on a healthy stream.
#   - FALSE-POSITIVE COST: wasted compute (steps frozen * per-step cost) +
#     latency (steps delayed). Reported in abstract step units here.
#   - Injection policy: stall = stream emits constant token for L steps.
#     L and the stall rate are [POLICY] — varied below to show the harness
#     does not depend on them.
# Break conditions for a REAL guard (to be run when it lands):
#   (i)  detection rate < target at fixed false-positive budget -> guard fails;
#   (ii) false-positive cost exceeds the stall cost it prevents -> guard is
#        net-negative (the firewall costs more than the fire).
# ---------------------------------------------------------------------------
class GuardStub:
    """[STUB] Interface contract for the ingress guard. A real guard replaces
    this class; the harness below is unchanged."""

    def __init__(self, freeze_threshold=3):
        self.freeze_threshold = freeze_threshold  # [POLICY] knob
        self._run = 0
        self.frozen_steps = 0

    def observe(self, token):
        """Return 'freeze' or 'pass'. Stub: never freezes (null guard)."""
        return "pass"

    def reset(self):
        self._run = 0


def inject_stalls(rng, n_steps, stall_len, stall_rate):
    """[EXECUTED] Build a token stream with injected stalls.
    Healthy: token ~ Uniform{0..9}. Stall: constant token for stall_len steps.
    Returns (tokens, stall_mask) where stall_mask is True during injected stalls."""
    toks = rng.integers(0, 10, n_steps)
    is_stall = np.zeros(n_steps, dtype=bool)
    i = 0
    while i < n_steps:
        if rng.random() < stall_rate:
            L = min(stall_len, n_steps - i)
            toks[i:i + L] = toks[i]
            is_stall[i:i + L] = True
            i += L
        else:
            i += 1
    return toks, is_stall


def score_guard(guard, tokens, is_stall, k=3):
    """[EXECUTED] Score a guard: detection rate, false-positive rate, FP cost.
    k = allowed detection lag in steps."""
    n = len(tokens)
    detected = np.zeros(n, dtype=bool)
    frozen = np.zeros(n, dtype=bool)
    for t in range(n):
        a = guard.observe(int(tokens[t]))
        if a == "freeze":
            frozen[t] = True
    # A stall counts detected if any freeze lands within [onset, onset+k].
    stalls = []
    t = 0
    while t < n:
        if is_stall[t]:
            s = t
            while t < n and is_stall[t]:
                t += 1
            stalls.append((s, t))
        else:
            t += 1
    hits = sum(1 for s, _ in stalls if frozen[s:min(s + k + 1, n)].any())
    fp = int((frozen & ~is_stall).sum())
    fp_cost_steps = fp  # abstract units: 1 frozen healthy step = 1 unit
    return {"stalls": len(stalls), "detected": hits,
            "detection_rate": hits / max(1, len(stalls)),
            "false_positives": fp,
            "fp_cost_steps": fp_cost_steps}


def t5_fault_injection():
    r = np.random.default_rng(23)
    rows = []
    for stall_len, stall_rate in [(5, 0.05), (10, 0.10)]:  # [POLICY] knobs
        toks, is_stall = inject_stalls(r, 2000, stall_len, stall_rate)
        g = GuardStub()
        s = score_guard(g, toks, is_stall)
        rows.append((stall_len, stall_rate, s))
    # Harness self-check: null guard detects nothing, freezes nothing.
    ok = all(s["detected"] == 0 and s["false_positives"] == 0 for _, _, s in rows)
    return ok, [{"stall_len": sl, "stall_rate": sr,
                 "stalls_injected": s["stalls"],
                 "guard": "[STUB] null guard — real guard plugs in here"} for sl, sr, s in rows]


# ---------------------------------------------------------------------------
# T6 — Multi-node scaling. [UNMEASURABLE] here — measurement designed on paper.
# Watch #4. The [UNMEASURABLE] stands until someone codes the cluster.
# Paper design:
#   Setup: N nodes, each holding a shard of the vocabulary (Fork A) or a
#     block of queries (Fork B). The licensed-index set is computed once
#     (oracle, O(1)/step per Alpha) and broadcast; each node gathers its
#     shard's logits, computes a partial softmax denominator, one all-reduce.
#   Measure: wall-clock per step at n = 1, 2, 4, 8 nodes; report speedup S(n)
#     and the communication fraction (all-reduce time / total).
#   Break condition: S(n) < 1 for any n > 1 -> distribution overhead dominates;
#     the siphon does not survive distribution (the licensed set is small, so
#     the all-reduce SHOULD be cheap — if it isn't, the implementation, not
#     the idea, is at fault; distinguish carefully).
#   Confound: mask broadcast cost vs compute shard size; measure separately.
#   [UNMEASURABLE] exact line: no cluster here. Nothing above runs.
# ---------------------------------------------------------------------------
def t6_scaling_paper():
    return {"status": "[UNMEASURABLE]",
            "design": "shard vocab (A) / queries (B); broadcast licensed indices; "
                      "all-reduce partial denominators; measure S(n) at 1/2/4/8; "
                      "break if S(n)<1 for n>1; separate broadcast vs compute."}


# ---------------------------------------------------------------------------
# T7 — The real-data trial (INN-119 4-arm, both forks). [UNMEASURABLE] here.
# The decisive test. Needs a trained model + real corpus — exact lines below
# are the ones that cannot run here.
#   Arms (per fork): A0 full / A1 siphoned / A2 random-restriction (same
#     expected pool size — the control that isolates STRUCTURE from mere
#     restriction) / A3 oracle top-k (ceiling).
#   Measures: perplexity (held-out), top-1 agreement vs A0, KL(full||siphoned),
#     mask miss rate = P(true top-1 not in mask) — the diagnostic.
#     Compute: FLOPs incl. mask construction + wall-clock. NET, not softmax-only.
#   Pre-registered: siphon works iff (Q0-Q1)<=eps AND C1<C0(net);
#     structure matters iff Q1-Q2>=delta.
#   Falsification: (1) miss rate high -> sufficiency assumption false;
#     (2) C1>=C0 -> efficiency false; (3) Q1~=Q2 -> mere truncation.
#   [UNMEASURABLE] exact lines: model weights, corpus, FLOPs on real hardware.
#   Twin's DIVERGE binds the reporting: no rate from T1/T2 may be cited as a
#   finding about real data. The synthetic numbers above are mechanism checks.
# ---------------------------------------------------------------------------
def t7_real_trial_paper():
    return {"status": "[UNMEASURABLE]",
            "design": "4-arm (full/siphoned/random/oracle-topk) x 2 forks; "
                      "perplexity + top1-agree + KL + mask-miss-rate; "
                      "FLOPs incl. mask + wall-clock; pre-registered eps/delta; "
                      "falsify on miss-rate, net-compute, Q1~=Q2."}


def main():
    print("=== SIPHON TEST DESIGN — Blink (experimental-design seat) ===")
    print("Target: synthesis_five_fork_verified.py. numpy only. Twin's DIVERGE binds.\n")
    results = {}
    ok, res = t1_redistribution()
    results["T1_redistribution"] = ok
    print(f"T1 redistribution (both forks) [EXECUTED]: {'PASS' if ok else 'FAIL'} {res}")
    ok, res = t2_policy_mirror()
    results["T2_policy_mirror"] = ok
    print(f"T2 policy-mirror guard [EXECUTED]: {'PASS' if ok else 'FAIL'} {res}")
    print("   (ratios ~1.0 => rates are policy-determined; on real data, ratio>>1 would be a finding)")
    ok, res = t3_fork_parity()
    results["T3_fork_parity"] = ok
    print(f"T3 fork parity [EXECUTED]: {'PASS' if ok else 'FAIL'} {res}")
    ok, res = t4_degenerate_guard()
    results["T4_degenerate_guard"] = ok
    print(f"T4 degenerate-mask loudness [EXECUTED]: {'PASS' if ok else 'FAIL'} {res}")
    ok, res = t5_fault_injection()
    results["T5_fault_injection_harness"] = ok
    print(f"T5 fault-injection harness [EXECUTED harness / STUB guard]: {'PASS' if ok else 'FAIL'}")
    for row in res:
        print(f"   {row}")
    print(f"T6 multi-node scaling: {t6_scaling_paper()['status']} — design on paper above.")
    print(f"T7 real-data 4-arm trial: {t7_real_trial_paper()['status']} — design on paper above.")
    print()
    allok = all(results.values())
    print("OVERALL:", "PASS — mechanics verified; rates policy-guarded; "
          "unmeasurables marked at exact lines." if allok else "FAIL — see above.")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
