import datetime
from django.db.models import Q
from django.db.models.aggregates import Count
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

from visits.models import PatientEncounter, EncounterRoute
from accounts.models import User
from accounts.decorators import allowed_users

from .models import Patient#, NextOfKin, Address
from .forms import PatientBiodataForm, PatientImageForm#, FotoForm#, AddressForm, NextOfKinForm


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','doctor','nurse'])
def patient_folder_view(request, enc_id):
    current_encounter = PatientEncounter.objects.filter(id=enc_id, active=True).order_by("-id")
    
    template = "patients/patient_folder.html"
    context = {"current_encounter":current_encounter}
    return render (request, template, context)



@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','doctor','nurse'])
def patient_archives_view(request, patient_id):
    patient_ecounter = PatientEncounter.objects.filter(patient_id=patient_id).order_by("-id")
    
    template = "patients/archives.html" # Change this template with patient_folder_view
    context = {"patient_ecounter":patient_ecounter}
    return render (request, template, context)



@login_required(login_url="auth_login")
def search_patient_view(request):
	try:
		query = request.GET.get('q')
	except:
		query = None
	if query:
		# lookups = Q(title__icontains=query) | Q(description__icontains=query)
		# product = Product.objects.filter(lookups).distinct()
		patient = Patient.objects.search(query)
		context = {'query': query, 'patient': patient}
		template = 'patients/search_result.html'
	else:
		a = "Please enter a search parameter!"
		template = 'patients/search_result.html'
		context = {'query1': a}
	return render(request, template, context)



@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['HIM','admin','doctor','nurse','cashier'])
def patient_detail_view(request, id):
    patient = Patient.objects.filter(id=id, active=True)
    # print(patient)
    template = "patients/patient_info.html"
    context = {"patient":patient}
    return render(request, template, context)


def home(request):
    patients = Patient.objects.all()
    outpatient_count = PatientEncounter.objects.filter(current_clinic__isnull=False, active=True).count()
    inpatient_count = PatientEncounter.objects.filter(current_ward__isnull=False, active=True).count()
        # total_outpatients = patient.patientencounter_set.filter(current_clinic__isnull=False).count()
    patient_count = Patient.objects.filter(active=True).count()
    today_patient_count = Patient.objects.filter(active=True, date_created__gte=datetime.date.today()).count()
    today_outpatient_count = PatientEncounter.objects.filter(current_clinic__isnull=False, date_created__gte=datetime.date.today(), active=True).count()
    today_inpatient_count = EncounterRoute.objects.filter(ward__isnull=False, date_created__gte=datetime.date.today(), active=True).count()
    user_count = User.objects.filter(is_a_patient=False).count()
    gopd_encounter =  PatientEncounter.objects.filter(current_clinic=1, active=True).count()

    template = "home/dashboard.html"
    context = {
        "patients": patients, 
        "patient_count":patient_count,
        "user_count":user_count,
        "today_patient_count":today_patient_count,
        "gopd_encounter":gopd_encounter,
        "outpatient_count":outpatient_count,
        "inpatient_count":inpatient_count,
        "today_outpatient_count":today_outpatient_count,
        "today_inpatient_count":today_inpatient_count
        }
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','HIM'])
def patient_registration_form(request):
    form = PatientBiodataForm(request.POST or None)#, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        last_id = Patient.objects.last()
        pid = last_id.id
        foto = last_id.foto
        messages.success(request, "Your registration was successful, your PID is: "+str(pid))
        return render(request, 'patients/success.html', {"pid":pid})                    

    template = "patients/registration.html"
    context = {"form": form}



@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['HIM'])
def upload_patient_image_form(request, pid):
    patient_instance = Patient.objects.get(id=pid)
    pid = patient_instance.id
    form1 = PatientImageForm(instance=patient_instance) 
    if request.method == "POST":
        form1 = PatientImageForm(request.POST or None, request.FILES or None, instance=patient_instance)
        if form1.is_valid():
            form1.save()
            print("Uploaded Successfully")
            return redirect("patient_detail", id=pid)
        else:
            return redirect("patient_detail", id=pid)

    template = "patients/patient_foto.html"
    context = {"form": form1, "patient_instance":patient_instance}
    return render(request, template, context)