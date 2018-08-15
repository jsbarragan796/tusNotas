# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from notas.models import Evento, User

# Register your models here.
admin.site.register(Evento)
admin.site.register(User)