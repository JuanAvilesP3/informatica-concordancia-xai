"""
P10 - Concordancia entre metodos de explicabilidad
04c_grouped_attribution_check.py

Comprobacion anadida tras la revision cruzada interna (16/10/2026).

Con one-hot, cada categoria de una variable categorica recibe su propia
atribucion y su propio puesto en el ranking (p. ej. chk_status_A14). Eso puede
inflar el desacuerdo en German Credit y OULAD, que tienen muchas dummies. Este
script suma la atribucion de las dummies de cada variable original (para SHAP y
LIME la atribucion ya es un valor absoluto; para permutation importance se suma
la importancia media de cada dummy, una aproximacion a la permutacion por grupo,
que no se recalcula aqui), vuelve a ordenar por variable original y recalcula el
tau de Kendall medio en los tres ejes.

Tambien guarda el numero de predictores antes y despues de la codificacion.
Salida: results/tables/grouped_attribution_tau.csv y predictor_counts.csv
"""
from itertools import combinations
from pathlib import Path

import joblib
import pandas as pd
from scipy.stats import kendalltau

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"
T = ROOT / "results" / "tables"


def original_columns(dataset):
    pre = joblib.load(PROC / f"{dataset}_preprocessor.joblib")
    num, cat = [], []
    for name, _, cols in pre.transformers_:
        if name == "num":
            num = list(cols)
        elif name == "cat":
            cat = list(cols)
    return num, cat


def to_original(feature, num, cat):
    if feature in num:
        return feature
    matches = [c for c in cat if feature.startswith(c + "_") or feature == c]
    if matches:
        return max(matches, key=len)
    # 03_experiment sanea algunos caracteres en los nombres; se compara sin ellos
    clean = lambda s: "".join(ch for ch in s if ch.isalnum())
    matches = [c for c in cat if clean(feature).startswith(clean(c))]
    return max(matches, key=len) if matches else feature


def mean_tau(rank_table):
    """rank_table: dict[(model, method, fold)] -> Series(feature -> importance)"""
    keys = list(rank_table)
    out = {"entre_folds": [], "entre_metodos": [], "entre_modelos": []}
    for a, b in combinations(keys, 2):
        same = [a[i] == b[i] for i in range(3)]
        axis = {(True, True, False): "entre_folds", (True, False, True): "entre_metodos",
                (False, True, True): "entre_modelos"}.get(tuple(same))
        if axis:
            ra, rb = rank_table[a], rank_table[b]
            idx = ra.index.intersection(rb.index)
            out[axis].append(kendalltau(ra[idx].rank(ascending=False), rb[idx].rank(ascending=False))[0])
    return {k: sum(v) / len(v) for k, v in out.items()}


def main():
    att = pd.read_csv(T / "attributions_long.csv")
    rows, counts = [], []
    for dataset, g in att.groupby("dataset"):
        num, cat = original_columns(dataset)
        g = g.copy()
        g["original"] = [to_original(f, num, cat) for f in g.feature]
        counts.append(dict(dataset=dataset, original_predictors=len(num) + len(cat), numeric=len(num),
                           categorical=len(cat), encoded_features=g.feature.nunique(),
                           mapped_originals=g.original.nunique()))
        for level, col in [("encoded", "feature"), ("grouped_by_original_variable", "original")]:
            tables = {}
            for (model, method, fold), s in g.groupby(["model", "method", "fold"]):
                tables[(model, method, fold)] = s.groupby(col)["importance"].sum()
            res = mean_tau(tables)
            rows.append(dict(dataset=dataset, level=level, n_features=g[col].nunique(), **res))
            print(dataset, level, g[col].nunique(), {k: round(v, 3) for k, v in res.items()})
    pd.DataFrame(rows).to_csv(T / "grouped_attribution_tau.csv", index=False)
    pd.DataFrame(counts).to_csv(T / "predictor_counts.csv", index=False)
    print(pd.DataFrame(counts).to_string(index=False))


if __name__ == "__main__":
    main()
