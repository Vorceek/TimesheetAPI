from rest_framework import serializers
from .models import Cliente, Servico, Atividade, RegistroAtividade

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

class RegistroAtividadeSerializer(serializers.ModelSerializer):

    duracao_formatada = serializers.ReadOnlyField(source='fazer_duracao')

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

    def validate_data_final(self, value):
        """
        Valida que `data_final` seja posterior a `data_inicial`.
        """
        data_inicial = self.instance.data_inicial if self.instance else self.initial_data.get('data_inicial')
        if data_inicial and value and value <= data_inicial:
            raise serializers.ValidationError("A data final deve ser posterior à data inicial.")
        return value