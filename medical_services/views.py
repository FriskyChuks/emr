from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import JsonResponse
from django.forms import inlineformset_factory

from visits.models import PatientEncounter

from accounts.decorators import allowed_users

from .forms import PatientEncounterServiceForm, MedicalServiceForm
from .models import MedicalService, PatientEncounterService



def search_medical_service_view(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText',"")

        items = MedicalService.objects.filter(medical_service__istartswith=search_str) | MedicalService.objects.filter(
                    type__icontains=search_str)

        data = items.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['doctor'])
def create_medical_service_view(request):
    form = MedicalServiceForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        form = MedicalServiceForm()

    template = "medical_services/create_service.html"
    context = {"form":form}
    return render(request, template, context)
    

@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','doctor', 'nurse'])
def raise_patient_medical_service_view(request, encounter_id):
    MedicalServiceFormSet = inlineformset_factory(
                                                PatientEncounter, PatientEncounterService,
                                                fields=('medical_service','unit'), 
                                                extra=5
                                            )
    encounter = PatientEncounter.objects.get(active=True, id=encounter_id)
    # print("id= ",encounter.patient.id) 
    formset = MedicalServiceFormSet(queryset=PatientEncounterService.objects.none(), instance=encounter)
    if request.method == "POST":
        formset = MedicalServiceFormSet(request.POST, instance=encounter)
        if formset.is_valid():
            instance = formset.save(commit=False) 
            for obj in instance:
                obj.patient_id = encounter.patient.id
                obj.created_by = request.user
                obj.save()
                formset = MedicalServiceFormSet()
        messages.success(request, "Lab investigation request successful!.")
        return redirect("patient_folder", enc_id = encounter_id)

    template = "medical_services/raise_patient_medical_service.html"
    context = {"formset":formset, "encounter":encounter}
    return render(request, template, context)
