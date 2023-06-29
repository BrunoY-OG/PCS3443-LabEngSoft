from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from datetime import date, datetime
from django.db.models import (
    Case, 
    When, 
    Sum, 
    Count, 
    FloatField
)

from .models import ( 
    Socio, 
    Funcionario, 
    Usuario, 
    Voo
)     

from .serializers import (
    FuncionarioSerializer, 
    VooSerializer, 
    SocioSerializer, 
    AlunoSerializer, 
    InstrutorSerializer
)

from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

from .authentication import UsuarioBackend, CustomJWTAuthentication



class LoginView(APIView):
    def post(self, request, format=None):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            # Authenticate the Usuario model
            # user = authenticate(request, username=username, password=password) 
            # Use the custom authentication backend to authenticate the user
            backend = UsuarioBackend()
            user = authenticate(request, username=username, password=password)

            # user = backend.authenticate(request, username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                response_data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
                return Response(response_data, status=200)
            else:
                # If the user is not authenticated via credentials, try token authentication
                user = backend.authenticate_with_token(request)
                if user is not None:
                    refresh = RefreshToken.for_user(user)
                    response_data = {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    return Response(response_data, status=200)
                else:
                    return Response({"detail": "Invalid credentials"}, status=401)
        
        except:
            return Response(
                {"error": "error"},
                status=400
            )
        
class FuncionarioViewSet(GenericAPIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]    
    serializer_class = FuncionarioSerializer
    
    def get(self, request, format=None):
        try:
            try:
                user = self.request.user
            except:
                return Response({"detail": "Invalid or expired token."}, status=401)
            
            if not user.is_funcionario:
                return Response({"detail": "You do not have permission to perform this action."}, status=403) 
            funcionarios = Funcionario.objects.all()
            serializer = FuncionarioSerializer(funcionarios, many=True)
            return Response(serializer.data)
        except:
            return Response(
                {"error": "error"},
                status=400
            )


    def post(self, request, format=None):
        try:
            if not request.user.is_funcionario:
                return Response({"detail": "You do not have permission to perform this action."}, status=403)
            # Retrieve the request data
            data = request.data
            # Create the Usuario object
            username = data.get("username")
            password = data.get("password")


            data_func = {
                "nome": data.get("nome"),
                "data_nascimento": datetime.strptime(data.get("data_nascimento"), '%Y-%m-%d').date(),
                "cpf": data.get("cpf"),
                "endereco": data.get("endereco")
            }
            funcionario_serializer = FuncionarioSerializer(data=data_func)
            if funcionario_serializer.is_valid():
                funcionario = funcionario_serializer.save()
            else: 
                return Response(funcionario_serializer.errors, status=400)
            try:
                usuario = User.objects.create_funcionario(username=username, password=password, id_funcionario=funcionario)
            except Exception as e:
                error_message = str(e)
                print("funcionario_serializer E:", error_message)

            # Return the response
            response_data = {
                "detail": "Funcionario and Usuario created successfully.",
                "funcionario_id": funcionario.id,
                "usuario_id": usuario.id
            }
            return Response(response_data, status=201)
        except:
            return Response(
                {"error": "error"},
                status=400
            )
    
class FuncionarioDetailViewSet(GenericAPIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = FuncionarioSerializer

    def get_object(self, pk):
        try:
            return Funcionario.objects.get(pk=pk)
        except Funcionario.DoesNotExist:
            return None
        
    def get(self, request, pk, format=None):
        try:
            if (not request.user.is_funcionario):
                return Response({"detail": "You do not have permission to perform this action."}, status=403)
            funcionario = self.get_object(pk)
            if funcionario is None:
                return Response({"detail": "Funcionario not found."}, status=404)
            serializer = FuncionarioSerializer(funcionario)
            return Response(serializer.data)
        except Funcionario.DoesNotExist:
            return Response({"detail": "Funcionario not found."}, status=404)

class AlunoViewSet(GenericAPIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AlunoSerializer


    def get(self, request, format=None):
        try:
            isInstrutor = request.user.is_instrutor
            isFuncionario = request.user.is_funcionario
            if ((not isFuncionario) and (not isInstrutor)):
                return Response({"detail": "You do not have permission to perform this action."}, status=403)
            alunos = Socio.objects.filter(categoria='A')
            serializer = AlunoSerializer(alunos, many=True)
            return Response(serializer.data)
        except:
            return Response(
                {"error": "error"},
                status=400
            )

class AlunoCreateViewSet(GenericAPIView):
    serializer_class = AlunoSerializer
    def post(self, request, format=None):
        try:
            # Retrieve the request data
            data = request.data
            # Create the Usuario object
            username = data.get("username")
            password = data.get("password")

            data_aluno = {
                "categoria": data.get("categoria"),
                "nome": data.get("nome"),
                "data_nascimento": datetime.strptime(data.get("data_nascimento"), '%Y-%m-%d').date(),
                "cpf": data.get("cpf"),
                "endereco": data.get("endereco"),
                "email": data.get("email"),
            }
            # Create the Aluno object
            aluno_serializer = AlunoSerializer(data=data_aluno)
            if aluno_serializer.is_valid():
                aluno = aluno_serializer.save()
            else:
                return Response(aluno_serializer.errors, status=400)


            usuario = User.objects.create_aluno(username=username, password=password, matricula=aluno)

            # Return the response
            response_data = {
                "detail": "Aluno and Usuario created successfully.",
                "aluno_id": aluno.id,
                "usuario_id": usuario.id
            }
            return Response(response_data, status=201)
        except:
            return Response(
                {"error": "error"},
                status=400
            )
    
    
class SocioViewSet(GenericAPIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SocioSerializer
    def get(self, request, format=None):
        try:
            isInstrutor = request.user.is_instrutor
            isFuncionario = request.user.is_funcionario
            if ((not isFuncionario) and (not isInstrutor)):
                return Response({"detail": "You do not have permission to perform this action."}, status=403)
            socios = Socio.objects.filter(categoria='P')
            serializer = SocioSerializer(socios, many=True)
            return Response(serializer.data)
        except:
            return Response(
                {"error": "error"},
                status=400
            )

class SocioCreateViewSet(GenericAPIView):
    serializer_class = SocioSerializer

    def post(self, request, format=None):
        try:
            # Retrieve the request data
            data = request.data
            # Create the Usuario object
            username = data.get("username")
            password = data.get("password")
            data_socio = {
                "categoria": data.get("categoria"),
                "nome": data.get("nome"),
                "data_nascimento": datetime.strptime(data.get("data_nascimento"), '%Y-%m-%d').date(),
                "cpf": data.get("cpf"),
                "endereco": data.get("endereco"),
                "email": data.get("email"),
                "breve":  data.get("breve"),
            }
            socio_serializer = SocioSerializer(data=data_socio)
            if socio_serializer.is_valid():
                socio = socio_serializer.save()
            else:
                return Response(socio_serializer.errors, status=400)

            usuario = User.objects.create_socio(username=username, password=password, matricula=socio)

            # Return the response
            response_data = {
                "detail": "Socio and Usuario created successfully.",
                "socio_id": socio.id,
                "usuario_id": usuario.id
            }
            return Response(response_data, status=201)
        except:
            return Response(
                {"error": "error"},
                status=400
            )

class SocioDetailViewSet(GenericAPIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SocioSerializer

    def get_object(self, pk):
        try:
            return Socio.objects.get(pk=pk)
        except Socio.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        try:
            isInstrutor = request.user.is_instrutor
            isSocio = request.user.is_socio or request.user.is_aluno
            isFuncionario = request.user.is_funcionario
            matricula = request.user.matricula
            if ((not isFuncionario) and (not isInstrutor)):
                if ((isSocio) and (pk != matricula)):
                    return Response({"detail": "You do not have permission to perform this action."}, status=403)
            socio = self.get_object(pk)
            if socio is None:
                return Response({"detail": "socio not found."}, status=404)
            elif socio.categoria == 'A':
                average_parecer = Voo.objects.filter(id_socio=pk) \
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
                if average_parecer["count_parecer"] > 0:
                    socio.nota_ponderada = average_parecer["total_parecer"] / average_parecer["count_parecer"]
                else:
                    socio.nota_ponderada = None
                serializer = AlunoSerializer(socio)
            elif socio.categoria == 'I':
                serializer = InstrutorSerializer(socio)
            else:
                serializer = SocioSerializer(socio)
            return Response(serializer.data)
        except:
            return Response(
                {"error": "error"},
                status=400
            )
        
class UsuarioUserNameViewSet(APIView):
    def get_object(self, name):
        try:
            return Usuario.objects.get(username=name)
        except Usuario.DoesNotExist:
            return None


    def post(self, request, format=None):
        try:           
            username = request.data.get("username")
            user = self.get_object(username)
            if user is None:
                return Response({"usernameFree":True}, status=200)
            else:
                return Response({"usernameFree":False}, status=200)

        except:
            return Response(
                {"error": "error"},
                status=400
            )
        

    
class InstrutorViewSet(GenericAPIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = InstrutorSerializer
    def get(self, request, format=None):
        try:
            isInstrutor = request.user.is_instrutor
            isFuncionario = request.user.is_funcionario
            if ((not isFuncionario) and (not isInstrutor)):
                return Response({"detail": "You do not have permission to perform this action."}, status=403)
            socios = Socio.objects.filter(categoria='I')
            serializer = InstrutorSerializer(socios, many=True)
            return Response(serializer.data)
        except:
            return Response(
                {"error": "error"},
                status=400
            )
        
class InstrutorCreateViewSet(GenericAPIView):
    serializer_class = InstrutorSerializer
    def post(self, request, format=None):
        try:
            # Retrieve the request data
            data = request.data
            # Create the Usuario object
            username = data.get("username")
            password = data.get("password")
            print("socio:")
            data_instrutor = {
                "categoria": data.get("categoria"),
                "nome": data.get("nome"),
                "data_nascimento": datetime.strptime(data.get("data_nascimento"), '%Y-%m-%d').date(),
                "cpf": data.get("cpf"),
                "endereco": data.get("endereco"),
                "email": data.get("email"),
                "breve":  data.get("breve"),
                "nome_do_curso": data.get("nome_do_curso"),
                "data_diploma": datetime.strptime(data.get("data_diploma"), '%Y-%m-%d').date(),
                "instituicao_diploma": data.get("instituicao_diploma"),
            }
            # Create the Instrutor object
            instrutor_serializer = InstrutorSerializer(data=data_instrutor)
            if instrutor_serializer.is_valid():
                instrutor = instrutor_serializer.save()
            else:
                return Response(instrutor_serializer.errors, status=400)


            usuario = User.objects.create_instrutor(username=username, password=password, matricula=instrutor)

            # Return the response
            response_data = {
                "detail": "Instrutor and Usuario created successfully.",
                "instrutor_id": instrutor.id,
                "usuario_id": usuario.id
            }
            return Response(response_data, status=201)
        except:
            return Response(
                {"error": "error"},
                status=400
            )
    

class VooViewSet(GenericAPIView):    
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VooSerializer


    def post(self, request, format=None):
        try:
            isInstrutor = request.user.is_instrutor
            isFuncionario = request.user.is_funcionario
            if ((not isFuncionario) and (not isInstrutor)):
                return Response({"detail": "You do not have permission to perform this action."}, status=403)

            # Retrieve the request data
            data = request.data

            voo_serializer = VooSerializer(data=data)
            if voo_serializer.is_valid():
                if isInstrutor:
                    if (not data.get("id_instrutor")):
                        return Response({"error": "invalid ID"}, status=400)
                    elif (data.get("id_instrutor") != request.user.id_socio):
                        return Response({"error": "invalid ID"}, status=403)
                    valid_choices = [choice[0] for choice in Voo.NOTA_CONCEITO]
                    if (data.get("parecer") not in valid_choices):
                        return Response({"error": "invalid Parecer"}, status=400)
                    voo = voo_serializer.save()
                elif isFuncionario:
                    if (data.get("id_instrutor")):
                        return Response({"error": "invalid ID"}, status=400)
                    if (data.get("parecer")):
                        return Response({"error": "invalid ID"}, status=400)
                    voo = voo_serializer.save()
            else:
                return Response(voo_serializer.errors, status=400)

            response_data = {
                "detail": "Voo created successfully.",
                "voo_id": voo.id,
            }
            return Response(response_data, status=201)
        except:
            return Response(
                {"error": "error"},
                status=400
            )
    

    def get(self, request, format=None):
        try:
            isFuncionario = request.user.is_funcionario
            isInstrutor = request.user.is_instrutor
            isSocio = request.user.is_socio or request.user.is_aluno
            if (isFuncionario or isInstrutor):
                voos = Voo.objects.all()
            elif (isSocio):
                socioID = request.user.matricula
                voos = Voo.objects.filter(id_socio=socioID)
            serializer = VooSerializer(voos, many=True)
            return Response(serializer.data)
        except:
            return Response(
                {"error": "error"},
                status=400
            )

class VooDetailViewSet(GenericAPIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VooSerializer

    def get_object(self, pk):
        try:
            return Voo.objects.get(pk=pk)
        except Voo.DoesNotExist:
            return None
        
    def get(self, request, pk, format=None):
        try:
            isInstrutor = request.user.is_instrutor
            isSocio = request.user.is_socio or request.user.is_aluno
            isFuncionario = request.user.is_funcionario
            matricula = request.user.matricula
            if ((not isFuncionario) and (not isInstrutor)):
                if ((isSocio) and (pk != matricula)):
                    return Response({"detail": "You do not have permission to perform this action."}, status=403)
            voo = self.get_object(pk)
            if voo is None:
                return Response({"detail": "Voo not found."}, status=404)
            serializer = VooSerializer(voo)
            return Response(serializer.data)
        except:
            return Response({"detail": "Voo not found."}, status=404)
        
        
class VooSocioDetailViewSet(GenericAPIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VooSerializer

    def get_object(self, matricula):
        try:
            return Voo.objects.get(matricula=matricula)
        except Voo.DoesNotExist:
            return None
        
    def post(self, request, pk, format=None):
        try:
            isInstrutor = request.user.is_instrutor
            isSocio = request.user.is_socio or request.user.is_aluno
            isFuncionario = request.user.is_funcionario
            if (pk is None):
                return Response({"error": "missing matricula param."}, 
                            status=404)
            elif ((not isFuncionario) and (not isInstrutor)):
                if ((isSocio) and (request.user.matricula != pk)):
                    return Response({"detail": "You do not have permission to perform this action."}, status=403)
            voo = self.get_object(pk)
            if voo is None:
                return Response({"detail": "Voo not found."}, 
                                status=404)
            serializer = VooSerializer(voo, many=True)
            return Response(serializer.data)
        except:
            return Response({"detail": "Voo not found."}, 
                            status=404)