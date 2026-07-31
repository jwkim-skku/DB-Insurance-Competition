"""Run the public fixed-effects demonstration and regenerate portfolio charts."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample_shipping_panel.csv"
OUTPUT_DIR = ROOT / "outputs"
ASSET_DIR = ROOT / "site" / "assets"

INK = "#102A2E"
TEAL = "#0B6B62"
MINT = "#90C9B9"
ORANGE = "#CB7B43"
SAND = "#F3EBDD"
SLATE = "#607074"
PAPER = "#FBFAF6"


def zscore(series: pd.Series) -> pd.Series:
    deviation = series.std(ddof=0)
    if deviation == 0 or not np.isfinite(deviation):
        raise ValueError(f"Cannot standardize {series.name}: zero or invalid variance")
    return (series - series.mean()) / deviation


def prepare_panel(path: Path = DATA_PATH) -> pd.DataFrame:
    panel = pd.read_csv(path).sort_values(["firm_id", "year"]).copy()
    panel["size"] = np.log(panel["total_assets"])
    panel["leverage"] = panel["total_debt"] / panel["total_assets"]
    panel["log_carbon"] = np.log(panel["carbon_intensity"])
    panel["lag_pd"] = panel.groupby("firm_id")["pd_merton"].shift(1)
    panel = panel.dropna(subset=["lag_pd"]).copy()
    panel["lag_pd_z"] = zscore(panel["lag_pd"])
    panel["carbon_z"] = zscore(panel["log_carbon"])
    panel["esg_z"] = zscore(panel["esg_score"])
    return panel


def fit_models(panel: pd.DataFrame) -> dict[str, object]:
    cluster = {"groups": panel["firm_id"]}
    common = "size + leverage + C(firm_id) + C(year)"
    models = {
        "credit_risk": smf.ols(
            f"cost_of_debt ~ lag_pd_z + {common}", data=panel
        ).fit(cov_type="cluster", cov_kwds=cluster),
        "dual_pricing": smf.ols(
            f"cost_of_debt ~ lag_pd_z + carbon_z + {common}", data=panel
        ).fit(cov_type="cluster", cov_kwds=cluster),
        "esg_moderation": smf.ols(
            f"cost_of_debt ~ lag_pd_z * esg_z + carbon_z + {common}", data=panel
        ).fit(cov_type="cluster", cov_kwds=cluster),
    }
    return models


def tidy_key_results(models: dict[str, object]) -> pd.DataFrame:
    rows: list[dict[str, float | str | int]] = []
    terms = ["lag_pd_z", "carbon_z", "esg_z", "lag_pd_z:esg_z"]
    for model_name, result in models.items():
        confidence = result.conf_int()
        for term in terms:
            if term not in result.params:
                continue
            rows.append(
                {
                    "model": model_name,
                    "term": term,
                    "estimate_bp": result.params[term] * 10_000,
                    "ci_low_bp": confidence.loc[term, 0] * 10_000,
                    "ci_high_bp": confidence.loc[term, 1] * 10_000,
                    "p_value": result.pvalues[term],
                    "observations": int(result.nobs),
                    "r_squared": result.rsquared,
                }
            )
    return pd.DataFrame(rows)


def _style_axes(ax: plt.Axes) -> None:
    ax.set_facecolor(PAPER)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#C9CEC8")
    ax.tick_params(colors=SLATE, labelsize=9)
    ax.grid(axis="y", color="#E4E5DF", linewidth=0.8, zorder=0)


def plot_dual_pricing(models: dict[str, object]) -> None:
    result = models["dual_pricing"]
    terms = ["lag_pd_z", "carbon_z"]
    labels = ["Lagged structural risk", "Carbon intensity"]
    estimates = np.array([result.params[t] * 10_000 for t in terms])
    confidence = result.conf_int().loc[terms].to_numpy() * 10_000
    errors = np.vstack(
        [estimates - confidence[:, 0], confidence[:, 1] - estimates]
    )

    fig, ax = plt.subplots(figsize=(8.4, 4.6), facecolor=PAPER)
    _style_axes(ax)
    ax.grid(False)
    ax.axvline(0, color="#AEB6B3", linewidth=1.2, zorder=1)
    positions = np.arange(len(terms))[::-1]
    ax.errorbar(
        estimates,
        positions,
        xerr=errors,
        fmt="o",
        markersize=9,
        color=TEAL,
        ecolor=MINT,
        elinewidth=5,
        capsize=0,
        zorder=3,
    )
    ax.set_yticks(positions, labels)
    ax.set_xlabel("Estimated change in cost of debt (basis points per 1 SD)")
    ax.set_title(
        "Public sample: conditional risk estimates",
        loc="left",
        fontsize=16,
        fontweight="bold",
        color=INK,
        pad=18,
    )
    ax.text(
        0,
        -0.33,
        "Firm and year fixed effects · firm-clustered 95% confidence intervals",
        transform=ax.transAxes,
        fontsize=9,
        color=SLATE,
    )
    fig.tight_layout(pad=2)
    fig.savefig(ASSET_DIR / "dual-pricing.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_sample_panel(panel: pd.DataFrame) -> None:
    annual = (
        panel.groupby("year", as_index=False)
        .agg(cost_of_debt=("cost_of_debt", "mean"), pd_merton=("pd_merton", "mean"))
        .copy()
    )
    annual["cost_bp"] = annual["cost_of_debt"] * 10_000
    annual["pd_pct"] = annual["pd_merton"] * 100

    fig, ax = plt.subplots(figsize=(9.2, 5.2), facecolor=PAPER)
    _style_axes(ax)
    ax.plot(
        annual["year"],
        annual["cost_bp"],
        color=TEAL,
        linewidth=2.8,
        marker="o",
        label="Mean cost of debt",
    )
    ax.set_ylabel("Cost of debt (basis points)", color=TEAL)
    ax.set_xlabel("Fiscal year")
    ax.set_xticks(annual["year"])

    second = ax.twinx()
    second.plot(
        annual["year"],
        annual["pd_pct"],
        color=ORANGE,
        linewidth=2.3,
        marker="s",
        label="Mean Merton PD",
    )
    second.set_ylabel("Merton probability (%)", color=ORANGE)
    second.spines["top"].set_visible(False)
    second.spines["right"].set_color("#C9CEC8")
    second.tick_params(colors=SLATE, labelsize=9)
    ax.set_title(
        "Synthetic panel: annual risk and funding conditions",
        loc="left",
        fontsize=16,
        fontweight="bold",
        color=INK,
        pad=18,
    )
    ax.text(
        0,
        -0.22,
        "Illustrative public data · 12 fictional firms · not submitted-study estimates",
        transform=ax.transAxes,
        fontsize=9,
        color=SLATE,
    )
    fig.tight_layout(pad=2)
    fig.savefig(ASSET_DIR / "sample-panel.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_sll_grid() -> None:
    improvement = np.array([0, 5, 10, 15, 20])
    margin = np.array([5, 0, -5, -10, -15])

    fig, ax = plt.subplots(figsize=(8.6, 4.8), facecolor=PAPER)
    _style_axes(ax)
    ax.axhline(0, color="#AEB6B3", linewidth=1.1)
    ax.plot(
        improvement,
        margin,
        color=TEAL,
        linewidth=3,
        marker="o",
        markersize=8,
    )
    ax.fill_between(improvement, margin, 0, color=MINT, alpha=0.24)
    for x, y in zip(improvement, margin, strict=True):
        label = f"{y:+d} bp" if y else "0 bp"
        offset = (-8, -16) if x == improvement[-1] else (0, 12 if y >= 0 else -19)
        alignment = "right" if x == improvement[-1] else "center"
        ax.annotate(
            label,
            (x, y),
            xytext=offset,
            textcoords="offset points",
            ha=alignment,
            fontsize=9,
            color=INK,
            fontweight="bold",
        )
    ax.set_xticks(improvement)
    ax.set_xlabel("Annual carbon-intensity improvement (%)")
    ax.set_ylabel("Illustrative margin adjustment")
    ax.set_title(
        "A transparent KPI-linked margin ratchet",
        loc="left",
        fontsize=16,
        fontweight="bold",
        color=INK,
        pad=18,
    )
    ax.text(
        0,
        -0.24,
        "Illustration only · final calibration depends on credit terms and KPI ambition",
        transform=ax.transAxes,
        fontsize=9,
        color=SLATE,
    )
    fig.tight_layout(pad=2)
    fig.savefig(ASSET_DIR / "sll-grid.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_social_card() -> None:
    fig = plt.figure(figsize=(12, 6.3), facecolor=INK)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.add_patch(
        plt.Rectangle((0.055, 0.09), 0.012, 0.82, transform=ax.transAxes, color=ORANGE)
    )
    ax.text(
        0.1,
        0.74,
        "CARBON RISK,\nPRICED TWICE",
        transform=ax.transAxes,
        color="#F8F4EA",
        fontsize=41,
        fontweight="bold",
        va="top",
        linespacing=0.93,
    )
    ax.text(
        0.1,
        0.30,
        "Shipping credit risk · Merton PD · SLL design",
        transform=ax.transAxes,
        color=MINT,
        fontsize=17,
        va="center",
    )
    ax.text(
        0.1,
        0.15,
        "DB Insurance & Finance Competition · Portfolio Edition",
        transform=ax.transAxes,
        color="#C7D1CF",
        fontsize=12,
        va="center",
    )
    for center, radius, color, alpha in [
        ((0.83, 0.72), 0.14, TEAL, 1.0),
        ((0.74, 0.45), 0.095, ORANGE, 0.9),
        ((0.88, 0.35), 0.18, MINT, 0.22),
    ]:
        ax.add_patch(
            plt.Circle(center, radius, transform=ax.transAxes, color=color, alpha=alpha)
        )
    fig.savefig(ASSET_DIR / "og-card.png", dpi=120, facecolor=INK)
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    panel = prepare_panel()
    models = fit_models(panel)
    results = tidy_key_results(models)
    results.to_csv(
        OUTPUT_DIR / "public_sample_results.csv",
        index=False,
        float_format="%.6f",
    )

    plot_dual_pricing(models)
    plot_sample_panel(panel)
    plot_sll_grid()
    plot_social_card()

    print(results.to_string(index=False, float_format=lambda value: f"{value:.4f}"))


if __name__ == "__main__":
    main()
