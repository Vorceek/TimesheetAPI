from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse

def user_login(request):

    #   Verificação de Usuário
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if user.groups.exists():
                return redirect(reverse("home"))
            else:
                return redirect("acesso-negado/")

    return render(request, "login/login.html")