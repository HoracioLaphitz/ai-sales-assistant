import os
import pandas as pd


def load_data(data_dir: str = "data") -> pd.DataFrame:
    orders = pd.read_csv(os.path.join(data_dir, "olist_orders_dataset.csv"),
                         parse_dates=["order_purchase_timestamp"])
    items = pd.read_csv(os.path.join(data_dir, "olist_order_items_dataset.csv"))
    products = pd.read_csv(os.path.join(data_dir, "olist_products_dataset.csv"))
    translation = pd.read_csv(os.path.join(data_dir, "olist_product_category_name_translation.csv"))
    payments = pd.read_csv(os.path.join(data_dir, "olist_order_payments_dataset.csv"))
    customers = pd.read_csv(os.path.join(data_dir, "olist_customers_dataset.csv"))

    products = products.merge(translation, on="product_category_name", how="left")

    payments_agg = (
        payments.groupby("order_id")["payment_value"].sum().reset_index()
    )

    items_agg = (
        items.groupby("order_id")
        .agg(price=("price", "sum"), freight_value=("freight_value", "sum"), product_id=("product_id", "first"))
        .reset_index()
    )

    df = (
        orders[orders["order_status"] == "delivered"]
        .merge(items_agg, on="order_id", how="left")
        .merge(products[["product_id", "product_category_name_english"]], on="product_id", how="left")
        .merge(payments_agg, on="order_id", how="left")
        .merge(customers[["customer_id", "customer_state"]], on="customer_id", how="left")
    )

    return df[[
        "order_id", "order_purchase_timestamp", "order_status",
        "price", "freight_value", "payment_value",
        "product_category_name_english", "customer_state",
    ]].reset_index(drop=True)
