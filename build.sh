#!/bin/bash

echo "Instalando dependencias de Python..."
python3.11 -m pip install -r requirements.txt

echo "Instalando dependencias de Node (Tailwind)..."
npm install

echo "Compilando Tailwind CSS..."
npm run build

echo "Ejecutando Collectstatic..."
# Esto moverá el output.css recién creado a la carpeta staticfiles/
python3.11 manage.py collectstatic --noinput --clear

echo "¡Build completado con éxito!"