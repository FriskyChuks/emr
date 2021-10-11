from django.urls import path

from .views import payment_reports_view, dashboard_with_pivot, pivot_data

urlpatterns = [
    path('payments/<user_id>/', payment_reports_view, name='payments'),
    path('', dashboard_with_pivot, name='dashboard_with_pivot'),
    path('data', pivot_data, name='pivot_data'),
]