from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import json
from django.http import JsonResponse
from django.forms import inlineformset_factory

from visits.models import PatientEncounter
from patients.models import Patient

from .forms import ItemForm, BrandForm, PrescriptionForm
from .models import Item, Prescription


def search_drug_view(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText',"")

        items = Item.objects.filter(title__istartswith=search_str) | Item.objects.filter(
                    type__icontains=search_str)

        data = items.values()
        return JsonResponse(list(data), safe=False)




@login_required(login_url="auth_login")
def create_item_view(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        form = ItemForm()

    template = "pharmacy/create_item.html"
    context = {"form": form}
    return render(request, template, context)


@login_required(login_url="auth_login")
def create_brand_view(request):
    form = BrandForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        form = BrandForm()

    template = "pharmacy/create_brand.html"
    context = {"form": form}
    return render(request, template, context)


@login_required(login_url="auth_login")
def view_prescription_view(request, pid):
    enc_id = (Prescription.objects.values('encounter_no').annotate(dcount=Count('encounter_no')).order_by('encounter_no').reverse())
    prescriptions = Prescription.objects.filter(patient=pid)
    
    template = "pharmacy/view_prescriptions.html"
    context = {"prescriptions": prescriptions, "enc_id":enc_id}
    return render(request, template, context)

@login_required(login_url="auth_login")
def dispense_prescription_view(request, encounter_id):
    prescriptions_by_encounter = Prescription.objects.filter(id=encounter_id)
    
    template = "pharmacy/view_prescriptions.html"
    context = {"prescriptions_by_encounter": prescriptions_by_encounter}
    return render(request, template, context)


@login_required(login_url="auth_login")
def prescription_view(request, encounter_id):
    item = Item.objects.all
    prescriptionFormSet = inlineformset_factory(
                                PatientEncounter, Prescription, fields=(
                                    'item', 'route','qty_per_take','times_daily','no_of_days'
                                    ), extra=5
                                )
    encounter = PatientEncounter.objects.get(active=True, id=encounter_id)
    formset = prescriptionFormSet(queryset=Prescription.objects.none(), instance=encounter)
    if request.method == "POST":
        formset = prescriptionFormSet(request.POST, instance=encounter)
        if formset.is_valid():
            # formset.save()
            instance = formset.save(commit=False) 
            for obj in instance:
                obj.patient_id = encounter.patient.id
                obj.created_by = request.user
                obj.save()
                formset = prescriptionFormSet()

    template = "pharmacy/prescribe.html"
    context = {"formset":formset, "encounter":encounter, "item":item}
    return render(request, template,context)