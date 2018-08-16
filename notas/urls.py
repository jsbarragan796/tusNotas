from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.autenticacion, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^usuario_create/$', views.usuario_create, name='usuario_create'),
    url(r'^evento_create/$', views.eventos_crate, name='evento_create'),
    url(r'^evento_update/(?P<pk>\d+)$', views.evento_update, name='evento_update')
]
