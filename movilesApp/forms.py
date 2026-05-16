import re

from django import forms
from django.db.models import Q
from django.utils import timezone

from .models import (
    Vehiculo,
    Conductor,
    UnidadSolicitante,
    ActividadSalud,
    Destino,
    ReservaMovil
)


ESTADOS_RESERVA_BLOQUEANTES = ['Pendiente', 'Aprobada', 'En proceso']


def validar_telefono_chileno(valor):
    if not valor:
        return valor

    telefono = valor.strip()

    if not re.fullmatch(r'[\d+\s()-]{8,20}', telefono):
        raise forms.ValidationError(
            'Ingrese un telefono valido. Use solo numeros, espacios, +, parentesis o guiones.'
        )

    digitos = re.sub(r'\D', '', telefono)

    if len(digitos) < 8:
        raise forms.ValidationError(
            'El telefono debe tener al menos 8 digitos.'
        )

    return telefono


def validar_texto_minimo(valor, nombre_campo, largo_minimo=3):
    if not valor or len(valor.strip()) < largo_minimo:
        raise forms.ValidationError(
            f'{nombre_campo} debe tener al menos {largo_minimo} caracteres.'
        )

    return valor.strip()


class VehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        fields = '__all__'

    def clean_patente(self):
        patente = self.cleaned_data.get('patente', '').strip().upper()
        patente = patente.replace('.', '').replace(' ', '').replace('-', '')

        if not re.fullmatch(r'[A-Z]{2}\d{4}|[A-Z]{4}\d{2}', patente):
            raise forms.ValidationError(
                'Ingrese una patente chilena valida. Ejemplos: AB1234 o ABCD12.'
            )

        existe_patente = Vehiculo.objects.filter(patente__iexact=patente)

        if self.instance and self.instance.id:
            existe_patente = existe_patente.exclude(id=self.instance.id)

        if existe_patente.exists():
            raise forms.ValidationError(
                'Ya existe un vehiculo registrado con esa patente.'
            )

        return patente

    def clean_marca(self):
        return validar_texto_minimo(self.cleaned_data.get('marca'), 'La marca')

    def clean_modelo(self):
        return validar_texto_minimo(self.cleaned_data.get('modelo'), 'El modelo')

    def clean_anio(self):
        anio = self.cleaned_data.get('anio')

        if anio is None:
            return anio

        anio_actual = timezone.now().year

        if anio > anio_actual:
            raise forms.ValidationError(
                'El anio del vehiculo no puede ser mayor al anio actual.'
            )

        if anio < 1990:
            raise forms.ValidationError(
                'El anio del vehiculo parece invalido.'
            )

        return anio

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')

        if capacidad is None:
            return capacidad

        if capacidad <= 0:
            raise forms.ValidationError(
                'La capacidad debe ser mayor que 0.'
            )

        return capacidad


