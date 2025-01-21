from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('atividades/', include('backend.api.urls')),
    path('', include('backend.login.urls'), name='login_page'),
]
