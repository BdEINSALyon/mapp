from django import forms
from .models import Member, Team, SubTeam
from django.utils import timezone
from bootstrap_datepicker_plus import DatePickerInput

BIRTH_YEAR_CHOICES = ['']
for i in range(1992,2005):
    BIRTH_YEAR_CHOICES.append(i)


class MemberForm(forms.ModelForm):
    subTeam = forms.ModelChoiceField(queryset=SubTeam.objects.all())
    class Meta:
        model = Member
        exclude = ('teams',)
        widgets = {
            'birthdate': forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),
        }
        help_texts = {
            'insa_email': ('Doit être unique'),
            'adhesion_id': ('Sera récupéré automatiquement si email insa = email dans adhesion'),
            'first_name': ('Obligatoire'),
            'last_name': ('Obligatoire'),
            'promo': ('Obligatoire'),
        }
        now = timezone.now()
        widgets = {'birthdate': DatePickerInput(format='%d/%m/%Y', options={
        "showClose": False,
        "showClear": False,
        "showTodayButton": False,
        "locale": "fr",
        "minDate": now.isoformat(),
        "defaultDate": now.isoformat(),
        })}

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields="__all__"
    # def __init__(self, *args, **kwargs):
    #     super(TeamForm, self).__init__(*args, **kwargs)
    #     self.fields['responsable'].queryset = Member.objects.filter(is_ma=True).all()

class SubTeamForm(forms.ModelForm):
    class Meta:
        model = SubTeam
        fields="__all__"

class AddMemberSubteamForm(forms.Form):
    member = forms.ModelChoiceField(queryset=Member.objects.all(), empty_label=None)
