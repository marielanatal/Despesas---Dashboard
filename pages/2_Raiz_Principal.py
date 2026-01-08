import streamlit as st
import plotly.express as px
from utils.load_data import load_data
from utils.metrics import resumo_por_grupo
from utils.formatters import format_brl, format_percent

# =========================
# DADOS
# =========================
df = load_data()
resumo = resumo_por_grupo(df, "RAIZ_PRINCIPAL")

# Ordenar por maior gasto em 2025
resumo = resumo.sort_values(2025, ascending=True)

st.markdown("## 🌳 Despesas por Raiz Principal")
st.markdown(
    "Comparação dos gastos por Raiz Principal, considerando **2024 como ano base** "
    "e **2025 como ano de comparação**."
)
st.markdown("---")

# =========================
# GRÁFICO (ORDEM CORRETA DE RENDERIZAÇÃO)
# =========================
fig = px.bar(
    resumo,
    y="RAIZ_PRINCIPAL",
    x=[2025, 2024],  # 👈 2025 DESENHADO PRIMEIRO (fica atrás)
    barmode="group",
    orientation="h",
    labels={
        "value": "Valor (R$)",
        "variable": "Ano"
    },
    color_discrete_map={
        2024: "#1f4fd8",  # azul escuro – ano base
        2025: "#8ec5ff"   # azul claro – ano atual
    }
)

fig.update_layout(
    legend_title_text="Ano",
    xaxis_tickformat=",.0f",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# TABELA ANALÍTICA
# =========================
tabela = resumo.copy()
tabela[2024] = tabela[2024].apply(format_brl)
tabela[2025] = tabela[2025].apply(format_brl)
tabela["Diferença (R$)"] = tabela["Diferença (R$)"].apply(format_brl)
tabela["Variação (%)"] = tabela["Variação (%)"].apply(format_percent)

st.markdown("### 📋 Visão Analítica por Raiz Principal")
st.dataframe(tabela, use_container_width=True)

