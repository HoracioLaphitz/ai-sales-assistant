import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def bar_chart(df: pd.DataFrame, x: str, y: str, title: str) -> go.Figure:
    fig = px.bar(df, x=x, y=y, title=title, color=y,
                 color_continuous_scale="Blues")
    fig.update_layout(showlegend=False, coloraxis_showscale=False,
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig


def line_chart(df: pd.DataFrame, x: str, y: str, title: str) -> go.Figure:
    fig = px.line(df, x=x, y=y, title=title, markers=True)
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig


def choropleth_brazil(df: pd.DataFrame, state_col: str, value_col: str, title: str) -> go.Figure:
    # Brazilian state codes in Olist are 2-letter (SP, RJ) — use bar chart as reliable fallback
    # since Plotly choropleth requires GeoJSON for subnational Brazil regions
    return bar_chart(
        df.sort_values(value_col, ascending=False),
        x=state_col,
        y=value_col,
        title=title,
    )
