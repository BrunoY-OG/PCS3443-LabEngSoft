from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from av_system.models import Funcionario, Usuario

User = get_user_model()


class Command(BaseCommand):
    help = 'Pre-creates a single Funcionario in the database.'
    def handle(self, *args, **options):
        funcionario = Funcionario(
            id =1,
            nome='John Doe',
            cpf='37100886821',
            data_nascimento='1990-01-01',
            endereco='123 Main Street',
        )
        funcionario.save()

        self.stdout.write(self.style.SUCCESS(f"Pre-created Funcionario: {funcionario.nome}"))

        funcionario_instance = Funcionario.objects.get(id=1)
        # Create a corresponding User object with is_funcionario set to True
        username = 'funcionario'
        password = 'superstring'
        user = Usuario.objects.create_funcionario(
            id=1,
            username=username,
            password=password,
            id_funcionario=funcionario_instance,
        )

        self.stdout.write(self.style.SUCCESS(f"Username: {username}"))
        self.stdout.write(self.style.SUCCESS(f"Password: {password}"))
