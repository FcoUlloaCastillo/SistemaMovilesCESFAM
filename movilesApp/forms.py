from django import forms
from django.utils import timezone
from .models import (
    Vehiculo,
    Conductor,
    UnidadSolicitante,
    ActividadSalud,
    Destino,
    ReservaMovil
)


class VehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        fields = '__all__'

    def clean_anio(self):
        anio = self.cleaned_data.get('anio')

        anio_actual = timezone.now().year

        if anio > anio_actual:
            raise forms.ValidationError(
                'El año del vehículo no puede ser mayor al año actual.'
            )

        if anio < 1990:
            raise forms.ValidationError(
                'El año del vehículo parece inválido.'
            )

        return anio

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')

        if capacidad <= 0:
            raise forms.ValidationError(
                'La capacidad debe ser mayor que 0.'
            )

        return capacidad


class ConductorForm(forms.ModelForm):

    class Meta:
        model = Conductor
        fields = '__all__'

    def clean_rut(self):
        rut = self.cleaned_data['rut']

        # Limpiar formato
        rut = rut.replace('.', '').replace('-', '').upper()

        # Validar largo mínimo
        if len(rut) < 2:
            raise forms.ValidationError(
                'El RUT ingresado es inválido.'
            )

        # Validar números
        if not rut[:-1].isdigit():
            raise forms.ValidationError(
                'El RUT debe contener números y un dígito verificador.'
            )

        cuerpo = rut[:-1]
        dv = rut[-1]

        suma = 0
        multiplo = 2

        for c in reversed(cuerpo):
            suma += int(c) * multiplo

            multiplo += 1

            if multiplo > 7:
                multiplo = 2

        resto = suma % 11
        dv_calculado = 11 - resto

        if dv_calculado == 11:
            dv_calculado = '0'

        elif dv_calculado == 10:
            dv_calculado = 'K'

        else:
            dv_calculado = str(dv_calculado)

        # Validar dígito verificador
        if dv != dv_calculado:
            raise forms.ValidationError(
                'El RUT ingresado es incorrecto. Verifique el dígito verificador.'
            )

        return self.cleaned_data['rut']


class UnidadSolicitanteForm(forms.ModelForm):
    class Meta:
        model = UnidadSolicitante
        fields = '__all__'


class ActividadSaludForm(forms.ModelForm):
    class Meta:
        model = ActividadSalud
        fields = '__all__'


class DestinoForm(forms.ModelForm):
    class Meta:
        model = Destino
        fields = '__all__'


class ReservaMovilForm(forms.ModelForm):
    class Meta:
        model = ReservaMovil
        fields = '__all__'
        widgets = {
            'fecha_reserva': forms.DateInput(attrs={'type': 'date','min': timezone.now().date().strftime('%Y-%m-%d')},format='%Y-%m-%d'),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'},format='%H:%M'),
            'hora_termino': forms.TimeInput(attrs={'type': 'time'},format='%H:%M'),
    }

    input_formats = {
        'fecha_reserva': ['%Y-%m-%d'],
        'hora_inicio': ['%H:%M'],
        'hora_termino': ['%H:%M'],
    }

    def clean(self):
        cleaned_data = super().clean()

        vehiculo = cleaned_data.get('vehiculo')
        conductor = cleaned_data.get('conductor')
        fecha_reserva = cleaned_data.get('fecha_reserva')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_termino = cleaned_data.get('hora_termino')

        if fecha_reserva:
            if fecha_reserva < timezone.now().date():
                raise forms.ValidationError(
                    'No se pueden registrar reservas con fechas anteriores a la fecha actual.'
        )

        # Validación 1: la hora de término debe ser mayor que la hora de inicio.
        if hora_inicio and hora_termino:
            if hora_termino <= hora_inicio:
                raise forms.ValidationError(
                    'La hora de término debe ser mayor que la hora de inicio.'
                )

        # Validación 2: no permitir reservar vehículos fuera de servicio,
        # en mantención o ya reservados por otra reserva.
        if vehiculo:
            es_edicion = self.instance and self.instance.id

            if vehiculo.estado != 'Disponible':
                if not es_edicion or self.instance.vehiculo_id != vehiculo.id:
                    raise forms.ValidationError(
                        'El vehículo seleccionado no se encuentra disponible para reservas.'
                    )

        # Validación 3: evitar cruce de horario del mismo vehículo.
        if vehiculo and fecha_reserva and hora_inicio and hora_termino:
            reservas_vehiculo = ReservaMovil.objects.filter(
                vehiculo=vehiculo,
                fecha_reserva=fecha_reserva
            )

            if self.instance and self.instance.id:
                reservas_vehiculo = reservas_vehiculo.exclude(id=self.instance.id)

            for reserva in reservas_vehiculo:
                conflicto = (
                    hora_inicio < reserva.hora_termino and
                    hora_termino > reserva.hora_inicio
                )

                if conflicto:
                    raise forms.ValidationError(
                        'El vehículo seleccionado ya tiene una reserva en ese horario.'
                    )

        # Validación 4: evitar cruce de horario del mismo conductor.
        if conductor and fecha_reserva and hora_inicio and hora_termino:
            reservas_conductor = ReservaMovil.objects.filter(
                conductor=conductor,
                fecha_reserva=fecha_reserva
            )

            if self.instance and self.instance.id:
                reservas_conductor = reservas_conductor.exclude(id=self.instance.id)

            for reserva in reservas_conductor:
                conflicto = (
                    hora_inicio < reserva.hora_termino and
                    hora_termino > reserva.hora_inicio
                )

                if conflicto:
                    raise forms.ValidationError(
                        'El conductor seleccionado ya tiene una reserva en ese horario.'
                    )

        return cleaned_data