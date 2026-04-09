from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from decimal import Decimal

from .models import RiskRequest, WalletSnapshot
from .sentinel import WalletRiskSentinel


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="X Layer Wallet Risk Sentinel CLI")
    parser.add_argument("--from-token", required=True)
    parser.add_argument("--to-token", required=True)
    parser.add_argument("--amount", required=True)
    parser.add_argument("--wallet-value", required=True)
    parser.add_argument("--stable-reserve", required=True)
    parser.add_argument("--largest-position-pct", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    request = RiskRequest(
        from_token=args.from_token,
        to_token=args.to_token,
        amount_usd=Decimal(args.amount),
        wallet=WalletSnapshot(
            total_value_usd=Decimal(args.wallet_value),
            stable_reserve_usd=Decimal(args.stable_reserve),
            largest_position_percent=Decimal(args.largest_position_pct),
        ),
    )
    response = WalletRiskSentinel().evaluate(request)
    print(json.dumps(asdict(response), indent=2, default=str))


if __name__ == "__main__":
    main()
