"""
P10 - Concordancia entre metodos de explicabilidad
05_figures.py

Las 4 figuras que pide la ficha tecnica (seccion 6), una por artefacto
(cada una con un panel 2x2 para los 4 datasets, salvo la Fig. 2 que ya
compara datasets directamente en un solo panel):

  Fig. 1 (la que sostiene el argumento): mapa de calor de tau de Kendall
         entre los 9 pares (modelo, metodo), promediado sobre folds.
  Fig. 2: diagramas de caja de tau por eje de comparacion (entre folds /
         entre metodos / entre modelos), agrupado por dataset.
  Fig. 3: top-10 de variables segun cada metodo (modelo random_forest),
         en 3 columnas paralelas con lineas conectando la misma variable.
  Fig. 4: tau medio por dataset y eje, con IC 95% bootstrap.
"""

import itertools
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import kendalltau

from figures_style import COLORS, apply_style, save_figure

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "tables"
FIG_DIR = Path(__file__).resolve().parent.parent / "results" / "figures"

MODELS = ["random_forest", "gradient_boosting", "logistic_regression"]
METHODS = ["shap", "lime", "permutation"]
DATASET_LABELS = {
    "oulad": "OULAD (educación)",
    "dropout": "Dropout (educación)",
    "german_credit": "German Credit (finanzas)",
    "rice": "Rice (agrícola)",
}
DATASETS = list(DATASET_LABELS.keys())


def get_ranking(df, dataset, model, method, fold):
    sub = df[(df.dataset == dataset) & (df.model == model) & (df.method == method) & (df.fold == fold)]
    return sub.set_index("feature")["rank"]


def truncate(label: str, n: int = 34) -> str:
    return label if len(label) <= n else label[: n - 1] + "…"


def fig1_heatmap(df):
    arms = list(itertools.product(MODELS, METHODS))
    arm_labels = [f"{m[:2].upper()}·{me[:4]}" for m, me in arms]

    fig, axes = plt.subplots(2, 2, figsize=(11, 10))
    for ax, dataset in zip(axes.flat, DATASETS):
        folds = sorted(df[df.dataset == dataset]["fold"].unique())
        n = len(arms)
        mat = np.full((n, n), np.nan)

        rankings_by_fold = {
            f: {arm: get_ranking(df, dataset, arm[0], arm[1], f) for arm in arms} for f in folds
        }

        for i, j in itertools.product(range(n), range(n)):
            if i == j:
                mat[i, j] = 1.0
                continue
            taus = []
            for f in folds:
                r1, r2 = rankings_by_fold[f][arms[i]], rankings_by_fold[f][arms[j]]
                common = r1.index.intersection(r2.index)
                if len(common) < 3:
                    continue
                tau, _ = kendalltau(r1.reindex(common), r2.reindex(common))
                taus.append(tau)
            mat[i, j] = np.mean(taus) if taus else np.nan

        im = ax.imshow(mat, vmin=-1, vmax=1, cmap="RdBu_r", interpolation="nearest")
        ax.set_xticks(range(n)); ax.set_xticklabels(arm_labels, rotation=90, fontsize=7)
        ax.set_yticks(range(n)); ax.set_yticklabels(arm_labels, fontsize=7)
        ax.grid(False)  # el grid global cae en el centro de cada celda (mismo problema que P8)
        ax.set_title(DATASET_LABELS[dataset], fontsize=10)
        for i, j in itertools.product(range(n), range(n)):
            ax.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center", fontsize=5.5,
                     color="white" if abs(mat[i, j]) > 0.6 else "black")

    fig.colorbar(im, ax=axes, shrink=0.7, label="τ de Kendall (promedio sobre folds)")
    fig.suptitle("Fig. 1 — Concordancia entre los 9 pares (modelo, método)", fontsize=12)
    save_figure(fig, FIG_DIR / "fig1_heatmap_tau")
    plt.close(fig)


def fig2_boxplots(detail):
    axis_order = ["entre_folds", "entre_metodos", "entre_modelos"]
    axis_labels = {"entre_folds": "Entre folds\n(mismo método)", "entre_metodos": "Entre métodos\n(mismo modelo)", "entre_modelos": "Entre modelos\n(mismo método)"}

    fig, ax = plt.subplots(figsize=(9, 5.5))
    width = 0.18
    palette = [COLORS["primary"], COLORS["secondary"], COLORS["neutral"], COLORS["accent"]]

    for d_idx, dataset in enumerate(DATASETS):
        positions = [i + (d_idx - 1.5) * width for i in range(len(axis_order))]
        data = [detail[(detail.dataset == dataset) & (detail.axis == axis)]["tau"].values for axis in axis_order]
        bp = ax.boxplot(data, positions=positions, widths=width * 0.9, patch_artist=True, showfliers=False)
        for box in bp["boxes"]:
            box.set_facecolor(palette[d_idx % len(palette)])
            box.set_alpha(0.8)
        for median in bp["medians"]:
            median.set_color("black")

    ax.set_xticks(range(len(axis_order)))
    ax.set_xticklabels([axis_labels[a] for a in axis_order])
    ax.set_ylabel("τ de Kendall")
    ax.set_ylim(-0.2, 1.05)
    ax.axhline(0, color="grey", linewidth=0.7)
    handles = [plt.Rectangle((0, 0), 1, 1, facecolor=palette[i], alpha=0.8) for i in range(len(DATASETS))]
    ax.legend(handles, [DATASET_LABELS[d] for d in DATASETS], fontsize=8, loc="lower left")
    ax.set_title("Fig. 2 — τ de Kendall por eje de comparación y dataset")
    save_figure(fig, FIG_DIR / "fig2_boxplots_ejes")
    plt.close(fig)


def fig3_top10_parallel(df):
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    model = "random_forest"

    for ax, dataset in zip(axes.flat, DATASETS):
        sub = df[(df.dataset == dataset) & (df.model == model)]
        mean_rank = sub.groupby(["method", "feature"])["rank"].mean().reset_index()

        top10 = {}
        for method in METHODS:
            m = mean_rank[mean_rank.method == method].nsmallest(10, "rank")
            top10[method] = list(m["feature"])

        for x, method in enumerate(METHODS):
            for y, feat in enumerate(top10[method]):
                ax.scatter(x, -y, color=COLORS["primary"], s=25, zorder=3)
                ha = "right" if x == 0 else ("left" if x == len(METHODS) - 1 else "center")
                offset = -0.08 if x == 0 else (0.08 if x == len(METHODS) - 1 else 0)
                ax.text(x + offset, -y, truncate(feat), fontsize=6.5, ha=ha, va="center")

        for x in range(len(METHODS) - 1):
            common = set(top10[METHODS[x]]) & set(top10[METHODS[x + 1]])
            for feat in common:
                y1 = top10[METHODS[x]].index(feat)
                y2 = top10[METHODS[x + 1]].index(feat)
                ax.plot([x, x + 1], [-y1, -y2], color=COLORS["secondary"], linewidth=1, alpha=0.7, zorder=1)

        ax.set_xlim(-2.1, len(METHODS) + 1.1)
        ax.set_ylim(-10, 1)
        ax.set_xticks(range(len(METHODS)))
        ax.set_xticklabels([m.upper() if m == "shap" else m.capitalize() for m in METHODS])
        ax.set_yticks([])
        ax.set_title(DATASET_LABELS[dataset], fontsize=10)
        for spine in ("left", "bottom"):
            ax.spines[spine].set_visible(False)

    fig.suptitle(f"Fig. 3 — Top-10 de variables por método (modelo: {model})", fontsize=12)
    save_figure(fig, FIG_DIR / "fig3_top10_paralelo")
    plt.close(fig)


def fig4_tau_por_dataset(summary):
    axis_order = ["entre_folds", "entre_metodos", "entre_modelos"]
    axis_labels = {"entre_folds": "Entre folds", "entre_metodos": "Entre métodos", "entre_modelos": "Entre modelos"}
    palette = {a: c for a, c in zip(axis_order, [COLORS["primary"], COLORS["secondary"], COLORS["neutral"]])}

    fig, ax = plt.subplots(figsize=(9, 5.5))
    width = 0.25
    x = np.arange(len(DATASETS))

    for i, axis in enumerate(axis_order):
        rows = summary[summary.axis == axis].set_index("dataset").reindex(DATASETS)
        means = rows["tau_mean"].values
        err_lo = means - rows["ci95_lo"].values
        err_hi = rows["ci95_hi"].values - means
        ax.bar(x + (i - 1) * width, means, width=width * 0.9, color=palette[axis], label=axis_labels[axis],
               yerr=[err_lo, err_hi], capsize=3)

    ax.set_xticks(x)
    ax.set_xticklabels([DATASET_LABELS[d] for d in DATASETS], rotation=15, ha="right")
    ax.set_ylabel("τ de Kendall medio (IC 95% bootstrap)")
    ax.axhline(0, color="grey", linewidth=0.7)
    ax.legend(fontsize=8)
    ax.set_title("Fig. 4 — τ de Kendall por dataset: ¿depende del dominio?")
    save_figure(fig, FIG_DIR / "fig4_tau_por_dataset")
    plt.close(fig)


def main():
    apply_style()
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(RESULTS_DIR / "attributions_long.csv")
    detail = pd.read_csv(RESULTS_DIR / "kendall_tau_detail.csv")
    summary = pd.read_csv(RESULTS_DIR / "kendall_tau_summary.csv")

    fig1_heatmap(df)
    print("Fig. 1 lista")
    fig2_boxplots(detail)
    print("Fig. 2 lista")
    fig3_top10_parallel(df)
    print("Fig. 3 lista")
    fig4_tau_por_dataset(summary)
    print("Fig. 4 lista")

    print(f"\nCompletado: 4 figuras guardadas en {FIG_DIR}")


if __name__ == "__main__":
    main()
