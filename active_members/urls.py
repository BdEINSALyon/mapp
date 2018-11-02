from django.urls import path, include
from django.views.generic import ListView, DetailView

from . import views
from .models import Member, SubTeam

urlpatterns = [
    # Nous allons réécrire l'URL de l'accueil
    path('accueil', ListView.as_view(model=Member,)),
    path('member/<int:pk>', DetailView.as_view(model=Member), name='show_member'),
    path('member/edit/<int:pk>', views.MemberUpdate.as_view(), name='edit_member'),
    path('member/add', views.MemberCreate.as_view(), name='create_member'),
    path('subteam/<int:pk>', DetailView.as_view(model=SubTeam), name='show_subteam'),
    path('subteam/<int:pk_subteam>/delete/<int:pk_membre>', views.deleteMemberSubteam, name='delete_member_subteam'),
]
