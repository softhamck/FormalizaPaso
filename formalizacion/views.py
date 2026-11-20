from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

from .models import Negocio, PasoRuta, RutaFormalizacion, Tramite


# TRÁMITES

def lista_tramites(request):
    tramites = Tramite.objects.order_by("nombre")
    return render(request, "listados/tramites.html", {"tramites": tramites})


def detalle_tramite(request, pk):
    tramite = get_object_or_404(Tramite, pk=pk)
    return render(request, "detalles/tramite.html", {"tramite": tramite})


# NEGOCIOS

@login_required
def lista_negocios(request):
    negocios = Negocio.objects.select_related("usuario").order_by("nombre")

    if not request.user.is_staff:
        negocios = negocios.filter(usuario=request.user)

    return render(request, "listados/negocios.html", {"negocios": negocios})


@login_required
def detalle_negocio(request, pk):
    negocios = Negocio.objects.select_related("usuario")

    if not request.user.is_staff:
        negocios = negocios.filter(usuario=request.user)

    negocio = get_object_or_404(negocios, pk=pk)
    rutas = negocio.rutas.order_by("-fecha_creacion")

    return render(request, "detalles/negocio.html", {
        "negocio": negocio,
        "rutas": rutas,
    })


# RUTAS DE FORMALIZACIÓN

@login_required
def lista_rutas(request):
    rutas = RutaFormalizacion.objects.select_related("negocio").order_by(
        "negocio__nombre", "-fecha_creacion"
    )

    if not request.user.is_staff:
        rutas = rutas.filter(negocio__usuario=request.user)

    return render(request, "listados/rutas.html", {"rutas": rutas})


@login_required
def detalle_ruta(request, pk):
    rutas = RutaFormalizacion.objects.select_related("negocio")

    if not request.user.is_staff:
        rutas = rutas.filter(negocio__usuario=request.user)

    ruta = get_object_or_404(rutas, pk=pk)
    pasos = ruta.pasos.select_related("tramite").order_by("orden")

    return render(request, "detalles/ruta.html", {
        "ruta": ruta,
        "pasos": pasos,
    })


# PASOS DE RUTA

@login_required
def lista_pasos(request):
    pasos = PasoRuta.objects.select_related("ruta__negocio", "tramite").order_by(
        "ruta__negocio__nombre", "ruta_id", "orden"
    )

    if not request.user.is_staff:
        pasos = pasos.filter(ruta__negocio__usuario=request.user)

    return render(request, "listados/pasos.html", {"pasos": pasos})


@login_required
def detalle_paso(request, pk):
    pasos = PasoRuta.objects.select_related("ruta__negocio", "tramite")

    if not request.user.is_staff:
        pasos = pasos.filter(ruta__negocio__usuario=request.user)

    paso = get_object_or_404(pasos, pk=pk)
    return render(request, "detalles/paso.html", {"paso": paso})


# USUARIOS

@staff_member_required(login_url="login")
def lista_usuarios(request):
    usuarios = User.objects.order_by("username")
    return render(request, "listados/usuarios.html", {"usuarios": usuarios})


@staff_member_required(login_url="login")
def detalle_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    negocios = usuario.negocios.order_by("nombre")

    return render(request, "detalles/usuario.html", {
        "usuario": usuario,
        "negocios": negocios,
    })