from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario = models.CharField(max_length=30, unique=True)
    contraseña = models.CharField(max_length=128)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.usuario

class Movimiento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=40)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.cliente.usuario}"
    
class Boveda(models.Model):
    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre