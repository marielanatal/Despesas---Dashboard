import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# =========================
# FORMATAÇÃO
# =========================
def format_percent(v):
    return f"{v:.1f}%"

def format_pp(v):
    sinal = "+" if v > 0 else ""
    return f"{sinal}{v:.1f} p.p."

# =========================
# CARREGAR DADOS
# =========================
df = pd.read_excel("custo_transferencia_2024_2025.xlsx")

df.columns = df.columns.str.strip().str.upper()

# Garantir coluna %
for col in df.columns:
    if "%" in col:
        df = df.rename(columns={col: "%"})

df["MÊS"] = df["MÊS"].astype(str).str.strip().str.capitalize()
df["ANO"] = pd.to_numeric(df["ANO"], errors="coerce")
df["%"] = pd.to_numeric(df["%"], errors="coerce")

# 🔴 AJUSTE DEFINITIVO DE ESCALA
df["%"] = df["%"] * 100

# =========================
# ORDEM DOS MESES
# =========================
ordem_meses = [
    "Maio", "Junho", "Julho",
    "Agosto", "Setembro", "Outubro", "Novembro"
]

df = df[df["MÊS"].isin(ordem_meses)]
df["MÊS"] = pd.Categorical(df["MÊS"], categories=ordem_meses, ordered=True)

# =========================
# PIVOT
# =========================
df_pivot = (
    df.pivot(index="MÊS", columns="ANO", values="%")
      .reset_index()
      .sort_values("MÊS")
)

# =========================
# MÉDIAS (AGORA EM % REAL)
# =========================
media_2024 = df_pivot[2024].mean()
media_2025 = df_pivot[2025].mean()
dif_pp = media_2025 - media_2024

# =========================
# HEADER
# =========================
st.markdown("## 🔄 Custo de Transferência – Comparativo Percentual")
st.markdown(
    "Comparação **mês a mês** do custo de transferência entre **2024 e 2025**, "
    "considerando apenas os meses de **Maio a Novembro**."
)
st.markdown("---")

# =========================
# KPIs
# =========================
c1, c2, c3 = st.columns(3)
c1.metric("Média 2024 (Mai–Nov)", format_percent(media_2024))
c2.metric("Média 2025 (Mai–Nov)", format_percent(media_2025))
c3.metric("Diferença Média", format_pp(dif_pp))

st.markdown("---")

# =========================
# GRÁFICO – BARRAS LADO A LADO
# =========================
st.markdown("### 📊 Comparativo Mensal – 2024 x 2025")

fig = go.Figure()

fig.add_bar(
    x=df_pivot["MÊS"],
    y=df_pivot[2024],
    name="2024",
    marker_color="#cfe8ff",
    text=[format_percent(v) for v in df_pivot[2024]],
    textposition="outside"
)

fig.add_bar(
    x=df_pivot["MÊS"],
    y=df_pivot[2025],
    name="2025",
    marker_color="#1f4fd8",
    text=[format_percent(v) for v in df_pivot[2025]],
    textposition="outside"
)

fig.update_layout(
    barmode="group",
    yaxis_title="Percentual (%)",
    xaxis_title="Mês",
    legend_title="Ano",
    bargap=0.25
)

fig.update_yaxes(
    ticksuffix="%",
    range=[
        0,
        max(df_pivot[2024].max(), df_pivot[2025].max()) * 1.25
    ]
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# TABELA COMPARATIVA
# =========================
st.markdown("### 📋 Tabela Comparativa – Percentual por Mês")

df_tabela = df_pivot.copy()
df_tabela["Diferença (p.p.)"] = df_tabela[2025] - df_tabela[2024]

df_tabela = df_tabela.rename(columns={
    2024: "2024 (%)",
    2025: "2025 (%)"
})

df_tabela["2024 (%)"] = df_tabela["2024 (%)"].map(format_percent)
df_tabela["2025 (%)"] = df_tabela["2025 (%)"].map(format_percent)
df_tabela["Diferença (p.p.)"] = df_tabela["Diferença (p.p.)"].map(format_pp)

st.dataframe(df_tabela, use_container_width=True)

