import streamlit as st
import plotly.express as px
import pandas as pd

# =========================
# FORMATAÇÃO
# =========================
def format_percent(valor):
    return f"{valor:.2f}%"

def format_pp(valor):
    sinal = "+" if valor > 0 else ""
    return f"{sinal}{valor:.2f} p.p."

# =========================
# CARREGAR DADOS
# =========================
df = pd.read_excel("custo_transferencia_2024_2025.xlsx")
df.columns = df.columns.str.strip()

# Tipos
df["ANO"] = df["ANO"].astype(int)
df["%"] = pd.to_numeric(df["%"], errors="coerce")

# =========================
# FILTRO DE MESES (MAIO–NOV)
# =========================
meses_validos = ["Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro"]

df = df[df["MÊS"].isin(meses_validos)]

# Ordem correta dos meses
ordem_meses = {
    "Maio": 5,
    "Junho": 6,
    "Julho": 7,
    "Agosto": 8,
    "Setembro": 9,
    "Outubro": 10,
    "Novembro": 11
}
df["ordem_mes"] = df["MÊS"].map(ordem_meses)

# =========================
# MÉDIA POR ANO (SEGURO)
# =========================
media_ano = (
    df.groupby("ANO")["%"]
    .mean()
    .reset_index()
)

media_2024 = media_ano.loc[media_ano["ANO"] == 2024, "%"]
media_2025 = media_ano.loc[media_ano["ANO"] == 2025, "%"]

media_2024 = media_2024.values[0] if not media_2024.empty else 0
media_2025 = media_2025.values[0] if not media_2025.empty else 0

dif_pp = media_2025 - media_2024

# =========================
# HEADER
# =========================
st.markdown("## 🔄 Custo de Transferência – Análise Percentual")
st.markdown(
    "Comparação do **percentual de custo de transferência** entre 2024 e 2025, "
    "considerando **apenas os meses de Maio a Novembro**."
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
# GRÁFICO MENSAL
# =========================
st.markdown("### 📈 Evolução Mensal – Comparação 2024 x 2025")

df = df.sort_values("ordem_mes")

fig = px.line(
    df,
    x="MÊS",
    y="%",
    color="ANO",
    markers=True,
    color_discrete_map={
        2024: "#1f4fd8",
        2025: "#7fb3ff"
    },
    labels={
        "%": "Percentual (%)",
        "MÊS": "Mês",
        "ANO": "Ano"
    }
)

fig.update_yaxes(ticksuffix="%")

st.plotly_chart(fig, use_container_width=True)

# =========================
# ALERTA SE FALTAR DADO
# =========================
if media_2024 == 0 or media_2025 == 0:
    st.warning(
        "⚠️ Atenção: algum ano não possui todos os meses disponíveis "
        "entre Maio e Novembro. A média foi calculada apenas com os dados existentes."
    )
