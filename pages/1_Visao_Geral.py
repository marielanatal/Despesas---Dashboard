import streamlit as st
from utils.load_data import load_data

# =========================
# FUNÇÕES DE FORMATAÇÃO
# =========================
def format_mi(valor):
    return f"R$ {valor/1_000_000:,.1f} mi".replace(",", "X").replace(".", ",").replace("X", ".")

def format_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percent(valor):
    return f"{valor*100:+.1f}%"

# =========================
# CSS
# =========================
st.markdown(
    """
    <style>
    .kpi-box {
        background-color: #f7f9fc;
        padding: 22px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
        white-space: nowrap;
    }
    .kpi-title {
        font-size: 14px;
        color: #6c757d;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 700;
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
# KPIs (VALORES RESUMIDOS)
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.markdown(
    f"""
    <div class="kpi-box">
        <div class="kpi-title">Despesa Total 2024</div>
        <div class="kpi-value">{format_mi(total_2024)}</div>
    </div>
    """,
    unsafe_allow_html=True
)

c2.markdown(
    f"""
    <div class="kpi-box">
        <div class="kpi-title">Despesa Total 2025</div>
        <div class="kpi-value">{format_mi(total_2025)}</div>
    </div>
    """,
    unsafe_allow_html=True
)

c3.markdown(
    f"""
    <div class="kpi-box">
        <div class="kpi-title">Variação Absoluta</div>
        <div class="kpi-value">{format_mi(dif)}</div>
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
# LEITURA EXECUTIVA (VALOR CHEIO)
# =========================
if dif < 0:
    st.success(
        f"📉 Em 2025 houve **redução de {format_brl(abs(dif))} ({format_percent(var)})** "
        f"nas despesas totais em relação a 2024, passando de "
        f"{format_brl(total_2024)} para {format_brl(total_2025)}."
    )
else:
    st.error(
        f"📈 Em 2025 houve **aumento de {format_brl(dif)} ({format_percent(var)})** "
        f"nas despesas totais em relação a 2024."
    )
