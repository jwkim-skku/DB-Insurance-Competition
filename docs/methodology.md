# Methodology

## 1. Research design

The study separates two channels through which carbon transition risk may enter
the cost of debt:

```text
Carbon exposure → firm-value risk → structural default probability → debt cost
Carbon exposure ────────────────────────────────────────────────→ debt cost
```

The first channel is conventional credit-risk transmission. The second captures
an additional carbon premium after structural default risk is controlled for.

## 2. Structural default probability

Following Merton’s contingent-claims framework, equity is modeled as a call
option on firm assets:

```text
E = V·N(d1) − D·exp(−rT)·N(d2)
σE·E = N(d1)·σV·V

d1 = [ln(V/D) + (r + 0.5σV²)T] / (σV√T)
d2 = d1 − σV√T
PD = N(−d2)
```

Observed equity value, equity volatility, debt, and the risk-free rate are used
to solve simultaneously for asset value `V` and asset volatility `σV`.
`src/merton.py` performs this calibration in log space to keep both unknowns
positive.

## 3. Panel specification

The public workflow estimates:

```text
CostDebt_it =
  β1·LaggedPD_it
  + β2·CarbonIntensity_it
  + β3·Size_it
  + β4·Leverage_it
  + FirmFE_i
  + YearFE_t
  + ε_it
```

A second specification interacts lagged structural risk with standardized ESG:

```text
CostDebt_it =
  β1·LaggedPD_it
  + β2·ESG_it
  + β3·LaggedPD_it×ESG_it
  + controls + fixed effects + ε_it
```

Standard errors are clustered by firm. These estimates describe conditional
associations; they are not presented as a causal design.

## 4. SLL translation

The financing proposal converts the empirical framework into a transparent
margin ratchet.

Suggested KPI families:

- annual improvement in revenue-based carbon intensity;
- vessel-level Carbon Intensity Indicator (CII) performance;
- predefined reporting boundaries and calculation methods; and
- independent verification of KPI performance.

The margin grid shown in the portfolio is illustrative. Actual pricing should
be calibrated to borrower risk, tenor, fleet composition, KPI ambition, and
the lender’s credit policy.
