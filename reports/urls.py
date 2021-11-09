from django.urls import path

from .views import payment_reports_view, dashboard_with_pivot, pivot_data, single_patient_reports_view

urlpatterns = [
    path('payments/<user_id>/', payment_reports_view, name='payments'),
    path('single_payments/<pid>/', single_patient_reports_view, name='single_payments'),
    path('', dashboard_with_pivot, name='dashboard_with_pivot'),
    path('data', pivot_data, name='pivot_data'),
]