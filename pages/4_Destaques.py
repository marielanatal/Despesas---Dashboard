import streamlit as st
from utils.load_data import load_data
from utils.metrics import resumo_por_grupo
from utils.formatters import format_brl

df = load_data()
resumo = resumo_por_grupo(df, "NATUREZA")

st.header("🔥 Destaques")

st.subheader("🚨 Maiores Aumentos")
st.dataframe(
    resumo.sort_values("Diferença (R$)", ascending=False).head(5),
    use_container_width=True
)

st.subheader("🟢 Maiores Reduções")
st.dataframe(
    resumo.sort_values("Diferença (R$)").head(5),
    use_container_width=True
)
