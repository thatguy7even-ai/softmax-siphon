"""
Softmax-Siphon toy prototype — mother's grounding rig for the council project.
Ordered 2026-10-13. NOT a model of attention; a toy of the *essence*:
deterministic structural mask -> restricted candidate pool -> reduced softmax.

Question it answers first: is the siphon only faster, or is it a different model?
Question it cannot answer: where structural adjacency comes from, or what it costs.
"""
import numpy as np

rng = np.random.default_rng(7)

VOCAB = 16          # toy vocabulary size V
GROUP = 4           # phrase-group size: the toy's "structural adjacency"
SEEDS = 200

def full_softmax(logits):
    e = np.exp(logits - logits.max())
    return e / e.sum()

def structural_casket(vocab, group, pos):
    """Boolean mask: tokens structurally adjacent = same phrase group as pos."""
    mask = np.zeros(vocab, dtype=bool)
    start = (pos // group) * group
    mask[start:start + group] = True
    return mask

def siphon_softmax(logits, mask):
    restricted = logits[mask]
    e = np.exp(restricted - restricted.max())
    return e / e.sum()

def main():
    top1_agree = 0
    mass_captured = []
    l1_shift = []
    for s in range(SEEDS):
        r = np.random.default_rng(s)
        logits = r.normal(0, 2.0, VOCAB)
        pos = int(r.integers(0, VOCAB))
        mask = structural_casket(VOCAB, GROUP, pos)
        k = int(mask.sum())

        p_full = full_softmax(logits)
        p_siph = siphon_softmax(logits, mask)

        pool_idx = np.where(mask)[0]
        if pool_idx[int(np.argmax(p_siph))] == int(np.argmax(p_full)):
            top1_agree += 1
        mass_captured.append(float(p_full[mask].sum()))

        p_embed = np.zeros(VOCAB)
        p_embed[mask] = p_siph
        l1_shift.append(float(np.abs(p_full - p_embed).sum()))

        if s == 0:
            print(f"example seed 0: V={VOCAB}, pool k={k}, pos={pos}")
            print(f"  full softmax ops ~ O(V)={VOCAB}; siphoned ops ~ O(k)={k} "
                  f"-> {VOCAB/k:.1f}x fewer normalization terms")
            print(f"  full top-1 token: {int(np.argmax(p_full))} "
                  f"(p={p_full.max():.3f}); siphon top-1: {int(pool_idx[np.argmax(p_siph)])} "
                  f"(p={p_siph.max():.3f})")

    print(f"\nover {SEEDS} random trials:")
    print(f"  top-1 agreement: {top1_agree}/{SEEDS} ({100*top1_agree/SEEDS:.1f}%)")
    print(f"  mean probability mass captured by pool: {np.mean(mass_captured):.3f}")
    print(f"  mean L1 distribution shift (full vs siphoned): {np.mean(l1_shift):.3f}")
    print("\nreading: the siphon is cheaper AND a different model. "
          "Restriction redistributes mass; it does not approximate the full softmax.")
    print("unaccounted: cost of computing the structural mask itself (the casket).")

if __name__ == "__main__":
    main()
