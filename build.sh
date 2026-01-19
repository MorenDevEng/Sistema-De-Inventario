#!/bin/bash

echo "--- 1. Instalando dependencias de Python ---"
python3.11 -m pip install -r requirements.txt

echo "--- 2. Instalando dependencias de Node (Tailwind) ---"
npm install

echo "--- 3. Compilando Tailwind CSS ---"
# Esto crea el archivo output.css basándose en el input.css
npx tailwindcss -i ./Apps/static/css/input.css -o ./Apps/static/css/output.css --minify

echo "--- 4. Recolectando archivos estáticos (Collectstatic) ---"
# Esto toma el output.css generado y lo mete en la carpeta 'staticfiles' para WhiteNoise
python3.11 manage.py collectstatic --noinput --clear

#!/bin/bash
# ... (todos los comandos anteriores: pip install, npm install, tailwind, collectstatic)

# Aseguramos que la carpeta de salida exista para Vercel
mkdir -p staticfiles

echo "--- ¡PROCESO FINALIZADO EXITOSAMENTE! ---"