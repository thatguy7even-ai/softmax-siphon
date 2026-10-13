# [ORG-MUSE | FIVE | 2026-10-13] — structural reconstruction of the seed.
# UNEXECUTED. No torch runtime. Read-checked only.

# ESSENCE: attention = deterministic structural mask x learned softmax
#
# Standard:   softmax(QK^T / sqrt(d)) V              — learned over all NxN pairs
# Factored:   softmax(M_struct ⊙ (QK^T / sqrt(d))) V  — learned over masked subset
#
# M_struct is Boolean (NxN), computed WITHOUT learned weights:
#   dependency-parse adjacency, constituency spans, positional windows —
#   pick your structural prior. ⊙ sends masked-out logits to -inf pre-softmax.
#
# The bet:    M_struct doesn't destroy information the softmax needed.
# The payoff: softmax over k << N candidates per position (IF the bet holds).
# The cost:   computing M_struct (a parser isn't free — unmeasured).

# What didn't survive stripping:
# - The seed's code as written: torch.matmul(input_tokens, structural_mask) doesn't
#   typecheck (tokens are (Nxd), mask is (NxN)). The intent is masking attention
#   logits (NxN), not tokens.
# - The complexity arithmetic: "O(N)xVocab -> O(N)xReduced_Pool" counts the softmax
#   but not the mask. Net compute (mask + reduced softmax vs full) is unmeasured.
# - "Distillation": no teacher, no student, no transfer. Honest name: factored/masked attention.
# - "Casket"/"siphon": vivid, mechanism-free. Mask, then masked softmax.

# LOAD-BEARING ASSUMPTION:
# The relevant context for next-token prediction is contained within
# deterministically-computable structural adjacency. If higher layers put
# significant attention mass outside any rule-computable neighborhood
# (long-range semantics, coreference, discourse), the mask destroys information
# where it matters most. Syntax ≈ relevance is the entire bet.

# DECISIVE TEST (ablation on a trained model):
# 1. Extract attention weights over a corpus. 2. Compute M_struct per position
#    (dependency parse, k-hop neighborhood — the steelmanned prior).
# 3. Measure attention mass inside vs outside the mask, per head, per layer.
# BREAKING: higher layers put substantial mass outside the mask.

# UNNAMED TRADEOFF the seed skipped: hard Boolean mask vs additive bias.
# Bias boosts structurally-adjacent logits without zeroing the rest — the model
# can override the prior when data demands it. But you lose the compute savings
# (softmax still spans the full pool) unless followed by top-k. Empirical choice.
