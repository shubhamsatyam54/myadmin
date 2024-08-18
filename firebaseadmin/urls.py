"""
URL configuration for myadmin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from firebaseadmin import views
from firebaseadmin.views import get_vehicles

urlpatterns = [
    path('', views.home, name='home'),  # Home page or dashboard
    path('create-account/', views.create_account, name='create_account'),
    path('add-vehicle/', views.add_vehicle, name='add_vehicle'),
    path('change-subscription/', views.change_subscription, name='change_subscription'),
    path('change-password/', views.change_password, name='change_password'),
path('get_vehicles/', get_vehicles, name='get_vehicles'),

]
