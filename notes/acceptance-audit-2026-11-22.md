# Acceptance audit — 2026-11-22

Existing work checked only against [ACCEPTANCE.md](../ACCEPTANCE.md), AGENTS.md, CLAUDE.md, `.cursor/rules/acceptance.mdc`, and README instructions. This is a notebook research export, not a UI application. No new scientific-quality or application-design criteria are introduced.

## Failing items

| Item | ACCEPTANCE § | Source rule | Status / evidence |
|------|--------------|-------------|-------------------|
| README missing product status and next human action | §5 | `AGENTS.md` 施工队安全条例; `ship-visible-mvp.mdc` | **Fixed here:** BLOCKED, with authorized dataset/environment next action. GitHub homepage null, has_pages false, Pages API HTTP 404, deployments `[]`; an unlisted external deployment remains possible. |
| README tree/execution paths do not match export | §6 | repo README instructions | **Fixed here:** root-level tree, actual DeezNode directory and existing aggregator notebook; advanced directories listed accurately. Historical organization plan explicitly distinguished from current paths. |
| README implies uniform documentation and self-contained notebooks despite absent inputs and incomplete files | §2, §6 | `verification.mdc`; repo README | **Fixed here:** document historical-output scope, missing data/environment, incomplete notebook files and variable artifact availability. No claim of a successful pipeline run. |
| Imbalance change log predicts ~3x more detections from a threshold change without measured evidence | §2 | `verification.mdc` | **Fixed here:** remove the quantitative improvement assertion, mark targets unvalidated and implementation-complete title as a change log, not successful-runtime proof. Original targets remain clearly labeled as unobserved. |
| Analysis cannot be reproduced from this checkout | §2, §7 | `verification.mdc`; `AGENTS.md` blocker table | **Not fixable here:** first notebook references absent raw Parquet; no Parquet files or dependency/environment specification included. Available Python lacks scientific/notebook packages. No fabricated inputs or guessed environment installed. |
| Two .ipynb paths are Markdown text, not notebook JSON | §2, §6, §7 | `verification.mdc`; README notebook instructions; blocker table | **Not fixable here without recovering intended content:** both fail JSON parsing at line 1. README now discloses that these are not executable notebooks; no missing analysis cells invented. |
| Some stored notebooks retain error outputs | §2, §7 | `verification.mdc`; blocker table | **Not fixed:** inventory reports four notebook files with saved errors, including checkpoints. These are historical outputs, not reproduced runtime failures; missing inputs/environment prevent a current root-cause/repair claim. |

## Passing items and historical limits

- **§1 workflow:** inspected instructions, implementation/export inventory, history and all PRs before patching. Documentation-only diff; no new dependencies, scientific algorithm changes, refactor, deleted flows or new application. No analysis code extracted to .py; audit utilities are outside the repo. Existing Python helpers are retained, not rewritten. Historical private planning/confirmation cannot be inferred and is not asserted.
- **§2 verification:** actually read all 23 notebook files, inventoried 33 CSVs, checked declared README locations, parsed existing Python syntax and captured changed documentation source at 390×844. JSON readability and stored CSV presence are not runtime or scientific validation. No build/lint/test runner or environment manifest exists. Full notebook execution, model training, Monte Carlo reruns and PDF regeneration were not run.
- **§3 bug discipline:** no speculative analysis-code fix. Documentation root causes are stale workspace paths, omitted reproducibility status and an unsupported quantitative projection. A lower threshold does not alone establish a measured case-count increase. Saved IndexError is explicitly not diagnosed as a current reachable failure without the original input/runtime.
- **§4 UI:** not applicable: no product UI or UI PR was found. This branch changes Markdown only. Source-text documentation screenshots are supplied as evidence, not presented as product screenshots. No animated interaction walkthrough is claimed or required for this non-UI repo; future UI-repo walkthroughs use 390×844 per owner instruction.
- **§5 ancestry:** only process PR #1 exists in `gh pr list --state all --limit 100`. API reports MERGED, SHA `ec9e999a07fac87a1afd3917817ea875830ed1cc`; after `git fetch origin main`, `git merge-base --is-ancestor ec9e999a07fac87a1afd3917817ea875830ed1cc origin/main` exits 0. This audit branch is not merged and no production/scientific completion is claimed.
- **§6 local rules:** AGENTS.md, CLAUDE.md and the only Cursor rule delegate to ACCEPTANCE.md. README's prohibition on new .py extraction respected; stale paths corrected rather than rewriting notebooks. Main-folder notes preserved as historical records.
- **§7 limitations:** blocker table below records inputs, environment and incomplete notebook content. No bypass or claims based solely on old saved results.
- **§8 historical PR check:** `gh api repos/lilaclilac09/solana-pamm-MEV-binary-monte-analysis-w-o-rawdata/pulls/1 --jq .body | python scripts/check_acceptance.py` prints `ACCEPTANCE.md: evidence closer complete`. **No historical PR bodies fail.** Analysis arrived through direct commits; original task replies are unavailable. No merged PR body edited. No draft PR body written, per owner instruction.

