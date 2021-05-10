import datetime
from django.db.models import Q
from django.db.models.aggregates import Count
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

from visits.models import PatientEncounter
from accounts.models import User

from .models import Patient#, NextOfKin, Address
from .forms import PatientBiodataForm, PatientImageForm#, FotoForm#, AddressForm, NextOfKinForm


@login_required(login_url="auth_login")
def patient_folder_view(request, patient_id):
    if not request.user.admin:
        messages.warning(request, "You do not have access to this page! thanks.")
        return HttpResponseRedirect('/')
    patient_ecounter = PatientEncounter.objects.filter(patient_id=patient_id).order_by("-id")
    current_encounter = Patient.objects.filter(id=patient_id)
    print(patient_ecounter)
    template = "patients/patient_folder.html"
    context = {"patient_ecounter":patient_ecounter, "current_encounter":current_encounter}
    return render (request, template, context)


@login_required(login_url="auth_login")
def current_patient_folder_view(request, id):
    current_patient_ecounter = PatientEncounter.objects.filter(id=id).order_by("-id")
    print(current_patient_ecounter)
    template = "patients/folder_body.html"
    context = {"current_patient_ecounter":current_patient_ecounter}
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
def patient_detail_view(request, id):
    if not request.user.admin:
        messages.warning(request, "You do not have access to this page! thanks.")
        return HttpResponseRedirect('/')
    patient = Patient.objects.filter(id=id, active=True)
    # print(patient)
    template = "patients/patient_info.html"
    context = {"patient":patient}
    return render(request, template, context)


def home(request):
    patients = Patient.objects.all
    patient_count = Patient.objects.filter(active=True).count()
    today_patient_count = Patient.objects.filter(active=True, date_created__gte=datetime.date.today()).count()
    user_count = User.objects.filter(is_a_patient=False).count()
    gopd_encounter =  PatientEncounter.objects.filter(current_clinic=1, active=True).count()

    template = "home.html"
    context = {
        "patients": patients, 
        "patient_count":patient_count,
        "user_count":user_count,
        "today_patient_count":today_patient_count,
        "gopd_encounter":gopd_encounter,
        }
    return render(request, template, context)


@login_required(login_url="auth_login")
def patient_registration_form(request):
    if not request.user.admin:
        messages.warning(request, "You do not have access to this page! thanks.")
        return HttpResponseRedirect('/')  
    form = PatientBiodataForm(request.POST or None)#, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        last_id = Patient.objects.last()
        id = last_id.id
        foto = last_id.foto
        messages.success(request, "PID: "+str(id))
        # messages.success(request, "PID is:"+str(last_id))
        return render(request, 'patients/success.html', {})
        # form_biodata = PatientBiodataForm() 
                     

    template = "patients/registration.html"
    context = {"form": form}
    return render(request, template, context)


# @login_required(login_url="auth_login")
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