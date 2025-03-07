from django import forms
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from patients.models import Patient
from medical_services.models import PatientEncounterService
from pharmacy.models import Prescription
from radiology.models import RadiologyRequest
from bills.models import Bill
from accounts.decorators import allowed_users
from locations.models import Clinic, Ward

from .models import PatientEncounter, EncounterRoute
from .forms import DischargeForm


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','doctor','nurse','HIM'])
def clinic_visits_display_view(request, id):
    qs = PatientEncounter.objects.filter(current_clinic=id, active=True)
    qs_ward = PatientEncounter.objects.filter(current_ward=id, active=True)
    bills = Bill.objects.all

    tempplate = "location/clinic_detail.html"
    context = {"qs": qs, "qs_ward":qs_ward, "bills":bills}

    return render(request, tempplate, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','doctor','nurse','HIM'])
def ward_visits_display_view(request, id):
    qs = PatientEncounter.objects.filter(current_ward=id, active=True)

    tempplate = "location/ward_detail.html"
    context = {"qs": qs}

    return render(request, tempplate, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','HIM'])
def create_new_encounter(request, patient_id):
    qs = Patient.objects.get(id=patient_id)
    clinics = Clinic.objects.all
    wards = Ward.objects.all

    if request.method=='POST':
        clinic = request.POST.get('clinic')
        ward = request.POST.get('ward')
        if not clinic and not ward:
            messages.error(request, 'Please select a location!')
            return redirect('create_new_encounter',patient_id=patient_id)
        else:
            PatientEncounter.objects.create(
                    patient_id=patient_id,
                    current_clinic_id=clinic,
                    current_ward_id=ward,
                    created_by= request.user
                )   
            Patient.objects.filter(id=patient_id).update(new=False) 
            messages.success(request, "Transfer successful!")
            return redirect("/patients/patient_registration")

    template = "visits/create_encounter.html"
    context = {"qs":qs, "clinics":clinics,"wards":wards}
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','doctor','nurse'])
def transfer_patient_view(request, id):
    clinics = Clinic.objects.all
    wards = Ward.objects.all
    qs = PatientEncounter.objects.get(id=id)
    clinic_id = qs.current_clinic_id
    ward_id = qs.current_ward_id

    if request.method=='POST':
        clinic = request.POST.get('clinic')
        ward = request.POST.get('ward')
        EncounterRoute.objects.create(
                encounter_no_id=id,
                clinic_id=clinic,
                ward_id=ward,
                created_by=request.user
            )
        if clinic_id:
            return redirect("clinic_visits_display", id = clinic_id)
        else:
            return redirect("ward_admission_display", id = ward_id)

    template = "visits/transfer_patient.html"
    context = {"clinic_id":clinic_id, "qs":qs, "clinics":clinics, "wards":wards, }
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','nurse'])
def discharge_patient_view(request, id):
    qs = PatientEncounter.objects.filter(id=id)
    for q in qs:
        clinic_id = q.current_clinic_id
        ward_id = q.current_ward_id

    form = DischargeForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.encounter_no_id = id
        obj.created_by = request.user
        obj.save()
        PatientEncounter.objects.filter(id=id, active=True).update(active=False)
        if clinic_id:
            return redirect("clinic_visits_display", id = clinic_id)
        else:
            return redirect("ward_admission_display", id = ward_id)

    template = "visits/discharge_patient.html"
    context = {"form":form, "qs":qs}
    return render(request, template, context)



