from django.urls import path

from .views import billing_home_view, pending_bills_view, load_wallet_view, clear_outstanding_bills_view

urlpatterns = [
    path('billing_home/', billing_home_view, name='billing_home'),
    path('pending_bills/<pid>/', pending_bills_view, name='pending_bills'),
    path('wallet/<pid>/', load_wallet_view, name='wallet'),
    path('outstanding_bills/<pid>/', clear_outstanding_bills_view, name='outstanding_bills'),
]