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

# Padronizar tipos
df["ANO"] = df["ANO"].astype(int)
df["%"] = pd.to_numeric(df["%"], errors="coerce")

# =========================
# FILTRAR MESES COMPARÁVEIS (MAIO A NOVEMBRO)
# =========================
meses_validos = ["Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro"]

df = df[df["MÊS"].isin(meses_validos)]

# Garantir ordem correta dos meses no gráfico
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
# MÉDIA POR ANO (SOMENTE MESES DISPONÍVEIS)
# =========================
media_ano = (
    df.groupby("ANO")["%"]
    .mean()
    .reset_index()
)

media_2024 = media_ano.loc[media_ano["ANO"] == 2024, "%"].values[0]
media_2025 = media_ano.loc[media_ano["ANO"] == 2025, "%"].values[0]

dif_pp = media_2025 - media_2024

# =========================
# HEADER
# =========================
st.markdown("## 🔄 Custo de Transferência – Análise Percentual")
st.markdown(
    "Comparação do **percentual de custo de transferência** entre 2024 e 2025, "
    "considerando **apenas os meses de Maio a Novembro**, disponíveis em ambos os anos."
)
st.markdown("---")

# =========================
# KPIs (MÉDIA DO PERÍODO)
# =========================
c1, c2, c3 = st.columns(3)

c1.metric("Média 2024 (Mai–Nov)", format_percent(media_2024))
c2.metric("Média 2025 (Mai–Nov)", format_percent(media_2025))
c3.metric("Diferença Média", format_pp(dif_pp))

st.markdown("---")

# =========================
# GRÁFICO MÊS A MÊS
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
        2024: "#1f4fd8",  # azul escuro
        2025: "#7fb3ff"   # azul claro
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
# LEITURA EXECUTIVA
# =========================
if dif_pp < 0:
    st.success(
        f"📉 Considerando os meses de Maio a Novembro, o custo médio de transferência "
        f"**reduziu de {format_percent(media_2024)} em 2024 para "
        f"{format_percent(media_2025)} em 2025**, representando uma melhora de "
        f"{format_pp(dif_pp)}."
    )
else:
    st.error(
        f"📈 Considerando os meses de Maio a Novembro, o custo médio de transferência "
        f"**aumentou de {format_percent(media_2024)} em 2024 para "
        f"{format_percent(media_2025)} em 2025**, com piora de "
        f"{format_pp(dif_pp)}."
    )
