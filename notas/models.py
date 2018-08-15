# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Evento(models.Model):
    usuario = models.ForeignKey(User, null=False)
    nombre = models.CharField(max_length=100, null=False, blank=False)
    lugar = models.CharField(max_length=500, null=False, blank=False)
    direccion = models.CharField(max_length=500, null=False, blank=False)

    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_terminacion = models.DateTimeField(null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_editado = models.DateTimeField(auto_now=True)

    CATEGORIA_CHOICES = (
        (1, 'Conferencia'),
        (2, 'Seminario'),
        (3, 'Congreso'),
        (4, 'Curso')
    )
    categoria = models.PositiveSmallIntegerField(choices=CATEGORIA_CHOICES, null=False, blank=False)

    TIPO_CHOICES = (
        (1, 'Virtual'),
        (2, 'Presencial')
    )
    tipo = models.PositiveSmallIntegerField(choices=TIPO_CHOICES, null=False, blank=False)

    def comparar_fecha_creacion(self, otro_evento):
        return self.fecha_creacion - otro_evento.fecha_creacion

