import streamlit as st
from utils.load_data import load_data
from utils.formatters import format_brl, format_percent

df = load_data()

total_2024 = df[df["ANO"] == 2024]["VALOR"].sum()
total_2025 = df[df["ANO"] == 2025]["VALOR"].sum()

dif = total_2025 - total_2024
var = dif / total_2024 if total_2024 != 0 else 0

st.header("📊 Visão Geral")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Despesa 2024", format_brl(total_2024))
c2.metric("Despesa 2025", format_brl(total_2025))
c3.metric("Diferença", format_brl(dif))
c4.metric("Variação", format_percent(var))
