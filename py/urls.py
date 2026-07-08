from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("registro/", views.registro, name="registro"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("deposito/", views.deposito, name="deposito"),
    path("retiro/", views.retiro, name="retiro"),
    path("transferencia/", views.transferencia, name="transferencia"),

    path("crear_boveda/", views.crear_boveda, name="crear_boveda"),
]