from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import List


@dataclass(frozen=True)
class WalletSnapshot:
    total_value_usd: Decimal
    stable_reserve_usd: Decimal
    largest_position_percent: Decimal


@dataclass(frozen=True)
class RiskRequest:
    from_token: str
    to_token: str
    amount_usd: Decimal
    wallet: WalletSnapshot


@dataclass(frozen=True)
class RiskFinding:
    severity: str
    code: str
    message: str


@dataclass(frozen=True)
class RiskResponse:
    request: RiskRequest
    verdict: str
    risk_score: int
    max_safe_trade_usd: Decimal
    findings: List[RiskFinding] = field(default_factory=list)
    agent_summary: str = ""
