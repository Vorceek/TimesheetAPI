from django.urls import path
from .views import AtividadesAPIView, GetAtividadesView, GetServicosView, AtividadeAPIView, ClienteAPIView, ServicoAPIView

urlpatterns = [
    path('get-api/atividades/', AtividadesAPIView.as_view(), name='atividades_api'),
    path('get-api/atividade/', AtividadeAPIView.as_view(), name='atividade_api'),
    path('get-api/cliente/', ClienteAPIView.as_view(), name='cliente_api'),
    path('get-api/servico/', ServicoAPIView.as_view(), name='servico_api'),
    path('get-servicos/', GetServicosView.as_view(), name='get-servicos'),
    path('get-atividades/', GetAtividadesView.as_view(), name='get-atividades'),
]
