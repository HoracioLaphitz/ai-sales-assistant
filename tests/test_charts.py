import pytest
import pandas as pd
from plotly.graph_objects import Figure
from src.charts import bar_chart, line_chart, states_bar_chart


def test_bar_chart_returns_figure(sample_df):
    top = sample_df.groupby("product_category_name_english")["payment_value"].sum().reset_index()
    fig = bar_chart(top, x="product_category_name_english", y="payment_value", title="Test")
    assert isinstance(fig, Figure)


def test_bar_chart_has_data(sample_df):
    top = sample_df.groupby("product_category_name_english")["payment_value"].sum().reset_index()
    fig = bar_chart(top, x="product_category_name_english", y="payment_value", title="Test")
    assert len(fig.data) > 0


def test_line_chart_returns_figure(sample_df):
    monthly = sample_df.copy()
    monthly["month"] = monthly["order_purchase_timestamp"].dt.to_period("M").astype(str)
    agg = monthly.groupby("month")["payment_value"].sum().reset_index()
    fig = line_chart(agg, x="month", y="payment_value", title="Monthly")
    assert isinstance(fig, Figure)


def test_states_bar_chart_returns_figure(sample_df):
    by_state = sample_df.groupby("customer_state")["payment_value"].sum().reset_index()
    fig = states_bar_chart(by_state, state_col="customer_state", value_col="payment_value", title="States")
    assert isinstance(fig, Figure)
