from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from . import views


urlpatterns = [
    path('home', views.Homepage, name='home'),
    path('signup', views.signup, name='signup'),
    path('', views.signin, name='signin'),
    path('logout', views.Logout, name='Logout'),
    path('edit', views.edit, name='edit'),
    path('search', views.search, name='search'),
    path('searchcn', views.searchcn, name='searchcn'),
    path('myprofile', views.myprofile, name='myprofile'),
    path('upload', views.upload, name='upload'),
    path('connections/<str:pk>', views.connections, name='connections'),
    path('mutuals/<str:pk>', views.mutuals, name='mutuals'),
    path('profile/<str:pk>', views.profile, name='profile'),

]
