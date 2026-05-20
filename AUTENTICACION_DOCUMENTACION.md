# 🔐 Documentación - Sistema de Autenticación y Permisos

## 📋 Descripción General

Se ha implementado un sistema profesional de autenticación y control de permisos con:
- ✅ Autenticación rigurosa con validaciones
- ✅ Protección con `never_cache` en todas las vistas
- ✅ Sistema de permisos de lectura/escritura
- ✅ Grupo especial "solo_lectura" para usuarios restringidos
- ✅ Solo superusuarios ven el enlace "Admin" en el menú
- ✅ Cierre de sesión seguro (no permite volver atrás)

---

## 👤 Usuarios Creados

### 1. **Superusuario (ADMIN)**
- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **Permisos:** Acceso total a todas las funciones
- **Menú:** Ve el enlace "🔐 Admin" en la navegación

### 2. **Usuario Solo Lectura (JAVIER)**
- **Usuario:** `javier`
- **Contraseña:** `soporte1@`
- **Permisos:** Solo visualizar datos (sin crear, editar ni eliminar)
- **Menú:** 
  - ✅ Puede ver todos los listados
  - ✅ Puede ver detalles de registros
  - ❌ NO ve botones de crear
  - ❌ NO ve botones de editar
  - ❌ NO ve botones de eliminar

---

## 🔒 Estructura de Autenticación

### **Carpeta creada:** `templates/autenticacion/`

Contiene:
- `login.html` - Formulario profesional de inicio de sesión
- `registro.html` - Formulario de registro de nuevos usuarios

### **Rutas de autenticación agregadas:**

```
/login/              → Iniciar sesión
/registro/           → Registrarse
/cerrar-sesion/      → Cerrar sesión
```

---

## 🛡️ Sistema de Permisos

### **Decorador personalizado: `@solo_lectura`**

Este decorador verifica si el usuario está en el grupo "solo_lectura" y lo redirige si intenta acceder a:
- Crear registros (POST)
- Editar registros (PUT)
- Eliminar registros (DELETE)

**Vistas protegidas con `@solo_lectura`:**
- ✅ `crear_vehiculo`, `editar_vehiculo`, `eliminar_vehiculo`
- ✅ `crear_conductor`, `editar_conductor`, `eliminar_conductor`
- ✅ `crear_unidad`, `editar_unidad`, `eliminar_unidad`
- ✅ `crear_actividad`, `editar_actividad`, `eliminar_actividad`
- ✅ `crear_destino`, `editar_destino`, `eliminar_destino`
- ✅ `crear_reserva`, `editar_reserva`, `eliminar_reserva`

### **Decorador `@never_cache`**

Aplicado a TODAS las vistas para prevenir:
- Caché de páginas protegidas
- Acceso mediante botón "atrás" del navegador sin autenticación
- Uso de datos en caché cuando se cierra sesión

---

## 🔑 Validaciones Rigurosas

### **Login:**
- ✅ Valida que usuario y contraseña no estén vacíos
- ✅ Valida credenciales contra base de datos
- ✅ Mensaje claro si son incorrectos

### **Registro:**
- ✅ Usuario: máximo 150 caracteres
- ✅ Usuario: solo acepta letras, números, @, ., +, - y _
- ✅ Usuario: no puede existir otro con el mismo nombre
- ✅ Email: debe ser válido y único
- ✅ Contraseña: mínimo 8 caracteres
- ✅ Confirmación de contraseña: debe coincidir
- ✅ Mensajes de error claros y específicos

---

## 🎨 Interfaz de Usuario

### **Barra de Navegación Mejorada:**

**Lado izquierdo:**
- Inicio
- Vehículos
- Conductores
- Unidades
- Actividades
- Destinos
- Reservas
- 🔐 Admin (solo si es superusuario)

**Lado derecho:**
- Si está autenticado: `👤 [nombre_usuario] | Cerrar Sesión`
- Si no está autenticado: `Iniciar Sesión`

### **Formularios de Autenticación:**

Diseño profesional con:
- Gradientes de color
- Validación en tiempo real
- Mensajes de error detallados
- Responsive (adaptable a móviles)
- Enlace para alternar entre login/registro

---

## 🔄 Flujo de Autenticación

### **Primera vez (Usuario nuevo):**
```
1. Usuario no autenticado
2. Accede a cualquier página
3. Se redirige a /login/
4. Opción: Hacer clic en "Registrarse"
5. Completa formulario de registro
6. Si valida correctamente → Se crea usuario
7. Mensaje: "Cuenta creada, por favor inicia sesión"
8. Vuelve a /login/
9. Ingresa credenciales
10. Si son correctas → Accede a inicio
```

### **Usuario autenticado:**
```
1. Navega normalmente por la aplicación
2. Todas las vistas están cachidas (never_cache)
3. Cuando cierra sesión → Se redirige a /login/
4. Si presiona "atrás" → NO puede entrar sin autenticarse de nuevo
```

### **Usuario solo lectura (javier):**
```
1. Inicia sesión como 'javier'
2. Ve todos los listados y detalles
3. Intenta crear/editar/eliminar → Se redirige a inicio
4. Mensaje: "No tienes permiso para realizar esta acción"
5. Solo el admin puede hacer cambios
```

