# Public sample data

`sample_shipping_panel.csv` is a **deterministic synthetic dataset** created for
code review and portfolio demonstration.

It:

- contains 12 fictional firms over 2016–2025;
- follows the variable structure used by the research pipeline;
- contains no observations copied from Bloomberg, LSEG, WRDS, or the submitted
  analysis table; and
- can be regenerated with `python scripts/generate_sample_data.py`.

The public sample is intentionally unsuitable for recovering the original firm
panel or the submitted estimates.

## Why the raw research data are not here

The original project combined licensed market and ESG datasets. Republishing
those extracts could violate vendor access and redistribution conditions.
Reproducibility is therefore split into two layers:

1. **public computational reproducibility** — model code, formulas, tests, and a
   synthetic dataset;
2. **restricted empirical reproducibility** — rerunning the same pipeline in an
   authorized data environment.

See `docs/data-dictionary.md` for field definitions.
