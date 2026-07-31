"""Generate a deterministic, fully synthetic shipping-firm panel."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.merton import calibrate_merton  # noqa: E402


def main() -> None:
    rng = np.random.default_rng(20260227)
    rows: list[dict[str, float | int | str]] = []

    for firm_number in range(1, 13):
        firm_id = f"SHIP-{firm_number:02d}"
        scale = rng.uniform(900.0, 4_800.0)
        debt_ratio = rng.uniform(0.32, 0.68)
        baseline_carbon = rng.uniform(260.0, 1_150.0)
        baseline_esg = rng.uniform(37.0, 66.0)
        firm_spread = rng.normal(0.0, 0.003)
        previous_pd = 0.02

        for year in range(2016, 2026):
            time = year - 2016
            assets = scale * np.exp(0.025 * time + rng.normal(0.0, 0.08))
            leverage = np.clip(
                debt_ratio + 0.025 * np.sin(time / 2) + rng.normal(0.0, 0.035),
                0.22,
                0.78,
            )
            debt = assets * leverage
            market_cap = max(
                assets * (1.0 - leverage) * np.exp(rng.normal(0.0, 0.18)), 80.0
            )
            equity_vol = np.clip(
                0.28 + 0.55 * leverage + rng.normal(0.0, 0.07), 0.22, 0.88
            )
            risk_free = np.clip(
                0.014 + 0.006 * np.sin(time / 1.8) + rng.normal(0.0, 0.0025),
                0.004,
                0.04,
            )
            esg = np.clip(
                baseline_esg + 1.25 * time + rng.normal(0.0, 2.8), 25.0, 88.0
            )
            carbon = np.clip(
                baseline_carbon
                * np.exp(-0.028 * time)
                * np.exp(rng.normal(0.0, 0.09)),
                90.0,
                1_500.0,
            )

            merton = calibrate_merton(
                equity_value=market_cap,
                debt=debt,
                equity_volatility=equity_vol,
                risk_free_rate=risk_free,
            )

            carbon_scaled = (np.log(carbon) - np.log(520.0))
            esg_buffer = (esg - 55.0) / 20.0
            cost_of_debt = np.clip(
                0.024
                + firm_spread
                + 0.065 * previous_pd
                + 0.0028 * carbon_scaled
                - 0.0045 * previous_pd * esg_buffer
                + 0.18 * risk_free
                + rng.normal(0.0, 0.0022),
                0.008,
                0.13,
            )
            interest_expense = debt * cost_of_debt

            rows.append(
                {
                    "firm_id": firm_id,
                    "year": year,
                    "total_assets": round(assets, 4),
                    "total_debt": round(debt, 4),
                    "market_cap": round(market_cap, 4),
                    "equity_volatility": round(equity_vol, 6),
                    "risk_free_rate": round(risk_free, 6),
                    "esg_score": round(esg, 4),
                    "carbon_intensity": round(carbon, 4),
                    "interest_expense": round(interest_expense, 4),
                    "cost_of_debt": round(cost_of_debt, 8),
                    "pd_merton": round(merton.default_probability, 10),
                    "distance_to_default": round(merton.distance_to_default, 8),
                }
            )
            previous_pd = merton.default_probability

    frame = pd.DataFrame(rows)
    destination = ROOT / "data" / "sample_shipping_panel.csv"
    destination.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(destination, index=False)
    print(f"Wrote {len(frame)} synthetic firm-year rows to {destination}")


if __name__ == "__main__":
    main()
