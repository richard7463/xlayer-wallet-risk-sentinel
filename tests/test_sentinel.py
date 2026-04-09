from decimal import Decimal

from wallet_risk_sentinel.models import RiskRequest, WalletSnapshot
from wallet_risk_sentinel.sentinel import WalletRiskSentinel


def test_reduce_when_wallet_reserve_and_size_are_stressed():
    request = RiskRequest(
        from_token="USDC",
        to_token="OKB",
        amount_usd=Decimal("25"),
        wallet=WalletSnapshot(
            total_value_usd=Decimal("120"),
            stable_reserve_usd=Decimal("35"),
            largest_position_percent=Decimal("42"),
        ),
    )
    response = WalletRiskSentinel(lambda _: Decimal("0.75")).evaluate(request)
    assert response.verdict == "reduce"
    assert response.risk_score >= 28
    assert response.max_safe_trade_usd == Decimal("17.50")
