from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from formalizacion import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "accounts/login/",
        auth_views.LoginView.as_view(next_page="lista_negocios"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="inicio"),
        name="logout",
    ),

    path("", views.lista_negocios, name="inicio"),

    path("tramites/", views.lista_tramites, name="lista_tramites"),
    path("tramites/<int:pk>/", views.detalle_tramite, name="detalle_tramite"),

    path("negocios/", views.lista_negocios, name="lista_negocios"),
    path("negocios/<int:pk>/", views.detalle_negocio, name="detalle_negocio"),

    path("rutas/", views.lista_rutas, name="lista_rutas"),
    path("rutas/<int:pk>/", views.detalle_ruta, name="detalle_ruta"),

    path("pasos/", views.lista_pasos, name="lista_pasos"),
    path("pasos/<int:pk>/", views.detalle_paso, name="detalle_paso"),

    path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
    path("usuarios/<int:pk>/", views.detalle_usuario, name="detalle_usuario"),
]