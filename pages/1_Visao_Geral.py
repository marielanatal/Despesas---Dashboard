import streamlit as st
import plotly.express as px

from utils.load_data import load_data
from utils.load_faturamento import load_faturamento

# =========================
# FUNÇÕES DE FORMATAÇÃO
# =========================
def format_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_mi(valor):
    return f"R$ {valor/1_000_000:,.1f} mi".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percent(valor):
    return f"{valor*100:+.1f}%"

# =========================
# CARREGAR DADOS
# =========================
df_desp = load_data()
df_fat = load_faturamento()

# =========================
# CONSOLIDAÇÃO ANUAL
# =========================
desp_2024 = df_desp[df_desp["ANO"] == 2024]["VALOR"].sum()
desp_2025 = df_desp[df_desp["ANO"] == 2025]["VALOR"].sum()

fat_2024 = df_fat[df_fat["Ano"] == 2024]["Faturamento - Valor"].sum()
fat_2025 = df_fat[df_fat["Ano"] == 2025]["Faturamento - Valor"].sum()

res_2024 = fat_2024 - desp_2024
res_2025 = fat_2025 - desp_2025

var_fat = (fat_2025 - fat_2024) / fat_2024 if fat_2024 else 0
var_desp = (desp_2025 - desp_2024) / desp_2024 if desp_2024 else 0
var_res = (res_2025 - res_2024) / abs(res_2024) if res_2024 else 0

# =========================
# HEADER
# =========================
st.markdown("## 📊 Visão Geral – Resultado do Negócio")
st.markdown(
    "Resumo consolidado de **Receita, Despesa e Resultado**, com análise comparativa "
    "entre 2024 (ano base) e 2025."
)
st.markdown("---")

# =========================
# KPIs
# =========================
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("📈 Receita 2024", format_mi(fat_2024))
    st.metric("📈 Receita 2025", format_mi(fat_2025))
    st.caption(f"Variação: {format_percent(var_fat)}")

with c2:
    st.metric("💸 Despesa 2024", format_mi(desp_2024))
    st.metric("💸 Despesa 2025", format_mi(desp_2025))
    st.caption(f"Variação: {format_percent(var_desp)}")

with c3:
    st.metric("💰 Resultado 2024", format_mi(res_2024))
    st.metric("💰 Resultado 2025", format_mi(res_2025))
    st.caption(f"Variação: {format_percent(var_res)}")

st.markdown("---")

# =========================
# EVOLUÇÃO MENSAL FATURAMENTO
# =========================
st.markdown("### 📈 Evolução Mensal do Faturamento")

fat_mensal = (
    df_fat
    .groupby(["Ano", "Mês"])["Faturamento - Valor"]
    .sum()
    .reset_index()
)

fig = px.line(
    fat_mensal,
    x="Mês",
    y="Faturamento - Valor",
    color="Ano",
    markers=True,
    color_discrete_map={
        2024: "#1f4fd8",
        2025: "#7fb3ff"
    },
    labels={
        "Faturamento - Valor": "Faturamento (R$)",
        "Mês": "Mês",
        "Ano": "Ano"
    }
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# LEITURA EXECUTIVA
# =========================
if res_2025 > res_2024:
    st.success(
        f"💡 O resultado do negócio **melhorou em {format_percent(var_res)}** em 2025, "
        f"impulsionado por faturamento de {format_brl(fat_2025)} frente a despesas de "
        f"{format_brl(desp_2025)}."
    )
else:
    st.error(
        f"⚠️ Apesar do faturamento de {format_brl(fat_2025)}, o resultado de 2025 "
        f"foi inferior ao de 2024, pressionado pelo nível de despesas."
    )
