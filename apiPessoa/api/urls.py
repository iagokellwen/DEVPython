from django.urls import path
from .views import *


urlpatterns = [
    path('pessoa/', PessoaList.as_view(), name='pessoa-list'),
    path('pessoa/<int:pk>/', PessoaDetalhes.as_view(), name='pessoa-detalhes'),
    path('pessoa/<int:pk>/calcular_peso_ideal/', CalcularPesoIdeal.as_view()),
]