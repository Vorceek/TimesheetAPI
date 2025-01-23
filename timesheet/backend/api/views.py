from datetime import timedelta
from pyexpat.errors import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User
from django.utils.timezone import localdate, now
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from .models import Cliente, Servico, Atividade, RegistroAtividade
from .serializers import (
    ClienteSerializer,
    ServicoSerializer,
    AtividadeSerializer,
    RegistroAtividadeSerializer,
)


def formatar_duracao_segundos(total_segundos):
    # Converte os segundos totais em horas, minutos e segundos
    horas = total_segundos // 3600
    minutos = (total_segundos % 3600) // 60
    segundos = total_segundos % 60
    return f"{int(horas)}h {int(minutos)}m {int(segundos)}s"


# API para obter Clientes

class ClienteAPIView(APIView):
    def get(self, request):

        clientes = Cliente.objects.all()
        
        # Serializa os dados dos clientes
        clientes_serializer = ClienteSerializer(clientes, many=True)
        
        return Response(clientes_serializer.data)

# API para obter Serviços

class ServicoAPIView(APIView):
    def get(self, request):
        # Obtém o ID do cliente da query string
        cliente_id = request.GET.get('cliente')
        
        if cliente_id:
            # Filtra os serviços pelo cliente
            servicos = Servico.objects.filter(cliente_id=cliente_id)
        else:
            # Se não houver cliente, retorna todos os serviços
            servicos = Servico.objects.all()
        
        # Serializa os dados dos serviços
        servicos_serializer = ServicoSerializer(servicos, many=True)
        
        return Response(servicos_serializer.data)

# API para obter Atividades

class AtividadeAPIView(APIView):
    def get(self, request):
        # Obtém o ID do serviço da query string
        servico_id = request.GET.get('servico')
        
        if servico_id:
            # Filtra as atividades pelo serviço
            atividades = Atividade.objects.filter(servico_id=servico_id)
        else:
            # Se não houver serviço, retorna todas as atividades
            atividades = Atividade.objects.all()
        
        # Serializa os dados das atividades
        atividades_serializer = AtividadeSerializer(atividades, many=True)
        
        return Response(atividades_serializer.data)

class AtividadesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        # Obtém os grupos aos quais o usuário pertence (representando setores)
        grupos_usuario = user.groups.all()  # Retorna um QuerySet de grupos

        # Filtra clientes, serviços e atividades com base nos grupos (setores)
        clientes = Cliente.objects.filter(setor__in=grupos_usuario).distinct()
        servicos = Servico.objects.filter(setor__in=grupos_usuario).distinct()
        atividades = Atividade.objects.filter(setor__in=grupos_usuario).distinct()

        # Serializa os dados
        clientes_serializer = ClienteSerializer(clientes, many=True)
        servicos_serializer = ServicoSerializer(servicos, many=True)
        atividades_serializer = AtividadeSerializer(atividades, many=True)

        # Retorna os dados filtrados
        return Response({
            'clientes': clientes_serializer.data,
            'servicos': servicos_serializer.data,
            'atividades': atividades_serializer.data,
        })

class RegistroAtividadeAPIView(APIView):
    """
    Gerencia o registro de atividades do colaborador autenticado.
    """
    def get(self, request):
        """
        Retorna as atividades registradas do colaborador autenticado.
        Inclui paginação e cálculo da duração total.
        """
        atividades_usuario = RegistroAtividade.objects.filter(
            colaborador=request.user, hora__date=localdate()
        ).order_by('-hora')

        paginator = Paginator(atividades_usuario, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        serializer = RegistroAtividadeSerializer(page_obj, many=True)


        total_duracao_segundos = sum(
            (atividade.data_final - atividade.data_inicial).total_seconds()
            for atividade in atividades_usuario if atividade.data_final and atividade.data_inicial
        )

        # Formata o total de segundos em horas, minutos e segundos
        total_duracao_formatada = formatar_duracao_segundos(total_duracao_segundos)
            
        return Response({
            'atividades': serializer.data,
            'total_duracao': total_duracao_formatada,
            'page': page_number,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        })

    def post(self, request):
        """
        Registra uma nova atividade e finaliza a anterior, se existir.
        """
        user = request.user

        # Finaliza a atividade ativa
        atividade_ativa = RegistroAtividade.objects.filter(
            colaborador=user, ativo=True
        ).first()

        if atividade_ativa:
            atividade_ativa.data_final = now()
            atividade_ativa.ativo = False
            atividade_ativa.save()
            messages.success(
                request,
                f'A atividade ativa foi finalizada em {atividade_ativa.data_final.strftime("%d/%m/%Y %H:%M:%S")}'
            )

        # Registra uma nova atividade
        serializer = RegistroAtividadeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(colaborador=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from datetime import timedelta

class FinalizarAtividadeView(APIView):
    """
    Finaliza uma atividade específica do colaborador autenticado.
    """
    def post(self, request, atividade_id):
        # Busca a atividade que o usuário deseja finalizar
        atividade = RegistroAtividade.objects.filter(
            id=atividade_id, colaborador=request.user, ativo=True
        ).first()

        if not atividade:
            return Response({'error': 'Atividade não encontrada ou já finalizada.'}, status=status.HTTP_404_NOT_FOUND)

        # Calcula a duração da atividade
        if atividade.data_inicial:
            # Garantindo que o campo 'data_final' está presente
            atividade.data_final = now()

            # Calcule a duração subtraindo data_inicial de data_final
            atividade.duracao = atividade.data_final - atividade.data_inicial

            atividade.ativo = False  # Marca a atividade como finalizada
            atividade.save()

            # Serializa a atividade finalizada
            serializer = RegistroAtividadeSerializer(atividade)
            return Response(serializer.data)

        return Response({'error': 'Data inicial não definida para a atividade.'}, status=status.HTTP_400_BAD_REQUEST)

