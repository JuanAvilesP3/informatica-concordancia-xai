"""
P10 - Concordancia entre metodos de explicabilidad
03c_model_performance.py

Companion ligero a 03_experiment.py: entrena los mismos 3 modelos sobre
los mismos 4 datasets con los mismos folds (StratifiedKFold, seed=42,
10 folds) pero SOLO mide desempeno predictivo (accuracy, F1 macro,
log-loss), sin generar atribuciones SHAP/LIME/permutacion (el paso
caro). Responde a un hallazgo de la revision adversarial ronda 2: el
articulo mide desacuerdo entre metodos de explicabilidad pero nunca
reporta si los modelos explicados son siquiera buenos -- una tabla de
referencia de desempeno contextualiza si el desacuerdo importa (un
modelo casi al azar cuyas explicaciones "concuerdan" no dice mucho).
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, log_loss
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder

sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib import import_module

_exp = import_module("03_experiment")
DATASETS = _exp.DATASETS
SEED = _exp.SEED
load_dataset = _exp.load_dataset
make_models = _exp.make_models

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "tables"


def run(n_folds=10):
    rows = []
    models = make_models()

    for dataset_name in DATASETS:
        X, y_raw = load_dataset(dataset_name)
        label_encoder = LabelEncoder()
        y = pd.Series(label_encoder.fit_transform(y_raw), index=y_raw.index, name="target")
        n_classes = len(label_encoder.classes_)
        skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=SEED)

        for fold, (train_idx, test_idx) in enumerate(skf.split(X, y)):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

            for model_name, model in models.items():
                fitted = model.__class__(**model.get_params())
                fitted.fit(X_train, y_train)
                pred = fitted.predict(X_test)
                proba = fitted.predict_proba(X_test)

                rows.append({
                    "dataset": dataset_name,
                    "model": model_name,
                    "fold": fold,
                    "n_classes": n_classes,
                    "accuracy": accuracy_score(y_test, pred),
                    "f1_macro": f1_score(y_test, pred, average="macro"),
                    "log_loss": log_loss(y_test, proba, labels=list(range(n_classes))),
                })
        print(f"[{dataset_name}] listo")

    df = pd.DataFrame(rows)
    df.to_csv(RESULTS_DIR / "model_performance_por_fold.csv", index=False)

    summary = (
        df.groupby(["dataset", "model"])
        .agg(
            n_classes=("n_classes", "first"),
            accuracy_mean=("accuracy", "mean"), accuracy_std=("accuracy", "std"),
            f1_macro_mean=("f1_macro", "mean"), f1_macro_std=("f1_macro", "std"),
            log_loss_mean=("log_loss", "mean"), log_loss_std=("log_loss", "std"),
        )
        .reset_index()
    )
    summary.to_csv(RESULTS_DIR / "model_performance_resumen.csv", index=False)
    print(summary.to_string(index=False))
    print(f"\nCompletado: {RESULTS_DIR}")


if __name__ == "__main__":
    run()
