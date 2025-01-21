from django.urls import path
from apps.admin.relacionamento.views import get_servicos, get_atividades
from . import views

urlpatterns = [
    path('', views.HomeGerenciarAtividadesView.as_view(), name='home'),
    path('get-servicos/<int:cliente_id>/', get_servicos, name='get-servicos'),
    path('get-atividades/<int:servico_id>/', get_atividades, name='get-atividades'),
]
