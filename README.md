# Fiestas Clandestinas

A system for managing clandestine parties at houses and farms. Allows users to publish events, accept guests, and locate parties on a map — all within a Django monolith with server-side rendering and logical layer separation.

**Authors:** Kevin Espinoza · Daniel Campos
**Course:** Software Design — Computer Engineering

---

## Implementation: Technology, Paradigm & Topology

### Technology

- **Runtime:** Python 3.11+
- **Framework:** Django 5.x monolith with server-side rendering
- **Database:** SQLite local
- **Templates:** Django Templates (plain HTML/CSS, no external JS frameworks)
- **Map:** Leaflet.js via CDN for coordinate visualization
- **Testing:** Django TestCase + unittest.mock

### Paradigm

- **Monolithic Architecture** with logical layer separation: models, repositories, business_logic, views
- **Server-Side Rendering (SSR):** Django renders complete HTML on the server before sending it to the browser
- **REST API:** JSON endpoints at `/fiestas` and `/invitados` for CRUD operations
- **Repository Pattern:** all database communication goes through repository classes, never directly from business logic
- **Service Layer:** all domain logic lives in `business_logic/`, views are thin controllers

### Topology

```
Browser
   │
   ▼
Django Monolith (manage.py runserver)
   │
   ├── urls.py  ──────────────────────────────────────────────────────────────
   │                                                                          │
   ├── views.py (Controller Layer)                                            │
   │     ├── Parses HTTP requests                                             │
   │     ├── Calls service layer                                              │
   │     └── Returns JsonResponse or render(template)                        │
   │                                                                          │
   ├── business_logic/ (Service Layer)                                        │
   │     ├── FiestaService   → validations + orchestration                   │
   │     └── InvitadoService → capacity rules + status management            │
   │                                                                          │
   ├── repositories/ (Data Access Layer)                                      │
   │     ├── FiestaRepository   → abstracts Fiesta ORM                       │
   │     └── InvitadoRepository → abstracts Invitado ORM                     │
   │                                                                          │
   ├── models/ (Model Layer)                                                  │
   │     ├── Fiesta   → schema + to_dict()                                   │
   │     └── Invitado → schema + to_dict()                                   │
   │                                                                          │
   └── SQLite (db.sqlite3)                                                    │
                                                                              │
Frontend Bundles (SSR Templates)                                              │
   ├── frontend_invitados/templates/   ←── /invitados/*  ────────────────────┘
   └── frontend_localizacion/templates/ ←── /localizacion/*
```

---

## Architecture & Design Patterns

### Layered Architecture (n-tier)

The project implements 4 logical layers with strictly separated responsibilities:

```
┌──────────────────────────────────────────────────────────┐
│  views.py  (Controller / Presentation Layer)             │
│  - Parses HTTP request/response                         │
│  - Calls the service layer                              │
│  - Renders templates or returns JSON                    │
└──────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────┐
│  business_logic/  (Service Layer)                        │
│  - All domain logic                                     │
│  - Business rule validation                             │
│  - Orchestrates operations                              │
└──────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────┐
│  repositories/  (Data Access Layer)                      │
│  - Abstracts the Django ORM                             │
│  - One class per entity                                 │
│  - Single point of contact with the database            │
└──────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────┐
│  models/  (Model Layer)                                  │
│  - Django ORM schema                                    │
│  - No business logic                                    │
│  - to_dict() for serialization                          │
└──────────────────────────┬───────────────────────────────┘
                           │
                      SQLite (db.sqlite3)
```

### Repository Pattern

Views and services never import the ORM directly. All data access goes through `FiestaRepository` and `InvitadoRepository`:

```python
# BAD — direct ORM in the service
parties = Fiesta.objects.all()

# GOOD — through the repository
parties = self.fiesta_repo.find_all()
```

This allows switching the database implementation without touching business logic.

### Service Layer Pattern

`FiestaService` and `InvitadoService` contain all domain rules: capacity validation, field constraints, and status rules. Views only orchestrate the request/response cycle:

```python
# views.py — thin controller
def fiestas(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        result = fiesta_service.crear_fiesta(payload)  # logic lives in the service
        return JsonResponse(result, status=201)
```

### Custom Error Handling

`ValidationError` carries its own `status_code`, enabling clean propagation from any layer up to the controller:

```python
class ValidationError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code
```

### Dependency Injection for Testability

