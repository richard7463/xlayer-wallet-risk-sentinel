# X Layer Wallet Risk Sentinel

Reusable pre-trade risk skill for X Layer agents.

`X Layer Wallet Risk Sentinel` is built for the **OKX Build X Hackathon Skills Arena**.
It helps any agent decide whether a wallet should execute a proposed trade, reduce the order size, or block the action entirely.

## One-Line Pitch

Give any agent a wallet state plus a proposed X Layer trade and Wallet Risk Sentinel returns a risk score, size cap, key warnings, and a final `allow / reduce / block` verdict.

## Why This Fits Skills Arena

This project is a reusable decision skill, not a product shell.

Its job is narrow and valuable:

- inspect wallet concentration and cash reserve
- inspect route impact and execution size
- translate raw state into a risk verdict
- give another agent a safe execution boundary

## Project Intro

Most agents can generate trade ideas. Fewer agents can decide whether they should touch the wallet at all.

Wallet Risk Sentinel exists to answer the question before execution:

- is this trade safe enough for the current wallet?
- if not, how much should the size be reduced?
- what exact risk caused the block?

## Architecture Overview

There are four layers:

1. `wallet_risk_sentinel.client.OnchainOSClient`
   - token and quote access through OnchainOS DEX surfaces
   - pluggable wallet snapshot provider

2. `wallet_risk_sentinel.sentinel.WalletRiskSentinel`
   - evaluates wallet posture against a proposed trade
   - computes concentration, reserve, and impact warnings
   - returns a risk verdict

3. `wallet_risk_sentinel.models`
   - typed request, wallet snapshot, and result models

4. `wallet_risk_sentinel.cli`
   - local CLI for demos and reproducible screenshots

## Onchain OS / Uniswap Skill Usage

Current code is designed around:

- wallet posture input from an Agentic Wallet or upstream wallet skill
- quote and route-impact context from OnchainOS DEX APIs
- token resolution on X Layer

Another agent can call Wallet Risk Sentinel before handing the order to an execution skill.

## Working Mechanics

1. An agent provides a proposed trade plus wallet state.
2. Wallet Risk Sentinel resolves token and route context.
3. It measures concentration, stable reserve, order share, and price impact.
4. It emits warnings and a capped safe size.
5. It returns one final verdict:
   - `allow`
   - `reduce`
   - `block`

## Example Output

```json
{
  "verdict": "reduce",
  "risk_score": 62,
  "max_safe_trade_usd": "18.00",
  "warnings": [
    "Trade consumes too much of the wallet's stable reserve.",
    "Quoted price impact is above the clean-execution threshold."
  ]
}
```

## Local Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 -m wallet_risk_sentinel.cli \
  --from-token USDC \
  --to-token OKB \
  --amount 25 \
  --wallet-value 120 \
  --stable-reserve 35 \
  --largest-position-pct 42
```

## Environment Variables

- `ONCHAINOS_API_KEY`
- `ONCHAINOS_API_SECRET`
- `ONCHAINOS_API_PASSPHRASE`
- `ONCHAINOS_CHAIN_INDEX=196`
- `ONCHAINOS_PROXY=http://127.0.0.1:7890`

## Submission Positioning

This repo belongs in the **Skills Arena**.

Why:

- it is a reusable pre-trade risk layer
- any treasury, trading, or bounty agent can call it
- it turns wallet state plus quote data into a decision object

## Team

- `richard7463` - solo builder

## Status

Already done:

- standalone repo structure
- reusable skill spec
- risk scoring engine
- CLI demo surface
- Skills Arena docs

Still required:

- live OnchainOS credentials for real quote validation
- optional Agentic Wallet state wiring
- Moltbook submission post
- demo video

## Docs

- [Skill Spec](/Users/yanqing/Documents/GitHub/miraix-interface/projects/xlayer-wallet-risk-sentinel/SKILL.md)
- [Project Positioning](/Users/yanqing/Documents/GitHub/miraix-interface/projects/xlayer-wallet-risk-sentinel/docs/project-positioning.md)
- [Skills Arena Checklist](/Users/yanqing/Documents/GitHub/miraix-interface/projects/xlayer-wallet-risk-sentinel/docs/skills-arena-checklist.md)
