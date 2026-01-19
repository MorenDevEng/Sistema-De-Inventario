import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
import json
from datetime import datetime, timedelta


BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)
ubicacion_json = os.path.join(BASE_DIR, 'dolar_bcv.json')

encabezados = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

url = 'https://www.bcv.org.ve/'

def obtener_dolar_bcv():
    """Busca el dato con WebScrapping"""

    respuesta = requests.get(url, verify=os.path.join(BASE_DIR, 'bcv.org.ve.crt'), headers=encabezados)

    if respuesta.status_code == 200:

        soup = BeautifulSoup(respuesta.text, 'html.parser')

        valor_dolar = soup.find('div', id='dolar').find('strong').string

        dolar_bcv = float(valor_dolar.replace(" ", "").replace(',', '.'))
        
        return round(dolar_bcv, 2)

def debe_actualizar_json(horas):
    """Retorna True si ya pasaron X horas desde la última consulta"""

    if not os.path.exists(ubicacion_json):
        return True

    with open(ubicacion_json, 'r', encoding='utf-8') as archivo:
        data = json.load(archivo)

    ultima_actualizacion = datetime.fromisoformat(data['fecha'])
    ahora = datetime.now()
    
    return ahora - ultima_actualizacion >= timedelta(hours=horas)

def consulta_valor_json():
    """Verifica si ya paso el tiempo y reescribe el JSON de ser necesario"""

    if not debe_actualizar_json(horas=24):
        return  # Usa el valor guardado, no consulta la web

    data = {
        'precio': obtener_dolar_bcv(),
        'fecha': datetime.now().isoformat(" ")
    }

    try:
        # Crea el archivo por primera vez

        with open(ubicacion_json, 'x', encoding='utf-8') as archivo:
            json.dump(data, archivo, indent=4)    

    except FileExistsError:
        # Modifica el contenido del archivo si ya existe

        with open(ubicacion_json, 'w', encoding='utf-8') as archivo:
            json.dump(data, archivo, indent=4)


def valor_obtenido():
    """Busca el valor en el JSON y verifica si debe actualizarse con la funcion consulta"""
    try:
        consulta_valor_json()
    except Exception:
        pass  

    with open(ubicacion_json, 'r', encoding='utf-8') as ar:
        respuesta = json.load(ar)
        
        return respuesta['precio']
    
