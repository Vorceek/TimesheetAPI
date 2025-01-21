from django.urls import path
from . import views

urlpatterns = [
    path('atividades/criar/', views.CriarAtividadeAPIView.as_view(), name='criar_atividade'),
]
