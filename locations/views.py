from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Clinic, Ward


def clinic_view(request):
    clinics = Clinic.objects.filter(active=True).order_by('clinic')
    tempplate = "location/clinic.html"
    context = {"clinics": clinics}

    return render(request, tempplate, context)


# @login_required(login_url="auth_login")
# def clinic_detail_view(request, id):
#     clinics = Clinic.objects.filter(id=id)
#     for c in clinics:
#         print(c.id)
    
#     tempplate = "location/clinic_detail.html"
#     context = {"clinics": clinics}

#     return render(request, tempplate, context)


def ward_view(request):
    wards = Ward.objects.filter(active=True).order_by('ward')
    
    tempplate = "location/ward.html"
    context = {"wards": wards}

    return render(request, tempplate, context)


# @login_required(login_url="auth_login")
# def ward_detail_view(request, id):
#     ward = Ward.objects.filter(id=id)
    
#     tempplate = "location/ward_detail.html"
#     context = {"ward": ward}

#     return render(request, tempplate, context)


