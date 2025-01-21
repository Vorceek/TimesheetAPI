from django.shortcuts import render

def acesso_negado(request):
    return render(request, 'login/sem_acesso.html')
