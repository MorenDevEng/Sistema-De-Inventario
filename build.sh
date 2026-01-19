#!/bin/bash

echo "--- 1. Instalando dependencias de Python ---"
# En Vercel Build, usamos python3
python3 -m pip install -r requirements.txt

echo "--- 2. Instalando dependencias de Node (Tailwind) ---"
npm install

echo "--- 3. Compilando Tailwind CSS ---"
npx tailwindcss -i ./Apps/static/css/input.css -o ./Apps/static/css/output.css --minify

echo "--- 4. Recolectando archivos estáticos (Collectstatic) ---"
# Cambiamos a python3
python3 manage.py collectstatic --noinput --clear

echo "--- ¡PROCESO FINALIZADO EXITOSAMENTE! ---"