---

## 📝 Cambios en Archivos Principales

### **settings.py**
```python
# Nuevas configuraciones agregadas:
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'login'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600  # 1 hora
```

### **urls.py (movilesApp)**
```python
# Rutas de autenticación agregadas al inicio
path('login/', views.login_usuario, name='login'),
path('registro/', views.registro_usuario, name='registro'),
path('cerrar-sesion/', views.cerrar_sesion_usuario, name='cerrar_sesion'),
```

### **views.py**
```python
# Decoradores en todas las vistas:
@never_cache
@login_required(login_url='login')
@solo_lectura  # Solo en vistas de edición/eliminación

# Nuevas vistas:
- login_usuario()
- registro_usuario()
- cerrar_sesion_usuario()
```

### **base.html**
```html
<!-- Navbar mejorada con información de usuario -->
<div class="navbar-derecha">
    {% if user.is_authenticated %}
        <span class="usuario-info">👤 {{ user.username }}</span>
        <form method="POST" action="{% url 'cerrar_sesion' %}">
            <button type="submit">Cerrar Sesión</button>
        </form>
    {% else %}
        <a href="{% url 'login' %}">Iniciar Sesión</a>
    {% endif %}
</div>

<!-- Admin solo para superusuarios -->
{% if user.is_superuser %}
    <a href="/admin/">🔐 Admin</a>
{% endif %}
```

### **styles.css**
```css
/* Estilos mejorados para navbar -->
.navbar { display: flex; justify-content: space-between; }
.usuario-info { color: white; font-weight: bold; }
.btn-logout { background: #e74c3c; ... }
```

---

## 🚀 Cómo Usar el Sistema

### **1. Iniciar sesión:**
- Ir a `http://localhost:8000/login/`
- Ingresar usuario y contraseña
- Hacer clic en "Iniciar Sesión"

### **2. Registrar nuevo usuario:**
- Hacer clic en "Registrarse aquí" en la página de login
- Completar todos los campos
- El sistema validará automáticamente
- Después de registrarse, volver a login

### **3. Cerrar sesión:**
- Hacer clic en botón "Cerrar Sesión" en la navbar
- Se redirige a login automáticamente
- No es posible volver atrás sin autenticarse

### **4. Crear nuevo grupo de permisos:**
En Django shell:
```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Crear grupo
grupo = Group.objects.create(name='nombre_grupo')

# Asignar permisos específicos
grupo.permissions.add(permiso1, permiso2, ...)
```

---

## ⚙️ Administración de Usuarios

### **Crear superusuario adicional:**
```bash
python manage.py createsuperuser
```

### **Agregar usuario a grupo 'solo_lectura':**
En Django shell:
```python
from django.contrib.auth.models import User, Group

usuario = User.objects.get(username='nombre_usuario')
grupo = Group.objects.get(name='solo_lectura')
usuario.groups.add(grupo)
```

### **Ver usuarios:**
En Django shell:
```python
from django.contrib.auth.models import User
usuarios = User.objects.all()
for u in usuarios:
    print(f"{u.username} - Staff: {u.is_staff}, Superuser: {u.is_superuser}")
```

---

## 🔍 Estándares de Programación Aplicados

✅ **Seguridad:**
- Autenticación con Django's built-in auth
- Validaciones rigurosas en server-side
- CSRF tokens en todos los formularios
- Protección con never_cache

✅ **Arquitectura:**
- Separación de responsabilidades
- Decoradores reutilizables
- Vistas limpias y bien organizadas
- Modelos de permisos estándar Django

✅ **UX/UI:**
- Interfaz profesional y responsiva
- Mensajes de error claros
- Navegación intuitiva
- Accesibilidad mejorada

✅ **Buenas Prácticas:**
- Nombres en español (carpeta "autenticacion")
- Comentarios documentados
- Código limpio y legible
- Validaciones exhaustivas

---

## 📱 Características Profesionales

🎯 **Seguridad de Sesión:**
- Las sesiones expiran después de 1 hora
- No se puede reutilizar token de sesión
- Never cache previene ataques

🎯 **Control de Permisos:**
- Modelo granular de permisos Django
- Grupos reutilizables
- Decoradores extensibles

🎯 **Experiencia de Usuario:**
- Login/Registro en la misma interfaz
- Mensajes SweetAlert mejorados
- Soporte para recuperación de permisos

🎯 **Mantenibilidad:**
- Código documentado
- Fácil de extender
- Compatible con estándares Django

---

## 📞 Soporte y Próximas Mejoras

**Posibles mejoras futuras:**
- Recuperación de contraseña por email
- Autenticación de dos factores (2FA)
- Auditoría de acciones por usuario
- Sistema de roles más avanzado
- Integración SSO/LDAP

---

## ✅ Resumen Final

Sistema de autenticación **profesional a nivel estudiante preocupado**, con:

✓ Autenticación segura y validada
✓ Permisos granulares y flexibles  
✓ Interfaz moderna y responsiva
✓ Protección contra ataques comunes
✓ Código limpio y bien documentado
✓ Fácil de mantener y extender

¡El sistema está listo para producción con los ajustes de seguridad necesarios!
