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
        if auth_header is None:
            return None
        raw_header = authenticator.get_raw_token(auth_header)
        try:
            validated_token = authenticator.get_validated_token(raw_header)
            user = self.get_user(validated_token.get('id'))
            return user, validated_token
        except InvalidToken:
            return None, None
        
class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            user, token = UsuarioBackend().authenticate_with_token(request=request)
            return user, token
        except AuthenticationFailed:
            return None
