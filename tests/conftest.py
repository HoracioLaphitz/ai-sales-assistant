import pytest
import pandas as pd
from datetime import datetime


@pytest.fixture
def sample_df():
    """DataFrame con el schema exacto que produce load_data()."""
    return pd.DataFrame({
        "order_id": ["o1", "o1", "o2", "o2", "o3"],
        "order_purchase_timestamp": [
            datetime(2018, 1, 15),
            datetime(2018, 1, 15),
            datetime(2018, 3, 10),
            datetime(2018, 3, 10),
            datetime(2018, 6, 5),
        ],
        "order_status": ["delivered", "delivered", "delivered", "delivered", "delivered"],
        "price": [100.0, 50.0, 200.0, 80.0, 150.0],
        "freight_value": [10.0, 5.0, 20.0, 8.0, 15.0],
        "payment_value": [110.0, 55.0, 220.0, 88.0, 165.0],
        "product_category_name_english": [
            "electronics", "books", "electronics", "furniture", "books"
        ],
        "customer_state": ["SP", "RJ", "SP", "MG", "RJ"],
    })
