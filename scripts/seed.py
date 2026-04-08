#!/usr/bin/env python
"""
Seed script — populates the SQLite database with sample data.
Run after migrate: python scripts/seed.py
"""
import os
import sys
import django
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from backend.models import Fiesta, Invitado  # noqa: E402

print('Limpiando datos existentes...')
Invitado.objects.all().delete()
Fiesta.objects.all().delete()

print('Creando fiestas...')
f1 = Fiesta.objects.create(
    nombre='La Fiesta del Cerro',
    ubicacion='Finca Los Robles, Cartago',
    latitud=9.8765,
    longitud=-83.9123,
    capacidad=50,
    fecha='2025-08-15',
    hora='22:00',
    descripcion='Fiesta en finca privada con vista al volcán. Traer cobija.',
)

f2 = Fiesta.objects.create(
    nombre='Noche de Cumbia',
    ubicacion='Casa Barrio Escalante, San José',
    latitud=9.9341,
    longitud=-84.0603,
    capacidad=30,
    fecha='2025-08-22',
    hora='21:00',
    descripcion='Música en vivo. Cuota de entrada: 5 mil colones.',
)

f3 = Fiesta.objects.create(
    nombre='Ranchera Secreta',
    ubicacion='Rancho La Palma, Liberia',
    latitud=10.6375,
    longitud=-85.4428,
    capacidad=100,
    fecha='2025-09-01',
    hora='20:00',
    descripcion='Gran fiesta de fin de temporada. Piscina disponible.',
)

print('Creando invitados...')
Invitado.objects.create(fiesta=f1, nombre='Ana Rodríguez', contacto='ana@correo.com', estado='confirmado')
Invitado.objects.create(fiesta=f1, nombre='Carlos Méndez', contacto='8888-1234', estado='confirmado')
Invitado.objects.create(fiesta=f1, nombre='Laura Jiménez', contacto='laura@correo.com', estado='pendiente')
Invitado.objects.create(fiesta=f2, nombre='Pedro Vargas', contacto='7777-5678', estado='confirmado')
Invitado.objects.create(fiesta=f2, nombre='María Solano', contacto='maria@correo.com', estado='rechazado')

print('✅ Seed completado.')
print(f'   Fiestas creadas: {Fiesta.objects.count()}')
print(f'   Invitados creados: {Invitado.objects.count()}')
