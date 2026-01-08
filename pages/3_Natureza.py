import streamlit as st
import plotly.express as px
from utils.load_data import load_data
from utils.metrics import resumo_por_grupo
from utils.formatters import format_brl, format_percent

# =========================
# DADOS
# =========================
df = load_data()

st.markdown("## 🔍 Análise por Natureza")
st.markdown(
    "Detalhamento das despesas por **Natureza**, com comparação entre 2024 (ano base) "
    "e 2025 (ano de análise)."
)
st.markdown("---")

# =========================
# FILTRO
# =========================
raiz = st.selectbox(
    "Selecione a Raiz Principal",
    sorted(df["RAIZ_PRINCIPAL"].unique())
)

df_filtrado = df[df["RAIZ_PRINCIPAL"] == raiz]
resumo = resumo_por_grupo(df_filtrado, "NATUREZA")

# =========================
# INSIGHTS AUTOMÁTICOS
# =========================
crescimento = resumo.sort_values("Diferença (R$)", ascending=False).head(3)
reducao = resumo.sort_values("Diferença (R$)").head(3)

st.markdown("### 📌 Destaques do Período")

c1, c2 = st.columns(2)

with c1:
    st.error("🚨 Maiores Crescimentos")
    for _, row in crescimento.iterrows():
        st.markdown(
            f"- **{row['NATUREZA']}**  \n"
            f"  + {format_brl(row['Diferença (R$)'])} ({format_percent(row['Variação (%)'])})"
        )

with c2:
    st.success("🟢 Maiores Reduções")
    for _, row in reducao.iterrows():
        st.markdown(
            f"- **{row['NATUREZA']}**  \n"
            f"  {format_brl(row['Diferença (R$)'])} ({format_percent(row['Variação (%)'])})"
        )

st.markdown("---")

# =========================
# GRÁFICO
# =========================
# Ordenar por impacto em 2025
resumo = resumo.sort_values(2025, ascending=True)

fig = px.bar(
    resumo,
    y="NATUREZA",
    x=[2025, 2024],  # ordem de renderização correta
    barmode="group",
    orientation="h",
    labels={
        "value": "Valor (R$)",
        "variable": "Ano"
    },
    color_discrete_map={
        2024: "#1f4fd8",  # azul escuro
        2025: "#7fb3ff"   # azul claro
    }
)

# Forçar legenda: 2024 → 2025
fig.for_each_trace(
    lambda t: t.update(
        legendrank=1 if t.name == "2024" else 2
    )
)

fig.update_layout(
    legend_title_text="Ano",
    height=550,
    margin=dict(l=40, r=40, t=40, b=40)
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# TABELA ANALÍTICA
# =========================
st.markdown("### 📋 Visão Analítica Detalhada")

tabela = resumo.copy()
tabela[2024] = tabela[2024].apply(format_brl)
tabela[2025] = tabela[2025].apply(format_brl)
tabela["Diferença (R$)"] = tabela["Diferença (R$)"].apply(format_brl)
tabela["Variação (%)"] = tabela["Variação (%)"].apply(format_percent)

st.dataframe(tabela, use_container_width=True)
