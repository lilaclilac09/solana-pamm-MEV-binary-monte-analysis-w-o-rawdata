# Notebooks - MEV Analysis Pipeline

Status: BLOCKED — raw input data and a reproducible scientific Python environment are not included; next human action: supply the authorized input dataset and environment specification before rerunning the analysis.

This repository is an offline research export, not a deployed application. GitHub homepage is unset, Pages is disabled, and deployment records are empty as of 2026-11-22; an unlisted external deployment has not been ruled out.

Notebooks are organized by analysis type at the repository root. Included outputs and notes are historical artifacts, not evidence of a fresh successful run. Reported metrics, implementation-complete headings and projected improvements must not be treated as independently verified results. See [the acceptance audit](notes/acceptance-audit-2026-11-22.md) for checks and limitations.

## Reproducibility limits

- The first data-cleaning notebook reads `/Users/aileen/Downloads/pamm/pamm_updates_391876700_391976700.parquet`; that file is absent here, and this export contains no Parquet files. Do not substitute synthetic data for the original results.
- No requirements file, environment lock, build command or automated test runner is provided. The available Python interpreter lacks the notebook/scientific packages; no full analysis rerun is claimed.
- `10_advanced_FP_solution/01_improved_fat_sandwich_detection.ipynb` and its `_COMBINED.ipynb` counterpart contain Markdown text, not valid notebook JSON. Recover the intended notebooks from their source before attempting execution; this audit does not invent missing cells.
- Some valid notebooks retain saved error outputs, including an `IndexError` in `08_monte_carlo_risk/08_monte_carlo_risk.ipynb`. Saved errors describe earlier runs, not a reproduced current failure.
- Existing `.py` helpers and `CODE_ORGANIZATION_PLAN.md` are retained as historical material. The plan includes paths from the original workspace that do not exist in this export; the tree below describes current locations.

## 📁 Folder Structure

```
./
├── 01_data_cleaning/              # Data cleaning & parsing
├── 01a_data_cleaning_DeezNode_filters/ # DeezNode filter
├── 01b_jito_tip_filter/           # Jito tip filter
├── 02_mev_detection/              # All MEV detection algorithms
├── 03_oracle_analysis/           # Oracle timing & burst detection
├── 04_validator_analysis/         # Validator MEV metrics & clustering
├── 05_token_pair_analysis/       # Single AMM token pair MEV (with aggregator + MEV selection)
├── 06_pool_analysis/              # General pool MEV analysis
├── 07_ml_classification/          # ML classification for MEV bots
├── 08_monte_carlo_risk/           # Monte Carlo risk simulation
├── 09a_advanced_ml/              # Advanced ML notebook and legacy helpers
└── 10_advanced_FP_solution/      # Markdown-only notebook placeholders (not executable)
```

## 📊 Execution Order

1. **01_data_cleaning/** - Clean and parse raw data
2. **01a_data_cleaning_DeezNode_filters/** - Filter DeezNode transactions
3. **01b_jito_tip_filter/** - Filter Jito tip transactions
4. **02_mev_detection/** - Detect all MEV patterns
5. **03_oracle_analysis/** - Analyze oracle patterns
6. **04_validator_analysis/** - Analyze validator MEV metrics
7. **05_token_pair_analysis/** - Deep-dive single token pair analysis
8. **06_pool_analysis/** - General pool analysis
9. **07_ml_classification/** - ML model training and classification
10. **08_monte_carlo_risk/** - Risk simulation
11. **07_ml_classification/07c_aggregator_separation.ipynb** - Aggregator separation (no `09_aggregator_mev_analysis/` directory exists in this export)

## 📝 Included Artifacts (availability varies)

- **Notebook file** (`.ipynb`) - The analysis notebook
- **notes.md** - Detailed documentation of the analysis
- **outputs/** - Analysis outputs
  - **csv/** - CSV data files
  - **images/** - Visualization images

## 🔍 Quick Reference

| Notebook | Purpose | Key Outputs |
|----------|---------|-------------|
| `01_data_cleaning` | Parse account_updates, trades, timing | Cleaned dataset |
| `01a_data_cleaning_filters` | Filter DeezNode addresses | Filtered dataset |
| `01b_jito_tip_filter` | Filter Jito tip addresses | Filtered dataset |
| `02_mev_detection` | All 7 MEV algorithms | `comprehensive_mev_all_with_pnl.csv` |
| `03_oracle_analysis` | Oracle timing patterns | `oracle_bursts.csv`, `top_oracle_updaters.csv` |
| `04_validator_analysis` | Validator MEV metrics | `mev_trades_bots_per_validator.csv` |
| `05_token_pair_analysis` | Single token pair deep-dive | `per_pool_analysis.csv`, `monte_carlo_by_token_pair.csv` |
| `06_pool_analysis` | General pool analysis | `pool_density_analysis.csv` |
| `07_ml_classification` | ML bot classification | `ml_model_performance.csv`, `feature_importance.csv` |
| `08_monte_carlo_risk` | Risk simulation | `monte_carlo_by_*.csv` |


## 📚 Documentation

- The main analysis folders through `08_monte_carlo_risk/` have `notes.md` files. Advanced folders do not all have notes or complete executable notebooks.


## 🔗 Key Code Locations

`CODE_ORGANIZATION_PLAN.md` preserves the historical organization plan, with 📍 markers pointing to original workspace locations, not a validated map of this export:
- Source notebook locations
- Specific cell numbers
- Reference documentation

## ⚠️ Important Notes

- **All code stays in `.ipynb` notebooks** - NO `.py` file extraction
- Outputs are organized in each notebook's `outputs/` folder
- Execution depends on external datasets, packages and workspace paths; notebooks are not certified self-contained or reproducible in this export
