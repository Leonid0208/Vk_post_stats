from django.contrib import admin
from django.urls import path, include
from .views import crate_wall, show_stat

urlpatterns = [
    path('', crate_wall, name='main'),
    path('stat', show_stat, name='stat'),
]