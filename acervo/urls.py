from django.contrib.auth import views as auth_views
from django.urls import path

from reservas import views

urlpatterns = [
    path("", views.reservas, name="reservas"),
    path("reservas/<int:pk>/cancelar/", views.cancelar_reserva, name="cancelar_reserva"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("entrar/", auth_views.LoginView.as_view(), name="login"),
    path("sair/", auth_views.LogoutView.as_view(), name="logout"),
]
