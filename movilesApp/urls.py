from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    # Vehículos
    path('vehiculos/', views.listar_vehiculos, name='listar_vehiculos'),
    path('vehiculos/crear/', views.crear_vehiculo, name='crear_vehiculo'),
    path('vehiculos/editar/<int:id>/', views.editar_vehiculo, name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:id>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
    path('vehiculos/detalle/<int:id>/', views.detalle_vehiculo, name='detalle_vehiculo'),

    # Conductores
    path('conductores/', views.listar_conductores, name='listar_conductores'),
    path('conductores/crear/', views.crear_conductor, name='crear_conductor'),
    path('conductores/editar/<int:id>/', views.editar_conductor, name='editar_conductor'),
    path('conductores/eliminar/<int:id>/', views.eliminar_conductor, name='eliminar_conductor'),
    path('conductores/detalle/<int:id>/', views.detalle_conductor,name='detalle_conductor'),

    # Unidades solicitantes
    path('unidades/', views.listar_unidades, name='listar_unidades'),
    path('unidades/crear/', views.crear_unidad, name='crear_unidad'),
    path('unidades/editar/<int:id>/', views.editar_unidad, name='editar_unidad'),
    path('unidades/eliminar/<int:id>/', views.eliminar_unidad, name='eliminar_unidad'),
    path('unidades/detalle/<int:id>/', views.detalle_unidad, name='detalle_unidad'),

    # Actividades de salud
    path('actividades/', views.listar_actividades, name='listar_actividades'),
    path('actividades/crear/', views.crear_actividad, name='crear_actividad'),
    path('actividades/editar/<int:id>/', views.editar_actividad, name='editar_actividad'),
    path('actividades/eliminar/<int:id>/', views.eliminar_actividad, name='eliminar_actividad'),
    path('actividades/detalle/<int:id>/', views.detalle_actividad, name='detalle_actividad'),

    # Destinos
    path('destinos/', views.listar_destinos, name='listar_destinos'),
    path('destinos/crear/', views.crear_destino, name='crear_destino'),
    path('destinos/editar/<int:id>/', views.editar_destino, name='editar_destino'),
    path('destinos/eliminar/<int:id>/', views.eliminar_destino, name='eliminar_destino'),
    path('destinos/detalle/<int:id>/', views.detalle_destino, name='detalle_destino'),

    # Reservas
    path('reservas/', views.listar_reservas, name='listar_reservas'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),
    path('reservas/editar/<int:id>/', views.editar_reserva, name='editar_reserva'),
    path('reservas/eliminar/<int:id>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('reservas/detalle/<int:id>/', views.detalle_reserva, name='detalle_reserva'),

    # Exportar Vehiculos excel y pdf
    path('vehiculos/exportar/excel/', views.exportar_vehiculos_excel, name='exportar_vehiculos_excel'),
    path('vehiculos/exportar/pdf/', views.exportar_vehiculos_pdf, name='exportar_vehiculos_pdf'),

    # Exportar Conductores excel y pdf
    path('conductores/exportar/excel/', views.exportar_conductores_excel, name='exportar_conductores_excel'),
    path('conductores/exportar/pdf/', views.exportar_conductores_pdf, name='exportar_conductores_pdf'),

    # Exportar Unidades excel y pdf
    path('unidades/exportar/excel/', views.exportar_unidades_excel, name='exportar_unidades_excel'),
    path('unidades/exportar/pdf/', views.exportar_unidades_pdf, name='exportar_unidades_pdf'),

    # Exportar Actividades excel y pdf
    path('actividades/exportar/excel/', views.exportar_actividades_excel, name='exportar_actividades_excel'),
    path('actividades/exportar/pdf/', views.exportar_actividades_pdf, name='exportar_actividades_pdf'),

    # Exportar Destinos excel y pdf
    path('destinos/exportar/excel/', views.exportar_destinos_excel, name='exportar_destinos_excel'),
    path('destinos/exportar/pdf/', views.exportar_destinos_pdf, name='exportar_destinos_pdf'),

    # Exportar Reservas excel y pdf
    path('reservas/exportar/excel/', views.exportar_reservas_excel, name='exportar_reservas_excel'),
    path('reservas/exportar/pdf/', views.exportar_reservas_pdf, name='exportar_reservas_pdf'),

]