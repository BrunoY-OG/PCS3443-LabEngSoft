from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Case, When, Sum, Count, FloatField

from .models import Socio, Funcionario, Usuario, Voo     
from .serializers import FuncionarioSerializer, VooSerializer
from .serializers import SocioSerializer, AlunoSerializer, InstrutorSerializer

from django.contrib.auth import get_user_model, authenticate


User = get_user_model()

class LoginView(APIView):
    def post(self, request, format=None):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            # For example, using Django's authenticate() function
            user = authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(response_data, status=200)
            else:
                return Response({'detail': 'Invalid credentials'}, status=401)
        except:
            return Response(
                {"error": "error"},
                status=400
            )
        
class FuncionarioViewSet(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        try:
            if not request.user.is_funcionario:
                return Response({"detail": "You do not have permission to perform this action."}, status=403)

            # Retrieve the request data
            data = request.data
            # Create the Usuario object
            username = data.get('username')
            password = data.get('password')

            # Create the Funcionario object
            funcionario_serializer = FuncionarioSerializer(data=data)
            if funcionario_serializer.is_valid():
                funcionario = funcionario_serializer.save()
            else:
                return Response(funcionario_serializer.errors, status=400)


            usuario = User.objects.create_funcionario(username=username, password=password, id_funcionario=funcionario.id_funcionario)

            # Return the response
            response_data = {
                "detail": "Funcionario and Usuario created successfully.",
                "funcionario_id": funcionario.id_funcionario,
                "usuario_id": usuario.id_usuario
            }
            return Response(response_data, status=201)
        except:
            return Response(
                {"error": "error"},
                status=400
            )
    
class AlunoViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            if not request.user.is_funcionario:
                return Response({"detail": "You do not have permission to perform this action."}, status=403)

            # Retrieve the request data
            data = request.data
            # Create the Usuario object
            username = data.get('username')
            password = data.get('password')

            # Create the Aluno object
            aluno_serializer = AlunoSerializer(data=data)
            if aluno_serializer.is_valid():
                aluno = aluno_serializer.save()
            else:
                return Response(aluno_serializer.errors, status=400)


            usuario = User.objects.create_aluno(username=username, password=password, matricula=aluno.matricula)

            # Return the response
            response_data = {
                "detail": "Aluno and Usuario created successfully.",
                "aluno_id": aluno.matricula,
                "usuario_id": usuario.id_usuario
            }
            return Response(response_data, status=201)
        except:
            return Response(
                {"error": "error"},
                status=400
            )
    

    def get(self, request, format=None):
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
                status=400
            )

class SocioViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            if not request.user.is_funcionario:
                return Response({"detail": "You do not have permission to perform this action."}, status=403)

            # Retrieve the request data
            data = request.data
            # Create the Usuario object
            username = data.get('username')
            password = data.get('password')

            # Create the Socio object
            socio_serializer = SocioSerializer(data=data)
            if socio_serializer.is_valid():
                socio = socio_serializer.save()
            else:
                return Response(socio_serializer.errors, status=400)


            usuario = User.objects.create_socio(username=username, password=password, matricula=socio.matricula)

            # Return the response
            response_data = {
                "detail": "Socio and Usuario created successfully.",
                "socio_id": socio.matricula,
                "usuario_id": usuario.id_usuario
            }
            return Response(response_data, status=201)
        except:
            return Response(
                {"error": "error"},
                status=400
            )

class InstrutorViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            if not request.user.is_funcionario:
                return Response({"detail": "You do not have permission to perform this action."}, status=403)

            # Retrieve the request data
            data = request.data
            # Create the Usuario object
            username = data.get('username')
            password = data.get('password')

            # Create the Instrutor object
            instrutor_serializer = InstrutorSerializer(data=data)
            if instrutor_serializer.is_valid():
                instrutor = instrutor_serializer.save()
            else:
                return Response(instrutor_serializer.errors, status=400)


            usuario = User.objects.create_instrutor(username=username, password=password, matricula=instrutor.matricula)

            # Return the response
            response_data = {
                "detail": "Instrutor and Usuario created successfully.",
                "instrutor_id": instrutor.matricula,
                "usuario_id": usuario.id_usuario
            }
            return Response(response_data, status=201)
        except:
            return Response(
                {"error": "error"},
                status=400
            )
    

class VooViewSet(APIView):    
    permission_classes = [IsAuthenticated]
