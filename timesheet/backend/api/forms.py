from django import forms
from django.contrib.auth import get_user_model
from .models import Cliente, RegistroAtividade, Servico, Atividade

class RegistroAtividadeForm(forms.ModelForm):
    class Meta:
        model = RegistroAtividade
        fields = ['cliente', 'servico', 'atividade']

User = get_user_model()
class FiltroRelatorioForm(forms.Form):
    colaborador = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)
    servico = forms.ModelChoiceField(queryset=Servico.objects.all(), required=False)
    atividade = forms.ModelChoiceField(queryset=Atividade.objects.all(), required=False)
    data_inicial = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    data_final = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)