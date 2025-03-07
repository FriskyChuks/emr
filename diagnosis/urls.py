from django.urls import path

from .views import make_dianosis_view

urlpatterns = [
    path('make_diagnosis/<enc_id>/', make_dianosis_view, name='make_diagnosis')
]