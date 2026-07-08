from django.contrib import admin
from .models import Cliente, Movimiento


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("usuario", "saldo")
    search_fields = ("usuario",)


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ("cliente", "tipo", "monto", "fecha")
    search_fields = ("cliente__usuario",)
    list_filter = ("tipo",)
