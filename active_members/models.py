# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.datetime_safe import date

# Create your models here.
GENRES = [
    ('H', "Homme"),
    ('F', "Femme"),
    ('I', 'Indéfini/Inconnu')
]
TYPE_EQUIPE = [
    ('M', "Manifs"),
    ('A', "Animations"),
    ('S', "Services"),
    ('T', 'Transversal')
]

TYPE_MAILING = [
    ('S', "Sous-Equipe"),
    ('R', "Resps"),
]


class INSASecurityGroup(models.Model):
    name = models.CharField(verbose_name='Nom du groupe sur AD', blank=False, max_length=255, null=False)

    def __str__(self):
        return self.name


class LedMailing(models.Model):
    mail = models.CharField(verbose_name='Adresse Email de la Mailing', blank=False, max_length=255, null=False)
    type = models.CharField(max_length=1, choices=TYPE_MAILING, default='S')

    def __str__(self):
        return self.mail

    @property
    def email(self):
        if (self.type == "S"):
            mail = self.subTeams.members.get().insa_email
            return mail
        else:
            return "none"


class BDESecurityGroup(models.Model):
    name = models.CharField(verbose_name='Nom du groupe sur AD', blank=False, max_length=255, null=False)

    def __str__(self):
        return self.name


class Member(models.Model):
    adhesion_id = models.IntegerField(verbose_name='ID sur Adhésion', unique=True, null=True,
                                      blank=True)  # Non utilisé pour l'instant
    last_name = models.CharField(verbose_name='Nom', blank=False, max_length=255, null=False)
    first_name = models.CharField(verbose_name='Prénom', blank=False, max_length=255, null=False)
    insa_email = models.EmailField(verbose_name='Email INSA', blank=False, max_length=255, null=False, unique=True)
    insa_username = models.CharField(verbose_name='Login INSA', blank=True, max_length=20, null=True)
    office365_email = models.EmailField(verbose_name='Email BdE', blank=True, max_length=255, null=True)
    genre = models.CharField(max_length=1, choices=GENRES, default='I')
    birthdate = models.DateField(verbose_name="Date de naissance", default=date.today, blank=True)
    promo = models.IntegerField(verbose_name='Promo INSA', null=False, blank=False)
    teams = models.ManyToManyField("SubTeam", related_name="members", blank=True)

    def __str__(self):
        return "{0} {1} - Promo {2}".format(self.first_name, self.last_name, self.promo)


class Team(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom de l'équipe")
    type = models.CharField(max_length=1, choices=TYPE_EQUIPE, verbose_name="Type d'équipe")
    is_ma = models.BooleanField(verbose_name="Considère le membre comme actif ?", default=True)
    responsable = models.ForeignKey(to=Member, null=True, on_delete=models.PROTECT, blank=True, related_name="+")
    resp_mailing = models.OneToOneField("LedMailing", null=True, on_delete=models.PROTECT, related_name="team",
                                        blank=True)
    team_insa_group = models.ForeignKey("INSASecurityGroup", null=True, on_delete=models.PROTECT, related_name="+",
                                        blank=True)
    team_bde_group = models.ForeignKey("BDESecurityGroup", null=True, on_delete=models.PROTECT, related_name="+",
                                       blank=True)
    responsable_insa_group = models.ForeignKey("INSASecurityGroup", null=True, on_delete=models.PROTECT,
                                               related_name="+", blank=True)
    responsable_bde_group = models.ForeignKey("BDESecurityGroup", null=True, on_delete=models.PROTECT, related_name="+",
                                              blank=True)

    def __str__(self):
        return "{0} ".format(self.name)

    @property
    def nombre(self):
        return Member.objects.filter(teams__in=self.subTeams.all()).distinct().count()


class SubTeam(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom de l'équipe")
    responsable = models.ForeignKey(to=Member, null=True, on_delete=models.PROTECT, blank=True, related_name="+")
    mailing = models.OneToOneField("LedMailing", null=True, on_delete=models.PROTECT, related_name="subTeams",
                                   blank=True)
    team = models.ForeignKey("Team", null=False, on_delete=models.PROTECT, related_name="subTeams", blank=False)

    def __str__(self):
        return "{0} -  {1}".format(self.team.name, self.name)

    @property
    def nombre(self):
        return self.members.count()