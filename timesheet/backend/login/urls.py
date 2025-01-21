from django.urls import path
from . import views
from .acesso import acesso_negado  # Importar a view de erro
from django.contrib.auth import views as auth_views
from backend.login.views import user_login

urlpatterns = [
    path('', user_login, name='login'),
    path('acesso-negado/', acesso_negado, name='acesso_negado'),
]
