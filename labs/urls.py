from django.urls import path

from .views import (
    lab_request_view, 
    request_list_view, 
    request_detail_view,
    send_lab_results_view,
)

urlpatterns = [
    path("lab_request/<enc_id>/", lab_request_view, name="lab_request"),
    path("request_list_view/", request_list_view, name="request_list_view"),  
    path("request_detail/<enc_id>/", request_detail_view, name="request_detail"),
    path("lab_results/<enc_id>/", send_lab_results_view, name="lab_results"),
]