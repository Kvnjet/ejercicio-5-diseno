#!/bin/bash
export DJANGO_SETTINGS_MODULE=backend.settings
echo "🚀 Servidor completo corriendo en http://localhost:8000"
echo "   → Invitados:     http://localhost:8000/invitados/"
echo "   → Localización:  http://localhost:8000/localizacion/"
echo "   → API fiestas:   http://localhost:8000/fiestas"
echo ""
python manage.py runserver 8000
