# Carbon Risk, Priced Twice

> A portfolio edition of **“The Dual Pricing Structure of Carbon Regulatory Risk:<br>
> An Empirical Analysis of Shipping Firms’ Cost of Capital and an SLL Design.”**

[![Portfolio](https://img.shields.io/badge/GitHub%20Pages-Portfolio-0B6B62?style=flat-square)](https://jwkim-skku.github.io/DB-Insurance-Competition/)
[![Python](https://img.shields.io/badge/Python-3.11+-1B3A4B?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Data](https://img.shields.io/badge/Public%20data-Synthetic-CB7B43?style=flat-square)](data/README.md)
[![License](https://img.shields.io/badge/Code-MIT-5D6470?style=flat-square)](LICENSE)

## Project at a glance

This research asks whether the debt market prices a shipping company’s carbon
regulatory exposure only through conventional credit risk, or whether carbon
intensity carries an additional premium of its own.

The submitted study built a 2016–2025 global shipping panel and combined:

- a **Merton structural default probability** derived from balance-sheet and
  market information;
- corporate **cost of debt**;
- revenue-based **carbon intensity** and ESG scores; and
- firm and year fixed effects with firm-clustered standard errors.

The central interpretation is a **dual-pricing channel**:

1. carbon transition risk can weaken firm value and increase structural default
   risk; and
2. lenders may additionally price carbon exposure that is not fully summarized
   by the default-risk measure.

The financing application is a **Carbon Risk-Responsive Sustainability-Linked
Loan (SLL)** that links a margin ratchet to both carbon-intensity improvement
and vessel-level CII performance.

| Research panel | Submitted manuscript |
|---|---:|
| Period | 2016–2025 |
| Shipping firms | 27 |
| Firm-year observations | 254 |
| Carbon-intensity observations | 60 |
| ESG observations | 82 |
| Length | 37 pages |

## Repository map

```text
.
├── data/                     # Synthetic public sample and data documentation
├── docs/                     # Methodology, data dictionary, and limitations
├── outputs/                  # Reproducible results from the public sample
├── scripts/                  # Deterministic synthetic-data generator
├── site/                     # GitHub Pages portfolio
├── src/                      # Merton model and panel-analysis code
└── tests/                    # Numerical sanity checks
```

## Reproduce the public demonstration

The public demonstration preserves the analytical structure of the study
without redistributing licensed vendor data.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_sample_data.py
python src/analysis.py
python -m unittest discover -s tests
```

The analysis writes:

- `outputs/public_sample_results.csv`
- `site/assets/dual-pricing.png`
- `site/assets/sample-panel.png`
- `site/assets/sll-grid.png`

Results produced from the synthetic sample are **workflow demonstrations**, not
the estimates reported in the competition manuscript.

## Data and disclosure policy

Bloomberg, LSEG, and WRDS data are governed by their respective access and
redistribution terms. They are therefore not included. Application receipts,
contact information, third-party papers, historical competition submissions,
and copyrighted audio are also excluded.

The committed CSV is fully synthetic, uses fictional firm identifiers, and can
be regenerated from a fixed random seed. See [data/README.md](data/README.md)
and [docs/reproducibility.md](docs/reproducibility.md).

## Interpretation notes

Descriptive scatterplots and fixed-effects estimates answer different
questions. A raw cross-sectional slope can differ from the within-firm
coefficient after firm and year effects are absorbed. The portfolio therefore:

- labels synthetic and submitted-study results separately;
- treats fixed-effects estimates as conditional associations rather than causal
  effects; and
- documents sample changes caused by incomplete carbon and ESG coverage.

## Team and credit

Competition team **Deoksang (덕상)**<br>
Jaewon Kim (김재원) · Hong Kim (김홍), Sungkyunkwan University

The project was submitted to the 16th DB Insurance & Finance Competition in the
Insurance & Banking category.

## Documentation

- [Methodology](docs/methodology.md)
- [Data dictionary](docs/data-dictionary.md)
- [Reproducibility and limitations](docs/reproducibility.md)
- [Interactive portfolio](https://jwkim-skku.github.io/DB-Insurance-Competition/)

## License

Source code is released under the [MIT License](LICENSE). The license does not
apply to the original manuscript, third-party data, or third-party publications.
