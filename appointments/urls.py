from django.urls import path

from .views import( schedule_appointment_view,
                    display_appointment_view,
                    appointment_search_view,
                    edit_appointment_view,
                    update_appointment_view,
                    AppointmentUpdateView
                )

urlpatterns = [
    path('schedule_appointment/<patient_id>/', schedule_appointment_view, name='schedule_appointment'),
    path('edit_appointment/<int:pk>/', edit_appointment_view, name='edit_appointment'),
    path('update_appointment/<int:pk>/', update_appointment_view, name='update_appointment'),
    path('display_appointment/', display_appointment_view, name='display_appointment'),
    path('search_appointment/', appointment_search_view, name='search_appointment'),
    path('<pk>/cbv_update_appointment/', AppointmentUpdateView.as_view(), name='cbv_update_appointment'),
]