from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from datetime import datetime
import pytz

# TABELA CLIENTE, SERVIÇO, ATIVIDADE

class Cliente(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    setor = models.ManyToManyField(Group, related_name="cliente", blank=True)
    servicos = models.ManyToManyField('Servico', related_name='clientes', blank=True)

    def __str__(self):
        return self.nome

    def get_setores(self):
        return ", ".join([grupo.name for grupo in self.setor.all()])
    
class Servico(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    setor = models.ManyToManyField(Group, related_name="servico", blank=True)
    atividades = models.ManyToManyField('Atividade', related_name='servicos', blank=True)

    def __str__(self):
        return self.nome
    
    def get_setores(self):
        return ", ".join([grupo.name for grupo in self.setor.all()])

class Atividade(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    setor = models.ManyToManyField(Group, related_name="atividades", blank=True)

    def __str__(self):
        return self.nome
    
    def get_setores(self):
        return ", ".join([grupo.name for grupo in self.setor.all()])

# TABELA PARA REGISTRAR ATIVIDADE

def hora_atual():
    return datetime.now(pytz.timezone('America/Sao_Paulo'))

class RegistroAtividade(models.Model):
    ativo = models.BooleanField(default=True)
    colaborador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    cliente = models.ForeignKey(Cliente, default="Dome", on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, default="Outros", on_delete=models.CASCADE)
    atividade = models.ForeignKey(Atividade, default="Canva", on_delete=models.CASCADE)
    data_inicial = models.DateTimeField(default=hora_atual, editable=False)
    data_final = models.DateTimeField(null=True, blank=True)
    duracao = models.DurationField(null=True, blank=True)
