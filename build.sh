#!/bin/bash

# Instalar dependencias
pip install -r requirements.txt

# SI tienes Tailwind (node), necesitas esto:
# npm install && npm run build 

# Ejecutar el recolector de estáticos en el servidor de Vercel
python3.11 manage.py collectstatic --noinput --clear