from datetime import timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from apps.admin.relacionamento.forms import RegistroAtividadeForm
from apps.admin.relacionamento.models import Cliente, Atividade, Servico
from apps.admin.relacionamento.views import FinalizarAtividadesHandler
from apps.admin.relatorio.formatar_segundos import formatar_duracao
from apps.admin.relatorio.models import RegistroAtividade
from django.core.paginator import Paginator
from django.utils.timezone import localdate
from apps.home.grupo_usuario import usuario_tem_grupo
from django.contrib import messages
from django.utils.timezone import now

class HomeGerenciarAtividadesView(View):

    def get_context_data(self, user):
        """
        Recupera os dados necessários para o contexto do template.
        """
        setores_usuario = user.colaborador.setores.all().order_by('nome') if hasattr(user, 'colaborador') else []
        clientes = Cliente.objects.filter(setor__in=setores_usuario).distinct().order_by('nome')
        servicos = Servico.objects.filter(setor__in=setores_usuario).distinct().order_by('nome')
        atividades = Atividade.objects.filter(setor__in=setores_usuario).distinct().order_by('nome')

        is_admin = user.groups.filter(name='Admin').exists()

        return {
            'clientes': clientes,
            'servicos': servicos,
            'atividades': atividades,
            'is_admin': is_admin,
        }

    def calcular_total_duracao(self, atividades_usuario):
        """
        Calcula a duração total das atividades.
        """
        total_duracao = sum(
            (atividade.data_fim - atividade.hora).total_seconds()
            for atividade in atividades_usuario if atividade.data_fim and atividade.hora
        )
        return formatar_duracao(total_duracao)

    def get(self, request):
        """
        Exibe o formulário e lista as atividades do colaborador.
        """
        user = request.user
        context = self.get_context_data(user)

        # Lista as atividades do usuário
        atividades_usuario = RegistroAtividade.objects.filter(hora__date=localdate(), colaborador=request.user).order_by('-hora')

        # Paginação
        paginator = Paginator(atividades_usuario, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Formata a duração total das atividades
        context.update({
            'form': RegistroAtividadeForm(),
            'page_obj': page_obj,
            'total_duracao': self.calcular_total_duracao(atividades_usuario),
        })

        return render(request, 'home/minhas_atividades.html', context)

    def post(self, request):
        """
        Processa o registro de uma nova atividade.
        """
        user = request.user
        handler = FinalizarAtividadesHandler(user)

        # Finaliza a atividade ativa, se existir
        atividade_ativa = handler.finalizar_atividades_ativas()
        if atividade_ativa:
            messages.success(
                request,
                f'A atividade ativa foi finalizada em {atividade_ativa.data_fim.strftime("%d/%m/%Y %H:%M:%S")}'
            )

        # Registra uma nova atividade
        form = RegistroAtividadeForm(request.POST)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.colaborador = user
            atividade.save()
            return redirect('relacionamento:minhas_atividades')

        # Em caso de erro, reexibe o formulário com os dados inseridos
        context = self.get_context_data(user)
        atividades_usuario = RegistroAtividade.objects.filter(colaborador=user).order_by('-hora')

        # Paginação
        paginator = Paginator(atividades_usuario, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context.update({
            'form': form,
            'page_obj': page_obj,
            'total_duracao': self.calcular_total_duracao(atividades_usuario),
        })

        return render(request, 'home/minhas_atividades.html', context)
