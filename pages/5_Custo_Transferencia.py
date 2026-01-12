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

# Normalizar nomes de colunas
df.columns = df.columns.str.strip().str.upper()

# Renomear coluna de percentual (qualquer variação vira "%")
for col in df.columns:
    if "%" in col:
        df = df.rename(columns={col: "%"})

# Normalizar conteúdo
df["MÊS"] = (
    df["MÊS"]
    .astype(str)
    .str.strip()
    .str.capitalize()
)

df["ANO"] = pd.to_numeric(df["ANO"], errors="coerce")
df["%"] = pd.to_numeric(df["%"], errors="coerce")

# =========================
# MAPA DE MESES (ROBUSTO)
# =========================
mapa_meses = {
    "Maio": 5,
    "Junho": 6,
    "Julho": 7,
    "Agosto": 8,
    "Setembro": 9,
    "Outubro": 10,
    "Novembro": 11
}

df["ordem_mes"] = df["MÊS"].map(mapa_meses)

# Filtrar apenas meses válidos
df = df[df["ordem_mes"].notna()]

# =========================
# MÉDIA POR ANO
# =========================
media_ano = (
    df.groupby("ANO")["%"]
    .mean()
    .reset_index()
)

media_2024 = media_ano.loc[media_ano["ANO"] == 2024, "%"]
media_2025 = media_ano.loc[media_ano["ANO"] == 2025, "%"]

media_2024 = media_2024.values[0] if not media_2024.empty else None
media_2025 = media_2025.values[0] if not media_2025.empty else None

dif_pp = (media_2025 - media_2024) if media_2024 is not None and media_2025 is not None else 0

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

c1.metric(
    "Média 2024 (Mai–Nov)",
    format_percent(media_2024) if media_2024 is not None else "—"
)
c2.metric(
    "Média 2025 (Mai–Nov)",
    format_percent(media_2025) if media_2025 is not None else "—"
)
c3.metric(
    "Diferença Média",
    format_pp(dif_pp) if media_2024 is not None and media_2025 is not None else "—"
)

st.markdown("---")

# =========================
# GRÁFICO
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
# ALERTA
# =========================
if media_2024 is None or media_2025 is None:
    st.warning(
        "⚠️ Não foram encontrados dados completos para ambos os anos "
        "entre Maio e Novembro. Verifique a escrita dos meses e do ano na planilha."
    )
