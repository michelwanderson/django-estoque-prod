from django.urls import path
from . import views 

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('entrada/', views.criar_nota, name='criar_nota'),
    path('historico/', views.historico, name='historico'),
    path('entrada/<int:nota_id>/', views.entrada_nota, name='entrada_nota'),
    path('entrada/<int:nota_id>/confirmar/', views.confirmar_nota, name='confirmar_nota'),

]