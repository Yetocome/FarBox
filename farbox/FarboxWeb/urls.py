from django.conf.urls import patterns, url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^upload', views.upload, name='upload'),
    url(r'^home', views.home, name='home'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^download', views.download, name='download'),
    url(r'^delete_file', views.delete_file, name='delete_file'),
    url(r'^share_file', views.share_file, name='share_file'),
    url(r'^share_page', views.share_page, name='share_page'),
    url(r'^save_to_mine', views.save_to_mine, name='save_to_mine'),
]

