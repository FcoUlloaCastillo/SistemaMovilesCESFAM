## 🚀 Inicio Rápido - Sistema de Autenticación

### **Prueba Inmediata**

#### **1. Usuarios predefinidos:**

```
ADMIN (Acceso Total)
├─ Usuario: admin
├─ Contraseña: admin123
└─ Acceso: Todo + Panel Admin 🔐

USUARIO SOLO LECTURA (Visualización)
├─ Usuario: javier  
├─ Contraseña: soporte1@
└─ Acceso: Solo ver datos ✅
```

#### **2. URLs Importantes:**

```
http://localhost:8000/login/          ← Iniciar sesión
http://localhost:8000/registro/       ← Crear cuenta nueva
http://localhost:8000/                ← Panel principal (requiere login)
http://localhost:8000/admin/          ← Admin (solo superusuario)
```

#### **3. Pruebas Recomendadas:**

**Prueba 1: Acceso sin autenticación**
1. Cierra el navegador completamente
2. Intenta acceder a http://localhost:8000/
3. ✅ Debes ser redirigido a login

**Prueba 2: Login con "javier"**
1. Inicia sesión como: `javier` / `soporte1@`
2. ✅ Debes ver el usuario en navbar: "👤 javier"
3. Intenta crear un vehículo
4. ❌ Debes ver: "No tienes permiso para realizar esta acción"

**Prueba 3: Login con "admin"**
1. Cierra sesión (Cerrar Sesión)
2. Inicia sesión como: `admin` / `admin123`
3. ✅ Debes ver "🔐 Admin" en navbar
4. ✅ Puedes crear, editar, eliminar
5. Ve a /admin/ 
6. ✅ Debes acceder al panel de administración

**Prueba 4: Protección contra cache**
1. Inicia sesión como cualquier usuario
2. Abre el Dev Tools (F12) → Application → Cookies
3. Cierra sesión
4. Presiona "Atrás" varias veces
5. ✅ No debes poder ver ninguna página (se redirige a login)

**Prueba 5: Crear nuevo usuario**
1. Desde login, haz clic en "Registrarse aquí"
2. Intenta crear usuario con datos inválidos:
   - Usuario: `a` (muy corto)
   - Email: `correo_invalido`
   - Contraseña: `123` (muy corta)
3. ✅ Debes ver mensajes de error específicos
4. Crea con datos válidos y comprueba que funciona

---

## 📋 Detalles Técnicos

### **Archivos Modificados:**

```
✅ templates/autenticacion/login.html       (Nuevo)
✅ templates/autenticacion/registro.html    (Nuevo)
✅ templates/base.html                      (Navbar mejorada)
✅ static/css/styles.css                    (Estilos navbar)
✅ movilesApp/views.py                      (Vistas autenticación + decoradores)
✅ movilesApp/urls.py                       (Rutas autenticación)
✅ gestionMovilesProject/settings.py        (Configuración seguridad)
✅ script_crear_usuarios.py                 (Script inicialización - Nuevo)
✅ AUTENTICACION_DOCUMENTACION.md           (Documentación completa - Nuevo)
```

### **Decoradores Implementados:**

```python
@never_cache                    ← Previene caché del navegador
@login_required                 ← Requiere autenticación
@solo_lectura                   ← Restringe edición/eliminación
```

### **Permisos por Rol:**

| Operación | Admin | Solo Lectura |
|-----------|-------|--------------|
| Ver listados | ✅ | ✅ |
| Ver detalles | ✅ | ✅ |
| Crear | ✅ | ❌ |
| Editar | ✅ | ❌ |
| Eliminar | ✅ | ❌ |
| Exportar | ✅ | ✅ |
| Ver Admin | ✅ | ❌ |

---

## 🔐 Seguridad Implementada

```python
✅ Validación de entrada rigurosa
✅ CSRF tokens en formularios
✅ Never cache en vistas sensibles
✅ Expiración automática de sesión (1 hora)
✅ Hash seguro de contraseñas (PBKDF2)
✅ Protección contra fuerza bruta (built-in Django)
✅ Validación de email en registro
✅ Confirmación de contraseña
```

---

## 📝 Crear Más Usuarios

### **Opción 1: Desde Admin**

```
1. Inicia sesión como admin
2. Ve a /admin/
3. Usuarios → Agregar usuario
4. Completa los datos
5. Para agregar grupo: Ve a "Grupos" y asigna "solo_lectura"
```

### **Opción 2: Django Shell**

```bash
python manage.py shell

>>> from django.contrib.auth.models import User, Group
>>> usuario = User.objects.create_user(
...     username='nuevo_usuario',
...     email='nuevo@cesfam.local',
...     password='micontraseña123'
... )
>>> grupo = Group.objects.get(name='solo_lectura')
>>> usuario.groups.add(grupo)
>>> exit()
```

---

## 🆘 Solución de Problemas

**P: Me dice "Usuario o contraseña incorrectos"**
- R: Verifica que escribes bien el usuario/contraseña (sensibles a mayúsculas)

**P: No puedo ver el botón Admin**
- R: Debes estar logueado como superusuario (admin)

**P: Dice "No tienes permiso" cuando intento editar**
- R: Si eres "javier", ese es el comportamiento correcto. Prueba con "admin"

**P: La sesión expira muy rápido**
- R: Por defecto es 1 hora. Cambiar en settings.py: SESSION_COOKIE_AGE

**P: No se redirige a login después de cerrar sesión**
- R: Asegúrate de que `LOGOUT_REDIRECT_URL = 'login'` en settings.py

---

## ✅ Checklist de Verificación

- [ ] Puedo acceder a http://localhost:8000/login/
- [ ] Puedo ver los formularios de login y registro
- [ ] Puedo crear una nueva cuenta
- [ ] Puedo iniciar sesión con javier/soporte1@
- [ ] No puedo editar/eliminar como javier
- [ ] Puedo iniciar sesión con admin/admin123
- [ ] Puedo editar/eliminar como admin
- [ ] Veo "🔐 Admin" en navbar como admin
- [ ] Al cerrar sesión y presionar atrás no puedo entrar
- [ ] Los mensajes de validación funcionan correctamente

---

## 📚 Documentación Completa

Para más detalles, consulta: **AUTENTICACION_DOCUMENTACION.md**

---

**¡Hecho! Sistema de autenticación profesional listo para usar. 🎉**
