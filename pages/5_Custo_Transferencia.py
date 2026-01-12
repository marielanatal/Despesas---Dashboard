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

# Normalizar colunas
df.columns = df.columns.str.strip().str.upper()

# Garantir coluna de percentual como "%"
for col in df.columns:
    if "%" in col:
        df = df.rename(columns={col: "%"})

# Normalizar conteúdo
df["MÊS"] = df["MÊS"].astype(str).str.strip().str.capitalize()
df["ANO"] = pd.to_numeric(df["ANO"], errors="coerce")
df["%"] = pd.to_numeric(df["%"], errors="coerce")

# =========================
# MAPA E ORDEM DOS MESES
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
df = df[df["ordem_mes"].notna()].sort_values("ordem_mes")

# =========================
# MÉDIAS (SOMENTE MAI–NOV)
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

dif_pp = (
    media_2025 - media_2024
    if media_2024 is not None and media_2025 is not None
    else None
)

# =========================
# HEADER
# =========================
st.markdown("## 🔄 Custo de Transferência – Análise Percentual")
st.markdown(
    "Comparação do **percentual de custo de transferência** entre 2024 e 2025, "
    "considerando **exclusivamente os meses de Maio a Novembro**, disponíveis em ambos os anos."
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
    format_pp(dif_pp) if dif_pp is not None else "—"
)

st.markdown("---")

# =========================
# GRÁFICO – BARRAS COMPARATIVAS
# =========================
st.markdown("### 📊 Comparativo Mensal – 2024 x 2025")

fig = px.bar(
    df,
    x="MÊS",
    y="%",
    color="ANO",
    barmode="group",
    text_auto=".2f",
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

# =========================
# LINHAS DE MÉDIA
# =========================
if media_2024 is not None:
    fig.add_hline(
        y=media_2024,
        line_dash="dot",
        line_color="#1f4fd8",
        annotation_text="Média 2024",
        annotation_position="top left"
    )

if media_2025 is not None:
    fig.add_hline(
        y=media_2025,
        line_dash="dot",
        line_color="#7fb3ff",
        annotation_text="Média 2025",
        annotation_position="top right"
    )

# =========================
# DESTAQUE VISUAL (MELHOR / PIOR)
# =========================
df_pivot = df.pivot(index="MÊS", columns="ANO", values="%").reset_index()

for _, row in df_pivot.iterrows():
    if 2024 in row and 2025 in row:
        if row[2025] < row[2024]:
            fig.add_annotation(
                x=row["MÊS"],
                y=max(row[2024], row[2025]),
                text="⬇",
                showarrow=False,
                font=dict(color="green", size=16)
            )
        elif row[2025] > row[2024]:
            fig.add_annotation(
                x=row["MÊS"],
                y=max(row[2024], row[2025]),
                text="⬆",
                showarrow=False,
                font=dict(color="red", size=16)
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
if media_2024 is None or media_2025 is None:
    st.warning(
        "⚠️ Não foi possível calcular a média de ambos os anos. "
        "Verifique se há dados para 2024 e 2025 entre Maio e Novembro."
    )
else:
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

