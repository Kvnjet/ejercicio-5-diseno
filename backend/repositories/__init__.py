from typing import Optional
from backend.models import Fiesta, Invitado


class FiestaRepository:
    """
    Repository Pattern: abstracts all data access for the Fiesta entity.
    The business logic layer never touches the ORM directly.
    """

    def find_all(self) -> list[Fiesta]:
        return list(Fiesta.objects.all())

    def find_by_id(self, fiesta_id: int) -> Optional[Fiesta]:
        try:
            return Fiesta.objects.get(pk=fiesta_id)
        except Fiesta.DoesNotExist:
            return None

    def save(self, data: dict) -> Fiesta:
        fiesta = Fiesta(
            nombre=data['nombre'],
            ubicacion=data['ubicacion'],
            latitud=data.get('latitud'),
            longitud=data.get('longitud'),
            capacidad=data['capacidad'],
            fecha=data['fecha'],
            hora=data['hora'],
            descripcion=data.get('descripcion', ''),
        )
        fiesta.save()
        return fiesta

    def count_invitados_confirmados(self, fiesta_id: int) -> int:
        return Invitado.objects.filter(
            fiesta_id=fiesta_id,
            estado='confirmado',
        ).count()


class InvitadoRepository:
    """
    Repository Pattern: abstracts all data access for the Invitado entity.
    """

    def find_by_fiesta(self, fiesta_id: int) -> list[Invitado]:
        return list(Invitado.objects.filter(fiesta_id=fiesta_id).select_related('fiesta'))

    def find_all(self) -> list[Invitado]:
        return list(Invitado.objects.all().select_related('fiesta'))

    def find_by_id(self, invitado_id: int) -> Optional[Invitado]:
        try:
            return Invitado.objects.select_related('fiesta').get(pk=invitado_id)
        except Invitado.DoesNotExist:
            return None

    def save(self, data: dict) -> Invitado:
        invitado = Invitado(
            fiesta_id=data['fiesta_id'],
            nombre=data['nombre'],
            contacto=data['contacto'],
            estado=data.get('estado', 'pendiente'),
        )
        invitado.save()
        return invitado

    def update_estado(self, invitado_id: int, estado: str) -> Optional[Invitado]:
        try:
            invitado = Invitado.objects.get(pk=invitado_id)
            invitado.estado = estado
            invitado.save()
            return invitado
        except Invitado.DoesNotExist:
            return None
