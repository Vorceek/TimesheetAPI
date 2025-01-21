from django.db import models
from django.contrib.auth.models import User

class Setor(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

    def get_colaboradores(self):
        return self.colaboradores.all()

class Colaborador(models.Model):
    nome = models.OneToOneField(User, on_delete=models.CASCADE)
    setores = models.ManyToManyField(Setor, related_name="colaboradores", blank=True)

    def __str__(self):
        return self.nome.username
