# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from notas.forms import UserForm, EventoForm
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

# Autenticación
def login_view(request):
    if request.user.is_authenticated():
        return redirect(reverse('catalogo:index'))
    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('catalogo:index'))
        else:
            mensaje = 'Nombre de usuario o clave no valida'
    return render(request, 'login.html', {'mensaje': mensaje})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('catalogo:index'))


def usuario_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')

            user_model = User.objects.create_user(username=username, password=password)
            user_model.save()

            return HttpResponseRedirect(reverse('catalogo:users_list'))
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})