## Evidence and exact checks

| Command | Observed result |
|---------|-----------------|
| `python /home/ubuntu/audit-artifacts/solana-pamm-MEV-binary-monte-analysis-w-o-rawdata/audit_inventory.py` | 23 notebook files: 21 JSON-readable, 2 invalid; 4 files with saved errors; 33 CSV files read; 0 Parquet files; first raw input absent; corrected README paths/status and unvalidated-target labels pass |
| `python -` using `ast.parse` on each `Path('.').rglob('*.py')` | `PASS: 7 existing Python files parse; imports/analysis not executed` |
| `node /home/ubuntu/audit-artifacts/solana-pamm-MEV-binary-monte-analysis-w-o-rawdata/capture.cjs` | `PASS: documentation-source screenshots captured at 390x844; no product UI or interaction walkthrough applies` |

Inventory includes tracked checkpoints. Invalid files:

- `10_advanced_FP_solution/01_improved_fat_sandwich_detection.ipynb` (987 bytes): plain Markdown, not JSON.
- `10_advanced_FP_solution/01_improved_fat_sandwich_detection_COMBINED.ipynb` (918 bytes): plain Markdown, not JSON.

Saved-error files: `03_oracle_analysis/.ipynb_checkpoints/03_oracle_analysis-checkpoint.ipynb`, `07_ml_classification/07_ml_classification.ipynb`, `08_monte_carlo_risk/.ipynb_checkpoints/08_monte_carlo_risk-checkpoint.ipynb`, `08_monte_carlo_risk/08_monte_carlo_risk.ipynb`. The last includes `IndexError: too many indices for array: array is 0-dimensional, but 1 were indexed`. Empty error-name fields also occur; exact entries are preserved in inventory.json.

First raw input path comes from the first data-cleaning code cell: `/Users/aileen/Downloads/pamm/pamm_updates_391876700_391976700.parquet`. Path existence check is false. No Parquet file is present anywhere in this export. This is evidence for blocked reproduction, not proof of any published metric's truth or falsity.

Environment diagnosed once: current Python resolves to `/home/ubuntu/airflow-venv/bin/python`, VIRTUAL_ENV is unset, and no repo-specific venv or dependency manifest is supplied. `importlib.util.find_spec` reports pandas, numpy, nbformat and nbclient unavailable. No safe documented repo environment activation/install is available, so the audit uses standard-library inventory only and does not claim scientific execution.

Artifacts, not committed, under `/home/ubuntu/audit-artifacts/solana-pamm-MEV-binary-monte-analysis-w-o-rawdata/`:

- `inventory.json`, `inventory.log`, `audit_inventory.py`
- `readme-390x844.png`, `ml-verification-scope-390x844.png`, `capture.cjs`

Screenshots display the actual changed Markdown source in a wrapping browser text preview; both were opened and inspected. They are documentation evidence, not an invented product interface or live deployment.

## Blockers

| blocked_on | evidence | impact | human_action | not_doing |
|------------|----------|--------|--------------|-----------|
| Authorized input dataset | first notebook raw path absent; 0 Parquet files in checkout | blocked for end-to-end analysis | Supply authorized source dataset and intended local input location | No synthetic replacement or claimed recomputation |
| Scientific environment | no environment manifest; pandas/numpy/nbformat/nbclient unavailable in current interpreter | blocked for notebook execution | Supply original dependency/environment specification | No guessed package versions or unrelated Airflow environment changes |
| Intended advanced notebooks | two .ipynb files are Markdown, not valid JSON | blocked for those notebook flows | Restore intended notebook files from original source | No invented cells or conversion falsely represented as recovered analysis |

Status: BLOCKED — next human action: supply authorized raw inputs and environment specification. Safe-to-merge below assesses the documentation diff, not analysis validity or production readiness.

```txt
root cause: README described an original workspace as a reproducible export and omitted product status; imbalance change log included an unmeasured quantitative improvement projection.
files changed: README.md; 07_ml_classification/IMBALANCE_FIXES_COMPLETE.md; notes/acceptance-audit-2026-11-22.md.
checks run: notebook/CSV inventory and corrected documentation references checked; seven Python files parse; historical PR #1 evidence closer passes; documentation screenshots captured; scientific execution not run.
manual QA: opened and inspected both 390x844 documentation-source screenshots; no product UI exists to exercise.
verification: inventory and screenshots saved under /home/ubuntu/audit-artifacts/solana-pamm-MEV-binary-monte-analysis-w-o-rawdata/; no data recomputation or production verification claimed.
remaining risks: missing raw data and scientific environment; two invalid notebook files; historical saved errors; results and target metrics not independently reproduced.
manual steps: supply authorized input dataset and environment specification, and recover intended advanced notebooks before analysis acceptance.
safe to merge: yes
```
