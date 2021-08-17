from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory

from visits.models import PatientEncounter
from accounts.decorators import allowed_users

from .forms import RadiologyServiceForm, RaiseRadiologyServiceForm
from .models import RadiologyService, RaiseRadiologyService


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin'])
def create_radiology_service_view(request):
    form = RadiologyServiceForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        form = RadiologyServiceForm()

    template = "radiology/create_radiology_service.html"
    context = {"form":form}
    return render(request, template, context)
    

@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin', 'doctor','radiology'])
def raise_patient_radiology_service_view(request, encounter_id):
    MedicalServiceFormSet = inlineformset_factory(
                                                PatientEncounter, RaiseRadiologyService,
                                                fields=('radiology_service','unit'), 
                                                extra=5
                                            )
    encounter = PatientEncounter.objects.get(active=True, id=encounter_id) 
    formset = MedicalServiceFormSet(queryset=RaiseRadiologyService.objects.none(), instance=encounter)
    # print(encounter.current_clinic.id)
    if request.method == "POST":
        formset = MedicalServiceFormSet(request.POST, instance=encounter)
        if formset.is_valid():
            # formset.save()
            instance = formset.save(commit=False) 
            for obj in instance:
                obj.patient_id = encounter.patient.id
                obj.created_by = request.user
                obj.save()
                formset = MedicalServiceFormSet()
        messages.success(request, "Lab investigation request successful!.")
        return redirect("patient_folder", enc_id = encounter_id)

    template = "radiology/raise_radiology_service.html"
    context = {"formset":formset, "encounter":encounter}
    return render(request, template, context)
