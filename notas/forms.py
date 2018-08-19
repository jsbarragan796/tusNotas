# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.contrib.auth.forms import forms
from django.contrib.auth.models import User
from notas.models import Evento
from django.forms import widgets
from django.contrib.auth import password_validation


class UserForm(ModelForm):
    username = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput())
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirmación de contraseña", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    # verificacion correo unico
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Correo ya ha sido registrado')
        return username

    # verificacion las contraseñas coinciden y seguridad
    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Contraseñas no coinciden')
        try:
            password_validation.validate_password(password2)
        except password_validation.ValidationError as errores:
            mensajes = []
            for m in errores.messages:
                if m == 'This password is too short. It must contain at least 8 characters.':
                    mensajes.append('Contraseña muy corta, debe contener más de 7 caracteres')
                if m == 'This password is too common.':
                    mensajes.append('Contraseña muy común')
                if m == 'This password is entirely numeric.':
                    mensajes.append('Contraseña no puede contener solo números')
                if m.startswith("The password is too similar"):
                    mensajes.append('Contraseña muy similar a los datos del usuario')
            raise forms.ValidationError(mensajes)
        return password2

class loginForm(ModelForm):
    usernameL = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput())
    passwordL = forms.CharField(label="Contraseña", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['usernameL', 'passwordL']

class EventoForm(ModelForm):
    nombre = forms.CharField(max_length=100)
    lugar = forms.CharField(max_length=500)
    direccion = forms.CharField(max_length=500)

    fecha_inicio = forms.DateField(widget=widgets.SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ))
    fecha_terminacion =forms.DateField(widget=widgets.SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ))
    CATEGORIA_CHOICES = (
        (1, 'Conferencia'),
        (2, 'Seminario'),
        (3, 'Congreso'),
        (4, 'Curso')
    )
    categoria = forms.ChoiceField(label="Sistema Operativo",
                              choices=CATEGORIA_CHOICES)

    TIPO_CHOICES = (
        (1, 'Virtual'),
        (2, 'Presencial')
    )
    tipo = forms.ChoiceField(label="Tipo Evento", choices=TIPO_CHOICES)

    class Meta:
        model = Evento
        fields = ['nombre', 'lugar', 'direccion', 'fecha_inicio', 'fecha_terminacion', 'categoria','tipo']
