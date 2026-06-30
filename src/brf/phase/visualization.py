from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np


def plot_phase_diagram(
    S_list: List[float],
    E_list: List[float],
    labels: Optional[List[str]] = None,
    classes: Optional[List[str]] = None,
    title: str = "BRF Phase Diagram",
    save_path: Optional[str] = None,
):
    fig, ax = plt.subplots(figsize=(8, 6))

    if classes is not None:
        color_map = {"Reliable": "#2ecc71", "Fragile": "#f39c12", "Void": "#e74c3c"}
        for cls in set(classes):
            mask = [c == cls for c in classes]
            ax.scatter(
                np.array(S_list)[mask],
                np.array(E_list)[mask],
                c=color_map.get(cls, "#95a5a6"),
                label=cls,
                s=80,
                edgecolors="black",
                linewidths=0.5,
                alpha=0.8,
            )
        ax.legend(fontsize=12)
    else:
        ax.scatter(S_list, E_list, c="#3498db", s=80, edgecolors="black", linewidths=0.5)

    if labels:
        for i, label in enumerate(labels):
            ax.annotate(label, (S_list[i], E_list[i]), fontsize=8, alpha=0.8)

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.4, label="E = 0.5 (Fragile boundary)")
    ax.axvline(x=0.0, color="gray", linestyle="--", alpha=0.4, label="S = 0.0 (Void boundary)")

    ax.set_xlabel("Signal Identifiability (S = N - I)", fontsize=12)
    ax.set_ylabel("Epistemic Completeness (E = B + M)", fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.grid(True, alpha=0.3)

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig
