from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Equipamento, Reserva


@login_required
def reservas(request):
    itens = Reserva.objects.filter(titular=request.user).select_related("equipamento")
    return render(request, "reservas/lista.html", {"reservas": itens, "agora": timezone.now()})


@login_required
def catalogo(request):
    equipamentos = Equipamento.objects.order_by("nome")
    return render(request, "reservas/catalogo.html", {"equipamentos": equipamentos})


@login_required
@require_POST
@transaction.atomic
def cancelar_reserva(request, pk):
    reserva = get_object_or_404(
        Reserva.objects.select_for_update(), pk=pk, titular=request.user
    )
    if reserva.estado == Reserva.Estado.CANCELADA:
        messages.info(request, "Esta reserva já está cancelada.")
    elif reserva.inicio <= timezone.now():
        messages.error(request, "O horário desta reserva já começou.")
    else:
        reserva.estado = Reserva.Estado.CANCELADA
        reserva.save(update_fields=["estado"])
        messages.success(request, "Reserva cancelada.")
    return redirect("reservas")
