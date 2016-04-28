from django.conf.urls import patterns, url, include
from account import views

urlpatterns = [
    url(r'^$', views.register, name='register'),
    url(r'^register/$', views.register, name='register'),
    url('^', include('django.contrib.auth.urls'))
]