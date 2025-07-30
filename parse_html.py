from bs4 import BeautifulSoup
import json
import re

def parse_historia_academica(html_str: str):
    soup = BeautifulSoup(html_str, 'html.parser')
    materias = []

    for materia_div in soup.select("div.catedras"):
        materia_id = materia_div.get("materia")
        titulo = materia_div.select_one("h3.titulo-corte").get_text(strip=True)

        # Extraer código de materia entre paréntesis
        match = re.search(r"\((.*?)\)", titulo)
        codigo_materia = match.group(1) if match else None

        catedras = []
        for catedra_div in materia_div.select("div.catedra"):
            tipo = next((k for k in catedra_div.attrs if k in ['examen', 'regularidad', 'promocion', 'encurso']), None)
            estado = catedra_div.get(tipo)
            descripcion = catedra_div.select_one("div.catedra_nombre span").get_text(strip=True)

            catedras.append({
                "tipo": tipo.capitalize() if tipo else None,
                "estado": estado,
                "descripcion": descripcion
            })

        materias.append({
            "materia_id": materia_id,
            "titulo": titulo,
            "codigo_materia": codigo_materia,
            "catedras": catedras
        })

    return materias
