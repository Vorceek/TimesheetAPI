from rest_framework import serializers
from .models import Cliente, Servico, Atividade, RegistroAtividade
from django.utils.timezone import now

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'setor']

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = ['id', 'nome', 'setor']

class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = ['id', 'nome', 'setor']

from rest_framework import serializers
from datetime import timedelta

class RegistroAtividadeSerializer(serializers.ModelSerializer):
    duracao_formatada = serializers.SerializerMethodField()

    class Meta:
        model = RegistroAtividade
        fields = [
            'id',
            'ativo',
            'colaborador',
            'setor_do_colaborador',
            'cliente',
            'servico',
            'atividade',
            'data_inicial',
            'data_final',
            'duracao',
            'duracao_formatada',
        ]
        read_only_fields = ['colaborador', 'setor_do_colaborador', 'data_inicial', 'duracao', 'duracao_formatada']

    def get_duracao_formatada(self, obj):
        if obj.duracao:
            total_seconds = int(obj.duracao.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours}h {minutes}m {seconds}s"
        return "0h 0m 0s"

