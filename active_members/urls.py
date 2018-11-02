from django.urls import path, include
from django.views.generic import ListView, DetailView

from . import views
from .models import Member

urlpatterns = [
    # Nous allons réécrire l'URL de l'accueil
    path('accueil', ListView.as_view(model=Member,)),
    path('member/<int:pk>', DetailView.as_view(model=Member), name='show_member'),
]
