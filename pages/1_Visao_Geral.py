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
# CSS GLOBAL
# =========================
st.markdown(
    """
    <style>
    .kpi-box {
        background-color: #f7f9fc;
        padding: 18px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
    }
    .kpi-title {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .kpi-year {
        font-size: 13px;
        color: #6c757d;
        margin-top: 6px;
    }
    .kpi-value {
        font-size: 22px;
        font-weight: 700;
    }
    .kpi-delta {
        font-size: 13px;
        margin-top: 8px;
        color: #495057;
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
    "Comparação direta entre **2024 (ano base)** e **2025**, considerando "
    "Receita, Despesa e Resultado."
)
st.markdown("---")

# =========================
# KPIs
# =========================
c1, c2, c3 = st.columns(3)

def render_kpi(col, titulo, v24, v25, var):
    col.html(
        f"""
        <div class="kpi-box">
            <div class="kpi-title">{titulo}</div>

            <div class="kpi-year">2024</div>
            <div class="kpi-value">{format_brl(v24)}</div>

            <div class="kpi-year">2025</div>
            <div class="kpi-value">{format_brl(v25)}</div>

            <div class="kpi-delta">
                Variação: {format_percent(var)}
            </div>
        </div>
        """
    )

render_kpi(c1, "📈 Receita", fat_2024, fat_2025, var_fat)
render_kpi(c2, "💸 Despesa", desp_2024, desp_2025, var_desp)
render_kpi(c3, "💰 Resultado", res_2024, res_2025, var_res)

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
