from django.urls import path

from .views import lab_request_view

urlpatterns = [
    path("lab_request/<enc_id>", lab_request_view, name="lab_request"), 
]