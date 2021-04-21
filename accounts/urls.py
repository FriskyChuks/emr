from django.contrib import admin
from django.urls import path
from .views import registration_view, login_view, logout_view

urlpatterns = [
    path('accounts/registration/', registration_view, name='register'),
    path('', login_view, name='auth_login'),
    path('accounts/logout/', logout_view, name='auth_logout'),
]
