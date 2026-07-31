"""Merton structural credit-risk calibration.

The implementation solves for unobserved asset value and asset volatility from
observed equity value and equity volatility. Monetary inputs may use any common
unit as long as equity value and debt use the same unit.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import least_squares
from scipy.stats import norm


@dataclass(frozen=True)
class MertonResult:
    asset_value: float
    asset_volatility: float
    distance_to_default: float
    default_probability: float
    converged: bool


def _validate_positive(name: str, value: float) -> None:
    if not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite positive number")


def calibrate_merton(
    equity_value: float,
    debt: float,
    equity_volatility: float,
    risk_free_rate: float,
    horizon: float = 1.0,
) -> MertonResult:
    """Calibrate a one-period Merton model.

    Parameters
    ----------
    equity_value:
        Market value of equity.
    debt:
        Default boundary or debt proxy.
    equity_volatility:
        Annualized equity volatility as a decimal.
    risk_free_rate:
        Continuously compounded annual risk-free rate as a decimal.
    horizon:
        Model horizon in years.
    """

    _validate_positive("equity_value", equity_value)
    _validate_positive("debt", debt)
    _validate_positive("equity_volatility", equity_volatility)
    _validate_positive("horizon", horizon)
    if not np.isfinite(risk_free_rate):
        raise ValueError("risk_free_rate must be finite")

    initial_asset = equity_value + debt * np.exp(-risk_free_rate * horizon)
    initial_asset_vol = max(equity_volatility * equity_value / initial_asset, 1e-4)

    def residual(log_parameters: np.ndarray) -> np.ndarray:
        asset_value, asset_vol = np.exp(log_parameters)
        root_t = np.sqrt(horizon)
        d1 = (
            np.log(asset_value / debt)
            + (risk_free_rate + 0.5 * asset_vol**2) * horizon
        ) / (asset_vol * root_t)
        d2 = d1 - asset_vol * root_t

        modeled_equity = (
            asset_value * norm.cdf(d1)
            - debt * np.exp(-risk_free_rate * horizon) * norm.cdf(d2)
        )
        modeled_equity_vol = (
            norm.cdf(d1) * asset_vol * asset_value / equity_value
        )

        return np.array(
            [
                (modeled_equity - equity_value) / equity_value,
                (modeled_equity_vol - equity_volatility) / equity_volatility,
            ]
        )

    solution = least_squares(
        residual,
        np.log([initial_asset, initial_asset_vol]),
        bounds=(np.log([1e-8, 1e-6]), np.log([1e12, 10.0])),
        xtol=1e-12,
        ftol=1e-12,
        gtol=1e-12,
        max_nfev=2_000,
    )
    asset_value, asset_vol = np.exp(solution.x)
    root_t = np.sqrt(horizon)
    d1 = (
        np.log(asset_value / debt)
        + (risk_free_rate + 0.5 * asset_vol**2) * horizon
    ) / (asset_vol * root_t)
    d2 = d1 - asset_vol * root_t

    return MertonResult(
        asset_value=float(asset_value),
        asset_volatility=float(asset_vol),
        distance_to_default=float(d2),
        default_probability=float(norm.cdf(-d2)),
        converged=bool(solution.success and np.linalg.norm(solution.fun) < 1e-6),
    )
