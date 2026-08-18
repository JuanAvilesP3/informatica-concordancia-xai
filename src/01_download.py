"""
P10 - Concordancia entre metodos de explicabilidad
01_download.py

Descarga los 4 datasets tabulares de dominios distintos (ver ficha
tecnica, seccion 3) desde el UCI Machine Learning Repository, que los
aloja a los cuatro de forma directa y estable:

  - OULAD (educacion)                         -> UCI id 349
  - Predict Students' Dropout... (educacion)   -> UCI id 697
  - Statlog German Credit Data (finanzas)      -> UCI id 144
  - Rice (Cammeo and Osmancik) (agricola)      -> UCI id 545

Se eligio Rice como el "cuarto dataset ambiental o agricola tabular"
que pide la ficha: clasificacion binaria de variedad de arroz a partir
de features morfometricas, 3810 instancias.
"""

import io
import zipfile
from pathlib import Path

import requests

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

DATASETS = {
    "oulad": {
        "url": "https://archive.ics.uci.edu/static/public/349/open+university+learning+analytics+dataset.zip",
        "domain": "educacion",
    },
    "dropout": {
        "url": "https://archive.ics.uci.edu/static/public/697/predict+students+dropout+and+academic+success.zip",
        "domain": "educacion",
    },
    "german_credit": {
        "url": "https://archive.ics.uci.edu/static/public/144/statlog+german+credit+data.zip",
        "domain": "finanzas",
    },
    "rice": {
        "url": "https://archive.ics.uci.edu/static/public/545/rice+cammeo+and+osmancik.zip",
        "domain": "agricola",
    },
}


def download_and_extract(name: str, url: str, domain: str):
    out_dir = RAW_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{name}] ({domain}) descargando {url}")
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        zf.extractall(out_dir)

    files = sorted(p.name for p in out_dir.rglob("*") if p.is_file())
    print(f"[{name}] {len(files)} archivo(s) extraído(s): {files[:6]}{'...' if len(files) > 6 else ''}")


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for name, meta in DATASETS.items():
        download_and_extract(name, meta["url"], meta["domain"])
    print("\nCompletado: 4 datasets descargados en data/raw/")


if __name__ == "__main__":
    main()
