from django.conf import settings
from django.db import models


class Equipamento(models.Model):
    nome = models.CharField(max_length=100, unique=True)


class Reserva(models.Model):
    class Estado(models.TextChoices):
        ATIVA = "ativa", "Ativa"
        CANCELADA = "cancelada", "Cancelada"

    titular = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT)
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    estado = models.CharField(max_length=10, choices=Estado, default=Estado.ATIVA)

    class Meta:
        ordering = ["inicio", "pk"]
