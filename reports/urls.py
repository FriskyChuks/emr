from django.urls import path

from .views import *

urlpatterns = [
    path('reports_home_view/', reports_home_view,
         name='reports_home'),
    path('general_financial_reports_view/',
         general_financial_reports_view, name='general_financial_reports'),
    path('patient_visit_report/', patient_visit_report_view,
         name='patient_visit_report'),
    path('reports_by_service/', reports_by_service_view, name='reports_by_service'),
    path('receipt_detail/<payment_id>/',
         receipt_detail_view, name='receipt_detail'),
    path('diagnosis_report/', diagnosis_report_view, name='diagnosis_report'),
    path('diagnosis_detail_report/<diagnosis_id>/',
         diagnosis_detail_report_view, name='diagnosis_detail_report'),
    path('cashiers_reports/', cashiers_reports_view, name='cashiers_reports'),
]
