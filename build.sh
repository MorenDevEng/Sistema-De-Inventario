#!/bin/bash

echo "--- INSTALANDO PYTHON DEPENDENCIES ---"
python3.11 -m pip install -r requirements.txt

echo "--- INSTALANDO NODE DEPENDENCIES ---"
# Esto busca tu package.json y descarga Tailwind
npm install

echo "--- COMPILANDO TAILWIND ---"
# Usamos la ruta de tu package.json: ../Apps/static/css/
# Pero como el script corre desde la raíz, ajustamos:
npx tailwindcss -i ./Apps/static/css/input.css -o ./Apps/static/css/output.css --minify

echo "--- EJECUTANDO COLLECTSTATIC ---"
python3.11 manage.py collectstatic --noinput --clear