def resumo_por_grupo(df, grupo):
    resumo = (
        df.groupby(["ANO", grupo])["VALOR"]
        .sum()
        .reset_index()
    )

    pivot = resumo.pivot(index=grupo, columns="ANO", values="VALOR").fillna(0)

    pivot["Diferença (R$)"] = pivot[2025] - pivot[2024]
    pivot["Variação (%)"] = pivot.apply(
        lambda x: (x[2025] - x[2024]) / x[2024] if x[2024] != 0 else 0,
        axis=1
    )

    return pivot.reset_index()
