from django.urls import path, include
from django.views.generic import ListView, DetailView
from . import views
from .models import Member, SubTeam, Team
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Nous allons réécrire l'URL de l'accueil
    path('',login_required(ListView.as_view(model=Member,)), name="home"),
    path('member', login_required(ListView.as_view(model=Member,)), name='list_member'),
    path('member/<int:pk>', login_required(DetailView.as_view(model=Member)), name='show_member'),
    path('member/edit/<int:pk>', views.MemberUpdate.as_view(), name='edit_member'),
    path('member/add', login_required(views.memberCreate), name='create_member'),
    path('member/sync/<int:pk>', login_required(views.sync_member), name="sync_member"),
    path('member/update_membership/<int:pk>', login_required(views.update_membership), name="update_membership_member"),
    path('subteam/<int:pk>', login_required(DetailView.as_view(model=SubTeam)), name='show_subteam'),
    path('subteam/add_member/<int:pk>', views.add_member_subteam, name='edit_member_subteam'),
    path('subteam/edit/<int:pk>', views.SubTeamUpdate.as_view(), name='edit_subteam'),
    path('subteam/<int:pk_subteam>/delete/<int:pk_member>', views.deleteMemberSubteam, name='delete_member_subteam'),
    path('subteam/<int:pk_subteam>/clean', views.cleanSubteam, name='clean_subteam'),
    path('team', login_required(ListView.as_view(model=Team,)), name='list_team'),
    path('team/<int:pk>', login_required(DetailView.as_view(model=Team)), name='show_team'),
    path('team/edit/<int:pk>', views.TeamUpdate.as_view(), name='edit_team'),
    path('team/<int:pk_team>/clean', views.cleanTeam, name='clean_team'),
]
