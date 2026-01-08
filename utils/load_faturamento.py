import pandas as pd
import streamlit as st

@st.cache_data
def load_faturamento():
    df = pd.read_excel("Consolidado de Faturamento - 2024 e 2025.xlsx")

    df.columns = df.columns.str.strip()

    df["Ano"] = df["Ano"].astype(int)
    df["Faturamento - Valor"] = pd.to_numeric(
        df["Faturamento - Valor"], errors="coerce"
    )

    return df
