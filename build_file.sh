#!/bin/bash

echo "--- 1. Instalando dependencias de Python ---"
# En Vercel Build, usamos python3
python3.12 -m pip install -r requirements.txt

echo "--- 4. Recolectando archivos estáticos (Collectstatic) ---"
# Cambiamos a python3
python3.12 manage.py collectstatic --noinput --clear

echo "--- ¡PROCESO FINALIZADO EXITOSAMENTE! ---"