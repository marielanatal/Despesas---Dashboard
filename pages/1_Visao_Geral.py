import streamlit as st
from utils.load_data import load_data
from utils.formatters import format_brl, format_percent

# =========================
# CONFIG VISUAL
# =========================
st.markdown(
    """
    <style>
    .kpi-box {
        background-color: #f7f9fc;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
    }
    .kpi-title {
        font-size: 14px;
        color: #6c757d;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        margin-top: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# DADOS
# =========================
df = load_data()

total_2024 = df[df["ANO"] == 2024]["VALOR"].sum()
total_2025 = df[df["ANO"] == 2025]["VALOR"].sum()

dif = total_2025 - total_2024
var = dif / total_2024 if total_2024 != 0 else 0

# =========================
# HEADER
# =========================
st.markdown("## 📊 Resumo Executivo das Despesas")
st.markdown("Comparativo consolidado entre os anos de 2024 e 2025.")

st.markdown("---")

# =========================
# KPIs
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.markdown(
    f"""
    <div class="kpi-box">
        <div class="kpi-title">Despesa Total 2024</div>
        <div class="kpi-value">{format_brl(total_2024)}</div>
    </div>
    """,
    unsafe_allow_html=True
)

c2.markdown(
    f"""
    <div class="kpi-box">
        <div class="kpi-title">Despesa Total 2025</div>
        <div class="kpi-value">{format_brl(total_2025)}</div>
    </div>
    """,
    unsafe_allow_html=True
)

c3.markdown(
    f"""
    <div class="kpi-box">
        <div class="kpi-title">Variação Absoluta</div>
        <div class="kpi-value">{format_brl(dif)}</div>
    </div>
    """,
    unsafe_allow_html=True
)

c4.markdown(
    f"""
    <div class="kpi-box">
        <div class="kpi-title">Variação Percentual</div>
        <div class="kpi-value">{format_percent(var)}</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# =========================
# LEITURA EXECUTIVA
# =========================
if dif < 0:
    st.success(
        f"📉 Em 2025 houve **redução de {format_brl(abs(dif))} ({format_percent(var)})** "
        "nas despesas totais em relação a 2024, indicando melhora no controle de gastos."
    )
else:
    st.error(
        f"📈 Em 2025 houve **aumento de {format_brl(dif)} ({format_percent(var)})** "
        "nas despesas totais em relação a 2024, exigindo atenção sobre os principais direcionadores de custo."
    )
