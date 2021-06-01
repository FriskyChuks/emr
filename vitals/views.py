from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from visits.models import PatientEncounter
from accounts.decorators import allowed_users

from .models import PatientVitalSigns, PatientNotes
from .forms import VitalSignsForm, PatientNotesForm

@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','doctor','nurse'])
def take_vital_signs_view(request, id):
    encounter = PatientEncounter.objects.get(id=id)
    p_encounter = PatientEncounter.objects.filter(id=id)
    print(encounter.id)
    current_encounter_vitals = PatientVitalSigns.objects.filter(patient_encounter=encounter.id).order_by('-date')
    # all_vitals_signs = PatientVitalSigns.objects.order_by('-date')
    
    form = VitalSignsForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.patient_encounter_id = encounter.id
        obj.created_by = request.user
        obj.save()
        form = VitalSignsForm()
    else:
        form = VitalSignsForm()

    template = "vitals/new_vitals.html"
    context = {
        "current_encounter_vitals":current_encounter_vitals, 
        #"all_vitals_signs": all_vitals_signs,
        "form":form,
        "p_encounter":p_encounter,
    }
    return render(request, template, context)



@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','doctor','nurse'])
def patient_notes_view(request, id):
    encounter = PatientEncounter.objects.get(id=id)
    p_encounter = PatientEncounter.objects.filter(id=id)
    print(encounter.id)
    current_encounter_notes = PatientNotes.objects.filter(patient_encounter=encounter.id).order_by('-date')
    all_notes = PatientNotes.objects.all
    
    form = PatientNotesForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.patient_encounter_id = encounter.id
        obj.created_by = request.user
        obj.save()
        form = PatientNotesForm()
    else:
        form = PatientNotesForm()

    template = "vitals/add_patient_notes.html"
    context = {
        "current_encounter_notes":current_encounter_notes, 
        "all_notes": all_notes,
        "form":form,
        "p_encounter":p_encounter,
    }
    return render(request, template, context)