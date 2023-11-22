from django.urls import path
from core.views import index, login, fechamento, logout, pedidos, itens_pendentes, gera_lista
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', index, name='index'),
    path("conta/login/", login, name='login'),
    path('fechamento/', fechamento, name='fechamento'),
    path('conta/logout/', logout, name='logout'),
    path('pedidos/', pedidos, name='pedidos'),
    path('pendentes/', itens_pendentes, name='pendentes'),
    path('lista/', gera_lista, name='lista'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)