class ConductorForm(forms.ModelForm):

    class Meta:
        model = Conductor
        fields = '__all__'

    def clean_nombre_completo(self):
        return validar_texto_minimo(
            self.cleaned_data.get('nombre_completo'),
            'El nombre del conductor'
        )

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        rut = rut.replace('.', '').replace('-', '').upper()

        if len(rut) < 2:
            raise forms.ValidationError(
                'El RUT ingresado es invalido.'
            )

        if not rut[:-1].isdigit():
            raise forms.ValidationError(
                'El RUT debe contener numeros y un digito verificador.'
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

        if dv != dv_calculado:
            raise forms.ValidationError(
                'El RUT ingresado es incorrecto. Verifique el digito verificador.'
            )

        rut_formateado = f'{int(cuerpo):,}'.replace(',', '.') + f'-{dv}'
        existe_rut = Conductor.objects.filter(
            Q(rut__iexact=rut_formateado) | Q(rut__iexact=rut)
        )

        if self.instance and self.instance.id:
            existe_rut = existe_rut.exclude(id=self.instance.id)

        if existe_rut.exists():
            raise forms.ValidationError(
                'Ya existe un conductor registrado con ese RUT.'
            )

        return rut_formateado

    def clean_telefono(self):
        return validar_telefono_chileno(self.cleaned_data.get('telefono'))


class UnidadSolicitanteForm(forms.ModelForm):
    class Meta:
        model = UnidadSolicitante
        fields = '__all__'

    def clean_nombre(self):
        nombre = validar_texto_minimo(
            self.cleaned_data.get('nombre'),
            'El nombre de la unidad'
        )

        existe_nombre = UnidadSolicitante.objects.filter(nombre__iexact=nombre)

        if self.instance and self.instance.id:
            existe_nombre = existe_nombre.exclude(id=self.instance.id)

        if existe_nombre.exists():
            raise forms.ValidationError(
                'Ya existe una unidad solicitante con ese nombre.'
            )

        return nombre

    def clean_responsable(self):
        return validar_texto_minimo(
            self.cleaned_data.get('responsable'),
            'El responsable'
        )

    def clean_telefono_contacto(self):
        return validar_telefono_chileno(self.cleaned_data.get('telefono_contacto'))


class ActividadSaludForm(forms.ModelForm):
    class Meta:
        model = ActividadSalud
        fields = '__all__'

    def clean_nombre(self):
        nombre = validar_texto_minimo(
            self.cleaned_data.get('nombre'),
            'El nombre de la actividad'
        )

        existe_nombre = ActividadSalud.objects.filter(nombre__iexact=nombre)

        if self.instance and self.instance.id:
            existe_nombre = existe_nombre.exclude(id=self.instance.id)

        if existe_nombre.exists():
            raise forms.ValidationError(
                'Ya existe una actividad de salud con ese nombre.'
            )

        return nombre


class DestinoForm(forms.ModelForm):
    class Meta:
        model = Destino
        fields = '__all__'

    def clean_nombre_lugar(self):
        return validar_texto_minimo(
            self.cleaned_data.get('nombre_lugar'),
            'El nombre del lugar'
        )

    def clean_direccion(self):
        direccion = validar_texto_minimo(
            self.cleaned_data.get('direccion'),
            'La direccion',
            5
        )

        existe_destino = Destino.objects.filter(direccion__iexact=direccion)

        if self.instance and self.instance.id:
            existe_destino = existe_destino.exclude(id=self.instance.id)

        if existe_destino.exists():
            raise forms.ValidationError(
                'Ya existe un destino registrado con esa direccion.'
            )

        return direccion

    def clean(self):
        cleaned_data = super().clean()
        latitud = cleaned_data.get('latitud')
        longitud = cleaned_data.get('longitud')

        if (latitud is None) != (longitud is None):
            raise forms.ValidationError(
                'Debe ingresar latitud y longitud juntas, o dejar ambas vacias.'
            )

        if latitud is not None and not (-90 <= latitud <= 90):
            self.add_error('latitud', 'La latitud debe estar entre -90 y 90.')

        if longitud is not None and not (-180 <= longitud <= 180):
            self.add_error('longitud', 'La longitud debe estar entre -180 y 180.')

        return cleaned_data


class ReservaMovilForm(forms.ModelForm):
    class Meta:
        model = ReservaMovil
        fields = '__all__'
        widgets = {
            'fecha_reserva': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': timezone.now().date().strftime('%Y-%m-%d')
                },
                format='%Y-%m-%d'
            ),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'hora_termino': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_reserva'].input_formats = ['%Y-%m-%d']
        self.fields['hora_inicio'].input_formats = ['%H:%M']
        self.fields['hora_termino'].input_formats = ['%H:%M']

    def clean(self):
        cleaned_data = super().clean()

        vehiculo = cleaned_data.get('vehiculo')
        conductor = cleaned_data.get('conductor')
        fecha_reserva = cleaned_data.get('fecha_reserva')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_termino = cleaned_data.get('hora_termino')
        estado = cleaned_data.get('estado') or 'Pendiente'
        es_estado_bloqueante = estado in ESTADOS_RESERVA_BLOQUEANTES

        if fecha_reserva and fecha_reserva < timezone.now().date():
            raise forms.ValidationError(
                'No se pueden registrar reservas con fechas anteriores a la fecha actual.'
            )

        if hora_inicio and hora_termino and hora_termino <= hora_inicio:
            raise forms.ValidationError(
                'La hora de termino debe ser mayor que la hora de inicio.'
            )

        if vehiculo and es_estado_bloqueante:
            if vehiculo.estado in ['Mantencion', 'Fuera de servicio']:
                raise forms.ValidationError(
                    'El vehiculo seleccionado esta en mantencion o fuera de servicio.'
                )

        if conductor and es_estado_bloqueante and conductor.estado != 'Disponible':
            raise forms.ValidationError(
                'El conductor seleccionado no se encuentra disponible para reservas.'
            )

        if vehiculo and conductor and es_estado_bloqueante:
            licencias_por_tipo = {
                'Ambulancia': ['A2', 'A3'],
                'Furgon': ['A1', 'A2', 'A3', 'B'],
                'Camioneta': ['A2', 'A3', 'A4', 'A5', 'B'],
                'Otro': ['A1', 'A2', 'A3', 'A4', 'A5', 'B', 'C', 'D', 'E', 'F'],
            }
            licencias_permitidas = licencias_por_tipo.get(vehiculo.tipo, [])

            if licencias_permitidas and conductor.tipo_licencia not in licencias_permitidas:
                raise forms.ValidationError(
                    'La licencia del conductor no es compatible con el tipo de vehiculo seleccionado.'
                )

        if es_estado_bloqueante and vehiculo and fecha_reserva and hora_inicio and hora_termino:
            reservas_vehiculo = ReservaMovil.objects.filter(
                vehiculo=vehiculo,
                fecha_reserva=fecha_reserva,
                estado__in=ESTADOS_RESERVA_BLOQUEANTES
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
                        'El vehiculo seleccionado ya tiene una reserva activa en ese horario.'
                    )

        if es_estado_bloqueante and conductor and fecha_reserva and hora_inicio and hora_termino:
            reservas_conductor = ReservaMovil.objects.filter(
                conductor=conductor,
                fecha_reserva=fecha_reserva,
                estado__in=ESTADOS_RESERVA_BLOQUEANTES
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
                        'El conductor seleccionado ya tiene una reserva activa en ese horario.'
                    )

        return cleaned_data
