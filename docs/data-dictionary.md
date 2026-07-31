# Data dictionary

| Field | Unit | Description |
|---|---:|---|
| `firm_id` | — | Fictional public-sample firm identifier |
| `year` | year | Fiscal year |
| `total_assets` | USD million | Book assets |
| `total_debt` | USD million | Interest-bearing debt proxy |
| `market_cap` | USD million | Average equity market value |
| `equity_volatility` | decimal | Annualized equity-return volatility |
| `risk_free_rate` | decimal | Annual risk-free rate |
| `esg_score` | 0–100 | Composite ESG score |
| `carbon_intensity` | tCO₂e / USDm revenue | Revenue-based emissions intensity |
| `interest_expense` | USD million | Annual interest expense |
| `cost_of_debt` | decimal | Interest expense divided by debt |
| `pd_merton` | decimal | One-year Merton default probability |
| `distance_to_default` | standard deviations | Structural distance to default |

## Engineered fields

| Field | Definition |
|---|---|
| `size` | Natural log of total assets |
| `leverage` | Total debt divided by total assets |
| `log_carbon` | Natural log of carbon intensity |
| `lag_pd` | Prior-year Merton probability within firm |
| `lag_pd_z` | Standardized lagged probability |
| `carbon_z` | Standardized log carbon intensity |
| `esg_z` | Standardized ESG score |
