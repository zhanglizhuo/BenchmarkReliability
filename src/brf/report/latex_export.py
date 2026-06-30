def export_latex(brf_vector: dict) -> str:
    lines = [
        r"\begin{tabular}{lcc}",
        r"\toprule",
        r"Dimension & Value & Interpretation \\",
        r"\midrule",
        f"B (Baseline Gain) & {brf_vector['B']:.3f} & Model improvement over mean predictor \\\\",
        f"I (Instability) & {brf_vector['I']:.3f} & Sensitivity to split choice \\\\",
        f"N (Null Separability) & {brf_vector['N']:.3f} & Signal distinguishability from noise \\\\",
        f"M (Metadata Sufficiency) & {brf_vector['M']:.3f} & Group structure completeness \\\\",
        r"\midrule",
        f"S (Signal Identifiability) & {brf_vector['S']:.3f} & N - I \\\\",
        f"E (Epistemic Completeness) & {brf_vector['E']:.3f} & B + M \\\\",
        r"\midrule",
        f"Class & \\multicolumn{{2}}{{c}}{{{brf_vector['class']}}} \\\\",
        r"\bottomrule",
        r"\end{tabular}",
    ]
    return "\n".join(lines)
