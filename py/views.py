from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Cliente, Movimiento, Boveda


# ---------------- LOGIN ----------------

def login(request):
    if request.method == "POST":
        usuario = request.POST["username"]
        contraseña = request.POST["password"]
        try:
            cliente = Cliente.objects.get(
                usuario=usuario,
                contraseña=contraseña
            )
            request.session["cliente"] = cliente.id
            return redirect("dashboard")
        except Cliente.DoesNotExist:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "login.html")


# ---------------- REGISTRO ----------------

def registro(request):
    if request.method == "POST":
        usuario = request.POST["username"]
        contraseña = request.POST["password"]
        if Cliente.objects.filter(usuario=usuario).exists():
            messages.error(request, "Ese usuario ya existe.")
            return redirect("registro")
        Cliente.objects.create(
            usuario=usuario,
            contraseña=contraseña
        )
        messages.success(request, "Cuenta creada correctamente.")
        return redirect("login")
    return render(request, "registro.html")


# ---------------- DASHBOARD ----------------

def dashboard(request):
    if "cliente" not in request.session:
        return redirect("login")

    cliente = Cliente.objects.get(id=request.session["cliente"])
    historial = Movimiento.objects.filter(cliente=cliente).order_by("-fecha")
    bovedas = Boveda.objects.filter(cliente=cliente)

    return render(request, "dashboard.html", {
        "cuenta": cliente,
        "historial": historial,
        "bovedas": bovedas,
    })
from decimal import Decimal, InvalidOperation
from django.shortcuts import redirect
from django.contrib import messages

# ---------------- DEPOSITO ----------------

def deposito(request):
    if request.method == "POST":
        cliente = Cliente.objects.get(id=request.session["cliente"])
        try:
            monto = Decimal(request.POST["monto"])
            if monto <= 0:
                messages.error(request, "El monto debe ser mayor que cero.")
                return redirect("dashboard")
            cliente.saldo += monto
            cliente.save()
            Movimiento.objects.create(
                cliente=cliente,
                tipo="Depósito",
                monto=monto
            )
            messages.success(request, "Depósito realizado correctamente.")
        except (InvalidOperation, KeyError):
            messages.error(request, "Monto inválido.")
    return redirect("dashboard")


# ---------------- RETIRO ----------------

def retiro(request):

    if request.method == "POST":
        cliente = Cliente.objects.get(id=request.session["cliente"])
        try:
            monto = Decimal(request.POST["monto"])
            if monto <= 0:
                messages.error(request, "El monto debe ser mayor que cero.")
                return redirect("dashboard")
            if cliente.saldo >= monto:
                cliente.saldo -= monto
                cliente.save()
                Movimiento.objects.create(
                    cliente=cliente,
                    tipo="Retiro",
                    monto=monto
                )
                messages.success(request, "Retiro realizado correctamente.")
            else:
                messages.error(request, "Saldo insuficiente.")
        except (InvalidOperation, KeyError):
            messages.error(request, "Monto inválido.")
    return redirect("dashboard")


# ---------------- TRANSFERENCIA ----------------

def transferencia(request):
    if request.method == "POST":
        origen = Cliente.objects.get(id=request.session["cliente"])
        try:
            destino = Cliente.objects.get(
                usuario=request.POST["destino"]
            )
        except Cliente.DoesNotExist:
            messages.error(request, "El usuario destino no existe.")
            return redirect("dashboard")
        try:
            monto = Decimal(request.POST["monto"])
            if monto <= 0:
                messages.error(request, "El monto debe ser mayor que cero.")
                return redirect("dashboard")
            if origen.saldo >= monto:
                origen.saldo -= monto
                destino.saldo += monto
                origen.save()
                destino.save()
                Movimiento.objects.create(
                    cliente=origen,
                    tipo="Transferencia enviada",
                    monto=monto
                )
                Movimiento.objects.create(
                    cliente=destino,
                    tipo="Transferencia recibida",
                    monto=monto
                )
                messages.success(request, "Transferencia realizada correctamente.")
            else:
                messages.error(request, "Saldo insuficiente.")
        except (InvalidOperation, KeyError):
            messages.error(request, "Monto inválido.")
    return redirect("dashboard")

def crear_boveda(request):
    if "cliente" not in request.session:
        return redirect("login")

    if request.method == "POST":
        cliente = Cliente.objects.get(id=request.session["cliente"])
        nombre = request.POST.get("nombre")

        if not nombre:
            messages.error(request, "Debes escribir un nombre para la bóveda.")
            return redirect("dashboard")

        Boveda.objects.create(
            cliente=cliente,
            nombre=nombre
        )

        messages.success(request, "Bóveda creada correctamente.")

    return redirect("dashboard")