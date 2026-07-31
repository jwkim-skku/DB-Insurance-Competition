# Reproducibility and limitations

## Public workflow

The repository makes the model logic inspectable without publishing restricted
records:

1. regenerate the synthetic panel;
2. calibrate a Merton probability for every firm-year;
3. create lagged risk and standardized carbon/ESG measures;
4. estimate firm/year fixed-effects models with clustered errors; and
5. regenerate the figures used by the GitHub Pages portfolio.

The synthetic generator uses a fixed seed, so committed results should be
stable up to small numerical differences between library versions.

## Deliberate exclusions

The repository excludes:

- vendor datasets and identifiers that could facilitate reconstruction;
- application receipts and personal contact details;
- third-party articles, prior competition papers, and manuals;
- copyrighted audio and transcripts; and
- exploratory datasets unrelated to the final shipping-finance design.

## Interpretation limits

- Carbon and ESG coverage is substantially smaller than the accounting panel.
- A descriptive slope need not match a within-firm fixed-effects coefficient.
- Structural PD is model-dependent and sensitive to the debt boundary,
  volatility window, risk-free rate, and horizon.
- An SLL margin ratchet is a product-design illustration, not a quoted lending
  offer.
- The public synthetic results demonstrate the workflow and must not be cited
  as the competition manuscript’s empirical estimates.

## Restricted rerun checklist

An authorized rerun should pin the vendor query dates, preserve raw-to-clean
crosswalks, record unit conversions, validate ISIN-year joins, report winsor and
clipping rules, and export a machine-readable regression table alongside the
manuscript.
