from django.urls import path

from .views import(
    single_user_cash_reports_view,
    all_user_cash_reports_view,
    clinical_reports_view,receipt_detail_view,
    clinical_reports_home_view,
    reports_by_service_view,
    diagnosis_report_view,
    diagnosis_detail_report_view
)

urlpatterns = [
    path('clinical_reports_home/', clinical_reports_home_view, name='clinical_reports_home'),
    path('single_user_reports/', single_user_cash_reports_view, name='single_user_reports'),
    path('all_user_reports/', all_user_cash_reports_view, name='all_user_reports'),
    path('clinical_reports/', clinical_reports_view, name='clinical_reports'),
    path('reports_by_service/', reports_by_service_view, name='reports_by_service'),
    path('receipt_detail/<payment_id>/', receipt_detail_view, name='receipt_detail'),
    path('diagnosis_report/', diagnosis_report_view, name='diagnosis_report'),
    path('diagnosis_detail_report/<diagnosis_id>/', diagnosis_detail_report_view, name='diagnosis_detail_report'),
]