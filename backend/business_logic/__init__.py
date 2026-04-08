from datetime import date, time
from backend.repositories import FiestaRepository, InvitadoRepository


class ValidationError(Exception):
    """Custom error carrying an HTTP status code for clean handler propagation."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


class FiestaService:
    """
    Service Layer: encapsulates all business logic for Fiesta operations.
    Coordinates between repositories and enforces domain rules.
    Uses constructor injection so dependencies can be mocked in tests.
    """

    def __init__(
        self,
        fiesta_repo: FiestaRepository = None,
        invitado_repo: InvitadoRepository = None,
    ):
        self.fiesta_repo = fiesta_repo or FiestaRepository()
        self.invitado_repo = invitado_repo or InvitadoRepository()

    def listar_fiestas(self) -> list[dict]:
        fiestas = self.fiesta_repo.find_all()
        result = []
        for f in fiestas:
            data = f.to_dict()
            confirmados = self.fiesta_repo.count_invitados_confirmados(f.id)
            data['invitados_confirmados'] = confirmados
            data['cupos_disponibles'] = f.cupos_disponibles(confirmados)
            result.append(data)
        return result

    def obtener_fiesta(self, fiesta_id: int) -> dict:
        fiesta = self.fiesta_repo.find_by_id(fiesta_id)
        if not fiesta:
            raise ValidationError(f'Fiesta con id {fiesta_id} no encontrada.', status_code=404)
        data = fiesta.to_dict()
        confirmados = self.fiesta_repo.count_invitados_confirmados(fiesta_id)
        data['invitados_confirmados'] = confirmados
        data['cupos_disponibles'] = fiesta.cupos_disponibles(confirmados)
        return data

    def crear_fiesta(self, payload: dict) -> dict:
        self._validate_fiesta_payload(payload)
        fiesta = self.fiesta_repo.save(payload)
        return fiesta.to_dict()

    def _validate_fiesta_payload(self, payload: dict) -> None:
        required = ['nombre', 'ubicacion', 'capacidad', 'fecha', 'hora']
        for field in required:
            if not payload.get(field):
                raise ValidationError(f'El campo "{field}" es obligatorio.')

        if not isinstance(payload['capacidad'], int) or payload['capacidad'] <= 0:
            raise ValidationError('La capacidad debe ser un número entero positivo.')

        if payload['capacidad'] > 500:
            raise ValidationError('Capacidad máxima permitida: 500 personas.')

        if len(payload['nombre']) < 3:
            raise ValidationError('El nombre debe tener al menos 3 caracteres.')


class InvitadoService:
    """
    Service Layer: encapsulates all business logic for Invitado operations.
    Enforces capacity rules before accepting a guest.
    """

    ESTADOS_VALIDOS = {'pendiente', 'confirmado', 'rechazado'}

    def __init__(
        self,
        fiesta_repo: FiestaRepository = None,
        invitado_repo: InvitadoRepository = None,
    ):
        self.fiesta_repo = fiesta_repo or FiestaRepository()
        self.invitado_repo = invitado_repo or InvitadoRepository()

    def listar_invitados(self, fiesta_id: int = None) -> list[dict]:
        if fiesta_id:
            invitados = self.invitado_repo.find_by_fiesta(fiesta_id)
        else:
            invitados = self.invitado_repo.find_all()
        return [i.to_dict() for i in invitados]

    def aceptar_invitado(self, payload: dict) -> dict:
        self._validate_invitado_payload(payload)

        fiesta = self.fiesta_repo.find_by_id(payload['fiesta_id'])
        if not fiesta:
            raise ValidationError(f'Fiesta con id {payload["fiesta_id"]} no encontrada.', 404)

        confirmados = self.fiesta_repo.count_invitados_confirmados(fiesta.id)
        if fiesta.cupos_disponibles(confirmados) == 0:
            raise ValidationError('No hay cupos disponibles en esta fiesta.')

        invitado = self.invitado_repo.save({**payload, 'estado': 'confirmado'})
        return invitado.to_dict()

    def actualizar_estado(self, invitado_id: int, estado: str) -> dict:
        if estado not in self.ESTADOS_VALIDOS:
            raise ValidationError(
                f'Estado inválido. Opciones válidas: {", ".join(self.ESTADOS_VALIDOS)}'
            )
        invitado = self.invitado_repo.update_estado(invitado_id, estado)
        if not invitado:
            raise ValidationError(f'Invitado con id {invitado_id} no encontrado.', 404)
        return invitado.to_dict()

    def _validate_invitado_payload(self, payload: dict) -> None:
        required = ['fiesta_id', 'nombre', 'contacto']
        for field in required:
            if not payload.get(field):
                raise ValidationError(f'El campo "{field}" es obligatorio.')

        if len(payload['nombre']) < 2:
            raise ValidationError('El nombre del invitado debe tener al menos 2 caracteres.')
