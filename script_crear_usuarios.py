"""
Script para crear usuarios y grupos de permisos en el sistema.
Ejecutar con: python manage.py shell < script_crear_usuarios.py

Este script crea:
1. Grupo 'solo_lectura' con permisos restrictivos
2. Superusuario 'admin' 
3. Usuario 'javier' con permisos de solo lectura
"""

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from movilesApp.models import Vehiculo, Conductor, UnidadSolicitante, ActividadSalud, Destino, ReservaMovil

print("=" * 70)
print("CREANDO USUARIOS Y GRUPOS DE PERMISOS")
print("=" * 70)

# 1. Crear grupo 'solo_lectura'
print("\n1. Creando grupo 'solo_lectura'...")
grupo_lectura, created = Group.objects.get_or_create(name='solo_lectura')
if created:
    print("   ✓ Grupo 'solo_lectura' creado exitosamente")
else:
    print("   ℹ Grupo 'solo_lectura' ya existe")

# Agregar solo permisos de visualización (view)
modelos = [Vehiculo, Conductor, UnidadSolicitante, ActividadSalud, Destino, ReservaMovil]
permisos_view = []

for modelo in modelos:
    content_type = ContentType.objects.get_for_model(modelo)
    try:
        permiso = Permission.objects.get(
            content_type=content_type,
            codename=f'view_{modelo._meta.model_name}'
        )
        permisos_view.append(permiso)
    except Permission.DoesNotExist:
        pass

grupo_lectura.permissions.set(permisos_view)
print(f"   ✓ Se asignaron {len(permisos_view)} permisos de visualización")

# 2. Crear o actualizar superusuario 'admin'
print("\n2. Creando/actualizando superusuario 'admin'...")
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@cesfam.local',
        'is_staff': True,
        'is_superuser': True
    }
)

if created:
    admin_user.set_password('admin123')
    admin_user.save()
    print("   ✓ Superusuario 'admin' creado exitosamente")
    print("   📧 Usuario: admin")
    print("   🔐 Contraseña: admin123")
else:
    print("   ℹ Superusuario 'admin' ya existe")

# 3. Crear usuario 'javier' con permisos de solo lectura
print("\n3. Creando usuario 'javier' con permisos de solo lectura...")
javier_user, created = User.objects.get_or_create(
    username='javier',
    defaults={
        'email': 'javier@cesfam.local'
    }
)

if created:
    javier_user.set_password('soporte1@')
    javier_user.save()
    # Agregar al grupo solo_lectura
    javier_user.groups.add(grupo_lectura)
    print("   ✓ Usuario 'javier' creado exitosamente")
    print("   📧 Usuario: javier")
    print("   🔐 Contraseña: soporte1@")
    print("   📋 Permisos: Solo lectura (sin editar ni eliminar)")
else:
    print("   ℹ Usuario 'javier' ya existe")
    # Asegurarse de que tiene el grupo correcto
    if not javier_user.groups.filter(name='solo_lectura').exists():
        javier_user.groups.add(grupo_lectura)
        print("   ✓ Se agregó el grupo 'solo_lectura' a 'javier'")

print("\n" + "=" * 70)
print("RESUMEN DE USUARIOS CREADOS")
print("=" * 70)
print("\n📌 SUPERUSUARIO (acceso total)")
print("   Usuario: admin")
print("   Contraseña: admin123")
print("   Acceso: Todas las funciones + Admin panel")
print("\n📌 USUARIO SOLO LECTURA")
print("   Usuario: javier")
print("   Contraseña: soporte1@")
print("   Acceso: Solo ver (sin crear, editar ni eliminar)")
print("\n" + "=" * 70)
print("✅ INICIALIZACIÓN COMPLETADA")
print("=" * 70)
print("\n💡 Recomendaciones de seguridad:")
print("   1. Cambiar las contraseñas predeterminadas después de la primera sesión")
print("   2. Usar HTTPS en producción")
print("   3. Configurar variables de entorno para credenciales sensibles")
print("   4. Revisar y actualizar los permisos según sea necesario")
print("\n")
