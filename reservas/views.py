from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Equipamento, Reserva


@login_required
def reservas(request):
    itens = Reserva.objects.filter(titular=request.user).select_related("equipamento")
    return render(request, "reservas/lista.html", {"reservas": itens})


@login_required
def catalogo(request):
    equipamentos = Equipamento.objects.order_by("nome")
    return render(request, "reservas/catalogo.html", {"equipamentos": equipamentos})
