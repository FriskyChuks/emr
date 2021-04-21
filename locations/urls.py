from django import urls
from django.urls import path

from .views import clinic_view, ward_view#, clinic_detail_view, ward_detail_view

urlpatterns = [
    path('clinic/', clinic_view, name='clinic_view'),
    # path('clinic_detail/<id>/', clinic_detail_view, name='clinic_detail_view'),
    path('ward/', ward_view, name='ward_view'),
    # path('ward_detail/<id>/', ward_detail_view, name='ward_detail_view'),
    
]