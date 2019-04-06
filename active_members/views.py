from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse
from .models import Member, SubTeam, Team
from .forms import MemberForm, TeamForm, SubTeamForm, AddMemberSubteamForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def memberCreate(request):
    form = MemberForm(request.POST or None)
    if form.is_valid():
        content = form.save()
        print(form.cleaned_data["subTeam"])
        content.teams.add(form.cleaned_data["subTeam"])
        content.save()
        return redirect(reverse('show_member', args=[content.pk]))
    else:
        return render(request, 'active_members/form_basic.html', {"form": form})


class MemberUpdate(LoginRequiredMixin,UpdateView):
    model = Member
    template_name = 'active_members/form_basic.html'
    form_class = MemberForm
    def get_success_url(self):
        return reverse('show_member', args=(self.object.pk,))

class TeamUpdate(LoginRequiredMixin,UpdateView):
    model = Team
    template_name = 'active_members/form_basic.html'
    form_class = TeamForm
    def get_success_url(self):
        return reverse('show_team', args=(self.object.pk,))

class SubTeamUpdate(LoginRequiredMixin,UpdateView):
    model = SubTeam
    template_name = 'active_members/form_basic.html'
    form_class = SubTeamForm
    def get_success_url(self):
        return reverse('show_subteam', args=(self.object.pk,))

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