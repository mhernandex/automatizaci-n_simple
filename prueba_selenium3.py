from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

empresa = "microsoft"
driver.get(f"https://www.google.com/search?q=precio+acción+{empresa}")
# Google sirve una página intermedia "Haz clic aquí si no se te redirecciona...".
# Damos unos segundos para que complete el redirect y el contenido cargue.
sleep(5)

try:
    # En la vista que recibe Chrome headless, el precio en USD aparece dentro de un
    # <span class="vA9HTb MDvRSc"> incrustado en el resumen de Google.
    # Esa clase también la usan otros segmentos (p. ej. "Dividendos:"), así que
    # filtramos al primero que contenga signo $ y la moneda.
    spans = driver.find_elements(By.CSS_SELECTOR, "span.vA9HTb.MDvRSc")
    precio = next((s.text for s in spans if "$" in s.text and "USD" in s.text), None)
    if not precio:
        raise ValueError("No se encontró el precio en el HTML.")
    print(f"{empresa.capitalize()}: {precio}")
except Exception as e:
    print("No se pudo obtener el precio de la acción en este momento.")

driver.quit()
