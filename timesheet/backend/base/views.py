import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.timezone import localdate
from django.core.paginator import Paginator
from django.views import View
from backend.api.forms import RegistroAtividadeForm
from backend.api.models import RegistroAtividade

class HomeGerenciarAtividadesView(View):

    def get_context_data(self, user):
        """
        Recupera os dados necessários para o contexto do template via API,
        aplicando filtro de grupos (setores) do usuário.
        """
        # URLs das APIs separadas
        api_url_clientes = f"http://127.0.0.1:8000/api/get-api/cliente/"
        api_url_servicos = f"http://127.0.0.1:8000/api/get-api/servico/"
        api_url_atividades = f"http://127.0.0.1:8000/api/get-api/atividade/"
        print("Requisitando APIs:", api_url_clientes, api_url_servicos, api_url_atividades)

        # Faz as requisições para cada API
        try:
            response_clientes = requests.get(api_url_clientes)
            response_clientes.raise_for_status()
            clientes = response_clientes.json()
            
            response_servicos = requests.get(api_url_servicos)
            response_servicos.raise_for_status()
            servicos = response_servicos.json()
            
            response_atividades = requests.get(api_url_atividades)
            response_atividades.raise_for_status()
            atividades = response_atividades.json()

            # Filtro com base nos grupos do usuário
            grupos_usuario = user.groups.all()

            # Filtro dos dados para clientes, serviços e atividades
            clientes = [cliente for cliente in clientes if any(grupo.id in cliente['setor'] for grupo in grupos_usuario)]
            servicos = [servico for servico in servicos if any(grupo.id in servico['setor'] for grupo in grupos_usuario)]
            atividades = [atividade for atividade in atividades if any(grupo.id in atividade['setor'] for grupo in grupos_usuario)]
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a API: {e}")
            clientes = []
            servicos = []
            atividades = []

        # Lógica de controle de permissões de admin
        is_admin = user.groups.filter(name='admin').exists()

        return {
            'clientes': clientes,
            'servicos': servicos,
            'atividades': atividades,
            'is_admin': is_admin,
        }

    def calcular_total_duracao(self, atividades_usuario):
        """
        Calcula a duração total das atividades e formata em horas, minutos e segundos.
        """
        total_duracao = sum(
            (atividade.data_final - atividade.data_inicial).total_seconds()
            for atividade in atividades_usuario if atividade.data_final and atividade.data_inicial
        )
        
        # Converte os segundos totais em horas, minutos e segundos
        horas = total_duracao // 3600
        minutos = (total_duracao % 3600) // 60
        segundos = total_duracao % 60

        # Retorna a duração formatada
        return f"{int(horas)}h {int(minutos)}m {int(segundos)}s"


    def get(self, request):
        """
        Exibe o formulário e lista as atividades do colaborador.
        """
        user = request.user
        context = self.get_context_data(user)

        # Lista as atividades do usuário no dia atual
        atividades_usuario = RegistroAtividade.objects.filter(
            data_inicial__date=localdate(), colaborador=user
        ).order_by('-data_inicial')

        # Paginação
        paginator = Paginator(atividades_usuario, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Atualiza o contexto com a duração formatada
        context.update({
            'form': RegistroAtividadeForm(),
            'page_obj': page_obj,
            'total_duracao': self.calcular_total_duracao(atividades_usuario),  # Passando a duração formatada
        })

        return render(request, 'base/minhas_atividades.html', context)

    def post(self, request):
        """
        Processa o registro de uma nova atividade.
        """
        user = request.user

        # Registra uma nova atividade usando o formulário
        form = RegistroAtividadeForm(request.POST)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.colaborador = user
            atividade.save()
            return redirect('atividades')

        # Em caso de erro, reexibe o formulário com os dados inseridos
        context = self.get_context_data(user)
        atividades_usuario = RegistroAtividade.objects.filter(
            data_inicial__date=localdate(), colaborador=user
        ).order_by('-data_inicial')

        # Paginação
        paginator = Paginator(atividades_usuario, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Atualiza o contexto com a duração formatada
        context.update({
            'form': form,
            'page_obj': page_obj,
            'total_duracao': self.calcular_total_duracao(atividades_usuario),  # Passando a duração formatada
        })

        return render(request, 'base/minhas_atividades.html', context)