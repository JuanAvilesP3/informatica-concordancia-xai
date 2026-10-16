"""
P10 - Concordancia entre metodos de explicabilidad
03d_majority_baseline.py

Linea base de clase mayoritaria por dataset, para leer la exactitud de los
modelos (model_performance_resumen.csv) contra una referencia mas exigente que
el azar 1/n_clases. Guarda results/tables/majority_baseline.csv.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROC_DIR = ROOT / "data" / "processed"
TABLES_DIR = ROOT / "results" / "tables"


def main():
    perf = pd.read_csv(TABLES_DIR / "model_performance_resumen.csv")
    rows = []
    for ds in ["oulad", "dropout", "german_credit", "rice"]:
        y = pd.read_csv(PROC_DIR / f"{ds}_y.csv").iloc[:, -1]
        share = y.value_counts(normalize=True)
        acc = perf.loc[perf["dataset"] == ds, "accuracy_mean"]
        rows.append({"dataset": ds, "n": len(y), "n_classes": len(share),
                     "majority_class": share.index[0], "majority_baseline_accuracy": share.iloc[0],
                     "chance_accuracy": 1 / len(share),
                     "model_accuracy_min": acc.min(), "model_accuracy_max": acc.max()})
    out = pd.DataFrame(rows)
    out.to_csv(TABLES_DIR / "majority_baseline.csv", index=False)
    print(out.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
