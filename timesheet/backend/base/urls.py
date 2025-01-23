from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeGerenciarAtividadesView.as_view(), name='atividades'),
]
