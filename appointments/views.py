from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.urls.base import reverse_lazy

from patients.models import Patient

from .models import Appointment
from .filters import AppointmentFilter
from .forms import AppointmentForm, UpdateAppointmentForm


class AppointmentUpdateView(UpdateView):
    form_class = UpdateAppointmentForm
    model = Appointment
    template_name = "appointments/cbv_update_appointment.html"
    success_url = reverse_lazy('display_appointment')


@login_required(login_url="auth_login")
def schedule_appointment_view(request, patient_id):
    patient = Patient.objects.filter(id=patient_id, active=True)
    # appointments = Appointment.objects.all
    appointment = Appointment.objects.filter(patient_id=patient_id, active=True)

    form = AppointmentForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.patient_id = patient_id
        obj.created_by = request.user
        obj.save()
        form = AppointmentForm()

    template = "appointments/schedule_appointment.html"
    context = {"form": form,"patient":patient,"appointment":appointment,}
    return render(request, template, context)


@login_required(login_url="auth_login")
def edit_appointment_view(request, pk): 
    obj = Appointment.objects.get(id=pk)
    template = "appointments/update_appointment.html"
    context = {"obj": obj}
    return render(request, template, context)


@login_required(login_url="auth_login")
def update_appointment_view(request, pk): 
    update = Appointment.objects.get(id=pk)
    form = AppointmentForm(request.POST, instance=update)      
    if form.is_valid(): 
        form.save()
        return redirect("/")

    template = "appointments/update_appointment.html"
    context = {"obj":update}
    return render(request, template, context)


@login_required(login_url="auth_login")
def display_appointment_view(request):
    appointments = Appointment.objects.all

    myFilter = AppointmentFilter(request.GET, queryset=Appointment.objects.all())
    appointments = myFilter.qs

    template = "appointments/display_appointment.html"
    context = {"appointments":appointments, "myFilter":myFilter}
    return render(request, template, context)


def appointment_search_view(request):
    # return redirect ('/')
    template = "appointments/appointment_search.html"
    context = {}
    return render(request, template, context)

