import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Importación de las funciones del agente y utilidades
from funciones_agente.obtener_clima import obtener_clima
from funciones_agente.obtener_precio_accion import obtener_precio_accion
from utils.sanitizar import sanitizar

# --- Configuración de Selenium ---
# Se utilizan opciones para ejecutar el navegador de forma silenciosa (headless)
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# Simulación de un User-Agent real para evitar bloqueos por parte de algunos sitios
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument('--disable-blink-features=AutomationControlled')

# --- Gestión del Driver (ChromeDriver) ---
# Se utiliza webdriver-manager para descargar automáticamente el driver compatible
driver_path = ChromeDriverManager().install()
driver = webdriver.Chrome(service=Service(driver_path), options=options)


def procesar_input(user_input):
    if "clima" in user_input or "temperatura" in user_input:
        return obtener_clima
    elif "precio" in user_input or "accion" in user_input or "valor" in user_input:
        return obtener_precio_accion
    return None


print("Hola, soy tu asistente virtual. ¿En qué puedo ayudarte hoy?")
while True:
    user_input = sanitizar(input("---> "))
    funcion_agente = procesar_input(user_input)
    if funcion_agente is None:
        print("No entendí tu solicitud. Intenta nuevamente.")
    else:
        respuesta = funcion_agente(driver, user_input)
        print(f">>> {respuesta}")
