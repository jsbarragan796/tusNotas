from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.autenticacion, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^usuario_create/$', views.usuario_create, name='usuario_create'),
    # url(r'^herramienta_create/$', views.herramienta_create, name='herramienta_create'),
    # url(r'^herramienta_update/(?P<pk>\d+)$', views.herramienta_update, name='herramienta_update')
]
