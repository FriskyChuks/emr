from django.urls.base import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic import ListView
import datetime
from django.db.models import Q
from django.db.models.aggregates import Count
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from visits.models import *
from accounts.models import *
from diagnosis.models import MakeDiagnosis
from accounts.decorators import allowed_users

from .models import *
from .forms import PatientImageForm, UpdatePatientForm
import json


def home(request):
    patients = Patient.objects.all()
    outpatient_count = PatientEncounter.objects.filter(
        current_clinic__isnull=False, active=True).count()
    inpatient_count = PatientEncounter.objects.filter(
        current_ward__isnull=False, active=True).count()
    patient_count = Patient.objects.filter(active=True).count()
    today_patient_count = Patient.objects.filter(
        active=True, date_created__gte=datetime.date.today()).count()
    today_outpatient_count = EncounterRoute.objects.filter(
        clinic__isnull=False, date_created__gte=datetime.date.today(), active=True).count()
    today_inpatient_count = EncounterRoute.objects.filter(
        ward__isnull=False, date_created__gte=datetime.date.today(), active=True).count()
    # user_count = User.objects.filter(is_a_patient=False).count()

    template = "home/dashboard.html"
    context = {
        "patients": patients,
        "patient_count": patient_count,
        # "user_count": user_count,
        "today_patient_count": today_patient_count,
        # "today_encounters":today_encounters,
        "outpatient_count": outpatient_count,
        "inpatient_count": inpatient_count,
        "today_outpatient_count": today_outpatient_count,
        "today_inpatient_count": today_inpatient_count,
        # "today_encounters":today_encounters
    }
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin', 'doctor', 'nurse'])
def patient_folder_view(request, enc_id):
    current_encounter = PatientEncounter.objects.filter(
        id=enc_id, active=True).order_by("-id")
    encounter = PatientEncounter.objects.get(id=enc_id)
    diagnosis = MakeDiagnosis.objects.filter(encounter=enc_id).order_by('-id')

    template = "patients/patient_folder.html"
    context = {"current_encounter": current_encounter,
               "encounter": encounter, "diagnosis": diagnosis}
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin', 'doctor', 'nurse'])
def patient_archives_view(request, patient_id):
    patient_ecounter = PatientEncounter.objects.filter(
        patient_id=patient_id).order_by("-id")

    # Change this template with patient_folder_view
    template = "patients/archives.html"
    context = {"patient_ecounter": patient_ecounter}
    return render(request, template, context)


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
@allowed_users(alllowed_roles=['HIM', 'admin', 'doctor', 'nurse', 'cashier'])
def patient_detail_view(request, id):
    patient = Patient.objects.filter(id=id, active=True)

    template = "patients/patient_info.html"
    context = {"patient": patient}
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin', 'HIM'])
def patient_registration_view(request):
    countries = list(Country.objects.filter(active=True).values())
    states = list(State.objects.all().values())
    lgas = list(LGA.objects.all().values())
    relationships = Relationship.objects.all()

    if request.method == 'POST':
        obj = Patient.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            other_names=request.POST.get('other_names'),
            gender=request.POST.get('gender'),
            date_of_birth=request.POST.get('date_of_birth'),
            marital_status=request.POST.get('marital_status'),
            phone_1=request.POST.get('phone_1'),
            # phone_2=request.POST.get('phone_2'),
            country_id=request.POST.get('country'),
            state_id=request.POST.get('state'),
            l_g_a_id=request.POST.get('l_g_a'),
            address=request.POST.get('address'),
            next_of_kin_relationship_id=request.POST.get('next_of_kin_rel'),
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            next_of_kin_address=request.POST.get('next_of_kin_addr')
        )
        obj.save()
        messages.success(request, "Your registration was successful")
        return render(request, 'patients/success.html', {'obj': obj})

    json_states = json.dumps(states)
    json_countries = json.dumps(countries)
    context = {'countries': countries, 'states': states, "json_countries": json_countries,
               'lgas': lgas, 'json_states': json_states, "relationships": relationships}
    return render(request, 'patients/registration.html', context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['HIM'])
def upload_patient_image_form(request, pid):
    patient_instance = Patient.objects.get(id=pid)
    pid = patient_instance.id
    form1 = PatientImageForm(instance=patient_instance)
    if request.method == "POST":
        form1 = PatientImageForm(
            request.POST or None, request.FILES or None, instance=patient_instance)
        if form1.is_valid():
            form1.save()
            print("Uploaded Successfully")
            return redirect("patient_detail", id=pid)
        else:
            return redirect("patient_detail", id=pid)

    template = "patients/patient_foto.html"
    context = {"form": form1, "patient_instance": patient_instance}
    return render(request, template, context)


class PatientListView(ListView):
    model = Patient
    paginate_by = 50
    ordering = ['id']


class UpdatePatientView(SuccessMessageMixin, UpdateView):
    form_class = UpdatePatientForm
    model = Patient
    template_name = "patients/cbv_update_patient.html"
    success_message = 'Patient record updated successfully!'
    success_url = reverse_lazy('home')
