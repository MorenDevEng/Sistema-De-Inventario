#!/bin/bash

echo "--- 1. Instalando dependencias de Python ---"
# Usamos --break-system-packages para permitir la instalación en el entorno de Vercel
python3.12 -m pip install -r requirements.txt --break-system-packages

echo "--- 3. Collectstatic ---"
# Aquí ejecutamos el comando que fallaba
python3.12 manage.py collectstatic --noinput --clear

echo "--- 4. Verificando carpeta de salida ---"
# Forzamos la creación por si acaso
mkdir -p staticfiles

echo "--- ¡PROCESO FINALIZADO EXITOSAMENTE! ---"