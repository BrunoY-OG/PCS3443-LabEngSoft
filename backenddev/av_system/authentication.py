from django.contrib.auth.backends import BaseBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import Usuario, Funcionario, Socio
from rest_framework.exceptions import AuthenticationFailed

class UsuarioBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            return None
        print("authenticate: " + user.username)
        if user.check_password(password):
            return user

        return None

    def get_user(self, id):
        try:
            return Usuario.objects.get(id=id)
        except Usuario.DoesNotExist:
            return None
        
    def authenticate_with_token(self, request):
        authenticator = CustomJWTAuthentication()
        auth_header = authenticator.get_header(request=request)
        print("authenticate_with_token: ", str(auth_header))
        if auth_header is None:
            return None
        print("headers: ", request.headers)
        try:
            validated_token = authenticator.get_validated_token(auth_header)
            print("validated_token: ", str(validated_token))
            user = self.get_user(validated_token)
            if user is not None:
                if user.id_funcionario is not None:
                    user.funcionario = Funcionario.objects.get(id=user.id_funcionario)
                if user.matricula is not None:
                    user.socio = Socio.objects.get(id=user.matricula)
            return user
        except InvalidToken:
            return None
        
class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            user = UsuarioBackend().authenticate_with_token(request=request)
            return user
        except AuthenticationFailed:
            auth_header = self.get_header(request)
            if auth_header is None:
                return None

            try:
                validated_token = super().get_validated_token(auth_header)
                user = self.get_user(validated_token)
                return user
            except AuthenticationFailed:
                return None
