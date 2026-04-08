# AGENTS.md — Fiestas Clandestinas

This file defines the AI agent instructions used to generate this project.
All code in this repository was produced by an AI coding agent following these specifications.

---

## Project Specification

Build a Django monolith for managing clandestine parties. The system allows users to publish parties
at houses or farms, accept guests, and query party locations — all within a single monolith with
server-side rendering and logical layer separation.

---

## Architecture Requirements

- **Framework:** Django 5.x monolith with server-side rendering (SSR) via Django templates
- **Monorepo:** Single repository containing backend logic and two independent frontend template bundles
- **Database:** SQLite local with seed data
- **Layers:** business_logic, repositories, models — strictly separated
- **No external frontend frameworks** — pure Django templates + HTML/CSS

---

## Layer Definitions

### models/
Defines Django ORM models only. No business logic, no service calls.
Each model must implement a `to_dict()` method returning a plain Python dict.
Models: `Fiesta`, `Invitado`.

### repositories/
One repository class per model. Abstracts all ORM/database access.
Services never import Django ORM directly — only through repository methods.
Classes: `FiestaRepository`, `InvitadoRepository`.

### business_logic/
Service classes that contain all domain rules and orchestration.
Must use constructor injection for repositories so they can be mocked in tests.
Must define a `ValidationError` exception class with a `status_code` attribute.
Classes: `FiestaService`, `InvitadoService`.

### views.py
Thin controller layer. Parses HTTP requests, calls service methods, returns responses.
Never contains business logic or direct ORM queries.
Handles both JSON API endpoints and SSR HTML views.

---

## Frontend Bundles

### frontend_invitados/
Templates for the guest management interface.
Routes served: `/invitados/`, `/invitados/fiesta/<id>/`
Features: list parties with availability, register guests via POST form, show guest table per party.

### frontend_localizacion/
Templates for the party discovery interface.
Routes served: `/localizacion/`, `/localizacion/nueva/`
Features: interactive Leaflet map showing party coordinates, list of all parties, create new party form.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/fiestas` | List all parties with guest counts |
| POST | `/fiestas` | Create a new party |
| GET | `/invitados` | List all guests (optional `?fiesta_id=`) |
| POST | `/invitados` | Accept a new guest |
| PATCH | `/invitados/<id>/estado` | Update guest status |

---

## Data Models

### Fiesta
- nombre (CharField, max 200)
- ubicacion (CharField, max 300)
- latitud (FloatField, nullable)
- longitud (FloatField, nullable)
- capacidad (PositiveIntegerField)
- fecha (DateField)
- hora (TimeField)
- descripcion (TextField, optional)
- created_at (auto)

### Invitado
- fiesta (ForeignKey → Fiesta)
- nombre (CharField)
- contacto (CharField)
- estado (CharField: pendiente | confirmado | rechazado)
- registered_at (auto)

---

## Business Rules

1. A party cannot have more confirmed guests than its `capacidad`.
2. Registering a guest automatically sets their status to `confirmado`.
3. Capacity must be between 1 and 500.
4. Party name must have at least 3 characters.
5. Guest name must have at least 2 characters.
6. All required fields must be validated in the service layer before hitting the repository.

---

## Scripts

- `scripts/setup.sh` — installs deps, runs migrations, seeds data
- `scripts/run_server.sh` — runs full monolith on port 8000
- `scripts/run_invitados.sh` — runs on port 8001 (invitados frontend)
- `scripts/run_localizacion.sh` — runs on port 8002 (localizacion frontend)
- `scripts/seed.py` — populates DB with 3 parties and 5 guests

---

## Code Style Rules

- All Python files use type hints where practical
- Docstrings on all classes explaining their architectural role
- No business logic in views.py
- No ORM imports outside of models/ and repositories/
- Repository methods return model instances or lists, never raw querysets
- Services return plain dicts (via `to_dict()`), never model instances
