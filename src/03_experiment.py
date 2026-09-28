"""
P10 - Concordancia entre metodos de explicabilidad
03_experiment.py

3 modelos (Random Forest, Gradient Boosting, Regresion Logistica) x
4 datasets x K folds. Por cada combinacion, genera atribuciones con
SHAP, LIME e importancia por permutacion y guarda el ranking completo
de variables (no solo el top-10) en formato largo.

Decisiones de diseno que hay que documentar en el manuscrito (la
ficha tecnica exige esto explicitamente para LIME; aqui se extiende
a SHAP porque OULAD y Dropout son multiclase):

  - SHAP: se usa shap.Explainer generico (TreeExplainer para RF/GB,
    LinearExplainer para regresion logistica). Para datasets
    multiclase, se agregan las atribuciones promediando el valor
    absoluto de SHAP sobre todas las clases y sobre las instancias
    evaluadas -> un unico ranking global por (dataset, modelo, fold).

  - LIME: es local por diseno. Para obtener un ranking global se
    explica una muestra de instancias del fold de prueba (parametro
    --lime-instances), se toma para cada instancia la explicacion de
    su clase predicha, se usa el valor absoluto del peso de cada
    variable y se promedia sobre las instancias.

  - Importancia por permutacion: sklearn.inspection.permutation_importance
    con --permutation-repeats repeticiones, usando neg_log_loss como
    scoring (funciona para binario y multiclase por igual). El
    ENTRENAMIENTO del modelo siempre usa el fold completo (no se
    reduce nunca); solo el CALCULO de esta metrica de importancia se
    hace sobre una submuestra del fold de prueba cuando este es muy
    grande (--eval-max-samples), siguiendo el mismo principio
    que la ficha tecnica autoriza explicitamente para LIME ("SHAP es
    lento en Random Forest grande -> usar TreeSHAP y submuestreo para
    LIME"): submuestrear el diagnostico posterior, nunca el
    entrenamiento. En datasets como OULAD (fold de prueba ~16k filas
    con folds=2, ~3.3k con folds=10) esto evita recalcular 200
    arboles x 49 variables x N repeticiones sobre decenas de miles de
    filas.
"""

import argparse
import itertools
import time
from pathlib import Path

import numpy as np
import pandas as pd
import shap
from lime.lime_tabular import LimeTabularExplainer
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

PROC_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "tables"

DATASETS = ["oulad", "dropout", "german_credit", "rice"]
SEED = 42


def make_models():
    # n_estimators=100 (antes 200): hiperparametro nuestro, no exigido
    # por la ficha; reduce el costo de permutation_importance y SHAP
    # sin afectar los datos de entrenamiento.
    #
    # max_depth=12 en Random Forest: sin este limite, los arboles
    # crecen sin restriccion (comprobado: profundidad no acotada en
    # OULAD, con categoricas de alta cardinalidad one-hot-encoded), lo
    # que hace que TreeSHAP sea extremadamente lento (>10 min para
    # explicar 1500 filas) porque su costo crece con la profundidad
    # del arbol. Con max_depth=12 el mismo calculo tarda ~114s. Es
    # ademas una regularizacion estandar (evita sobreajuste), no una
    # reduccion de datos.
    return {
        "random_forest": RandomForestClassifier(n_estimators=100, max_depth=12, random_state=SEED, n_jobs=-1),
        "gradient_boosting": XGBClassifier(
            n_estimators=100, max_depth=6, random_state=SEED, eval_metric="logloss",
            use_label_encoder=False, verbosity=0,
        ),
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=SEED),
    }


def load_dataset(name: str):
    X = pd.read_csv(PROC_DIR / f"{name}_X.csv")
    y = pd.read_csv(PROC_DIR / f"{name}_y.csv")["target"]
    # XGBoost prohibe "[", "]", "<" en nombres de columna. OULAD tiene
    # una categoria "55<=" (age_band) que genera ese caracter al
    # codificar; se sanea para los 4 datasets por igual.
    X.columns = (
        X.columns.str.replace("<", "lt", regex=False)
        .str.replace("[", "(", regex=False)
        .str.replace("]", ")", regex=False)
    )
    return X, y


def shap_ranking(model, model_name: str, X_train: pd.DataFrame, X_eval: pd.DataFrame, max_samples: int, rng: np.random.RandomState) -> pd.Series:
    """Devuelve una Serie feature -> importancia (valor absoluto de SHAP
    promediado sobre instancias y, si es multiclase, sobre clases).
    Mismo principio que permutation_ranking: se submuestrea el fold de
    PRUEBA para este calculo si es muy grande, nunca el entrenamiento."""
    if len(X_eval) > max_samples:
        idx = rng.choice(len(X_eval), size=max_samples, replace=False)
        X_eval = X_eval.iloc[idx]

    if model_name in ("random_forest", "gradient_boosting"):
        explainer = shap.TreeExplainer(model)
    else:
        explainer = shap.LinearExplainer(model, X_train)

    sv = explainer.shap_values(X_eval)

    if isinstance(sv, list):  # multiclase, una matriz por clase
        abs_per_class = [np.abs(class_sv) for class_sv in sv]
        importance = np.mean(np.stack(abs_per_class, axis=0), axis=(0, 1))
    else:
        arr = np.array(sv)
        if arr.ndim == 3:  # (n_samples, n_features, n_classes)
            importance = np.mean(np.abs(arr), axis=(0, 2))
        else:  # binario: (n_samples, n_features)
            importance = np.mean(np.abs(arr), axis=0)

    return pd.Series(importance, index=X_eval.columns)


