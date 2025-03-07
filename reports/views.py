import random
import datetime
from django.utils import timezone
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q, Count, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import User
from accounts.decorators import allowed_users
from labs.models import LabRequest
from bills.models import Bill, Payment, PaymentDetail
from diagnosis.models import Diagnosis, MakeDiagnosis
from locations.models import Clinic, Ward
from visits.models import PatientEncounter


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin', 'cashier'])
def reports_home_view(request):
    data, labels, colors = [], [], []
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if date_to:
        date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d")
        date_to = date_to + datetime.timedelta(days=1)

    payment = Payment.objects.filter(
        date_created__date=timezone.now()).values('created_by__first_name', 'created_by__last_name').annotate(
            total=Sum('amount_paid')).order_by()
    filters = {'date_created__lte': date_to if date_to else timezone.now(),
               'date_created__gte': date_from if date_from else timezone.now()}
    if filters:
        payment = Payment.objects.filter(**filters).values('created_by__first_name', 'created_by__last_name').annotate(
            total=Sum('amount_paid')).order_by()
    for i in payment:
        labels.append((i['created_by__first_name'] +
                      " " + (i['created_by__last_name'])))
        data.append(int(i['total']))
    # generate random colors
    for i in range(len(data)):
        colors.append(random.randint(0, 255))
    colors = ['#' + str(i) for i in colors]
    total = '%.2f' % float(sum(data))
    if date_to:
        date_to = date_to - datetime.timedelta(days=1)

    context = {"date_to": date_to, "date_from": date_from, "pay": payment, 'data': data,
               'labels': labels, 'colors': colors, 'total': total}

    return render(request, 'reports/reports_home.html', context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin', 'cashier'])
def cashiers_reports_view(request):
    data, labels, colors = [], [], []
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if date_to:
        date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d")
        date_to = date_to + datetime.timedelta(days=1)

    payment = Payment.objects.filter(
        date_created__date=timezone.now()).values('created_by__first_name', 'created_by__last_name').annotate(
            total=Sum('amount_paid')).order_by()
    filters = {'date_created__lte': date_to if date_to else timezone.now(),
               'date_created__gte': date_from if date_from else timezone.now()}
    if filters:
        payment = Payment.objects.filter(**filters).values('created_by__first_name', 'created_by__last_name').annotate(
            total=Sum('amount_paid')).order_by()
    for i in payment:
        labels.append((i['created_by__first_name'] +
                      " " + (i['created_by__last_name'])))
        data.append(int(i['total']))
    # generate random colors
    for i in range(len(data)):
        colors.append(random.randint(0, 255))
    colors = ['#' + str(i) for i in colors]
    total = '%.2f' % float(sum(data))
    if date_to:
        date_to = date_to - datetime.timedelta(days=1)

    context = {"date_to": date_to, "date_from": date_from, "pay": payment, 'data': data,
               'labels': labels, 'colors': colors, 'total': total}

    return render(request, 'reports/cashiers_reports.html', context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin', 'cashier'])
def general_financial_reports_view(request):
    cash_officers = User.objects.filter(group__name__iexact='cashier')

    pid_exact = request.GET.get('pid_exact')
    transaction_type = request.GET.get('transaction_type')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    get_date_from = request.GET.get('date_from')
    get_date_to = request.GET.get('date_to')
    cashier = request.GET.get('cashier')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if date_to:
        date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d")
        date_to = date_to + datetime.timedelta(days=1)

    payment = Payment.objects.filter(
        date_created__date=timezone.now(), created_by__id=request.user.id)

    filters = {'patient': pid_exact, 'date_created__lte': date_to,
               'action': transaction_type, 'created_by__id': cashier,
               'amount_paid__lte': max_amount, 'amount_paid__gte': min_amount,
               'date_created__gte': date_from if date_from else timezone.now(),
               }

    filters = {k: v for k, v in filters.items() if v}
    if filters:
        payment = Payment.objects.filter(**filters)

    sum_total = 0.00
    for p in payment:
        total = float(p.amount_paid)
        sum_total += total

    paginator = Paginator(payment, 10000)  # Show 100 contacts per page.
    # getting the desired page number from url
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj, "cash_officers": cash_officers, "sum_total": sum_total,
        "date_from": get_date_from, "date_to": get_date_to, "pay": payment
    }
    return render(request, 'reports/general_financial_reports.html', context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin', 'cashier'])
def reports_by_service_view(request):
    data, labels = [], []
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_to:
        date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d")
        date_to = date_to + datetime.timedelta(days=1)

    bills = Bill.objects.all()
    filters = {'date_created__gte': date_from if date_from else timezone.now(),
               'date_created__lte': date_to}
    filters = {k: v for k, v in filters.items() if v}
    if filters:
        bills = Bill.objects.filter(**filters)

        lab_services = bills.filter(lab_request__isnull=False)
        med_services = bills.filter(medical_service__isnull=False)
        pharm_services = bills.filter(dispensary__isnull=False)
        rad_services = bills.filter(radiology_service__isnull=False)

        lab_count = lab_services.count()
        med_service_count = med_services.count()
        pharm_count = pharm_services.count()
        rad_count = rad_services.count()
        data.extend([lab_count, med_service_count, pharm_count, rad_count])
        labels.extend(['Lab', 'Med. Services', 'Pharmacy', 'Radiology'])

    if date_to:
        date_to = date_to - datetime.timedelta(days=1)
    context = {
        "lab_count": lab_count, "med_service_count": med_service_count,
        "rad_count": rad_count, "pharm_count": pharm_count,
        "date_from": date_from, "date_to": date_to, 'data': data, 'labels': labels}

    return render(request, 'reports/reports_by_service.html', context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin'])
def patient_visit_report_view(request):
    encounters = PatientEncounter.objects.all()
    clinics = Clinic.objects.all()
    wards = Ward.objects.all()

    clinic_ward = request.GET.get('clinic_ward')
    clinic = request.GET.get('clinic')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    # if date_to:
    #     date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d")
    #     date_to = date_to + datetime.timedelta(days=1)

    filters = {'date_created__gte': date_from if date_from else timezone.now(),
               'date_created__lte': date_to, 'current_clinic': clinic,
               'current_clinic__isnull': True}
    filters = {k: v for k, v in filters.items() if v}
    if filters:
        encounters = PatientEncounter.objects.filter(**filters)
    for e in encounters:
        print(e)
    context = {'encounters': encounters, 'clinics': clinics, 'wards': wards}
    return render(request, 'reports/patient_visits.html', context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin', 'cashier'])
def receipt_detail_view(request, payment_id):
    payment_detail = PaymentDetail.objects.filter(payment_id=payment_id)

    return render(request, 'reports/receipt_details.html', {"payment_detail": payment_detail})


# DIAGNOSIS
def diagnosis_report_view(request):
    diagnosis = MakeDiagnosis.objects.values('diagnosis__id', 'diagnosis__title').annotate(
        Count('diagnosis')).filter(date_created__gte=datetime.date.today())

    get_date_from = request.GET.get('date_from')
    get_date_to = request.GET.get('date_to')
    search_variable = request.GET.get('diagnosis_contains')

    date_to = None
    date_from = None
    if get_date_from and get_date_to:
        date_to = datetime.datetime.strptime(get_date_to, "%Y-%m-%d")
        date_to = date_to + datetime.timedelta(days=1)
        date_from = datetime.datetime.strptime(get_date_from, "%Y-%m-%d")
    elif date_from and date_to:
        diagnosis = MakeDiagnosis.objects.values('diagnosis__id', 'diagnosis__title').annotate(
            Count('diagnosis')).filter(date_created__range=[date_from, date_to])

    if search_variable:
        diagnosis = MakeDiagnosis.objects.values('diagnosis__id', 'diagnosis__title').annotate(
            Count('diagnosis')).filter(diagnosis__title__icontains=search_variable, date_created__range=[date_from, date_to])

    paginator = Paginator(diagnosis, 25)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reports/diagnosis.html', {'page_obj': page_obj})


def diagnosis_detail_report_view(request, diagnosis_id):
    diagnosis = MakeDiagnosis.objects.filter(diagnosis_id=diagnosis_id)
    clinics = Clinic.objects.all()
    wards = Ward.objects.all()
    users = User.objects.all()

    select_clinic = request.GET.get('select_clinic')
    select_ward = request.GET.get('select_ward')
    get_date_from = request.GET.get('date_from')
    get_date_to = request.GET.get('date_to')

    date_to = None
    date_from = None
    if get_date_from and get_date_to:
        date_to = datetime.datetime.strptime(get_date_to, "%Y-%m-%d")
        date_to = date_to + datetime.timedelta(days=1)
        date_from = datetime.datetime.strptime(get_date_from, "%Y-%m-%d")

    if select_ward:
        if not date_from or not date_to:
            messages.error(request, 'Please enter "Transaction dates"')
            return redirect('diagnosis_detail_report', diagnosis_id=diagnosis_id)
        else:
            diagnosis = MakeDiagnosis.objects.filter(diagnosis_id=diagnosis_id,
                                                     encounter__current_ward__id=select_ward, date_created__range=[date_from, date_to])
    elif select_clinic:
        if not date_from or not date_to:
            messages.error(request, 'Please enter "Transaction dates"')
            return redirect('diagnosis_detail_report', diagnosis_id=diagnosis_id)
        else:
            diagnosis = MakeDiagnosis.objects.filter(
                diagnosis_id=diagnosis_id, encounter__current_clinic__id=select_clinic,
                date_created__range=[date_from, date_to])

    paginator = Paginator(diagnosis, 25)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, "clinics": clinics,
               "wards": wards, "users": users}
    return render(request, 'reports/diagnosis_details.html', context)
