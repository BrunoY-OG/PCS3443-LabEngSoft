from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Socio, Funcionario, Usuario, Voo     
from .serializers import SocioSerializer, FuncionarioSerializer, UsuarioSerializer, VooSerializer

class FuncionarioViewSet(ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    
    def get_queryset(self):
        return self.queryset
    
    @action(
        methods = ["POST"],
        detail = True,
        serializer_class = FuncionarioSerializer,
        url_path = "add-funcionario",
    )
    def add_funcionario(self, request, *args, **kwargs):
        funcionario_data = {
            "nome": request.data.get("nome"),
            "cpf": request.data.get("cpf"),
            "data_nascimento": request.data.get("data_nascimento"),
            "endereco": request.data.get("endereco"),
        }
        usuario_data = {
            "username": request.data.get("username"),
            "password": request.data.get("password"),
            "id_funcionario": -1
        }
        
        funcionario_serializer = self.get_serializer(data=funcionario_data)
        usuario_serializer = UsuarioSerializer(data=usuario_data)
        
        if funcionario_serializer.is_valid(raise_exception=True):            
            if usuario_serializer.is_valid(raise_exception=True):
                funcionario_instance = self.perform_create(funcionario_serializer)
                usuario_data = {
                    "username": request.data.get("username"),
                    "password": request.data.get("password"),
                    "id_funcionario": funcionario_instance.id_funcionario
                }
                usuario_serializer = UsuarioSerializer(data=usuario_data)
                if usuario_serializer.is_valid(raise_exception=True):
                    self.perform_create(usuario_serializer)
                    headers = self.get_success_headers(funcionario_serializer.data)
                    return Response(funcionario_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response(
                    {"error": "Invalid Usuario Fields"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "Invalid Funcionario Fields"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class SocioViewSet(ModelViewSet):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializer
    
    def get_queryset(self):
        return self.queryset
    
    @action(
        methods = ["POST"],
        detail = True,
        serializer_class = SocioSerializer,
        url_path = "add-socio",
    )
    def add_funcionario(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)