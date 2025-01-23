from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('api/', include('backend.api.urls')),
    path('', include('backend.login.urls'), name='login_page'),
    path('atividades/', include('backend.base.urls'))
]
