from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from reservas.models import Equipamento, Reserva


class Command(BaseCommand):
    help = "Carrega as contas e reservas sintéticas do laboratório."

    @transaction.atomic
    def handle(self, *args, **options):
        agora = timezone.now()
        pessoas = get_user_model()
        ana, _ = pessoas.objects.get_or_create(username="ana")
        bruno, _ = pessoas.objects.get_or_create(username="bruno")
        for pessoa in (ana, bruno):
            pessoa.set_password("acervo-demo")
            pessoa.save(update_fields=["password"])

        projetor, _ = Equipamento.objects.get_or_create(nome="Projetor")
        notebook, _ = Equipamento.objects.get_or_create(nome="Notebook")
        for titular, equipamento, deslocamento in (
            (ana, projetor, timedelta(days=1)),
            (ana, notebook, timedelta(days=-1)),
            (bruno, notebook, timedelta(days=1)),
        ):
            inicio = agora + deslocamento
            Reserva.objects.get_or_create(
                titular=titular,
                equipamento=equipamento,
                defaults={"inicio": inicio, "fim": inicio + timedelta(hours=1)},
            )

        self.stdout.write("Contas de demonstração: ana e bruno. Senha: acervo-demo.")
