import streamlit as st
import plotly.express as px

from utils.load_data import load_data
from utils.load_faturamento import load_faturamento

# =========================
# FORMATAÇÃO
# =========================
def format_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percent(valor):
    return f"{valor*100:+.1f}%"

# =========================
# CSS (ANTI CORTE DE NÚMERO)
# =========================
st.markdown(
    """
    <style>
    .kpi-box {
        background-color: #f7f9fc;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
        white-space: nowrap;
    }
    .kpi-title {
        font-size: 14px;
        color: #6c757d;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 22px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# DADOS
# =========================
df_desp = load_data()
df_fat = load_faturamento()

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
    "Resumo consolidado de **Receita, Despesa e Resultado**, com comparação "
    "entre 2024 (ano base) e 2025."
)
st.markdown("---")

# =========================
# KPIs (VALOR INTEIRO)
# =========================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f"""
        <div class="kpi-box">
            <div class="kpi-title">📈 Receita 2024</div>
            <div class="kpi-value">{format_brl(fat_2024)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.caption(f"2025: {format_brl(fat_2025)} ({format_percent(var_fat)})")

with c2:
    st.markdown(
        f"""
        <div class="kpi-box">
            <div class="kpi-title">💸 Despesa 2024</div>
            <div class="kpi-value">{format_brl(desp_2024)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.caption(f"2025: {format_brl(desp_2025)} ({format_percent(var_desp)})")

with c3:
    st.markdown(
        f"""
        <div class="kpi-box">
            <div class="kpi-title">💰 Resultado 2024</div>
            <div class="kpi-value">{format_brl(res_2024)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.caption(f"2025: {format_brl(res_2025)} ({format_percent(var_res)})")

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

fig.update_yaxes(tickformat=",.0f")

st.plotly_chart(fig, use_container_width=True)

# =========================
# LEITURA EXECUTIVA
# =========================
if res_2025 > res_2024:
    st.success(
        f"💡 O resultado do negócio **melhorou em {format_percent(var_res)}** em 2025, "
        f"com faturamento total de {format_brl(fat_2025)} e despesas de {format_brl(desp_2025)}."
    )
else:
    st.error(
        f"⚠️ O resultado de 2025 ficou abaixo de 2024, mesmo com faturamento de "
        f"{format_brl(fat_2025)}, pressionado pelo nível de despesas."
    )

