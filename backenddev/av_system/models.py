from django.db import models
from django.core.validators import validate_email


class Funcionario(models.Model):
    id_funcionario = models.IntegerField(primary_key=True, 
                            auto_created=True, editable=False)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    data_nascimento = models.DateField()
    endereco = models.CharField(max_length=100)
    class Meta:
        indexes = [ models.Index(fields=['id_funcionario']) ]
        ordering = ['nome']

class Socio(models.Model):
    CATEGORIAS = [
        ('A', 'Aluno'),
        ('P', 'Piloto'),
        ('I', 'Instrutor')
        ]
    
    matricula = models.IntegerField(primary_key=True, 
                            auto_created=True, editable=False)
    categoria = models.CharField(max_length=9, choices=CATEGORIAS)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    data_nascimento = models.DateField()
    endereco = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, validators=[validate_email])
    nota_ponderada = models.FloatField(null=True)
    breve = models.CharField(max_length=100, null=True)
    nome_do_curso = models.CharField(max_length=100, null=True)
    data_diploma = models.DateField(null=True)
    instituicao_diploma = models.CharField(max_length=100, null=True)


class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True, 
                            auto_created=True, editable=False)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=300)
    id_funcionario = models.ForeignKey(Funcionario, 
                                        on_delete=models.SET_NULL,
                                        null=True)
    id_socio = models.ForeignKey(Socio, 
                                        on_delete=models.SET_NULL,
                                        null=True)
    class Meta:
        indexes = [models.Index(fields=['id_usuario'])]


class Voo(models.Model):
    NOTA_CONCEITO = [
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D')
    ]
    id_voo = models.IntegerField(primary_key=True, 
                            auto_created=True, editable=False)
    data = models.DateField()
    horario_saida = models.TimeField()
    horario_chegada = models.TimeField()
    parecer = models.CharField(max_length=1, choices=NOTA_CONCEITO)
    id_socio = models.ForeignKey(Socio, related_name='socio_voo', on_delete=models.DO_NOTHING)
    id_instrutor = models.ForeignKey(Socio, related_name='instrutor_voo', on_delete=models.DO_NOTHING)
    class Meta:
        indexes = [ models.Index(fields=['id_voo']) ]
        ordering = ['data','horario_saida']