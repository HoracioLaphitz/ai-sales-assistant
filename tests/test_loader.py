import pytest
import os
from src.loader import load_data

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


def test_load_data_returns_dataframe():
    df = load_data(FIXTURES)
    assert df is not None
    assert len(df) > 0


def test_load_data_filters_delivered_only():
    df = load_data(FIXTURES)
    assert (df["order_status"] == "delivered").all()


def test_load_data_has_required_columns():
    df = load_data(FIXTURES)
    required = {
        "order_id", "order_purchase_timestamp", "order_status",
        "price", "freight_value", "payment_value",
        "product_category_name_english", "customer_state",
    }
    assert required.issubset(set(df.columns))


def test_load_data_parses_timestamps():
    df = load_data(FIXTURES)
    import pandas as pd
    assert pd.api.types.is_datetime64_any_dtype(df["order_purchase_timestamp"])


def test_load_data_payment_value_numeric():
    df = load_data(FIXTURES)
    assert df["payment_value"].dtype in ["float64", "float32"]
