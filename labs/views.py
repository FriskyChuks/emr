from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages

from patients.models import Patient
from visits.models import PatientEncounter

from accounts.decorators import allowed_users

from .models import LabRequest, LabTest, LabUnit


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','doctor','MLS','lab_front_desk'])
def lab_request_view(request, enc_id):
    encounter = PatientEncounter.objects.get(id=enc_id, active=True)
    patient_id = encounter.patient_id
    microbiology_tests = LabTest.objects.filter(lab_unit=3)
    chem_path_tests = LabTest.objects.filter(lab_unit=2)
    hermatology_tests = LabTest.objects.filter(lab_unit=1)
    if request.method == "POST":
        if request.POST.get("test_id"):
            selected_test = LabRequest()
            selected_test.test_id = request.POST.get("test_id")
            test_request = selected_test.test_id
            l = len(test_request)
            t = type(test_request)

            if (l <= 2): 
                obj = LabRequest.objects.create(
                        encounter_id    = encounter.id,
                        patient_id      = patient_id,
                        test_id         = test_request,
                        created_by      = request.user
                    )
                obj.save()
            else:
            # Convert the string(test_request) to a tuple
                request_list = eval(test_request)
                for item in request_list:
                    obj = LabRequest.objects.create(
                        encounter_id    = encounter.id,
                        patient_id      = patient_id,
                        test_id         = item,
                        created_by      = request.user
                    )
                    obj.save()

            messages.success(request, "Lab investigation request successful!.")
            return redirect("patient_folder", patient_id = patient_id)
    else:
        template = "labs/lab_request2.html"
        context = {
            "encounter":encounter,
            "microbiology_tests":microbiology_tests,
            "chem_path_tests":chem_path_tests,
            "hermatology_tests":hermatology_tests
        }
        return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','MLS','lab_front_desk'])
def dispaly_request_view(request):
    lab_request = LabRequest.objects.values('encounter','patient').filter(decline=False, done=False).annotate(total=Count('id'))
    
    template = 'labs/display_request.html'
    context = {"lab_request":lab_request}
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','MLS'])
def request_detail_view(request, enc_id):
    request_detail = LabRequest.objects.filter(encounter_id=enc_id, decline=False, done=False)

    template = 'labs/request_detail.html'
    context = {"request_detail":request_detail}
    return render(request, template, context)

