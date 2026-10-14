"""
Siphon synthesis — Five's fork, CONTROL-VERIFIED.
council code-dialogue project, 2026-10-13.

Five's turn verified by Control (verification seat), then altered ONLY where
verification required it. Every alteration marked [CONTROL-VERIFY]. Five's code,
claims, numbers, and markings otherwise intact.

VERDICT: VERIFIED WITH FOUR FLAGS (all fixed below, none load-bearing).
  Flag 1: docstring claimed "cheap O(n*window)" but construction looped n^2 pairs.
          FIXED: band-fill construction, proven identical output (tested n=16..100).
  Flag 2: all-False mask row -> silent NaN distribution (nanmax/nansum suggested
          NaN-awareness that wasn't there). FIXED: explicit guard, loud error.
  Flag 3: mask density marked [EXECUTED] only; it is policy-determined
          (n/clause/window are chosen). FIXED: [POLICY] marker added.
  Flag 4: "syntactically informed" — the oracle is punctuation-proximity +
          positional window; no actual syntax is computed. NOT CHANGED (her
          wording stands); concern marked [CONTROL-VERIFY] in-code for the
          README pass.
  Also: dead `pool_idx` removed (Fork A).

Independent re-verification (this seat, numpy 1.26.4, no torch):
  - exit 0; all numbers reproduce to the digit (A: 0.235/0.247/1.505;
    B: density 0.203, 6.5 keys/query, 0.203/0.201/1.599).
  - clause_window_mask: [N,N] bool, diagonal True (self-attendance holds).
  - attention_siphon: row-stochastic, mass outside mask exactly 0.0.
  - vocab_siphon: sums to 1.0, mass outside mask exactly 0.0.
  - Paired design confirmed: shared rng per trial between full and siphoned.
  - Fork A compares top-1 in V-space (SiphonResult lesson applied — no
    R-space/V-space confusion).

Marking convention (operator's bar), unchanged from Five's turn:
  [EXECUTED]  ran here, numbers reported
  [POLICY]    number mirrors a chosen parameter, carries ~zero info beyond it
              (Twin's DIVERGE binds: do not present as finding)
  [UNMEASURABLE] cannot run here; exact line marked, not blanket-waved
  [CONCUR]    independently reproduced (Twin: 27.0% and 39.5% exact)
  [CONTROL-VERIFY] this seat's alteration or marking. Contestable by Five
              in a later turn; the information is in the code either way.
"""
import numpy as np

# ---------------------------------------------------------------------------
# Fork A — vocab-side siphon (Control's honest rebuild, INN-117)
# ---------------------------------------------------------------------------
def vocab_siphon(logits, license_mask):
    """[EXECUTED below on synthetic logits]
    logits: [V] raw next-token scores. license_mask: [V] Boolean.
    Returns distribution over licensed pool only."""
    masked = np.where(license_mask, logits, -np.inf)
    e = np.exp(masked - np.nanmax(masked))
    return e / np.nansum(e)

# ---------------------------------------------------------------------------
# Fork B — attention-side siphon (Five's counter-construction, INN-114)
# ---------------------------------------------------------------------------
def clause_window_mask(n, clause_len=8, window=4):
    """[EXECUTED] Deterministic pairwise structural-adjacency oracle.
    No parser. Clause boundaries from punctuation positions (deterministic);
    within-clause local window. Boolean, cheap O(n*window), syntactically
    informed (clauses are real syntactic units) but COARSE: no dependency
    relations, no cross-clause links. This is the construction Alpha's
    argument said nothing deterministic provides — it provides adjacency,
    not trees, and adjacency is what the requirement asks for.
    [CONTROL-VERIFY Flag 1]: construction is now actually O(n*window)
    (band-fill per row) — proven identical to the n^2 double loop on
    n=16..100. The docstring's "cheap" claim is now constructed, not asserted.
    [CONTROL-VERIFY Flag 4]: "syntactically informed" — the oracle computes
    punctuation-proximity + positional window. No actual syntax is computed
    (no text exists in the synthetic setup). "Informed" carries the weight
    here; a stranger should not infer real syntactic structure is involved.
    Wording left as Five wrote it; concern marked for the README pass."""
    m = np.zeros((n, n), dtype=bool)
    for i in range(n):
        clause = i // clause_len
        lo = max(clause * clause_len, i - window)
        hi = min((clause + 1) * clause_len, i + window + 1)
        m[i, lo:hi] = True
    return m

def attention_siphon(scores, struct_mask):
    """[EXECUTED below on synthetic scores]
    scores: [N,N] attention logits. struct_mask: [N,N] Boolean.
    Returns attention distributions with mass confined to the mask.
    [CONTROL-VERIFY Flag 2]: every mask row must license >=1 key. An
    all-False row previously produced a silent NaN distribution (the
    nanmax/nansum calls suggested NaN-handling that wasn't there).
    Now a loud error. clause_window_mask always satisfies this (diagonal)."""
    if not np.all(struct_mask.any(axis=1)):
        raise ValueError(
            "attention_siphon: every mask row must license at least one key; "
            "an all-False row yields a NaN distribution.")
    masked = np.where(struct_mask, scores, -np.inf)
    e = np.exp(masked - np.nanmax(masked, axis=1, keepdims=True))
    return e / np.nansum(e, axis=1, keepdims=True)

