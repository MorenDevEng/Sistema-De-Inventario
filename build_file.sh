#!/bin/bash

echo "--- 1. Instalando dependencias de Python ---"
# En Vercel Build, usamos python3
python3.12 -m pip install -r requirements.txt

echo "--- 4. Recolectando archivos estáticos (Collectstatic) ---"
# Cambiamos a python3
python3.12 manage.py collectstatic --noinput --clear

# ESTA LÍNEA ES LA QUE CORRIGE EL ERROR DE VERCEL
echo "--- 4. Verificando carpeta de salida ---"
mkdir -p staticfiles

echo "--- ¡PROCESO FINALIZADO EXITOSAMENTE! ---"