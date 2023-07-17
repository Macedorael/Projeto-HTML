from django.urls import path
from .views import index,contato,produto,editar_produto

urlpatterns = [
    path('', index, name= 'index'),
    path('contato/', contato, name= 'contato'),
    path('produto/', produto, name= 'produto'),
    path('editar_produto/', editar_produto , name='editar_produto')
]
