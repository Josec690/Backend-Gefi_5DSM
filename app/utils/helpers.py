from datetime import datetime

def get_month_range(mes=None, ano=None):
    """Retorna range de datas do mês"""
    if not mes or not ano:
        now = datetime.utcnow()
        mes = now.month
        ano = now.year
    
    start_date = datetime(ano, mes, 1)
    if mes == 12:
        end_date = datetime(ano + 1, 1, 1)
    else:
        end_date = datetime(ano, mes + 1, 1)
    
    return start_date, end_date

def format_currency(value: float, currency: str = "BRL") -> str:
    """Formata valor monetário"""
    if currency == "BRL":
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{value:,.2f}"