from django.db import models
import django_filters
from django_filters import DateFilter, CharFilter

from .models import Appointment


class AppointmentFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="appointment_date", lookup_expr='gte')
    end_date = DateFilter(field_name="appointment_date", lookup_expr='lte')
    # note = CharFilter(field_name='note', lookup_expr='icontains')


    class Meta:
        model = Appointment
        fields = ['patient','clinic']
        # exclude = ['appointment_date','appointment_time','']
        


