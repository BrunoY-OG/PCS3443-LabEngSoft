from django.contrib.auth.backends import BaseBackend
from .models import Usuario

class UsuarioBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, id_usuario):
        try:
            return Usuario.objects.get(id_usuario=id_usuario)
        except Usuario.DoesNotExist:
            return None