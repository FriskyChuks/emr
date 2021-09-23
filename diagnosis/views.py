from django.shortcuts import redirect, render

from .models import MakeDiagosis, Diagnosis, DiagnosisType


def make_dianosis_view(request, enc_id):
    diagnosis = Diagnosis.objects.all()
    type = DiagnosisType.objects.all()
    if request.method=="POST":
        diagnosis=request.POST.get('diagnosis')
        type=request.POST.get('type')
        created_by=request.user

        MakeDiagosis.objects.create(
            encounter_id=enc_id,
            diagnosis_id=diagnosis,
            type_id=type,
            created_by=created_by
        )
        return redirect("patient_folder", enc_id = enc_id)

    template = 'diagnosis/make_diagnosis.html'
    context = {"diagnosis":diagnosis, "type":type}
    return render(request, template, context)
