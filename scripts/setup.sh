#!/bin/bash
set -e

echo "📦 Instalando dependencias..."
pip install -r requirements.txt

echo "🗄️  Aplicando migraciones..."
python manage.py migrate

echo "🌱 Cargando datos de prueba..."
python scripts/seed.py

echo ""
echo "✅ Setup completo."
echo ""
echo "Comandos disponibles:"
echo "  bash scripts/run_server.sh         → Servidor completo en :8000"
echo "  bash scripts/run_invitados.sh      → Frontend invitados en :8001"
echo "  bash scripts/run_localizacion.sh   → Frontend localización en :8002"
