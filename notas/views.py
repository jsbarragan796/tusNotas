# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from notas.forms import UserForm, EventoForm , loginForm
from django.contrib.auth.models import User
from notas.models import Evento
from django.contrib import messages
# Create your views here.

# Autenticación
def autenticacion(request):
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
    if request.user.is_authenticated():
        eventos = Evento.objects.all().filter(usuario_id=request.user.id)
        context = {'eventos': eventos}
        return render(request, 'index.html', context)


def index_view(request):
    if request.user.is_authenticated():
        return eventos_view(request)
    else:
        return login_view(request)