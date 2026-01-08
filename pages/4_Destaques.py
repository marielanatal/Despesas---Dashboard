import streamlit as st
from utils.load_data import load_data
from utils.metrics import resumo_por_grupo
from utils.formatters import format_brl, format_percent

# =========================
# DADOS
# =========================
df = load_data()
resumo = resumo_por_grupo(df, "NATUREZA")

st.markdown("## 🔥 Resumo Executivo – Destaques")
st.markdown(
    "Principais **crescimentos e reduções de despesas** no comparativo "
    "entre 2024 (ano base) e 2025."
)
st.markdown("---")

# =========================
# TOP IMPACTOS
# =========================
top_aumento = resumo.sort_values("Diferença (R$)", ascending=False).head(5)
top_reducao = resumo.sort_values("Diferença (R$)").head(5)

c1, c2 = st.columns(2)

# 🔴 AUMENTOS
with c1:
    st.error("🚨 Maiores Aumentos de Despesa")
    for _, row in top_aumento.iterrows():
        st.markdown(
            f"""
            **{row['NATUREZA']}**  
            + {format_brl(row['Diferença (R$)'])}  
            ({format_percent(row['Variação (%)'])})
            """
        )

# 🟢 REDUÇÕES
with c2:
    st.success("🟢 Maiores Reduções de Despesa")
    for _, row in top_reducao.iterrows():
        st.markdown(
            f"""
            **{row['NATUREZA']}**  
            {format_brl(row['Diferença (R$)'])}  
            ({format_percent(row['Variação (%)'])})
            """
        )

st.markdown("---")

# =========================
# LEITURA EXECUTIVA
# =========================
qtd_total = resumo.shape[0]
qtd_reducao = (resumo["Diferença (R$)"] < 0).sum()
qtd_aumento = (resumo["Diferença (R$)"] > 0).sum()

st.info(
    f"📊 Do total de **{qtd_total} naturezas analisadas**, "
    f"**{qtd_reducao} apresentaram redução de custos** e "
    f"**{qtd_aumento} registraram aumento** no comparativo entre 2024 e 2025."
)

