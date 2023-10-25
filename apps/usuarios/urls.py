from django.urls import path
from apps.usuarios.views import login, cadastro, logout, enviar_aviso, relatorio, relatorio_fotos, relatorio_pizza

urlpatterns = [
    path('login', login, name='login'),
    path('cadastro', cadastro, name='cadastro'),
    path('logout', logout, name='logout'),
    path('enviar-aviso/', enviar_aviso, name='enviar_aviso'),
    path('relatorio-pdf/', relatorio, name='relatorio_pdf'),
    path('relatorio-foto/', relatorio_fotos, name='relatorio-foto'),
    path('relatorio-pizza/', relatorio_pizza, name='relatorio-pizza'),
]