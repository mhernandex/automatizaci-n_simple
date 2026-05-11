from time import sleep
from selenium.webdriver.common.by import By


def obtener_clima(driver, consulta):
    """
    Obtiene el clima actual de una ciudad scrapeando Google.
    Intenta primero el widget interactivo (IDs wob_*), y si no está disponible
    (Google a veces sirve un layout móvil simplificado a Chrome headless),
    cae al bloque ".kvKEAb" que contiene temperatura y descripción.
    """
    driver.get(f"https://www.google.com/search?q=clima+{consulta}")
    # Google sirve una página intermedia ("Haz clic aquí si no se te redirecciona...")
    # cuando detecta Selenium; esperamos a que termine el redirect y cargue el widget.
    sleep(3)

    # Plan A: widget bursátil/clima tradicional con IDs estables.
    try:
        temperatura = driver.find_element(By.ID, "wob_tm").text
        ubicacion = driver.find_element(By.ID, "wob_loc").text
        descripcion = driver.find_element(By.ID, "wob_dc").text
        return f"{ubicacion}: {descripcion} con {temperatura}°C"
    except Exception:
        pass

    # Plan B: layout móvil que recibe Chrome headless.
    try:
        # div.nB7Pqb ya incluye el sufijo "°C".
        temperatura = driver.find_element(By.CSS_SELECTOR, "div.nB7Pqb").text
        ubicacion = driver.find_element(By.CSS_SELECTOR, "span.d6Ejqe").text
        # div.d6Ejqe contiene "día hora\nDescripción" (p. ej. "domingo 11:47 p.m.\nNublado").
        bloque_desc = driver.find_element(By.CSS_SELECTOR, "div.d6Ejqe").text
        lineas = [linea.strip() for linea in bloque_desc.split("\n") if linea.strip()]
        descripcion = lineas[-1] if lineas else ""
        return f"{ubicacion}: {descripcion} con {temperatura}"
    except Exception:
        return "No se pudo obtener el clima en este momento."
