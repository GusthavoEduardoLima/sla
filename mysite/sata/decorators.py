from django.core.exceptions import PermissionDenied

def nivel_acesso_requerido(min_nivel):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.nivel_acesso >= min_nivel:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied  # Redireciona ou lança erro
        return _wrapped_view
    return decorator
