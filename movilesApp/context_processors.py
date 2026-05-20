"""
Context processor para determinar permisos de edición basado en grupos.
"""

def permisos_edicion(request):
    """
    Agrega 'puede_editar' al contexto de todos los templates.
    Retorna False si el usuario está en el grupo 'solo_lectura'.
    """
    puede_editar = True
    
    if request.user.is_authenticated:
        # Si el usuario está en el grupo 'solo_lectura', no puede editar
        puede_editar = not request.user.groups.filter(name='solo_lectura').exists()
    else:
        puede_editar = False
    
    return {
        'puede_editar': puede_editar,
        'es_solo_lectura': not puede_editar
    }
