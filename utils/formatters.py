def format_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percent(valor):
    return f"{valor*100:+.1f}%"
