from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^gps$', views.gps),
    url(r'^$', views.data),
]