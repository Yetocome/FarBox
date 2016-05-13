from django.conf.urls import patterns, url, include
from FarboxWeb import views

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
]