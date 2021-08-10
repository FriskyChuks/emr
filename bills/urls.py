from django.urls import path

from .views import pending_bills_view, load_wallet_view, clear_outstanding_bills_view

urlpatterns = [
    path('pending_bills/<pid>/', pending_bills_view, name='pending_bills'),
    path('wallet/<pid>/', load_wallet_view, name='wallet'),
    path('outstanding_bills/<pid>/', clear_outstanding_bills_view, name='outstanding_bills'),
]