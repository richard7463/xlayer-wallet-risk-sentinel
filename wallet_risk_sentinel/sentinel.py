from __future__ import annotations

from decimal import Decimal
from typing import List

from .models import RiskFinding, RiskRequest, RiskResponse


class WalletRiskSentinel:
    def __init__(self, quote_provider=None):
        self.quote_provider = quote_provider

    def evaluate(self, request: RiskRequest) -> RiskResponse:
        findings: List[RiskFinding] = []
        risk_score = 0
        wallet = request.wallet

        reserve_after = wallet.stable_reserve_usd - request.amount_usd
        reserve_ratio_after = reserve_after / wallet.total_value_usd if wallet.total_value_usd > 0 else Decimal("0")
        order_share = request.amount_usd / wallet.total_value_usd if wallet.total_value_usd > 0 else Decimal("1")

        price_impact = self._price_impact(request)

        if reserve_after < 0:
            risk_score += 35
            findings.append(RiskFinding("high", "INSUFFICIENT_STABLE_RESERVE", "Trade exceeds the current stable reserve."))
        elif reserve_ratio_after < Decimal("0.10"):
            risk_score += 22
            findings.append(RiskFinding("high", "THIN_RESERVE", "Trade would leave the wallet with a dangerously thin stable reserve."))
        elif reserve_ratio_after < Decimal("0.18"):
            risk_score += 12
            findings.append(RiskFinding("medium", "LOW_RESERVE", "Trade would leave the wallet with a low stable reserve."))

        if wallet.largest_position_percent > Decimal("55"):
            risk_score += 18
            findings.append(RiskFinding("high", "OVER_CONCENTRATED", "Wallet is already over-concentrated before the proposed trade."))
        elif wallet.largest_position_percent > Decimal("40"):
            risk_score += 10
            findings.append(RiskFinding("medium", "CONCENTRATED", "Wallet concentration is elevated before this trade."))

        if order_share > Decimal("0.28"):
            risk_score += 18
            findings.append(RiskFinding("high", "ORDER_TOO_LARGE", "Trade size is too large relative to total wallet value."))
        elif order_share > Decimal("0.18"):
            risk_score += 10
            findings.append(RiskFinding("medium", "ORDER_LARGE", "Trade consumes a large share of the wallet."))

        if price_impact > Decimal("1.20"):
            risk_score += 20
            findings.append(RiskFinding("high", "HIGH_PRICE_IMPACT", "Quoted price impact is above the clean-execution threshold."))
        elif price_impact > Decimal("0.60"):
            risk_score += 10
            findings.append(RiskFinding("medium", "ELEVATED_PRICE_IMPACT", "Quoted price impact is elevated."))

        verdict, max_safe_trade = self._finalize(request, risk_score)
        summary = self._summary(verdict, max_safe_trade, findings)
        return RiskResponse(
            request=request,
            verdict=verdict,
            risk_score=min(risk_score, 100),
            max_safe_trade_usd=max_safe_trade,
            findings=findings,
            agent_summary=summary,
        )

    def _price_impact(self, request: RiskRequest) -> Decimal:
        if self.quote_provider is None:
            return Decimal("0.40")
        return Decimal(str(self.quote_provider(request)))

    @staticmethod
    def _finalize(request: RiskRequest, risk_score: int) -> tuple[str, Decimal]:
        if risk_score >= 55:
            return "block", (request.amount_usd * Decimal("0.35")).quantize(Decimal("0.01"))
        if risk_score >= 28:
            return "reduce", (request.amount_usd * Decimal("0.70")).quantize(Decimal("0.01"))
        return "allow", request.amount_usd.quantize(Decimal("0.01"))

    @staticmethod
    def _summary(verdict: str, max_safe_trade: Decimal, findings: List[RiskFinding]) -> str:
        if not findings:
            return f"Verdict: {verdict}. Wallet posture is clean enough for the proposed execution size."
        codes = ", ".join(finding.code for finding in findings)
        return f"Verdict: {verdict}. Cap execution at {max_safe_trade} USD. Primary risk signals: {codes}."
