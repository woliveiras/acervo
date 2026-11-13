from datetime import datetime, timedelta, timezone

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
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


class CancelamentoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pessoas = get_user_model()
        cls.ana = pessoas.objects.create_user("ana")
        cls.bruno = pessoas.objects.create_user("bruno")
        cls.agora = datetime(2026, 11, 14, 12, tzinfo=timezone.utc)
        equipamento = Equipamento.objects.create(nome="Projetor")
        for nome, inicio in (
            ("futura", cls.agora + timedelta(hours=1)),
            ("no_limite", cls.agora),
            ("passada", cls.agora - timedelta(hours=1)),
        ):
            setattr(cls, nome, Reserva.objects.create(
                titular=cls.ana, equipamento=equipamento,
                inicio=inicio, fim=inicio + timedelta(hours=1),
            ))

    def setUp(self):
        relogio = patch("reservas.views.timezone.now", return_value=self.agora)
        relogio.start()
        self.addCleanup(relogio.stop)
        self.url = reverse("cancelar_reserva", args=[self.futura.pk])

    def test_titular_cancela_e_preserva_o_registro(self):
        self.client.force_login(self.ana)
        self.assertContains(self.client.get(reverse("reservas")), self.url)
        resposta = self.client.post(self.url, follow=True)
        self.assertContains(resposta, "Reserva cancelada.")
        self.assertContains(resposta, "Cancelada")
        self.assertNotContains(resposta, self.url)

        salva = Reserva.objects.get(pk=self.futura.pk)
        self.assertEqual(salva.estado, Reserva.Estado.CANCELADA)
        for campo in ("titular_id", "equipamento_id", "inicio", "fim"):
            self.assertEqual(getattr(salva, campo), getattr(self.futura, campo))

    def test_outra_conta_nao_pode_cancelar(self):
        self.client.force_login(self.bruno)
        self.assertNotContains(self.client.get(reverse("reservas")), self.url)
        self.assertEqual(self.client.post(self.url).status_code, 404)
        self.futura.refresh_from_db()
        self.assertEqual(self.futura.estado, Reserva.Estado.ATIVA)

    def test_recusa_reserva_passada_ou_no_instante_do_inicio(self):
        self.client.force_login(self.ana)
        for reserva in (self.passada, self.no_limite):
            with self.subTest(reserva=reserva.pk):
                url = reverse("cancelar_reserva", args=[reserva.pk])
                self.assertNotContains(self.client.get(reverse("reservas")), url)
                resposta = self.client.post(url, follow=True)
                self.assertContains(resposta, "O horário desta reserva já começou.")
                reserva.refresh_from_db()
                self.assertEqual(reserva.estado, Reserva.Estado.ATIVA)

    def test_repeticao_preserva_o_estado_sem_nova_escrita(self):
        self.client.force_login(self.ana)
        self.client.post(self.url)
        with patch.object(Reserva, "save", autospec=True) as salvar:
            resposta = self.client.post(self.url, follow=True)
            salvar.assert_not_called()
        self.assertContains(resposta, "Esta reserva já está cancelada.")
        self.futura.refresh_from_db()
        self.assertEqual(self.futura.estado, Reserva.Estado.CANCELADA)

    def test_cancelamento_exige_login_post_e_csrf(self):
        self.assertEqual(self.client.post(self.url).status_code, 302)
        self.client.force_login(self.ana)
        self.assertEqual(self.client.get(self.url).status_code, 405)
        com_csrf = Client(enforce_csrf_checks=True)
        com_csrf.force_login(self.ana)
        self.assertEqual(com_csrf.post(self.url).status_code, 403)
        self.futura.refresh_from_db()
        self.assertEqual(self.futura.estado, Reserva.Estado.ATIVA)
