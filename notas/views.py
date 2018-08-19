# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from notas.forms import UserForm, EventoForm , loginForm
from django.contrib.auth.models import User
from notas.models import Evento
from django.contrib import messages
# Create your views here.

# Autenticación
def autenticacion(request):

    if request.user.is_authenticated:
        if request.method == 'POST':
            eliminar = True if 'idE' in request.POST else False
            if eliminar:
                pk = request.POST.get('idE')
                evento = Evento.objects.get(id=pk)
                return eliminar_evento(evento,request)
        else:
            return eventos_view(request)

    else:
        if request.method == 'POST':
            registro = True if 'password2' in request.POST else False
            if registro:
                return usuario_create(request)
            else:
                return login_view(request)
        else:
            form = loginForm()
            formregistro = UserForm()
            return render(request, 'login.html', {'form': form, 'formRegistro': formregistro})

def login_view(request):
    mensaje = ''
    username = request.POST.get('usernameL')
    password = request.POST.get('passwordL')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('notas:index'))
    else:
        mensaje = 'Nombre de usuario o clave no valida'
        messages.warning(request, mensaje, extra_tags='alert alert-warning')
        return redirect(reverse('notas:index'))

def usuario_create(request):
    formregistro = UserForm(request.POST)
    if formregistro.is_valid():
        cleaned_data = formregistro.cleaned_data
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user_model = User.objects.create_user(username=username, password=password)
        user_model.save()
        messages.success(request, 'Se ha creado con éxito su cuenta, ahora inicie sesión',
                         extra_tags='alert alert-success')
        return HttpResponseRedirect(reverse('notas:index'))
    else:
        form = loginForm()
        return render(request, 'login.html', {'form': form, 'formRegistro': formregistro, "registro": True})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('notas:index'))


def eventos_view(request):
    if request.user.is_authenticated:
        eventos = Evento.objects.all().filter(usuario_id=request.user.id)
        context = {'eventos': eventos}
        return render(request, 'index.html', context)


def eventos_crate(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EventoForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                nombre = cleaned_data.get('nombre')
                lugar = cleaned_data.get('lugar')
                direccion = cleaned_data.get('direccion')
                tipo = cleaned_data.get('tipo')
                categoria = cleaned_data.get('categoria')
                fecha_inicio = cleaned_data.get('fecha_inicio')
                fechafin = cleaned_data.get('fecha_terminacion')

                evento = Evento.objects.create(usuario=request.user, nombre=nombre, lugar=lugar,
                                               direccion=direccion, tipo=tipo,
                                               categoria=categoria,fecha_inicio=fecha_inicio,
                                               fecha_terminacion=fechafin)
                evento.save()
                messages.success(request, 'Se ha creado con éxito el evento',
                                 extra_tags='alert alert-success')
                return redirect(reverse('notas:index'))
        else:
            form = EventoForm()
        return render(request, 'evento_crear.html', {'form': form})

def evento_update(request,pk):
    if request.user.is_authenticated:
        evento = Evento.objects.get(id=pk)
        if request.method == 'POST':
            form = EventoForm(request.POST,instance=evento)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                evento.nombre = cleaned_data.get('nombre')
                evento.lugar = cleaned_data.get('lugar')
                evento.direccion = cleaned_data.get('direccion')
                evento.tipo = cleaned_data.get('tipo')
                evento.categoria = cleaned_data.get('categoria')
                evento.fecha_inicio = cleaned_data.get('fecha_inicio')
                evento.fecha_terminacion = cleaned_data.get('fecha_terminacion')
                evento.save()
                messages.success(request, 'Se ha actualizado con éxito el evento',
                                 extra_tags='alert alert-success')
                return redirect(reverse('notas:index'))
        else:

            form = EventoForm(instance=evento)
        return render(request, 'evento_actualizar.html', {'form': form})

def eliminar_evento(evento, request):
    evento.delete()
    messages.success(request, 'Se ha eliminado con éxito a ' + str(evento.nombre),
                     extra_tags='alert alert-success')
    return redirect(reverse('notas:index'))