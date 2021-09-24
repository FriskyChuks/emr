from django.shortcuts import redirect, render

from .models import MakeDiagosis, Diagnosis


def make_dianosis_view(request, enc_id):
    diagnosis = Diagnosis.objects.all()
    if request.method=="POST":
        diagnosis=request.POST.get('diagnosis')
        preliminary=request.POST.get('preliminary')
        if preliminary:
            final=False
        else:
           final=True 
        created_by=request.user

        MakeDiagosis.objects.create(
            encounter_id=enc_id,
            diagnosis_id=diagnosis,
            created_by=created_by,
            final=final        
        )
        return redirect("patient_folder", enc_id = enc_id)

    template = 'diagnosis/make_diagnosis.html'
    context = {"diagnosis":diagnosis}
    return render(request, template, context)
