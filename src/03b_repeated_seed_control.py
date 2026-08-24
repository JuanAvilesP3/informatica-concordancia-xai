"""
P10 - Concordancia entre metodos de explicabilidad
03b_repeated_seed_control.py

Control pedido por la revision adversarial: LIME (muestrea una
submuestra de instancias del fold de prueba) e importancia por
permutacion (submuestrea el fold de prueba y permuta con una semilla)
son metodos ESTOCASTICOS. Parte del desacuerdo "entre metodos" que
reporta el articulo (tau entre 0.28 y 0.47) podria ser simplemente
ruido de muestreo de estos dos estimadores, no desacuerdo genuino
entre SHAP/LIME/permutacion como constructos teoricos.

Este script fija el modelo YA ENTRENADO (mismo fold, mismo modelo
que en 03_experiment.py) y recalcula el ranking de LIME y de
permutacion 5 veces cada uno, cambiando SOLO la semilla de muestreo
interna (no se reentrena el modelo, no cambia el fold). Con eso se
calcula tau de Kendall entre pares de repeticiones del MISMO metodo:
si ese tau "mismo metodo, distinta semilla" ya es bajo, gran parte
del tau "entre metodos" reportado en el articulo es ruido de
estimador, no desacuerdo real entre metodos. Si es alto (cercano a
1), el desacuerdo entre metodos reportado es genuino.

Cubre 1 fold representativo (fold 0) x los 3 modelos x los 4
datasets, para mantener el costo acotado; no se repite en los 10
folds porque el objetivo es acotar el ruido de estimador, no
recalcular el estudio completo.
"""

import itertools
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib import import_module

exp = import_module("03_experiment")

PROC_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "tables"
DATASETS = ["oulad", "dropout", "german_credit", "rice"]
SEED = 42
N_REPEATS = 5
LIME_INSTANCES = 100
PERMUTATION_REPEATS = 5
EVAL_MAX_SAMPLES = 2000


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    models = exp.make_models()

    for dataset_name in DATASETS:
        X, y_raw = exp.load_dataset(dataset_name)
        label_encoder = LabelEncoder()
        y = pd.Series(label_encoder.fit_transform(y_raw), index=y_raw.index, name="target")
        class_names = label_encoder.classes_
        skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=SEED)
        train_idx, test_idx = next(iter(skf.split(X, y)))  # fold 0 solamente
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        for model_name, model in models.items():
            fitted = model.__class__(**model.get_params())
            fitted.fit(X_train, y_train)
            print(f"[{dataset_name}][{model_name}] modelo entrenado, calculando {N_REPEATS} repeticiones...")

            lime_rankings = []
            perm_rankings = []
            for rep in range(N_REPEATS):
                rng = np.random.RandomState(1000 * (rep + 1) + hash(dataset_name + model_name) % 1000)
                lime_r = exp.lime_ranking(fitted, X_train, X_test, class_names, LIME_INSTANCES, rng)
                perm_r = exp.permutation_ranking(fitted, X_test, y_test, PERMUTATION_REPEATS, EVAL_MAX_SAMPLES, rng)
                lime_rankings.append(lime_r.rank(ascending=False))
                perm_rankings.append(perm_r.rank(ascending=False))

            for method, rankings in [("lime", lime_rankings), ("permutation", perm_rankings)]:
                for i, j in itertools.combinations(range(N_REPEATS), 2):
                    tau, _ = kendalltau(rankings[i].reindex(rankings[0].index),
                                        rankings[j].reindex(rankings[0].index))
                    rows.append(dict(dataset=dataset_name, model=model_name, method=method,
                                      rep_i=i, rep_j=j, tau=tau))

    out = pd.DataFrame(rows)
    out.to_csv(RESULTS_DIR / "repeated_seed_control.csv", index=False)

    print("\n=== Resumen: tau entre repeticiones del MISMO metodo, distinta semilla (ruido de estimador) ===")
    print(out.groupby(["method"])["tau"].agg(["mean", "std", "min", "max", "count"]).round(3))
    print("\nPor dataset:")
    print(out.groupby(["dataset", "method"])["tau"].mean().round(3))
    print(f"\nCompletado: {len(out)} filas guardadas en {RESULTS_DIR / 'repeated_seed_control.csv'}")


if __name__ == "__main__":
    main()
