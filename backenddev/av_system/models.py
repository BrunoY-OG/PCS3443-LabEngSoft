from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_socio(self, username, password=None, **extra_fields):
        # Create a new user of type socio
        user = self.create_user(username, password, **extra_fields)
        user.is_socio = True
        user.save()
        return user

    def create_funcionario(self, username, password=None, **extra_fields):
        # Create a new user of type funcionario
        user = self.create_user(username, password, **extra_fields)
        user.is_funcionario = True
        user.save()
        return user

    def create_aluno(self, username, password=None, **extra_fields):
        # Create a new user of type aluno
        user = self.create_user(username, password, **extra_fields)
        user.is_aluno = True
        user.save()
        return user

    def create_instrutor(self, username, password=None, **extra_fields):
        # Create a new user of type instrutor
        user = self.create_user(username, password, **extra_fields)
        user.is_instrutor = True
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(username, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
    

class Funcionario(models.Model):
    id_funcionario = models.IntegerField(primary_key=True, 
                            auto_created=True, editable=False)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField()
    endereco = models.CharField(max_length=100)
    class Meta:
        indexes = [ models.Index(fields=["id_funcionario"]) ]
        ordering = ["nome"]

class Socio(models.Model):
    CATEGORIAS = [
        ("A", "Aluno"),
        ("P", "Piloto"),
        ("I", "Instrutor")
        ]
    
    matricula = models.IntegerField(primary_key=True, 
                            auto_created=True, editable=False)
    categoria = models.CharField(max_length=9, choices=CATEGORIAS)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    data_nascimento = models.DateField()
    endereco = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, validators=[validate_email])
    # nota_ponderada = models.FloatField(null=True)
    breve = models.CharField(max_length=100, null=True)
    nome_do_curso = models.CharField(max_length=100, null=True)
    data_diploma = models.DateField(null=True)
    instituicao_diploma = models.CharField(max_length=100, null=True)
    class Meta:
        unique_together = ("cpf", "categoria")
        indexes = [models.Index(fields=["matricula"])]

class Voo(models.Model):
    NOTA_CONCEITO = [
        ("A",4.),
        ("B",3.),
        ("C",2.),
        ("D",1.)
    ]
    
    NOTA_CONCEITO_mapping = {
        "A": 4.0,
        "B": 3.0,
        "C": 2.0,
        "D": 1.0
    }
    
    id_voo = models.IntegerField(primary_key=True, 
                            auto_created=True, editable=False)
    data = models.DateField()
    horario_saida = models.TimeField()
    horario_chegada = models.TimeField()
    parecer = models.CharField(max_length=1, choices=NOTA_CONCEITO)
    id_socio = models.ForeignKey(Socio, related_name="socio_voo", on_delete=models.DO_NOTHING)
    id_instrutor = models.ForeignKey(Socio, related_name="instrutor_voo", on_delete=models.DO_NOTHING)
    class Meta:
        indexes = [ models.Index(fields=["id_voo"]) ]
        ordering = ["data","horario_saida"]


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    is_funcionario = models.BooleanField(default=False)
    is_socio = models.BooleanField(default=False)
    is_aluno = models.BooleanField(default=False)
    is_instrutor = models.BooleanField(default=False)
    id_usuario = models.IntegerField(primary_key=True, 
                            auto_created=True, editable=False)
    id_funcionario = models.ForeignKey(Funcionario, 
                                        on_delete=models.SET_NULL,
                                        null=True)
    matricula = models.ForeignKey(Socio, 
                                        on_delete=models.SET_NULL,
                                        null=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name='usuario_set',  # Added related_name
        related_query_name='usuario',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name='usuario_set',  # Added related_name
        related_query_name='usuario',
    )

    def save(self, *args, **kwargs):
        # Determine the access levels based on id_funcionario and matricula objects
        if self.id_funcionario:
            self.is_funcionario = True
        if self.matricula:
            if self.matricula.breve is None:
                self.is_aluno = True
            elif self.matricula.nome_do_curso is None:
                self.is_socio = True
            elif self.matricula.nome_do_curso is not None:
                self.is_instrutor = True
        super().save(*args, **kwargs)
    class Meta:
        permissions = (
            ('funcionario', 'Funcoes administrativas'),
            ('socio', 'Apenas consulta de voos'),
            ('aluno', 'Consulta de voos e requerimento de breve'),
            ('instrutor', 'Cadastro e consulta de voos'),
        )
