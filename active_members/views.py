from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse
from .models import Member, SubTeam, Team
from .forms import MemberForm, TeamForm, SubTeamForm, AddMemberSubteamForm, MemberCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from active_members.adhesion_api import AdhesionAPI
from active_members import utils
from django.http import HttpResponseServerError



def memberCreate(request):
    form = MemberCreateForm(request.POST or None)
    if form.is_valid():
        content = form.save()
        return redirect(reverse('show_member', args=[content.pk]))
    else:
        return render(request, 'active_members/form_new.html', {"form": form})


class MemberUpdate(LoginRequiredMixin, UpdateView):
    model = Member
    template_name = 'active_members/form_basic.html'
    form_class = MemberForm

    def get_success_url(self):
        return reverse('show_member', args=(self.object.pk,))


class TeamUpdate(LoginRequiredMixin, UpdateView):
    model = Team
    template_name = 'active_members/form_basic.html'
    form_class = TeamForm

    def get_success_url(self):
        return reverse('show_team', args=(self.object.pk,))


class SubTeamUpdate(LoginRequiredMixin, UpdateView):
    model = SubTeam
    template_name = 'active_members/form_basic.html'
    form_class = SubTeamForm

    def get_success_url(self):
        return reverse('show_subteam', args=(self.object.pk,))


def sync_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if member.office365_email is None:
        print("generate email")
    if member.adhesion_id is None:
        api = AdhesionAPI()
        adhesion_member = api.get_member_email(email=member.insa_email)
        if len(adhesion_member) == 1:
            member.adhesion_id = adhesion_member[0]["id"]
            member.has_valid_membership = adhesion_member[0]["has_valid_membership"]
            member.save()
    return redirect(reverse('show_member', args=[member.pk]))


def update_membership(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if utils.update_adhesion_membership(member):
        return redirect(reverse('show_member', args=[member.pk]))
    else:
        return HttpResponseServerError()



@login_required
def add_member_subteam(request, pk):
    form = AddMemberSubteamForm(request.POST or None)
    team = SubTeam.objects.get(pk=pk)
    form.fields["member"].queryset = Member.objects.exclude(teams=team).all()
    if form.is_valid():
        member = form.cleaned_data['member']
        member.teams.add(team)
        return redirect(reverse('show_subteam', args=(pk,)))
    else:
        return render(request, 'active_members/form_basic.html', {'form': form})


@login_required
def deleteMemberSubteam(request, pk_member, pk_subteam):
    member = Member.objects.get(pk=pk_member)
    subteam = SubTeam.objects.get(pk=pk_subteam)
    member.teams.remove(subteam)
    return redirect(reverse('show_subteam', args=(pk_subteam,)))


@login_required
def cleanSubteam(request, pk_subteam):
    subteam = SubTeam.objects.get(pk=pk_subteam)
    subteam.clean_team
    return redirect(reverse('show_subteam', args=(pk_subteam,)))


@login_required
def cleanTeam(request, pk_team):
    team = Team.objects.get(pk=pk_team)
    team.clean_team
    return redirect(reverse('show_team', args=(pk_team,)))
