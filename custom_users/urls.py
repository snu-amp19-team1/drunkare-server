from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^web$', views.web),
    url(r'^app$', views.app)
]