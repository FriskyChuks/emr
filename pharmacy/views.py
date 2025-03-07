import json
from operator import index
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.core import serializers

from visits.models import PatientEncounter
from accounts.decorators import allowed_users
from .forms import ItemForm, BrandForm
from .models import Item, Prescription, Brand, Dispensary
from bills.models import Bill


def search_drug_view(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText', "")

        items = Item.objects.filter(title__istartswith=search_str) | Item.objects.filter(
            type__icontains=search_str)

        data = items.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['store'])
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
@allowed_users(alllowed_roles=['store'])
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
@allowed_users(alllowed_roles=['admin', 'pharmacy'])
def view_prescription_view(request, pid):
    enc_id = (Prescription.objects.values('encounter_no').annotate(
        dcount=Count('encounter_no')).order_by('encounter_no').reverse())
    prescriptions = Prescription.objects.filter(patient=pid)

    template = "pharmacy/view_prescriptions.html"
    context = {"prescriptions": prescriptions, "enc_id": enc_id}
    return render(request, template, context)


@login_required(login_url="auth_login")
def dispense_prescription_view(request, encounter_id):
    prescriptions_by_encounter = Prescription.objects.filter(id=encounter_id)

    template = "pharmacy/view_prescriptions.html"
    context = {"prescriptions_by_encounter": prescriptions_by_encounter}
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin', 'doctor', 'nurse'])
def prescription_view(request, enc_id):
    # item = Item.objects.all
    brand = Brand.objects.all
    prescriptionFormSet = inlineformset_factory(
        PatientEncounter, Prescription, fields=(
            'item', 'route', 'qty_per_take', 'times_daily', 'no_of_days', 'note'
        ), extra=5
    )
    encounter = PatientEncounter.objects.get(active=True, id=enc_id)
    formset = prescriptionFormSet(
        queryset=Prescription.objects.none(), instance=encounter)
    if request.method == "POST":
        formset = prescriptionFormSet(request.POST, instance=encounter)
        if formset.is_valid():
            instance = formset.save(commit=False)
            for obj in instance:
                obj.patient_id = encounter.patient.id
                obj.created_by = request.user
                obj.save()
            messages.success(request, "Prescription was successful!.")
            return redirect("patient_folder", enc_id=enc_id)
        else:
            messages.error(
                request, "Kindly fill the form appropriately. Only note field is optional")

    template = "pharmacy/prescribe.html"
    # template = "pharmacy/prescription2.html"
    context = {"formset": formset, "encounter": encounter, "brand": brand}
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin', 'doctor', 'nurse'])
def prescription_view1(request, enc_id):
    prescribed = request.POST

    template = "pharmacy/prescription.html"
    context = {}
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['pharmacy'])
def dispensary_view(request, pid):
    prescription = Prescription.objects.filter(
        patient=pid, dispensed=False).order_by('-encounter_no')
    brands = Brand.objects.all()

    list_prescription = list(prescription.values())
    list_brands = list(brands.values())

    # template = "pharmacy/dispensary.html"
    template = "pharmacy/backup.html"
    context = {"prescription": prescription, "pid": pid, "brands": brands,
               "json_prescriptions": list_prescription, "json_brands": list_brands}
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['pharmacy'])
def submit_dispensery_view(request):
    if request.method == "POST":
        data = request.POST.get('data')
        # convert string to list
        list_data = json.loads(data)
        # extract dict in list and insert to db
        for dict_data in list_data:
            disp_obj = Dispensary.objects.create(prescription_id=dict_data['prescription_id'],
                                                 brand_id=dict_data['brand_id'], qty_dispensed=dict_data['quantity_dispensed'],
                                                 created_by_id=request.user.id)
            disp_obj.save()
            Prescription.objects.filter(
                id=dict_data['prescription_id']).update(dispensed=True)
            initial_stock = int(Brand.objects.get(
                id=dict_data['brand_id']).stock_level)
            Brand.objects.filter(id=dict_data['brand_id']).update(
                stock_level=initial_stock-int(dict_data['quantity_dispensed']))
        messages.success(request, "items dispensed successfully!")

        return JsonResponse({})
