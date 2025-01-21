from rest_framework import serializers
from .models import RegistroAtividade

class RegistroAtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroAtividade
        fields = ('id', 'cliente', 'servico', 'atividade', 'data_inicial', 'data_final', 'duracao', 'setor')