from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    NIVEL_ACESSO_CHOICES = [
        (1, 'Sem acesso à gerência'),
        (2, 'Gerência de pacientes e responsáveis'),
        (3, 'Gerência de pacientes, responsáveis e profissionais médicos')
    ]
    nivel_acesso = models.IntegerField(choices=NIVEL_ACESSO_CHOICES, default=1)
class Responsavel(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=15)
    
    celular = models.IntegerField()
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome

class Paciente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=255, unique=True, null=True)
    nascimento = models.DateField( null=True)
    endereco = models.CharField(max_length=255, null=True)
    bairro = models.CharField(max_length=255, null=True)
    cep = models.CharField(max_length=8, null=True)
    cidade = models.CharField(max_length=255, null=True)
    estado = models.CharField(max_length=2, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, null=True)
    criacao = models.DateTimeField(auto_now_add=True)
    modificacao = models.DateTimeField(auto_now=True)
    sexo = models.CharField(max_length=1, null=True)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome


class Profissao(models.Model):
    descricao = models.CharField(max_length=255)
    criacao = models.DateTimeField(auto_now_add=True)
    modificacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.descricao


class Instituicao(models.Model):
    descricao = models.CharField(max_length=255)
    
    criacao = models.DateTimeField(auto_now_add=True)
    modificacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.descricao


class Profissional(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20)
    criacao = models.DateTimeField(auto_now_add=True)
    modificacao = models.DateTimeField(auto_now=True)
    profissao = models.ForeignKey(Profissao, on_delete=models.CASCADE, default=1)
    instituicao = models.ForeignKey(Instituicao,on_delete=models.CASCADE, default=1)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True )

    def __str__(self):
        return self.nome

    def criar_relacao(self, paciente, status, inicio, termino=None):
        relacao = Relacao.objects.create(
            paciente=paciente,
            profissional=self,
            status=status,
            inicio=inicio,
            termino=termino
        )
        return relacao

    def fazer_avaliacao_CARS(self, paciente, respostas):
        relacao = Relacao.objects.get(paciente=paciente, profissional=self)
        cars = CARS.objects.create(
            relacao=relacao,
            q1=respostas.get('q1'),
            q2=respostas.get('q2'),
            q3=respostas.get('q3'),
            q4=respostas.get('q4'),
            q5=respostas.get('q5'),
            q6=respostas.get('q6'),
            q7=respostas.get('q7'),
            q8=respostas.get('q8'),
            q9=respostas.get('q9'),
            q10=respostas.get('q10'),
            q11=respostas.get('q11'),
            q12=respostas.get('q12'),
            q13=respostas.get('q13'),
            q14=respostas.get('q14'),
            q15=respostas.get('q15'),
            resultado=respostas.get('resultado'),
        )
        return cars


class Relacao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    inicio = models.DateField(auto_now=True)
    termino = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.paciente.nome} - {self.profissional.nome}'

from django.utils import timezone
class CARS(models.Model):
    relacao = models.OneToOneField(Relacao, on_delete=models.CASCADE, unique=False)
    q1 =  models.FloatField()
    q2 = models.FloatField()
    
    
    resultado = models.FloatField()
    criacao = models.DateTimeField(auto_now_add=True)
    data_avaliacao = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'CARS {self.relacao.paciente.nome} - {self.relacao.profissional.nome}'
