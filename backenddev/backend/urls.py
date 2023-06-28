"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework.permissions import AllowAny
from av_system.views import (
    LoginView,
    UsuarioUserNameViewSet,
    FuncionarioViewSet,
    FuncionarioDetailViewSet,
    AlunoViewSet,
    SocioViewSet,
    SocioDetailViewSet,
    InstrutorViewSet,
    VooViewSet,
    VooDetailViewSet,
    VooSocioDetailViewSet
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="LAB PCS3441",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.example.com/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('usuario/', UsuarioUserNameViewSet.as_view(), name='username-availability-check'),
    path('funcionarios/', FuncionarioViewSet.as_view(), name='funcionario-list'),
    path('funcionarios/<int:pk>/', FuncionarioDetailViewSet.as_view(), name='funcionario-detail'),
    path('alunos/', AlunoViewSet.as_view(), name='aluno-list'),
    path('socios/', SocioViewSet.as_view(), name='socio-list'),
    path('socios/<int:pk>/', SocioDetailViewSet.as_view(), name='socio-detail'),
    path('instrutores/', InstrutorViewSet.as_view(), name='instrutor-list'),
    path('voos/', VooViewSet.as_view(), name='voo-list'),
    path('voos/socio/<int:pk>/', VooSocioDetailViewSet.as_view(), name='voo-list-socio'),
    path('voos/<int:pk>/', VooDetailViewSet.as_view(), name='voo-detail'), 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),    
]