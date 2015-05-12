from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.search, name='index'),
    url(r'^stats/$', views.stats, name='stats'),
    url(r'^view/([0-9]+)/', views.details, name='details'),
]