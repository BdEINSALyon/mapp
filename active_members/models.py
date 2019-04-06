# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date

# Create your models here.
GENRES = [
    ('M', "Homme"),
    ('F', "Femme"),
    ('U', 'Indéfini/Inconnu')
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


class InsaSecurityGroup(models.Model):
    name = models.CharField(verbose_name='Nom du groupe sur AD', blank=False, max_length=255, null=False)
    def __str__(self):
        return self.name


class LedMailing(models.Model):
    mail = models.CharField(verbose_name='Adresse Email de la Mailing', blank=False, max_length=255, null=False)
    type = models.CharField(max_length=1, choices=TYPE_MAILING, default='S')

    def __str__(self):
        return self.mail

    @property
    def cmd_generator(self):
        if (self.type == "S"):
            liste = [];
            mail_list = self.subTeams.members.all()
            for mail in mail_list:
                liste.append(mail.insa_email)
            if(self.subTeams.team.check_resp is True and self.subTeams.check_resp is True):
                liste.append(self.subTeams.team.responsable.insa_email)
            else:
                return "Probleme avec les resp (sous equipe ou equipe g)"
            return liste(set(liste)) #To remove duplicate
        elif(self.type == "R"):
            liste=[];
            sub_list=SubTeam.objects.filter(team=self.team).all()
            for sub in sub_list:
                if(sub.check_resp is True):
                    liste.append(sub.responsable.insa_email)
                else:
                    return "Erreur resp sous equipe"
            if(self.team.check_resp is True):
                liste.append(self.team.responsable.insa_email)
            else:
                return "Erreur resp general"
            return liste(set(liste)) #To remove duplicate


class BdeSecurityGroup(models.Model):
    name = models.CharField(verbose_name='Nom du groupe sur AD', blank=False, max_length=255, null=False)

    def __str__(self):
        return self.name


class Member(models.Model):
    adhesion_id = models.IntegerField(verbose_name='ID sur Adhésion', unique=True, null=True,
                                      blank=True)
    has_valid_membership = models.BooleanField("A la carte VA", null=False, default=False)
    last_name = models.CharField(verbose_name='Nom', blank=False, max_length=255, null=False)
    first_name = models.CharField(verbose_name='Prénom', blank=False, max_length=255, null=False)
    insa_email = models.EmailField(verbose_name='Email INSA', blank=False, max_length=255, null=False, unique=True)
    insa_username = models.CharField(verbose_name='Login INSA', blank=True, max_length=20, null=True)
    office365_email = models.EmailField(verbose_name='Email BdE', blank=True, max_length=255, null=True)
    gender = models.CharField(max_length=1, choices=GENRES, default='U')
    birthdate = models.DateField(verbose_name="Date de naissance", default=date.today, blank=True)
    promo = models.IntegerField(verbose_name='Promo INSA', null=False, blank=False)
    teams = models.ManyToManyField("SubTeam", related_name="members", blank=True)
    def __str__(self):
        return "{0} {1} - Promo {2}".format(self.first_name, self.last_name, self.promo)
    @property
    def is_ma(self):
        return self.teams.filter(team__is_ma=True).all().count() > 0
    @property
    def profil_complete(self):
        if(self.insa_username is not None and self.office365_email is not None and self.birthdate is not None):
            return True
        else:
            return False
    @property
    def age(self):
        delta = date.today() - self.birthdate
        return delta.days//365


class Team(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom de l'équipe")
    type = models.CharField(max_length=1, choices=TYPE_EQUIPE, verbose_name="Type d'équipe")
    is_ma = models.BooleanField(verbose_name="Considère le membre comme actif ?", default=True)
    responsable = models.ForeignKey(to=Member, null=True, on_delete=models.PROTECT, blank=True)
    resp_mailing = models.OneToOneField("LedMailing", null=True, on_delete=models.PROTECT, related_name="team",
                                        blank=True)
    team_insa_group = models.ForeignKey("InsaSecurityGroup", null=True, on_delete=models.PROTECT, related_name="+",
                                        blank=True)
    team_bde_group = models.ForeignKey("BdeSecurityGroup", null=True, on_delete=models.PROTECT, related_name="+",
                                       blank=True)
    responsable_insa_group = models.ForeignKey("InsaSecurityGroup", null=True, on_delete=models.PROTECT,
                                               related_name="+", blank=True)
    responsable_bde_group = models.ForeignKey("BdeSecurityGroup", null=True, on_delete=models.PROTECT, related_name="+",
                                              blank=True)

    def __str__(self):
        return "{0} ".format(self.name)

    @property
    def nombre(self):
        return Member.objects.filter(teams__in=self.subTeams.all()).distinct().count()
    @property
    def check_resp(self):
        if (self.responsable is not None):
            if (Member.objects.filter(insa_email=self.responsable.insa_email).filter(teams__in=self.subTeams.all()).count()==1):
                return True
            else:
                return False
        else:
            return False
    @property
    def nombre_sous_equipe(self):
        return self.subTeams.count()
    @property
    def check_all_ok(self):
        check = True
        teams = SubTeam.objects.filter(team=self)
        for team in teams:
            if(not team.check_resp):
                check = False
        if(not self.check_resp):
            check = False
        return check
    @property
    def clean_team(self):
        teams=SubTeam.objects.filter(team=self)
        for team in teams:
            team.clean_team
        self.responsable=None
        self.save()



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
    @property
    def check_resp(self):
        if(self.responsable is not None):
            if (Member.objects.filter(insa_email=self.responsable.insa_email).filter(
                    teams=self).count() == 1):
                return True
            else:
                return False
        else:
            return False
    @property
    def clean_team(self):
        members=Member.objects.filter(teams=self)
        for member in members:
            member.teams.remove(self)
        self.responsable=None
        self.save()