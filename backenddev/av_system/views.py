from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from django.db.models import Case, When, Sum, Count, FloatField

from .models import Socio, Funcionario, Usuario, Voo     
from .serializers import SocioSerializer, FuncionarioSerializer, UsuarioSerializer, VooSerializer

class FuncionarioViewSet(ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    
    def get_queryset(self):
        return self.queryset
    
    @action(
        methods = ["POST"],
        detail = False,
        serializer_class = FuncionarioSerializer,
        url_path = "add-funcionario",
    )

    def add_funcionario(self, request, *args, **kwargs):
        try:
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
        except:
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
        detail = False,
        serializer_class = SocioSerializer,
        url_path = "add-socio",
    )    
    def add_socio(self, request, *args, **kwargs):
        try:
            socio_data = {
                "nome": request.data.get("nome"),
                "cpf": request.data.get("cpf"),
                "data_nascimento": request.data.get("data_nascimento"),
                "endereco": request.data.get("endereco"),
                "categoria": request.data.get("categoria"),
                "nome": request.data.get("nome"),
                "cpf": request.data.get("cpf"),
                "data_nascimento": request.data.get("data_nascimento"),
                "endereco": request.data.get("endereco"),
                "email": request.data.get("email"),
                "endereco": request.data.get("endereco"),
                "breve": request.data.get("breve"),
                "nome_do_curso": request.data.get("nome_do_curso"),
                "data_diploma": request.data.get("data_diploma"),
                "instituicao_diploma": request.data.get("instituicao_diploma")
            }
            usuario_data = {
                "username": request.data.get("username"),
                "password": request.data.get("password"),
                "id_socio": -1
            }
            
            funcionario_serializer = self.get_serializer(data=socio_data)
            usuario_serializer = UsuarioSerializer(data=usuario_data)
            
            if funcionario_serializer.is_valid(raise_exception=True):            
                if usuario_serializer.is_valid(raise_exception=True):
                    socio_instance = self.perform_create(funcionario_serializer)
                    usuario_data = {
                        "username": request.data.get("username"),
                        "password": request.data.get("password"),
                        "id_socio": socio_instance.id_socio
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
                    {"error": "Invalid Usuario Fields"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {"error": "Invalid Usuario Fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

    
    @action(
        methods = ["GET"],
        detail = True,
        serializer_class = SocioSerializer,
        url_path = "socio",
    )
    

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            average_parecer = Voo.objects.filter(id_socio=instance) \
                .aggregate(
                    total_parecer=Sum(
                        Case(
                            When(parecer__in=Voo.NOTA_CONCEITO_mapping.keys(), then=Voo.NOTA_CONCEITO_mapping.get("parecer")),
                            default=0,
                            output_field=FloatField()
                        )
                    ),
                    count_parecer=Count(
                        Case(
                            When(parecer__in=Voo.NOTA_CONCEITO_mapping.keys(), then=1),
                            default=0
                        )
                    )
                )
            if average_parecer['count_parecer'] > 0:
                instance.nota_ponderada = average_parecer['total_parecer'] / average_parecer['count_parecer']
            else:
                instance.nota_ponderada = None
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except:
            return Response(
                {"error": "error retrieving"},
                status=status.HTTP_400_BAD_REQUEST
            )