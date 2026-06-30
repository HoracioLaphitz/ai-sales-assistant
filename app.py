import os
import streamlit as st
from src.loader import load_data
from src.analysis import run_analysis
from src.agent import build_agent, ask

st.set_page_config(
    page_title="AI Sales Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Sales Assistant")
st.caption("Olist Brazilian E-Commerce · LangChain + Groq llama3-70b · [Código en GitHub](https://github.com/horaciolaphitz)")


@st.cache_data
def get_data():
    return load_data("data")


@st.cache_resource
def get_agent(_df, api_key):
    return build_agent(_df, api_key)


api_key = os.environ.get("GROQ_API_KEY", "")

if not api_key:
    st.error("❌ GROQ_API_KEY no encontrada. Configurá la variable de entorno GROQ_API_KEY antes de correr la app.")
    st.stop()

with st.spinner("Cargando datos de Olist (~100k órdenes)..."):
    df = get_data()

analysis = run_analysis(df)
kpis = analysis["kpis"]
figs = analysis["figs"]

tab1, tab2 = st.tabs(["📊 Análisis", "💬 Preguntas"])

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue Total", f"R$ {kpis['total_revenue']:,.0f}")
    col2.metric("Órdenes entregadas", f"{kpis['total_orders']:,}")
    col3.metric("Ticket promedio (AOV)", f"R$ {kpis['aov']:,.2f}")

    st.divider()

    st.plotly_chart(figs["monthly"], use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(figs["categories"], use_container_width=True)
    with col_b:
        st.plotly_chart(figs["states"], use_container_width=True)

with tab2:
    st.markdown("**Preguntale al assistant sobre los datos de ventas:**")

    example_questions = [
        "¿Cuál fue el mes con más revenue?",
        "¿Cuáles son los 5 estados con más órdenes?",
        "¿Cuál es el ticket promedio por categoría de producto?",
        "¿Qué porcentaje de órdenes tiene más de R$ 200 en precio?",
    ]
    with st.expander("💡 Ejemplos de preguntas"):
        for q in example_questions:
            st.markdown(f"- {q}")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Escribí tu pregunta..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analizando..."):
                agent = get_agent(df, api_key)
                result = ask(agent, prompt)

            st.markdown(result["answer"])

            if result["intermediate_steps"]:
                with st.expander("🔍 Ver código Pandas generado"):
                    for action, observation in result["intermediate_steps"]:
                        if hasattr(action, "tool_input"):
                            st.code(action.tool_input, language="python")
                        st.markdown(f"**Resultado:** `{str(observation)[:200]}`")

        st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
