import streamlit as st
import plotly.express as px
from utils.load_data import load_data
from utils.metrics import resumo_por_grupo
from utils.formatters import format_brl, format_percent

df = load_data()

raiz = st.selectbox(
    "Selecione a Raiz",
    sorted(df["RAIZ_PRINCIPAL"].unique())
)

df = df[df["RAIZ_PRINCIPAL"] == raiz]
resumo = resumo_por_grupo(df, "NATUREZA")

st.header("🔍 Detalhamento por Natureza")

fig = px.bar(resumo, x="NATUREZA", y=[2024, 2025], barmode="group")
st.plotly_chart(fig, use_container_width=True)

resumo[2024] = resumo[2024].apply(format_brl)
resumo[2025] = resumo[2025].apply(format_brl)
resumo["Diferença (R$)"] = resumo["Diferença (R$)"].apply(format_brl)
resumo["Variação (%)"] = resumo["Variação (%)"].apply(format_percent)

st.dataframe(resumo, use_container_width=True)
