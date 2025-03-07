from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Clinic, Ward


def clinic_view(request):
    clinics = Clinic.objects.filter(active=True).order_by('clinic')
    tempplate = "location/clinic.html"
    context = {"clinics": clinics}

    return render(request, tempplate, context)


def ward_view(request):
    wards = Ward.objects.filter(active=True).order_by('ward')
    
    tempplate = "location/ward.html"
    context = {"wards": wards}

    return render(request, tempplate, context)


