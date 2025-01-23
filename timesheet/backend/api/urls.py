from django.urls import path
from .views import AtividadesAPIView, AtividadeAPIView, ClienteAPIView, ServicoAPIView, FinalizarAtividadeView

urlpatterns = [
    path('get-api/atividades/', AtividadesAPIView.as_view(), name='atividades_api'),
    path('get-api/atividade/', AtividadeAPIView.as_view(), name='atividade_api'),
    path('get-api/cliente/', ClienteAPIView.as_view(), name='cliente_api'),
    path('get-api/servico/', ServicoAPIView.as_view(), name='servico_api'),
    path('get-api/finalizar_atividade/<int:atividade_id>/', FinalizarAtividadeView.as_view(), name='finalizar-atividade'),
]
