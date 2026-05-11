import yfinance as yf
from utils.sanitizar import sanitizar

# Diccionario para mapear nombres comunes de empresas a sus Tickers de bolsa correspondientes
COMPANY_TICKERS = {
    "microsoft": "MSFT",
    "apple": "AAPL",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "tesla": "TSLA",
    "meta": "META",
    "facebook": "META",
    "netflix": "NFLX",
    "nvidia": "NVDA",
    "apple inc": "AAPL",
    "microsoft corp": "MSFT",
    "tesla motors": "TSLA"
}

# Palabras a omitir del input para aislar el nombre de la empresa
_PALABRAS_OMITIR = {"precio", "accion", "valor", "de", "la", "el", "del", "una"}


def obtener_precio_accion(driver, consulta):
    """
    Obtiene el precio actual de una acción y su divisa usando yfinance.
    El argumento `driver` se acepta por consistencia con `obtener_clima` aunque
    yfinance no requiere navegador.
    """
    # 1) Aislar el nombre/alias de la empresa quitando palabras clave del input.
    nombre = " ".join(
        p for p in consulta.split() if p not in _PALABRAS_OMITIR
    ).strip()

    # 2) Resolver el ticker: si está en el diccionario lo usamos; si no, asumimos
    #    que el usuario escribió el ticker directamente.
    ticker = COMPANY_TICKERS.get(nombre, nombre.upper())

    # 3) Consultar yfinance para obtener precio y divisa.
    try:
        stock = yf.Ticker(ticker)
        fast = stock.fast_info
        precio = fast.last_price
        divisa = fast.currency or "USD"

        if precio is None:
            return f"No se encontraron datos de cotización para {ticker}."

        return f"{ticker}: ${precio:,.2f} {divisa}"

    except Exception as e:
        return f"Error al consultar el precio de {ticker}: {e}"
