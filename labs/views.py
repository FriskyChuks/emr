import datetime
from django.views.generic import ListView, TemplateView
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Count
from django.contrib import messages
import string

from patients.models import Patient
from visits.models import PatientEncounter

from accounts.decorators import allowed_users
from diagnosis.models import MakeDiagnosis

from .models import LabRequest, LabTest, LabUnit, LabResult
from .forms import LabResultForm, LabResultFormSet


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','doctor','MLS','lab_front_desk'])
def lab_request_view(request, enc_id):
    encounter = PatientEncounter.objects.get(id=enc_id, active=True)
    patient_id = encounter.patient_id

    immunolgy_tests = LabTest.objects.filter(lab_unit__title__icontains='immunology').order_by('-compound_test_id')
    parasitology_tests = LabTest.objects.filter(lab_unit__title__icontains='parasitology').order_by('-compound_test_id')
    bacteriology_tests = LabTest.objects.filter(lab_unit__title__icontains='bacteriology').order_by('-compound_test_id')
    chem_path_tests = LabTest.objects.filter(lab_unit__title__icontains="Chemical Pathology").order_by('-compound_test_id')
    hermatology_tests = LabTest.objects.filter(lab_unit__title__icontains="Hematology").order_by('-compound_test_id')
    BGS_tests = LabTest.objects.filter(lab_unit__title__icontains='Blood Group Serology').order_by('-compound_test_id')
    microbiology_tests = LabTest.objects.filter(lab_unit__title__icontains='Microbiology').order_by('-compound_test_id')

    if request.method == "POST":
        if request.POST.get("test_id"):
            selected_test = LabRequest()
            selected_test.test_id = request.POST.get("test_id")
            test_request = selected_test.test_id

            test_request = str(test_request)
            # convert Comma separated string to a python list
            request_list = test_request.split(",")

            for item in request_list:
                obj = LabRequest.objects.create(
                    encounter_id    = encounter.id,
                    # patient_id      = patient_id,
                    test_id         = item,
                    created_by      = request.user
                )
                obj.save()
        messages.success(request, "Lab investigation request successful!.")
        if request.user.group.name == 'MLS':
            return redirect("lab_request", enc_id = enc_id)
        else:
            return redirect("patient_folder", enc_id = enc_id)
        
    template = "labs/lab_request2.html"
    context = {
        "encounter":encounter,
        "immunolgy_tests":immunolgy_tests,"parasitology_tests":parasitology_tests,
        "bacteriology_tests":bacteriology_tests,"chem_path_tests":chem_path_tests,
        "hermatology_tests":hermatology_tests,"BGS_tests":BGS_tests,
        "microbiology_tests":microbiology_tests
    }
    return render(request, template, context)


# View for all Pending Request || CENTRAL LAB
@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','MLS','lab_front_desk'])
def request_list_view(request):
    # unique_request = LabRequest.objects.filter(done=False, date_created__gte=datetime.date.today()).distinct('encounter').order_by('-encounter')
    unique_request = LabRequest.objects.filter(done=False,date_created__gte=datetime.date.today()).values\
                ('encounter','encounter__patient','encounter__current_clinic__clinic','encounter__current_clinic__ward').annotate(\
                    total=Count('id'))

    template = 'labs/display_request.html'
    context = {"unique_request":unique_request}
    return render(request, template, context)



# Details of all Pending Request
@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','MLS'])
def request_detail_view(request, pid):
    request_detail = LabRequest.objects.filter(encounter_id__patient__id=pid, decline=False, done=False) 
    for r in request_detail:
        encounter_id = r.encounter.id
    diagnosis = MakeDiagnosis.objects.filter(encounter_id=encounter_id) 

    template = 'labs/request_detail.html'
    context = {"request_detail":request_detail, "diagnosis":diagnosis}
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['MLS'])
def send_lab_results_view(request, pid):
    lab_request = LabRequest.objects.filter(encounter_id__patient__id=pid, decline=False, done=False) 
    for r in lab_request:
        encounter_id = r.encounter.id
    diagnosis = MakeDiagnosis.objects.filter(encounter_id=encounter_id)
    
    result = request.POST
    result_trimmed = dict(result.lists())
    # del result_trimmed['csrfmiddlewaretoken']
    result_trimmed.pop('csrfmiddlewaretoken', None)

    for i, j in result_trimmed.items():
        # remove unwanted characters
        bad_chars = ['[', ']', "'"]
        # initializing test string
        cleaned_result = j 
        cleaned_result = ''.join((filter(lambda x: x not in bad_chars, cleaned_result)))
        print(i, cleaned_result) 
        if cleaned_result:
            lab_result = LabResult.objects.create(
                    lab_request_id = i,
                    result      = cleaned_result,
                    created_by  = request.user
                )
            lab_result.save()
            # Update LabResuest table and mark sent results as done
            LabRequest.objects.filter(id=i).update(done=True)
    # messages.success(request, "Result sent successfully!")

    template = "labs/lab_results.html"
    context = {"lab_request":lab_request, "diagnosis":diagnosis}
    return render(request, template, context)




