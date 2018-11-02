from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.urls import reverse
from .models import Member, SubTeam
from .forms import MemberForm

class MemberCreate(CreateView):
    model = Member
    template_name = 'active_members/add_membre.html'
    form_class = MemberForm
    def get_success_url(self):
        return reverse('show_member', args=(self.object.pk,))

class MemberUpdate(UpdateView):
    model = Member
    template_name = 'active_members/add_membre.html'
    form_class = MemberForm
    def get_success_url(self):
        return reverse('show_member', args=(self.object.pk,))

def deleteMemberSubteam(request):
    member = Member.objects.get(pk=request.pk_membre)
    subteam=SubTeam.objects.get(pk=request.pk_subteam)
    member.teams.remove(subteam)
    return reverse('show_subteam', args=(request.pk_subteam,))