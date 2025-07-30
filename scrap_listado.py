from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

EVA_USERNAME = os.getenv("EVA_USERNAME")
EVA_PASSWORD = os.getenv("EVA_PASSWORD")
CARRERA_ID = os.getenv("CARRERA_ID")
CARRERA_NOMBRE = os.getenv("CARRERA_NOMBRE")

def scrap_listado():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    # Ir a la página principal
    driver.get("https://autogestion.uca.edu.ar/acceso")

    # Clic en "Acceso al Campus"
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="Acceso al Campus"]'))).click()

    # Email
    wait.until(EC.presence_of_element_located((By.ID, "i0116"))).send_keys(EVA_USERNAME)

    # Botón "Siguiente"
    wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()

    # Esperar a que la página de contraseña se cargue
    time.sleep(2)

    # Escribir contraseña
    wait.until(EC.presence_of_element_located((By.ID, "i0118"))).send_keys(EVA_PASSWORD)

    wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()

    # Botón "No" (para no mantener sesión iniciada)
    wait.until(EC.presence_of_element_located((By.ID, "idBtn_Back")))
    no_button = driver.find_element(By.ID, "idBtn_Back")
    no_button.click()


    # Clic en "Sistema Guaraní"
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="Sistema Guaraní"]'))).click()

    # Abrir dropdown de carreras
    wait.until(EC.element_to_be_clickable((By.ID, "js-dropdown-toggle-carreras"))).click()

    # Seleccionar carrera específica
    wait.until(EC.element_to_be_clickable((By.XPATH, f'//a[@data-carrera-id="{CARRERA_ID}" and contains(text(), "{CARRERA_NOMBRE}")]'))).click()

    # Abrir menú "Reportes"
    wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Reportes")]'))).click()

    # Clic en "Historia académica"
    wait.until(EC.element_to_be_clickable((By.ID, "historia_academica"))).click()

    # Esperar que esté presente en el DOM
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[consulta="todo"]')))

    # Esperar que sea clickeable y hacer clic
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[consulta="todo"]'))).click()

    # Esperar a que el div esté presente
    wait.until(EC.presence_of_element_located((By.ID, "listado")))

    time.sleep(1)
    # Obtener el HTML interno
    html = driver.find_element(By.ID, "listado").get_attribute("innerHTML")
    driver.quit()
    return html