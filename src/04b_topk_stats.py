"""
P10 - Concordancia entre metodos de explicabilidad
04b_topk_stats.py

La revision adversarial señalo que el numero de features va de 7
(Rice) a 61 (German Credit, post-encoding), y que tau de Kendall
sobre la lista COMPLETA es mecanicamente mas grueso (sesgado hacia
valores altos) en listas cortas -- lo que podria producir el efecto
"dataset" del ANOVA como artefacto del largo de lista, no como una
propiedad real del dominio.

Este script recalcula tau restringido al top-10 de cada ranking
(interseccion de los top-10 de ambos metodos/modelos/folds
comparados) para el eje "entre metodos" (el eje central del
articulo), en los 4 datasets, y compara contra el tau de lista
completa ya reportado en kendall_tau_summary.csv.
"""

import itertools
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "tables"
INPUT_PATH = RESULTS_DIR / "attributions_long.csv"

MODELS = ["random_forest", "gradient_boosting", "logistic_regression"]
METHODS = ["shap", "lime", "permutation"]
TOP_K = 10


def get_ranking(df, dataset, model, method, fold):
    sub = df[(df.dataset == dataset) & (df.model == model) & (df.method == method) & (df.fold == fold)]
    return sub.set_index("feature")["rank"]


def topk_tau_between(r1: pd.Series, r2: pd.Series, k=TOP_K):
    top1 = set(r1[r1 <= k].index)
    top2 = set(r2[r2 <= k].index)
    common = top1 | top2  # union: penaliza features que estan en el top-k de uno pero no del otro
    common = [f for f in common if f in r1.index and f in r2.index]
    if len(common) < 3:
        return None
    tau, _ = kendalltau(r1.reindex(common), r2.reindex(common))
    return tau


def main():
    df = pd.read_csv(INPUT_PATH)
    datasets = sorted(df["dataset"].unique())
    rows = []

    for dataset in datasets:
        folds = sorted(df[df.dataset == dataset]["fold"].unique())
        n_features = df[df.dataset == dataset]["feature"].nunique()

        for model in MODELS:
            for fold in folds:
                rankings = {m: get_ranking(df, dataset, model, m, fold) for m in METHODS}
                for m1, m2 in itertools.combinations(METHODS, 2):
                    tau = topk_tau_between(rankings[m1], rankings[m2])
                    if tau is not None:
                        rows.append(dict(dataset=dataset, n_features=n_features, model=model,
                                          fold=fold, pair=f"{m1}-{m2}", tau_topk=tau))

    detail = pd.DataFrame(rows)
    detail.to_csv(RESULTS_DIR / "kendall_tau_topk_detail.csv", index=False)

    summary = detail.groupby(["dataset", "n_features"])["tau_topk"].agg(["mean", "median", "std", "count"]).round(3)
    summary.to_csv(RESULTS_DIR / "kendall_tau_topk_summary.csv")
    print("=== tau entre metodos, restringido al top-10 (union), por dataset ===")
    print(summary)

    # Comparar contra el tau de lista completa ya calculado
    try:
        full = pd.read_csv(RESULTS_DIR / "kendall_tau_summary.csv")
        full_between = full[full.axis == "entre_metodos"][["dataset", "tau_mean"]].set_index("dataset")
        print("\n=== Comparacion: tau lista completa vs tau top-10 ===")
        comp = summary["mean"].rename("tau_topk_mean").to_frame().join(
            full_between.rename(columns={"tau_mean": "tau_full_mean"}), how="left")
        print(comp)
        comp.to_csv(RESULTS_DIR / "tau_full_vs_topk_comparison.csv")
    except FileNotFoundError:
        print("(kendall_tau_summary.csv no encontrado, omitiendo comparacion)")

    print(f"\nCompletado: {len(detail)} comparaciones guardadas.")


if __name__ == "__main__":
    main()
