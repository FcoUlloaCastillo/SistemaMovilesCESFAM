from django.contrib import admin
from .models import Vehiculo, Conductor, UnidadSolicitante, ActividadSalud, Destino, ReservaMovil

admin.site.register(Vehiculo)
admin.site.register(Conductor)
admin.site.register(UnidadSolicitante)
admin.site.register(ActividadSalud)
admin.site.register(Destino)
admin.site.register(ReservaMovil)