import streamlit as st
import plotly.express as px
import pandas as pd

# =========================
# FORMATAÇÃO
# =========================
def format_percent(valor):
    return f"{valor:.1f}%"

def format_pp(valor):
    sinal = "+" if valor > 0 else ""
    return f"{sinal}{valor:.1f} p.p."

# =========================
# CARREGAR DADOS
# =========================
df = pd.read_excel("custo_transferencia_2024_2025.xlsx")

# Normalizar colunas
df.columns = df.columns.str.strip().str.upper()

# Garantir coluna percentual como "%"
for col in df.columns:
    if "%" in col:
        df = df.rename(columns={col: "%"})

# Normalizar valores
df["MÊS"] = df["MÊS"].astype(str).str.strip().str.capitalize()
df["ANO"] = pd.to_numeric(df["ANO"], errors="coerce")
df["%"] = pd.to_numeric(df["%"], errors="coerce")

# =========================
# ORDEM DOS MESES
# =========================
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
df = df[df["ordem_mes"].notna()].sort_values("ordem_mes")

# =========================
# MÉDIAS (MAI–NOV)
# =========================
media_ano = df.groupby("ANO")["%"].mean().reset_index()

media_2024 = media_ano.loc[media_ano["ANO"] == 2024, "%"].values[0]
media_2025 = media_ano.loc[media_ano["ANO"] == 2025, "%"].values[0]
dif_pp = media_2025 - media_2024

# =========================
# HEADER
# =========================
st.markdown("## 🔄 Custo de Transferência – Análise Percentual")
st.markdown(
    "Comparação do **percentual de custo de transferência** entre 2024 e 2025, "
    "considerando **exclusivamente os meses de Maio a Novembro**."
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

fig = px.bar(
    df,
    x="MÊS",
    y="%",
    color="ANO",
    barmode="group",
    text="%",
    color_discrete_map={
        2024: "#cfe8ff",  # azul claro
        2025: "#1f4fd8"   # azul escuro
    },
    labels={
        "%": "Percentual (%)",
        "MÊS": "Mês",
        "ANO": "Ano"
    }
)

fig.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig.update_yaxes(
    ticksuffix="%",
    range=[0, max(df["%"]) * 1.25]
)

fig.update_layout(
    bargap=0.25,
    bargroupgap=0.1,
    legend_title_text="Ano"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# LEITURA EXECUTIVA
# =========================
if dif_pp < 0:
    st.success(
        f"📉 Considerando os meses de Maio a Novembro, o custo médio de transferência "
        f"reduziu de {format_percent(media_2024)} em 2024 para "
        f"{format_percent(media_2025)} em 2025 "
        f"({format_pp(dif_pp)})."
    )
else:
    st.error(
        f"📈 Considerando os meses de Maio a Novembro, o custo médio de transferência "
        f"aumentou de {format_percent(media_2024)} em 2024 para "
        f"{format_percent(media_2025)} em 2025 "
        f"({format_pp(dif_pp)})."
    )

