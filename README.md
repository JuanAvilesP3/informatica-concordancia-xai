# Agreement among explainability methods

Data and code for the article *Agreement Among Explainability Methods: A Cross-Model, Cross-Domain Study*, submitted to *Informatica*.

**Authors:** Italo Javier Tenempaguay-Granizo, Juan Pablo Aviles-Esparza, Isaac David Torres-Paredes. Software Engineering, Faculty of Informatics and Electronics, Escuela Superior Politécnica de Chimborazo (ESPOCH), Riobamba, Ecuador.

## What the study does

On four public tabular datasets (OULAD, Dropout, German Credit, Rice), three models (random forest, XGBoost, logistic regression) are explained with SHAP, LIME and permutation importance under 10-fold cross-validation. The 360 resulting feature rankings are compared with Kendall's tau between folds, between methods and between models, with a repeated-seed control, a top-10 analysis and a check that groups one-hot features back into their original variables.

## Repository layout

| Path | Content |
|---|---|
| `src/01_download.py` | Download the four datasets from the UCI repository |
| `src/02_preprocess.py` | Imputation, scaling and one-hot encoding |
| `src/03_experiment.py` | Models, attributions and rankings for every fold |
| `src/03b_repeated_seed_control.py` | Same-method agreement across sampling seeds |
| `src/03c_model_performance.py`, `src/03d_majority_baseline.py` | Predictive performance and majority-class baseline |
| `src/04_stats.py`, `src/04b_topk_stats.py` | Kendall's tau, bootstrap intervals, ANOVA, top-10 agreement |
| `src/04c_grouped_attribution_check.py` | Agreement with one-hot features grouped by original variable |
| `src/05_figures.py` | Figures 1-4 |
| `src/run_all.py` | Runs the pipeline in order and logs package versions to `results/logs/` |
| `data/processed/` | Preprocessed datasets and preprocessing pipelines |
| `results/tables/`, `results/figures/` | Attribution rankings and every table and figure reported in the article |
| `paper/` | LaTeX source and compiled manuscript |

## Reproducing the analysis

```bash
pip install -r requirements.txt
python src/run_all.py
```

The datasets are distributed by the UCI Machine Learning Repository under CC BY 4.0.

## Citation

Archived on Zenodo: [10.5281/zenodo.22907629](https://doi.org/10.5281/zenodo.22907629) (this DOI always resolves to the latest version).
