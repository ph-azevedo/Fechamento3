from django.urls import path
from core.views import index, login, fechamento, logout, pedidos, itens_pendentes
urlpatterns = [
    path('', index, name='index'),
    path("conta/login/", login, name='login'),
    path('fechamento/', fechamento, name='fechamento'),
    path('conta/logout/', logout, name='logout'),
    path('pedidos/', pedidos, name='pedidos'),
    path('pendentes/', itens_pendentes, name='pendentes'),
    ]