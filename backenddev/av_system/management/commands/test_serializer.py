from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from av_system.serializers import FuncionarioSerializer
from av_system.models import Funcionario
from datetime import date, datetime

User = get_user_model()


class Command(BaseCommand):
    help = 'Pre-creates a single Funcionario in the database.'
    def handle(self, *args, **options):
        funcionario = {'nome': 'Func 2', 
                        'data_nascimento': datetime.strptime('1900-01-01', '%Y-%m-%d').date(), 
                        'cpf': '29142320046', 
                        'endereco': 'av nada'}
        func = FuncionarioSerializer(data=funcionario)

        try:
            if func.is_valid():
                print("Funcionario: valid")
            else:
                print("Funcionario: not valid")
        except Exception as e:
            error_message = str(e)
            print("funcionario_serializer E:", error_message)


