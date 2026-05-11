import unicodedata


def sanitizar(texto):
    """
    Limpia el texto ingresado por el usuario:
    - Convierte a minúsculas.
    - Elimina tildes (á → a, é → e, etc.).
    - Reemplaza 'ñ' por 'n'.
    - Elimina diéresis (ü → u).

    Ejemplos:
        sanitizar("Oaxaca de Juárez")                  -> "oaxaca de juarez"
        sanitizar("precio de la acción Microsoft")     -> "precio de la accion microsoft"
    """
    texto = texto.lower()
    # 'ñ' debe sustituirse manualmente porque NFKD no la descompone en 'n' + diacrítico.
    texto = texto.replace("ñ", "n")
    # Descomponer letras acentuadas en (letra base + marca combinante) y descartar las marcas.
    descompuesto = unicodedata.normalize("NFKD", texto)
    sin_diacriticos = "".join(c for c in descompuesto if not unicodedata.combining(c))
    return sin_diacriticos.strip()
