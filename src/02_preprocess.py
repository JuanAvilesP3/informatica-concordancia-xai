"""
P10 - Concordancia entre metodos de explicabilidad
02_preprocess.py

Codificacion de categoricas, imputacion y escalado. Mismo
preprocesamiento para los 3 modelos (Random Forest, Gradient Boosting,
Regresion Logistica), para que la comparacion de metodos de
explicabilidad sea limpia (ver ficha tecnica, seccion 4).

Decision metodologica (confirmada con el responsable el 18/08): se
mantienen las clases originales de cada dataset, sin simplificar a
binario. OULAD queda con sus 4 clases (Pass, Fail, Withdrawn,
Distinction) y Dropout con sus 3 (Dropout, Enrolled, Graduate); German
Credit y Rice ya eran binarios de origen. Esto implica que
03_experiment.py debe manejar atribucion multiclase para SHAP/LIME en
esos dos datasets (documentar explicitamente como se agrega/reporta,
igual que la ficha pide documentar la agregacion de LIME).

Salidas: data/processed/{dataset}_X.csv, {dataset}_y.csv,
{dataset}_feature_names.json y el ColumnTransformer ajustado en
{dataset}_preprocessor.joblib (para reutilizar en 03_experiment.py).
"""

import json
import re
from pathlib import Path

import joblib
import pandas as pd
from scipy.io import arff
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
PROC_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

GERMAN_COLUMNS = [
    "checking_account_status", "duration_months", "credit_history", "purpose",
    "credit_amount", "savings_account", "employment_since", "installment_rate_pct",
    "personal_status_sex", "other_debtors", "residence_since", "property",
    "age_years", "other_installment_plans", "housing", "num_existing_credits",
    "job", "num_dependents", "telephone", "foreign_worker", "target_raw",
]


def _fit_transform_and_save(name: str, X: pd.DataFrame, y: pd.Series):
    numeric_cols = X.select_dtypes(include="number").columns.tolist()
    categorical_cols = X.select_dtypes(exclude="number").columns.tolist()

    numeric_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    categorical_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    preprocessor = ColumnTransformer([
        ("num", numeric_pipe, numeric_cols),
        ("cat", categorical_pipe, categorical_cols),
    ])

    X_proc = preprocessor.fit_transform(X)

    cat_feature_names = []
    if categorical_cols:
        cat_feature_names = list(
            preprocessor.named_transformers_["cat"]["onehot"].get_feature_names_out(categorical_cols)
        )
    feature_names = numeric_cols + cat_feature_names

    PROC_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(X_proc, columns=feature_names).to_csv(PROC_DIR / f"{name}_X.csv", index=False)
    y.to_csv(PROC_DIR / f"{name}_y.csv", index=False)
    joblib.dump(preprocessor, PROC_DIR / f"{name}_preprocessor.joblib")
    with open(PROC_DIR / f"{name}_feature_names.json", "w", encoding="utf-8") as f:
        json.dump(feature_names, f, ensure_ascii=False, indent=2)

    balance = y.value_counts(normalize=True).round(3).to_dict()
    print(f"[{name}] n={len(y)}, features_originales={X.shape[1]}, features_tras_encoding={len(feature_names)}, balance_clase_positiva={balance}")


def process_oulad():
    df = pd.read_csv(RAW_DIR / "oulad" / "studentInfo.csv")
    y = df["final_result"].rename("target")  # Pass / Fail / Withdrawn / Distinction
    X = df.drop(columns=["final_result", "id_student"])
    _fit_transform_and_save("oulad", X, y)


def process_dropout():
    df = pd.read_csv(RAW_DIR / "dropout" / "data.csv", sep=";", encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    y = df["Target"].rename("target")  # Dropout / Enrolled / Graduate
    X = df.drop(columns=["Target"])
    _fit_transform_and_save("dropout", X, y)


def process_german_credit():
    df = pd.read_csv(RAW_DIR / "german_credit" / "german.data", sep=" ", header=None, names=GERMAN_COLUMNS)
    y = (df["target_raw"] == 2).astype(int).rename("target")  # 2 = bad credit
    X = df.drop(columns=["target_raw"])
    _fit_transform_and_save("german_credit", X, y)


def process_rice():
    data, meta = arff.loadarff(RAW_DIR / "rice" / "Rice_Cammeo_Osmancik.arff")
    df = pd.DataFrame(data)
    df["Class"] = df["Class"].apply(lambda v: v.decode("utf-8") if isinstance(v, bytes) else v)
    y = (df["Class"] == "Osmancik").astype(int).rename("target")
    X = df.drop(columns=["Class"])
    _fit_transform_and_save("rice", X, y)


def main():
    process_oulad()
    process_dropout()
    process_german_credit()
    process_rice()
    print(f"\nCompletado. Datasets procesados en {PROC_DIR}")


if __name__ == "__main__":
    main()
