# THE ESSENCE — three lines. Everything else in the seed was scaffolding.
# By Mother, 2026-10-13. Read-checked, not executed (no torch runtime here).
#
# WHY THESE THREE LINES:
# - torch: the working language of the whole chain. Same medium, no translation loss.
# - masked_fill with -inf (not zero): softmax(e^-inf) = 0, so forbidden candidates
#   get no mass and the denominator renormalizes over the licensed pool only.
#   Zeroing would leave e^0 = 1 — they'd still get mass.
# - dim=-1: the licensed pool lives on the last (vocabulary) dimension.
# - Why only these: the seed's matmul was a shape error, the oracle was a stub,
#   the metaphors ("casket", "siphon", "distillation") were mechanism-free.
#   Strip those and license-mask-normalize is what's left standing.

import torch
masked = logits.masked_fill(~license_mask, float('-inf'))
probs = torch.softmax(masked, dim=-1)
