import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_excel("despesas_2024_2025.xlsx")
    df.columns = df.columns.str.strip()
    df["ANO"] = df["ANO"].astype(int)
    df["VALOR"] = pd.to_numeric(df["VALOR"], errors="coerce")
    return df
