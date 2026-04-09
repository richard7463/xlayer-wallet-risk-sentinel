---
name: xlayer-wallet-risk-sentinel
description: Use this skill when an agent needs to decide whether a proposed X Layer trade is safe for the current wallet, compute a capped safe size, or block execution with explicit risk reasons.
---

# X Layer Wallet Risk Sentinel

Use this skill to judge whether a proposed trade should be allowed for the current wallet posture.

## When to use it

- The caller wants a pre-trade wallet risk verdict.
- Another agent needs a reusable `allow / reduce / block` skill.
- The caller wants a maximum safe trade size.
- The caller wants explicit reasons when an execution should be blocked.

## Required capabilities

Use `OnchainOS` as the factual layer:

- `DEX token` for token resolution
- `DEX quote` for route and impact context
- wallet posture from an Agentic Wallet or upstream wallet skill

Do not invent wallet balances, quote impact, or warnings.

## Workflow

1. Extract:
   - proposed trade pair
   - trade amount
   - wallet total value
   - stable reserve
   - current concentration
2. Resolve token data on X Layer.
3. Fetch route-impact context.
4. Score the wallet on reserve safety, concentration, and impact.
5. Return exactly one verdict:
   - `allow`
   - `reduce`
   - `block`
6. Return the max safe size and the reasons.

## Fixed output

Always return these sections in order:

1. `Wallet posture`
2. `Proposed trade`
3. `Risk findings`
4. `Max safe size`
5. `Verdict`
6. `Agent-ready summary`
