#!/bin/bash
python3.11 -m pip install -r requirements.txt
# Aquí es donde se crean los estilos REALES en el servidor
python3.11 manage.py collectstatic --noinput --clear