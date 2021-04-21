from django.urls import path

from .views import pending_bills_view

urlpatterns = [
    path('pending_bills/<pid>/', pending_bills_view, name='pending_bills'),

]