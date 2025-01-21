from django.urls import path
from . import views

urlpatterns = [
    path('atividades/', views.HomeGerenciarAtividadesView.as_view, name='criar_atividade'),
]
