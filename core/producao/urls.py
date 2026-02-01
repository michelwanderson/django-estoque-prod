from django.urls import path
from . import views

urlpatterns = [
    path('', views.producao, name='producao'),
]
