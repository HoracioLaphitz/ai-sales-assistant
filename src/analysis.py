import pandas as pd
from src.charts import bar_chart, line_chart, states_bar_chart


def run_analysis(df: pd.DataFrame) -> dict:
    total_revenue = round(df["payment_value"].sum(), 2)
    total_orders = df["order_id"].nunique()
    aov = round(total_revenue / total_orders, 2) if total_orders > 0 else 0.0

    monthly_agg = (
        df.assign(month=df["order_purchase_timestamp"].dt.to_period("M").astype(str))
        .groupby("month")["payment_value"].sum()
        .reset_index()
        .rename(columns={"payment_value": "revenue"})
        .sort_values("month")
    )
    fig_monthly = line_chart(monthly_agg, x="month", y="revenue", title="Revenue mensual (R$)")

    top_cats = (
        df.groupby("product_category_name_english")["payment_value"].sum()
        .reset_index()
        .rename(columns={"payment_value": "revenue"})
        .sort_values("revenue", ascending=False)
        .head(10)
    )
    fig_categories = bar_chart(top_cats, x="product_category_name_english", y="revenue",
                               title="Top 10 categorías por revenue (R$)")

    by_state = (
        df.groupby("customer_state")["payment_value"].sum()
        .reset_index()
        .rename(columns={"payment_value": "revenue"})
    )
    fig_states = states_bar_chart(by_state, state_col="customer_state",
                                  value_col="revenue", title="Revenue por estado (R$)")

    return {
        "kpis": {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "aov": aov,
        },
        "figs": {
            "monthly": fig_monthly,
            "categories": fig_categories,
            "states": fig_states,
        },
    }