def lime_ranking(model, X_train: pd.DataFrame, X_eval: pd.DataFrame, class_names, n_instances: int, rng: np.random.RandomState) -> pd.Series:
    explainer = LimeTabularExplainer(
        X_train.values,
        feature_names=list(X_train.columns),
        class_names=[str(c) for c in class_names],
        discretize_continuous=True,
        random_state=SEED,
    )

    n_instances = min(n_instances, len(X_eval))
    idx = rng.choice(len(X_eval), size=n_instances, replace=False)

    weights_sum = pd.Series(0.0, index=X_train.columns)
    for i in idx:
        instance = X_eval.iloc[i].values
        pred_class = int(np.argmax(model.predict_proba([instance])[0]))
        exp = explainer.explain_instance(
            instance, model.predict_proba, num_features=len(X_train.columns), labels=(pred_class,)
        )
        for feat_desc, weight in exp.as_list(label=pred_class):
            # feat_desc viene como "feature <= valor" o similar; se
            # recupera el nombre original ordenando por longitud descendente
            # para evitar que prefijos colisionen (ej. Area vs Convex_Area).
            for col in sorted(X_train.columns, key=len, reverse=True):
                if col in feat_desc:
                    weights_sum[col] += abs(weight)
                    break

    return weights_sum / n_instances


def permutation_ranking(model, X_eval: pd.DataFrame, y_eval: pd.Series, n_repeats: int, max_samples: int, rng: np.random.RandomState) -> pd.Series:
    # El modelo ya esta entrenado con el fold completo; aqui solo se
    # submuestrea el fold de PRUEBA para calcular este diagnostico mas
    # rapido (mismo principio que la ficha autoriza para LIME).
    if len(X_eval) > max_samples:
        idx = rng.choice(len(X_eval), size=max_samples, replace=False)
        X_eval, y_eval = X_eval.iloc[idx], y_eval.iloc[idx]

    result = permutation_importance(
        model, X_eval, y_eval, n_repeats=n_repeats, random_state=SEED,
        scoring="neg_log_loss", n_jobs=-1,
    )
    return pd.Series(result.importances_mean, index=X_eval.columns)


def run(datasets, n_folds, lime_instances, permutation_repeats, eval_max_samples):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.RandomState(SEED)
    rows = []
    models = make_models()

    for dataset_name in datasets:
        X, y_raw = load_dataset(dataset_name)
        # XGBoost exige etiquetas numericas 0..K-1 (no strings como
        # "Pass"/"Fail"); se codifican para los 3 modelos por igual asi
        # el fold de train/test es identico entre modelos. class_names
        # (para LIME) usa las etiquetas originales para que se lea bien.
        label_encoder = LabelEncoder()
        y = pd.Series(label_encoder.fit_transform(y_raw), index=y_raw.index, name="target")
        class_names = label_encoder.classes_
        skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=SEED)

        for fold, (train_idx, test_idx) in enumerate(skf.split(X, y)):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

            for model_name, model in models.items():
                t0 = time.time()
                fitted = model.__class__(**model.get_params())
                fitted.fit(X_train, y_train)

                rankings = {
                    "shap": shap_ranking(fitted, model_name, X_train, X_test, eval_max_samples, rng),
                    "lime": lime_ranking(fitted, X_train, X_test, class_names, lime_instances, rng),
                    "permutation": permutation_ranking(fitted, X_test, y_test, permutation_repeats, eval_max_samples, rng),
                }

                for method, ranking in rankings.items():
                    ranked = ranking.sort_values(ascending=False)
                    for rank, (feat, val) in enumerate(ranked.items(), start=1):
                        rows.append({
                            "dataset": dataset_name, "model": model_name, "method": method,
                            "fold": fold, "feature": feat, "importance": val, "rank": rank,
                        })

                elapsed = time.time() - t0
                print(f"[{dataset_name}][fold {fold}][{model_name}] listo en {elapsed:.1f}s")

    out = pd.DataFrame(rows)
    out_path = RESULTS_DIR / "attributions_long.csv"
    out.to_csv(out_path, index=False)
    print(f"\nCompletado: {len(out)} filas guardadas en {out_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", nargs="+", default=DATASETS, choices=DATASETS)
    parser.add_argument("--folds", type=int, default=10)
    parser.add_argument("--lime-instances", type=int, default=100)
    parser.add_argument("--permutation-repeats", type=int, default=5)
    parser.add_argument("--eval-max-samples", type=int, default=2000)
    args = parser.parse_args()

    run(args.datasets, args.folds, args.lime_instances, args.permutation_repeats, args.eval_max_samples)


if __name__ == "__main__":
    main()
