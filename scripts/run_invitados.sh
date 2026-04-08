#!/bin/bash
export DJANGO_SETTINGS_MODULE=backend.settings
echo "🎟️  Frontend Invitados corriendo en http://localhost:8001"
echo "   → http://localhost:8001/invitados/"
echo ""
python manage.py runserver 8001
