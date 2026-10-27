from django.contrib import admin

from .models import (
    Negocio,
    Tramite,
    RutaFormalizacion,
    PasoRuta,
)


admin.site.register(Negocio)
admin.site.register(Tramite)
admin.site.register(RutaFormalizacion)
admin.site.register(PasoRuta)