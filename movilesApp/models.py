from django.db import models


# Modelo que almacena los vehículos institucionales disponibles.
class Vehiculo(models.Model):
    ESTADO_CHOICES = [
        ('Disponible', 'Disponible'),
        ('Reservado', 'Reservado'),
        ('Mantencion', 'Mantención'),
        ('Fuera de servicio', 'Fuera de servicio'),
    ]

    TIPO_CHOICES = [
        ('Camioneta', 'Camioneta'),
        ('Furgon', 'Furgón'),
        ('Ambulancia', 'Ambulancia'),
        ('Otro', 'Otro'),
    ]

    patente = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()
    capacidad = models.IntegerField()
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='Disponible')
    observacion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='vehiculos/', blank=True, null=True)

    def __str__(self):
        return f"{self.patente} - {self.tipo}"

    class Meta:
        db_table = 'vehiculo'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'


# Modelo que registra los conductores o funcionarios responsables de manejar los móviles.
class Conductor(models.Model):
    ESTADO_CHOICES = [
        ('Disponible', 'Disponible'),
        ('No disponible', 'No disponible'),
        ('Licencia medica', 'Licencia médica'),
        ('Vacaciones', 'Vacaciones'),
    ]

    LICENCIA_CHOICES = [
        ('A1', 'A1 - Transporte de pasajeros'),
        ('A2', 'A2 - Taxi, ambulancia y transporte'),
        ('A3', 'A3 - Transporte remunerado de pasajeros'),
        ('A4', 'A4 - Transporte de carga'),
        ('A5', 'A5 - Vehículos articulados'),
        ('B', 'B - Vehículos particulares'),
        ('C', 'C - Motocicletas'),
        ('D', 'D - Maquinaria automotriz'),
        ('E', 'E - Vehículos de tracción animal'),
        ('F', 'F - Vehículos policiales y FF.AA.'),
    ]

    nombre_completo = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    tipo_licencia = models.CharField(max_length=10, choices=LICENCIA_CHOICES)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='Disponible')

    def __str__(self):
        return self.nombre_completo

    class Meta:
        db_table = 'conductor'
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'


# Modelo que representa los módulos, unidades o servicios que solicitan el uso de móviles.
class UnidadSolicitante(models.Model):
    nombre = models.CharField(max_length=100)
    responsable = models.CharField(max_length=100)
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True)
    correo_contacto = models.EmailField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'unidad_solicitante'
        verbose_name = 'Unidad solicitante'
        verbose_name_plural = 'Unidades solicitantes'


# Modelo que define las actividades de salud o administrativas asociadas a una reserva.
class ActividadSalud(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'actividad_salud'
        verbose_name = 'Actividad de salud'
        verbose_name_plural = 'Actividades de salud'


# Modelo que almacena la dirección o destino asociado a una actividad.
class Destino(models.Model):
    nombre_lugar = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)
    referencia = models.TextField(blank=True, null=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_lugar} - {self.direccion}"

    class Meta:
        db_table = 'destino'
        verbose_name = 'Destino'
        verbose_name_plural = 'Destinos'


# Modelo principal que registra la reserva de un móvil institucional.
class ReservaMovil(models.Model):
    ESTADOS_BLOQUEAN_RECURSOS = ['Pendiente', 'Aprobada', 'En proceso']

    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aprobada', 'Aprobada'),
        ('En proceso', 'En proceso'),
        ('Finalizada', 'Finalizada'),
        ('Cancelada', 'Cancelada'),
    ]

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT)
    conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT)
    unidad_solicitante = models.ForeignKey(UnidadSolicitante, on_delete=models.PROTECT)
    actividad = models.ForeignKey(ActividadSalud, on_delete=models.PROTECT)
    destino = models.ForeignKey(Destino, on_delete=models.PROTECT)

    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='Pendiente')
    observacion = models.TextField(blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    @classmethod
    def sincronizar_estado_vehiculo(cls, vehiculo):
        tiene_reservas_activas = cls.objects.filter(
            vehiculo=vehiculo,
            estado__in=cls.ESTADOS_BLOQUEAN_RECURSOS
        ).exists()

        if tiene_reservas_activas and vehiculo.estado == 'Disponible':
            vehiculo.estado = 'Reservado'
            vehiculo.save(update_fields=['estado'])

        if not tiene_reservas_activas and vehiculo.estado == 'Reservado':
            vehiculo.estado = 'Disponible'
            vehiculo.save(update_fields=['estado'])

    def save(self, *args, **kwargs):
        vehiculo_anterior = None

        if self.pk:
            vehiculo_anterior = (
                ReservaMovil.objects
                .filter(pk=self.pk)
                .values_list('vehiculo_id', flat=True)
                .first()
            )

        super().save(*args, **kwargs)

        vehiculos_a_sincronizar = {self.vehiculo_id}

        if vehiculo_anterior and vehiculo_anterior != self.vehiculo_id:
            vehiculos_a_sincronizar.add(vehiculo_anterior)

        for vehiculo_id in vehiculos_a_sincronizar:
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)
            self.sincronizar_estado_vehiculo(vehiculo)

    def delete(self, *args, **kwargs):
        vehiculo = self.vehiculo
        resultado = super().delete(*args, **kwargs)
        self.sincronizar_estado_vehiculo(vehiculo)
        return resultado

    def __str__(self):
        return f"Reserva {self.id} - {self.unidad_solicitante} - {self.fecha_reserva}"

    class Meta:
        db_table = 'reserva_movil'
        verbose_name = 'Reserva de móvil'
        verbose_name_plural = 'Reservas de móviles'
