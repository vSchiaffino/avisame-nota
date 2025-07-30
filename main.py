from dotenv import load_dotenv
load_dotenv()
from scrap_listado import scrap_listado
from parse_html import parse_historia_academica
from send_email import send_alert_email

import os
import time
import logging as log
import json


# Configurar log para guardar en un archivo
log.basicConfig(
    filename='avisame-nota.log',
    level=log.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

SUBJECTS = [s.strip() for s in os.getenv("SUBJECTS").split(",")]
FREQ_MINUTES = int(os.getenv("FREQ_MINUTES", 15))
SLEEP_TIME = 60 * FREQ_MINUTES

last_value = {}
for codigo in SUBJECTS:
    last_value[codigo] = None

while True:
    try:
        log.info("Iniciando el proceso de scraping... -------------------------------------")
        listado_html = scrap_listado()
        materias = parse_historia_academica(listado_html)
        
        for materia in materias:
            if(materia["codigo_materia"] not in SUBJECTS):
                continue
            
            log.info(f"- {materia['titulo']} ({materia['codigo_materia']})")
            for catedra in materia["catedras"]:
                log.info(f"  Cátedra: {catedra['descripcion']} ({catedra['tipo']}) - Estado: {catedra['estado']}")
        
            last_exams = materia["catedras"]
            if last_exams is None:
                last_exams = materia["catedras"]
                continue

            # check if the actual value is the same as last_value
            if len(last_exams) != len(materia["catedras"]):
                log.info(f"Las cátedras han cambiado para {materia['titulo']} ({materia['codigo_materia']}):")
                log.info(f"Antes: {last_exams}")
                log.info(f"Ahora: {materia['catedras']}")
                log.info("Enviando alerta por email...")
                send_alert_email()
            else:
                log.info(f"No hay cambios en las cátedras de {materia['titulo']} ({materia['codigo_materia']})"+
                          "porque  len(last_exams)={len(last_exams)} = len(materia['catedras'])={len(materia['catedras'])}.")
    except Exception as e:
        log.error("Error al scrapear la página. Reintentando en 5 minutos...")
        log.error(f"Detalles del error: {e}")

    log.info("Terminando el proceso de scraping. Esperando 5 minutos antes de volver a iniciar... -------------------------------------")
    time.sleep(SLEEP_TIME)
