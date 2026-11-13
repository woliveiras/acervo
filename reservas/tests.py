from datetime import datetime, timedelta, timezone

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Equipamento, Reserva


class ConsultaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pessoas = get_user_model()
        cls.ana = pessoas.objects.create_user("ana")
        cls.bruno = pessoas.objects.create_user("bruno")
        equipamento = Equipamento.objects.create(nome="Projetor")
        inicio = datetime(2026, 11, 14, 12, tzinfo=timezone.utc)
        cls.reserva = Reserva.objects.create(
            titular=cls.ana, equipamento=equipamento,
            inicio=inicio, fim=inicio + timedelta(hours=1),
        )

    def test_reservas_exigem_login(self):
        self.assertRedirects(self.client.get(reverse("reservas")), "/entrar/?next=/")

    def test_lista_exibe_apenas_as_reservas_da_conta(self):
        self.client.force_login(self.ana)
        self.assertContains(self.client.get(reverse("reservas")), "Projetor")
        self.client.force_login(self.bruno)
        resposta = self.client.get(reverse("reservas"))
        self.assertNotContains(resposta, "Projetor")
        self.assertContains(resposta, "Você ainda não tem reservas.")

    def test_catalogo_exibe_equipamentos(self):
        self.client.force_login(self.bruno)
        self.assertContains(self.client.get(reverse("catalogo")), "Projetor")
