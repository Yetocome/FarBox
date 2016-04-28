from django.conf.urls import patterns, url, include
from account import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
]