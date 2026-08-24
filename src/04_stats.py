"""
P10 - Concordancia entre metodos de explicabilidad
04_stats.py

Tau de Kendall entre rankings de variables, en los 3 ejes que pide la
ficha tecnica (seccion 4/5):
  - entre folds del mismo (modelo, metodo)      -> estabilidad del metodo
  - entre metodos del mismo (modelo, fold)      -> concordancia SHAP/LIME/permutacion
  - entre modelos del mismo (metodo, fold)      -> el metodo generaliza entre modelos?

Salidas en results/tables/:
  - kendall_tau_detail.csv   : un tau por cada par comparado (grano fino)
  - kendall_tau_summary.csv  : tau medio + IC bootstrap 95% por (dataset, eje)
  - anova_tau.csv            : ANOVA de dos factores, tau ~ dataset * eje
  - anova_tau_cluster.csv    : robustez -- misma ANOVA sobre medias por
                                cluster (dataset, eje, group), para no tratar
                                los 2.340 pares crudos como independientes
                                (Metodologia/Resultados)
"""

import itertools
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import kendalltau
from statsmodels.formula.api import ols

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "tables"
INPUT_PATH = RESULTS_DIR / "attributions_long.csv"

MODELS = ["random_forest", "gradient_boosting", "logistic_regression"]
METHODS = ["shap", "lime", "permutation"]
SEED = 42


def get_ranking(df, dataset, model, method, fold):
    sub = df[(df.dataset == dataset) & (df.model == model) & (df.method == method) & (df.fold == fold)]
    return sub.set_index("feature")["rank"]


def tau_between(r1: pd.Series, r2: pd.Series):
    common = r1.index.intersection(r2.index)
    if len(common) < 3:
        return None
    tau, _ = kendalltau(r1.reindex(common), r2.reindex(common))
    return tau


def bootstrap_ci(values, n_boot=2000, ci=95, seed=SEED):
    rng = np.random.RandomState(seed)
    values = np.asarray(values)
    boot_means = [rng.choice(values, size=len(values), replace=True).mean() for _ in range(n_boot)]
    lo, hi = np.percentile(boot_means, [(100 - ci) / 2, 100 - (100 - ci) / 2])
    return lo, hi


def main():
    df = pd.read_csv(INPUT_PATH)
    datasets = sorted(df["dataset"].unique())
    rows = []

    for dataset in datasets:
        folds = sorted(df[df.dataset == dataset]["fold"].unique())

        # Eje 1: entre folds, mismo (modelo, metodo)
        for model in MODELS:
            for method in METHODS:
                rankings = {f: get_ranking(df, dataset, model, method, f) for f in folds}
                for f1, f2 in itertools.combinations(folds, 2):
                    tau = tau_between(rankings[f1], rankings[f2])
                    if tau is not None:
                        rows.append(dict(dataset=dataset, axis="entre_folds", group=f"{model}|{method}", pair=f"{f1}-{f2}", tau=tau))

        # Eje 2: entre metodos, mismo (modelo, fold)
        for model in MODELS:
            for fold in folds:
                rankings = {m: get_ranking(df, dataset, model, m, fold) for m in METHODS}
                for m1, m2 in itertools.combinations(METHODS, 2):
                    tau = tau_between(rankings[m1], rankings[m2])
                    if tau is not None:
                        rows.append(dict(dataset=dataset, axis="entre_metodos", group=f"{model}|fold{fold}", pair=f"{m1}-{m2}", tau=tau))

        # Eje 3: entre modelos, mismo (metodo, fold)
        for method in METHODS:
            for fold in folds:
                rankings = {mo: get_ranking(df, dataset, mo, method, fold) for mo in MODELS}
                for mo1, mo2 in itertools.combinations(MODELS, 2):
                    tau = tau_between(rankings[mo1], rankings[mo2])
                    if tau is not None:
                        rows.append(dict(dataset=dataset, axis="entre_modelos", group=f"{method}|fold{fold}", pair=f"{mo1}-{mo2}", tau=tau))

    detail = pd.DataFrame(rows)
    detail.to_csv(RESULTS_DIR / "kendall_tau_detail.csv", index=False)
    print(f"kendall_tau_detail.csv: {len(detail)} comparaciones par-a-par")

    # Resumen: tau medio + IC bootstrap 95% por (dataset, eje)
    summary_rows = []
    for (dataset, axis), group in detail.groupby(["dataset", "axis"]):
        lo, hi = bootstrap_ci(group["tau"].values)
        summary_rows.append(dict(
            dataset=dataset, axis=axis, n=len(group),
            tau_mean=group["tau"].mean(), tau_median=group["tau"].median(),
            ci95_lo=lo, ci95_hi=hi,
        ))
    summary = pd.DataFrame(summary_rows).sort_values(["dataset", "axis"])
    summary.to_csv(RESULTS_DIR / "kendall_tau_summary.csv", index=False)
    print("\nkendall_tau_summary.csv:")
    print(summary.to_string(index=False))

    # ANOVA de dos factores: tau ~ dataset * eje de comparacion
    anova_model = ols("tau ~ C(dataset) * C(axis)", data=detail).fit()
    anova_table = sm.stats.anova_lm(anova_model, typ=2)
    anova_table.to_csv(RESULTS_DIR / "anova_tau.csv")
    print("\nanova_tau.csv:")
    print(anova_table.to_string())

    # Robustez: los 2.340 tau crudos no son independientes (muchos pares
    # comparten las mismas rankings de fold subyacentes -- ver columna
    # "group" ya calculada arriba). Colapsamos a una media por
    # (dataset, eje, group) -- 276 valores -- y repetimos la ANOVA sobre
    # esas medias de cluster para ver si los efectos principales sobreviven
    # a una especificacion mas conservadora (Metodologia/Resultados).
    cluster = detail.groupby(["dataset", "axis", "group"], as_index=False)["tau"].mean()
    cluster_model = ols("tau ~ C(dataset) * C(axis)", data=cluster).fit()
    cluster_anova = sm.stats.anova_lm(cluster_model, typ=2)
    cluster_anova.to_csv(RESULTS_DIR / "anova_tau_cluster.csv")
    print(f"\nanova_tau_cluster.csv ({len(cluster)} medias de cluster, de {len(detail)} pares crudos):")
    print(cluster_anova.to_string())


if __name__ == "__main__":
    main()
