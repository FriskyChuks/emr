import datetime
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory

from visits.models import PatientEncounter
from accounts.decorators import allowed_users

from .forms import RadiologyServiceForm, RaiseRadiologyServiceForm
from .models import RadiologyService, RadiologyRequest, RadiologyReport


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
                                                PatientEncounter, RadiologyRequest,
                                                fields=('radiology_service','unit','clinical_info'), 
                                                extra=5
                                            )
    encounter = PatientEncounter.objects.get(active=True, id=encounter_id) 
    formset = MedicalServiceFormSet(queryset=RadiologyRequest.objects.none(), instance=encounter)
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
        messages.success(request, "Radiology investigation request successful!.")
        return redirect("patient_folder", enc_id = encounter_id)

    template = "radiology/raise_radiology_service.html"
    context = {"formset":formset, "encounter":encounter}
    return render(request, template, context)


def desk_view(request):

    return render(request, 'radiology/desk.html',{})


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','radiology'])
def pending_radiology_request_view(request):
    patient_request = RadiologyRequest.objects.filter(done=False).values\
                ('patient', 'encounter_no').annotate(total=Count('id'))
    # patient_request = RadiologyRequest.objects.filter(date__gte=datetime.date.today()).distinct('-encounter_no')
  
    template = "radiology/pending_request.html"
    context = {"patient_request":patient_request}
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','radiology'])
def radiology_request_detail_view(request, enc_id):
    rad_request_detail = RadiologyRequest.objects.filter(encounter_no_id=enc_id, done=False, decline=False)  

    template = 'radiology/rad_request_detail.html'
    context = {"request_detail":rad_request_detail}
    return render(request, template, context)
    

@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['radiology', 'admin'])
def send_radiology_results_view(request, request_id):
    radiology_request = RadiologyRequest.objects.get(id=request_id)
    
    if request.method == 'POST':
        diagnosis = request.POST.get('diagnosis')
        findings = request.POST.get('findings')
        other_findings = request.POST.get('other_findings')

        RadiologyReport.objects.create(
            radiologyrequest_id=request_id,
            diagnosis=diagnosis,
            findings=findings,
            other_findings=other_findings
        )
        RadiologyRequest.objects.filter(id=request_id).update(done=True)
        messages.success(request, 'Report was sent successfully')
        return redirect('/radiology/pending_rad_request')
    
    template = "radiology/radiology_results.html"
    context = {"radiology_request":radiology_request}
    return render(request, template, context)

