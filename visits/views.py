from django import forms
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from patients.models import Patient
from medical_services.models import PatientEncounterService
from pharmacy.models import Prescription
from radiology.models import RaiseRadiologyService
from bills.models import Bill

from .models import PatientEncounter
from .forms import EncounterForm, DischargeForm, TransferForm


@login_required(login_url="auth_login")
def clinic_visits_display_view(request, id):
    qs = PatientEncounter.objects.filter(current_clinic=id, active=True)
    qs_ward = PatientEncounter.objects.filter(current_ward=id, active=True)
    bills = Bill.objects.all

    tempplate = "location/clinic_detail.html"
    context = {"qs": qs, "qs_ward":qs_ward, "bills":bills}

    return render(request, tempplate, context)


@login_required(login_url="auth_login")
def ward_visits_display_view(request, id):
    qs = PatientEncounter.objects.filter(current_ward=id, active=True)
    # qs_ward = PatientEncounter.objects.filter(current_ward=id, active=True)
    # User.objects.filter(Q(income__gte=5000) | Q(income__isnull=True))

    tempplate = "location/ward_detail.html"
    context = {"qs": qs}

    return render(request, tempplate, context)


@login_required(login_url="auth_login")
def create_new_encounter(request, patient_id):
    form = EncounterForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.patient_id = patient_id
        obj.created_by = request.user
        obj.save()
        Patient.objects.filter(id=patient_id).update(new=False) 
        form = EncounterForm()

    template = "visits/create_encounter.html"
    context = {"form":form}
    return render(request, template, context)


@login_required(login_url="auth_login")
def discharge_patient_view(request, id):
    qs = PatientEncounter.objects.filter(id=id)
    for q in qs:
        clinic_id = q.current_clinic_id
        ward_id = q.current_ward_id
        print(clinic_id)

    form = DischargeForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.encounter_no_id = id
        obj.created_by = request.user
        obj.save()
        if clinic_id:
            return redirect("clinic_visits_display", id = clinic_id)
        else:
            return redirect("ward_admission_display", id = ward_id)

    template = "visits/discharge_patient.html"
    context = {"form":form, "qs":qs}
    return render(request, template, context)


@login_required(login_url="auth_login")
def transfer_patient_view(request, id):
    qs = PatientEncounter.objects.filter(id=id)
    for q in qs:
        clinic_id = q.current_clinic_id
        ward_id = q.current_ward_id

    form = TransferForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.encounter_no_id = id
        obj.created_by = request.user
        obj.save()
        if clinic_id:
            return redirect("clinic_visits_display", id = clinic_id)
        else:
            return redirect("ward_admission_display", id = ward_id)

    template = "visits/transfer_patient.html"
    context = {"form":form, "clinic_id":clinic_id, "qs":qs}
    return render(request, template, context)



