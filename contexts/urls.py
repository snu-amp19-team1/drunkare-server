from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^infer', views.infer),
    url(r'^user/$', views.demo),
]