Services receive their repositories through the constructor, allowing them to be mocked in tests:

```python
class FiestaService:
    def __init__(self, fiesta_repo=None, invitado_repo=None):
        self.fiesta_repo = fiesta_repo or FiestaRepository()
        self.invitado_repo = invitado_repo or InvitadoRepository()
```

---

## Project Structure

```
fiestas-clandestinas/
├── manage.py                          # Django entry point
├── requirements.txt                   # Python dependencies
├── db.sqlite3                         # Local database (generated)
├── AGENTS.md                          # AI agent specification
├── README.md                          # This file
│
├── backend/                           # Main Django application
│   ├── __init__.py
│   ├── apps.py
│   ├── settings.py                    # Django configuration
│   ├── urls.py                        # URL routing
│   ├── views.py                       # Controller layer (SSR + API)
│   ├── wsgi.py
│   │
│   ├── models/
│   │   └── __init__.py               # Fiesta, Invitado (ORM + to_dict)
│   │
│   ├── repositories/
│   │   └── __init__.py               # FiestaRepository, InvitadoRepository
│   │
│   ├── business_logic/
│   │   └── __init__.py               # FiestaService, InvitadoService, ValidationError
│   │
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py           # Initial migration
│
├── frontend_invitados/                # Bundle: guest management interface
│   └── templates/
│       ├── base.html                  # Shared base template
│       └── invitados/
│           ├── home.html             # Party listing with availability
│           └── fiesta_detail.html    # Party detail + guest registration form
│
├── frontend_localizacion/             # Bundle: party location interface
│   └── templates/
│       └── localizacion/
│           ├── home.html             # Leaflet map + party listing
│           └── nueva.html            # Create new party form
│
└── scripts/
    ├── setup.sh                       # Installs deps + migrates + seeds
    ├── run_server.sh                  # Runs full monolith on :8000
    ├── run_invitados.sh               # Runs guest frontend on :8001
    ├── run_localizacion.sh            # Runs location frontend on :8002
    └── seed.py                        # Loads sample data into the database
```

---

## Prerequisites

- Python 3.11 or higher
- pip

```bash
python --version   # must show 3.11+
pip --version
```

---

## Installation & Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd fiestas-clandestinas

# 2. Full setup (installs, migrates, and seeds data)
bash scripts/setup.sh
```

Or manually:

```bash
pip install -r requirements.txt
python manage.py migrate
python scripts/seed.py
```

---

## How to Run

### Full server (recommended)

```bash
bash scripts/run_server.sh
# → http://localhost:8000/invitados/
# → http://localhost:8000/localizacion/
# → http://localhost:8000/fiestas  (JSON API)
```

### Frontends independently

```bash
# Terminal 1 — Guest Frontend
bash scripts/run_invitados.sh
# → http://localhost:8001/invitados/

# Terminal 2 — Location Frontend
bash scripts/run_localizacion.sh
# → http://localhost:8002/localizacion/
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/fiestas` | List all parties with available spots |
| POST | `/fiestas` | Create a new party |
| GET | `/invitados` | List all guests |
| GET | `/invitados?fiesta_id=1` | List guests for a specific party |
| POST | `/invitados` | Accept a new guest |
| PATCH | `/invitados/<id>/estado` | Update guest status |

### curl Examples

```bash
# List all parties
curl http://localhost:8000/fiestas

# Create a party
curl -X POST http://localhost:8000/fiestas \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Secret Party",
    "ubicacion": "Farm El Silencio, Heredia",
    "capacidad": 40,
    "fecha": "2025-09-20",
    "hora": "21:00",
    "latitud": 10.0167,
    "longitud": -84.1167
  }'

# Register a guest
curl -X POST http://localhost:8000/invitados \
  -H "Content-Type: application/json" \
  -d '{"fiesta_id": 1, "nombre": "Maria Lopez", "contacto": "maria@email.com"}'

# Update guest status
curl -X PATCH http://localhost:8000/invitados/1/estado \
  -H "Content-Type: application/json" \
  -d '{"estado": "rechazado"}'
```

---

## How to Stop

Press `Ctrl+C` in each active terminal.

---

## Seed Data

The `scripts/seed.py` script automatically creates:

- **3 parties** across different locations in Costa Rica with coordinates
- **5 guests** distributed across the first two parties with varied statuses

To reload data from scratch:

```bash
python scripts/seed.py
```