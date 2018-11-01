# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Member, BdeSecurityGroup, InsaSecurityGroup, LedMailing)
class Admin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "resp_mailing":
            kwargs["queryset"] = LedMailing.objects.filter(type="R")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(SubTeam)
class SubTeamAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "mailing":
            kwargs["queryset"] = LedMailing.objects.filter(type="S")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)