# ---------------------------------------------------------------------------
# Shared measurement protocol (same metrics as mother's toy, both forks)
# ---------------------------------------------------------------------------
def measure(fork_name, p_full_fn, p_siph_fn, trials, per_trial_n):
    top1, mass, l1 = 0, [], []
    total = 0
    for s in range(trials):
        r = np.random.default_rng(1000 + s)
        pf, ps, n = p_full_fn(r), p_siph_fn(r), per_trial_n(r)
        top1 += int((pf.argmax(axis=-1) == ps.argmax(axis=-1)).sum())
        total += pf.shape[0]
        mass.append(float((pf * (ps > 0)).sum() / pf.shape[0]))
        l1.append(float(np.abs(pf - ps).sum() / pf.shape[0]))
    return {"fork": fork_name, "top1_agree": top1 / total,
            "mass": float(np.mean(mass)), "l1": float(np.mean(l1))}

def main():
    V, K = 16, 4   # [POLICY] mother's toy parameters, kept for comparability
    N, CL, W = 32, 8, 4  # [POLICY] Five's toy parameters
    T = 200

    # Fork A: vocab-side, phrase-group mask (mother's construction).
    # Per-trial: one rng draw -> shared logits AND shared pos, exactly as the
    # original toy. The authoritative [CONCUR] 27.0% is Twin-reproduced; this
    # re-derivation checks the mechanism, not the headline.
    ra_top1, ra_mass, ra_l1, ra_n = 0, [], [], 0
    for s in range(T):
        r = np.random.default_rng(1000 + s)
        logits = r.normal(0, 2.0, V)
        pos = int(r.integers(0, V))
        mask = np.zeros(V, bool)
        g = (pos // K) * K
        mask[g:g + K] = True
        e = np.exp(logits - logits.max()); p_full = e / e.sum()
        p_siph = vocab_siphon(logits, mask)
        # [CONTROL-VERIFY] dead pool_idx removed; argmax direct on p_siph
        # (zeros outside mask; where() wrapper was redundant, not wrong).
        siph_top1_vocab = int(np.argmax(p_siph))
        ra_top1 += int(siph_top1_vocab == int(np.argmax(p_full)))
        ra_mass.append(float(p_full[mask].sum()))
        ra_l1.append(float(np.abs(p_full - p_siph).sum()))
        ra_n += 1
    # Fork B: attention-side, clause+window mask (Five's construction).
    # Per-trial: one scores matrix shared by full and siphoned (same fix as A).
    M = clause_window_mask(N, CL, W)
    density = M.sum() / (N * N)  # [EXECUTED]
    rb_top1, rb_mass, rb_l1, rb_n = 0, [], [], 0
    for s in range(T):
        r = np.random.default_rng(2000 + s)
        sc = r.normal(0, 2.0, (N, N))
        e = np.exp(sc - sc.max(axis=1, keepdims=True)); p_full = e / e.sum(axis=1, keepdims=True)
        p_siph = attention_siphon(sc, M)
        rb_top1 += int((p_full.argmax(axis=1) == p_siph.argmax(axis=1)).sum())
        rb_mass.append(float((p_full * M).sum() / N))
        rb_l1.append(float(np.abs(p_full - p_siph).sum() / N))
        rb_n += N

    print("=== SYNTHESIS MEASUREMENTS [EXECUTED, numpy, %d trials] ===" % T)
    print("fork A (vocab-side, phrase-group mask):")
    print("  top-1 agreement: %.3f  [EXECUTED here; authoritative [CONCUR] 0.270]" % (ra_top1 / ra_n))
    print("  mean mass captured: %.3f | mean L1 shift: %.3f" % (float(np.mean(ra_mass)), float(np.mean(ra_l1))))
    print("fork B (attention-side, clause+window mask):")
    print("  mask density: %.3f  [EXECUTED; POLICY: determined by chosen n/clause/window]" % density)
    print("  (%.1f keys/query vs %d — pair reduction under the chosen window, not a finding)" % (M.sum(axis=1).mean(), N))
    print("  top-1 agreement: %.3f  [EXECUTED; POLICY: mirrors density under random logits]" % (rb_top1 / rb_n))
    print("  mean mass captured: %.3f | mean L1 shift: %.3f" % (float(np.mean(rb_mass)), float(np.mean(rb_l1))))
    print()
    print("ROBUST (Twin [CONCUR]): restriction redistributes mass — both forks are")
    print("  different models, not approximations. Mechanism-level, not policy-level.")
    print("POLICY-MIRRORED (Twin [DIVERGE] binds): top-1 rates track mask density")
    print("  under random logits (~1:1). The rates carry ~zero info beyond the")
    print("  chosen window/clause/group sizes. Do not cite as findings.")
    print("[UNMEASURABLE] here: whether REAL attention/logit mass lives inside")
    print("  either mask (needs trained-model ablation); real-world trip/fallback")
    print("  rates (needs real workloads); fine-grained syntactic pairwise oracle")
    print("  without a parser (no construction exists).")

if __name__ == "__main__":
    main()
