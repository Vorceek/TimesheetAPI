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
    setor_do_colaborador = models.CharField(max_length=100, blank=True, null=True, editable=False)
    cliente = models.ForeignKey(Cliente, default="Dome", on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, default="Outros", on_delete=models.CASCADE)
    atividade = models.ForeignKey(Atividade, default="Outros", on_delete=models.CASCADE)
    data_inicial = models.DateTimeField(default=hora_atual, editable=False)
    data_final = models.DateTimeField(null=True, blank=True)
    duracao = models.DurationField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Atualiza o setor do colaborador
        if self.colaborador.groups.exists():
            self.setor_do_colaborador = ", ".join([grupo.name for grupo in self.colaborador.groups.all()])
        else:
            self.setor_do_colaborador = "Sem setor"

        # Calcula a duração se a data final estiver preenchida
        if self.data_final:
            self.duracao = self.data_final - self.data_inicial
        else:
            self.duracao = None

        super().save(*args, **kwargs)

    @property
    def fazer_duracao(self):
        if self.data_final:
            delta = self.data_final - self.data_inicial
            total_seconds = int(delta.total_seconds())
            
            # Calcula horas, minutos e segundos
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            # Se os segundos foram arredondados, ajusta minutos
            if rounded_seconds >= 60:
                minutes += 1
                rounded_seconds = 0

            return f"{hours}h {minutes}m {seconds}s"
        return "0h 0m 0s"  # ou outro valor padrão
    
    def __str__(self):
        return f"{self.data_inicial.strftime('%d/%m/%Y %H:%M')} - {self.atividade}"
    
    @property
    def duracao_formatada(self):
        if self.duracao:
            total_seconds = int(self.duracao.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours}h {minutes}m {seconds}s"
        elif not self.data_final:
            # Retorna "Em andamento" enquanto a atividade não for finalizada
            return "Em andamento"
        return "00:00:00"
