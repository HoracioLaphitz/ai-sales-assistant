import pytest
import plotly.graph_objects as go
from src.analysis import run_analysis


def test_run_analysis_returns_dict(sample_df):
    result = run_analysis(sample_df)
    assert isinstance(result, dict)
    assert "kpis" in result
    assert "figs" in result


def test_kpis_total_revenue(sample_df):
    result = run_analysis(sample_df)
    expected = round(sample_df["payment_value"].sum(), 2)
    assert abs(result["kpis"]["total_revenue"] - expected) < 0.01


def test_kpis_total_orders(sample_df):
    result = run_analysis(sample_df)
    expected = sample_df["order_id"].nunique()
    assert result["kpis"]["total_orders"] == expected


def test_kpis_aov(sample_df):
    result = run_analysis(sample_df)
    expected = round(sample_df["payment_value"].sum() / sample_df["order_id"].nunique(), 2)
    assert abs(result["kpis"]["aov"] - expected) < 0.01


def test_figs_are_plotly_figures(sample_df):
    result = run_analysis(sample_df)
    for key in ("monthly", "categories", "states"):
        assert key in result["figs"]
        assert isinstance(result["figs"][key], go.Figure)
