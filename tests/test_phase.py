import numpy as np
import pytest

from brf.phase import compute_phase_from_brf, classify_dataset, plot_phase_diagram
from brf.report import export_json, export_latex


class TestEmbedding:
    def test_phase_coordinates(self):
        S, E = compute_phase_from_brf(B=1.0, I=0.01, N=1.0, M=0.7)
        assert S == 0.99
        assert E == 1.70


class TestClassifier:
    def test_reliable(self):
        assert classify_dataset(S=1.0, E=0.8) == "Reliable"

    def test_fragile(self):
        assert classify_dataset(S=0.3, E=0.2) == "Fragile"

    def test_void_due_to_negative_s(self):
        assert classify_dataset(S=-0.1, E=0.8) == "Void"

    def test_void_due_to_zero_s(self):
        assert classify_dataset(S=0.0, E=0.8) == "Void"

    def test_custom_thresholds(self):
        assert classify_dataset(S=0.1, E=0.6, tau_s=0.2) == "Void"
        assert classify_dataset(S=0.5, E=0.4, tau_e=0.5) == "Fragile"

    def test_edge_case_boundary(self):
        assert classify_dataset(S=0.5, E=0.5) == "Fragile"


class TestReport:
    def test_export_json_none_raises(self):
        with pytest.raises(ValueError, match="None"):
            export_json({"B": None, "I": 0.5}, "dummy.json")

    def test_export_latex_none_raises(self):
        with pytest.raises(ValueError, match="None"):
            export_latex({"B": None, "I": 0.5})

    def test_export_json_roundtrip(self, tmp_path):
        p = str(tmp_path / "test.json")
        bv = {"B": 0.8, "I": 0.1, "N": 0.95, "M": 0.5, "S": 0.85, "E": 1.3, "class": "Reliable"}
        export_json(bv, p)
        import json
        with open(p) as f:
            loaded = json.load(f)
        assert loaded == bv

    def test_export_latex_output(self):
        bv = {"B": 0.8, "I": 0.1, "N": 0.95, "M": 0.5, "S": 0.85, "E": 1.3, "class": "Reliable"}
        out = export_latex(bv)
        assert "tabular" in out
        assert "Reliable" in out
        assert "0.800" in out


class TestVisualization:
    def test_plot_returns_figure(self):
        fig = plot_phase_diagram(
            S_list=[0.9, 0.3, -0.5],
            E_list=[1.5, 0.2, 0.8],
            labels=["A", "B", "C"],
        )
        assert fig is not None

    def test_plot_without_labels(self):
        fig = plot_phase_diagram(
            S_list=[0.5, 0.0],
            E_list=[0.6, 1.0],
        )
        assert fig is not None

    def test_plot_custom_thresholds(self):
        fig = plot_phase_diagram(
            S_list=[0.9, -0.1],
            E_list=[0.6, 0.4],
            tau_s=0.1,
            tau_e=0.3,
        )
        assert fig is not None

    def test_plot_save_path(self, tmp_path):
        from pathlib import Path
        save_path = str(tmp_path / "phase.png")
        fig = plot_phase_diagram(
            S_list=[0.5, 0.0],
            E_list=[0.6, 1.0],
            save_path=save_path,
        )
        assert Path(save_path).exists()
        assert fig is not None
