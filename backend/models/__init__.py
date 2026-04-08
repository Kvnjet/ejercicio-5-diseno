from django.db import models


class Fiesta(models.Model):
    """
    Domain model representing a clandestine party.
    Defines the data schema and encapsulates field-level constraints.
    """

    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=300)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    capacidad = models.PositiveIntegerField()
    fecha = models.DateField()
    hora = models.TimeField()
    descripcion = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fiestas'
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f'{self.nombre} — {self.ubicacion} ({self.fecha})'

    def cupos_disponibles(self, invitados_confirmados: int) -> int:
        return max(0, self.capacidad - invitados_confirmados)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'ubicacion': self.ubicacion,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'capacidad': self.capacidad,
            'fecha': str(self.fecha),
            'hora': str(self.hora),
            'descripcion': self.descripcion,
            'created_at': str(self.created_at),
        }


class Invitado(models.Model):
    """
    Domain model representing a guest accepted to a party.
    """

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('rechazado', 'Rechazado'),
    ]

    fiesta = models.ForeignKey(
        Fiesta,
        on_delete=models.CASCADE,
        related_name='invitados',
    )
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'invitados'
        ordering = ['registered_at']

    def __str__(self):
        return f'{self.nombre} → {self.fiesta.nombre} [{self.estado}]'

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'fiesta_id': self.fiesta_id,
            'fiesta_nombre': self.fiesta.nombre,
            'nombre': self.nombre,
            'contacto': self.contacto,
            'estado': self.estado,
            'registered_at': str(self.registered_at),
        }
