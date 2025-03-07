from django.shortcuts import redirect, render

from .models import MakeDiagnosis, Diagnosis


def make_dianosis_view(request, enc_id):
    diagnosis = Diagnosis.objects.all()
    user = request.user
    final = True
    if request.method == "POST":
        user_defined = request.POST.get('user_defined')
        _icd = request.POST.get('_icd')
        preliminary = request.POST.get('preliminary')
        if preliminary:
            final = False

        if user_defined:
            MakeDiagnosis.objects.create(encounter_id=enc_id, final=final,
                                         user_defined=user_defined, created_by=user)
            return redirect("patient_folder", enc_id=enc_id)

        elif _icd:
            print(_icd)
            MakeDiagnosis.objects.create(encounter_id=enc_id, final=final,
                                         icd_id=_icd, created_by=user)
            return redirect("patient_folder", enc_id=enc_id)

    template = 'diagnosis/make_diagnosis.html'
    context = {"diagnosis": diagnosis}
    return render(request, template, context)
