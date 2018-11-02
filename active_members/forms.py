from django import forms
from .models import Member
BIRTH_YEAR_CHOICES = ['']
for i in range(1992,2005):
    BIRTH_YEAR_CHOICES.append(i)

class MemberForm(forms.ModelForm):
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
