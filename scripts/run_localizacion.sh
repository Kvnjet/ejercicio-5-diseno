#!/bin/bash
export DJANGO_SETTINGS_MODULE=backend.settings
echo "🗺️  Frontend Localización corriendo en http://localhost:8002"
echo "   → http://localhost:8002/localizacion/"
echo ""
python manage.py runserver 8002
