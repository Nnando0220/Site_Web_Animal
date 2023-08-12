from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('postagem/', views.postagem, name='postagem'),
    path('membros/', views.membros, name='membros'),
    path('membros/detalhes/<int:id>', views.detalhes, name='detalhes'),
]