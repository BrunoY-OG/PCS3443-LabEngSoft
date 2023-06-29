from ast import parse
from rest_framework import serializers
from .models import Usuario, Funcionario, Socio, Voo
from datetime import date, datetime
from rest_framework.validators import UniqueValidator

class CurrentViewKwargs:
    requires_context = True
    def __init__(self, kwargs_key) -> None:
        self._kwargs_key = kwargs_key
    def __call__(self, field):
        return field.context["view"].kwargs[self._kwargs_key]
    def __repr__(self) -> str:
        return f"{self.__clas__.__name__}({self._kwargs_key})"


def _validate_data_nascimento(dob):
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if age < 18:
        raise serializers.ValidationError("Must be at least 18 years old")
    return dob

def _validate_date(date):
    current_date = datetime.now().date()    
    if date > current_date:
        raise serializers.ValidationError("Invalid Date")
    return date

def _validate_cpf(cpf):
    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        raise serializers.ValidationError("Invalid CPF")

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        raise serializers.ValidationError("Invalid CPF")

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        raise serializers.ValidationError("Invalid CPF")

    return cpf


def _validate_namelength(value):
    if (len(value.split()) < 2):
        raise serializers.ValidationError("Invalid Name: Needs At least a surname")
    return value

def _validate_addresslength(value):
    if (len(value.split()) < 2):
        raise serializers.ValidationError("Invalid address: Missing data")
    return value



class FuncionarioSerializer(serializers.ModelSerializer):    

    def validate_data_nascimento(self, dob):
        return _validate_data_nascimento(dob) 

    def validate_cpf(self, cpf):
        return _validate_cpf(cpf)

    def validate_nome(self, nome):
        return _validate_namelength(nome)

    def validate_endereco(self, endereco):
        return _validate_addresslength(endereco)
    class Meta:
        model = Funcionario
        fields = '__all__'
    
class SocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socio
        fields = '__all__'
    
    def validate_data_nascimento(self, dob):
        return _validate_data_nascimento(dob)
    def validate_cpf(self, cpf):
        return _validate_cpf(cpf)
    def validate_nome(self, nome):
        return _validate_namelength(nome)
    def validate_endereco(self, endereco):
        return _validate_addresslength(endereco)
    
    def validate_categoria(value):
        valid_choices = [choice[0] for choice in Socio.CATEGORIAS]
        if value not in valid_choices:
            raise serializers.ValidationError('Invalid Categoria')

    def validate(self, attrs):
        cat = attrs.get('categoria')

        if cat == 'P':
            breve = attrs.get('breve')
            if (not breve):
                raise serializers.ValidationError('Invalid Breve')
        else:
            raise serializers.ValidationError('Invalid Categoria')
        return attrs

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socio
        fields = '__all__'
    
    def validate_data_nascimento(self, dob):
        return _validate_data_nascimento(dob)
    def validate_cpf(self, cpf):
        return _validate_cpf(cpf)
    def validate_nome(self, nome):
        return _validate_namelength(nome)
    def validate_endereco(self, endereco):
        return _validate_addresslength(endereco)
    
    def validate_categoria(value):
        valid_choices = [choice[0] for choice in Socio.CATEGORIAS]
        if value not in valid_choices:
            raise serializers.ValidationError('Invalid Categoria')

    def validate(self, attrs):
        cat = attrs.get('categoria')

        if cat == 'A':
            nota = attrs.get('nota_ponderada')
        else:
            raise serializers.ValidationError('Invalid Categoria')
        return attrs
    

class InstrutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socio
        fields = '__all__'
    
    def validate_data_nascimento(self, dob):
        return _validate_data_nascimento(dob)
    def validate_cpf(self, cpf):
        return _validate_cpf(cpf)
    def validate_nome(self, nome):
        return _validate_namelength(nome)
    def validate_endereco(self, endereco):
        return _validate_addresslength(endereco)
    
    def validate_categoria(value):
        valid_choices = [choice[0] for choice in Socio.CATEGORIAS]
        if value not in valid_choices:
            raise serializers.ValidationError('Invalid Categoria')

    def validate(self, attrs):
        cat = attrs.get('categoria')

        if cat == 'I':
            breve = attrs.get('breve')
            curso = attrs.get('nome_do_curso')
            data_diploma = attrs.get('data_diploma')
            instituicao_diploma = attrs.get('instituicao_diploma')
            if ((not breve) or (not curso) or (not data_diploma) or (not instituicao_diploma)):
                raise serializers.ValidationError('Invalid fields for instructor')
            _validate_date(data_diploma)
        else:
            raise serializers.ValidationError('Invalid Categoria')
        return attrs


class VooSerializer(serializers.ModelSerializer):
    teacher_set = SocioSerializer(read_only=True)
    associate_set = SocioSerializer(read_only=True)
    class Meta:
        model = Voo
        fields = '__all__'
    
    def validate_data(self, date):
        return _validate_date(date)
        
    def validate(self, attrs):
        horario_saida = attrs.get('horario_saida')
        horario_chegada = attrs.get('horario_chegada')
        cur_time = datetime.now().time()
        if (not attrs.get('id_socio')):
            raise serializers.ValidationError('Missing ID Socio')
        if (not horario_saida):
            raise serializers.ValidationError('Missing Time Lift off')
        if (not horario_chegada):
            raise serializers.ValidationError('Missing Time Landing')
        if horario_saida >= cur_time:            
            raise serializers.ValidationError('Invalid Time Lift off')
        if horario_chegada > cur_time:            
            raise serializers.ValidationError('Invalid Time Landing')
        return attrs