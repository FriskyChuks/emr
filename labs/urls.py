from django.urls import path

from .views import lab_request_view, dispaly_request_view, request_detail_view

urlpatterns = [
    path("lab_request/<enc_id>/", lab_request_view, name="lab_request"),
    path("display_request/", dispaly_request_view, name="display_request"),  
     path("request_detail/<enc_id>", request_detail_view, name="request_detail"), 
]