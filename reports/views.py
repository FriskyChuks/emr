import datetime
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import User
from accounts.decorators import allowed_users
from labs.models import LabRequest
from bills.models import Bill, Payment, PaymentDetail
from diagnosis.models import Diagnosis, MakeDiagnosis
from locations.models import Clinic, Ward


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','cashier'])
def single_user_cash_reports_view(request):
    user_id = request.user.id
    payment = PaymentDetail.objects.values(
        'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(created_by=user_id, date_created__gte=datetime.date.today())

    cash_officers = User.objects.filter(group__name__iexact='cashier')

    # service_contains = request.GET.get('service_contains')
    pid_exact = request.GET.get('pid_exact')
    transaction_type = request.GET.get('transaction_type')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    get_date_from = request.GET.get('date_from')
    get_date_to = request.GET.get('date_to')
    cashier = request.GET.get('cashier')
    date_to=None
    date_from=None
    if get_date_to and get_date_from:
        date_to = datetime.datetime.strptime(get_date_to, "%Y-%m-%d")
        date_to = date_to + datetime.timedelta(days=1)
        date_from = datetime.datetime.strptime(get_date_from, "%Y-%m-%d")
    
    if is_valid_query_param(pid_exact):
        if date_from and date_to:
            payment = PaymentDetail.objects.values(
            'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
                Count('bill_id')).filter(created_by=user_id).filter(bill__patient__id__iexact=pid_exact,payment__date_created__range=[date_from, date_to])
        else:
            payment = PaymentDetail.objects.values(
            'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
                Count('bill_id')).filter(created_by=user_id).filter(bill__patient__id__iexact=pid_exact)
        
    elif is_valid_query_param(min_amount):
        payment = PaymentDetail.objects.values(
        'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(created_by=user_id).filter(payment__amount_paid__gte=min_amount)
        
    elif is_valid_query_param(max_amount):
        payment = PaymentDetail.objects.values(
        'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(created_by=user_id).filter(payment__amount_paid__lte=max_amount)
        
    elif is_valid_query_param(cashier):
        payment = PaymentDetail.objects.values(
        'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(created_by=user_id).filter(payment__created_by__id__iexact=cashier)
         
    elif is_valid_query_param(transaction_type):
        if not date_from or not date_to:
            messages.error(request, 'Please specify the "DATE RANGE"')
            return redirect('single_user_reports')
        payment = PaymentDetail.objects.values(
        'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(created_by=user_id).filter(
                payment__action=transaction_type,payment__date_created__range=[date_from, date_to])
  
    elif is_valid_query_param(date_from):
        if not date_to:
            messages.error(request, 'Please enter "Transaction date-to"')
            return redirect('single_user_reports')
        payment = PaymentDetail.objects.values(
        'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(created_by=user_id).filter(payment__date_created__range=[date_from, date_to])
            
    elif is_valid_query_param(date_to):
        payment = PaymentDetail.objects.values(
        'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(created_by=user_id).filter(payment__date_created__lte=date_to)

    sum_total = 0.00
    for p in payment:
        total = float(p['payment__amount_paid'])
        sum_total += total
    
    paginator = Paginator(payment, 50) # Show 50 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {"payment":page_obj, "cash_officers":cash_officers, "sum_total":sum_total,
                "date_from":get_date_from, "date_to":get_date_to
            }#
    return render(request, 'reports/single_user_transaction.html', context)


def is_valid_query_param(param):
    return param != '' and param != None


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','cashier'])
def all_user_cash_reports_view(request):
    payment = PaymentDetail.objects.values(
        'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(date_created__gte=datetime.date.today())

    cash_officers = User.objects.filter(group__name__iexact='cashier')
    
    pid_exact = request.GET.get('pid_exact')
    transaction_type = request.GET.get('transaction_type')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    get_date_from = request.GET.get('date_from')
    get_date_to = request.GET.get('date_to')
    cashier = request.GET.get('cashier')
    date_to=None
    date_from=None
    
    if get_date_from and get_date_to:
        date_to = datetime.datetime.strptime(get_date_to, "%Y-%m-%d")
        date_to = date_to + datetime.timedelta(days=1)
        date_from = datetime.datetime.strptime(get_date_from, "%Y-%m-%d")

    if is_valid_query_param(pid_exact):
        if date_from and date_to:
            payment = PaymentDetail.objects.values(
            'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
                Count('bill_id')).filter(bill__patient__id__iexact=pid_exact,payment__date_created__range=[date_from, date_to])
        else:
            payment = PaymentDetail.objects.values(
            'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
                Count('bill_id')).filter(bill__patient__id__iexact=pid_exact)
        
    elif is_valid_query_param(min_amount):
        payment = PaymentDetail.objects.values(
        'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(payment__amount_paid__gte=min_amount)
        
    elif is_valid_query_param(max_amount):
        payment = PaymentDetail.objects.values(
        'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(payment__amount_paid__lte=max_amount)
         
    elif is_valid_query_param(transaction_type):
        if not date_from or not date_to:
            messages.error(request, 'Please specify the "DATE RANGE"')
            return redirect('all_user_reports')
        elif cashier:
            print('Cashier', cashier)
            payment = PaymentDetail.objects.values(
            'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
                Count('bill_id')).filter(payment__action=transaction_type,payment__date_created__range=[date_from, date_to], payment__created_by__id__iexact=cashier)
        else:
            payment = PaymentDetail.objects.values(
            'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
                Count('bill_id')).filter(payment__action=transaction_type,payment__date_created__range=[date_from, date_to])
  
    elif is_valid_query_param(cashier):
        if not date_from or not date_to:
            messages.error(request, 'Please specify the "DATE RANGE"')
            return redirect('all_user_reports')
        if transaction_type:
            payment = PaymentDetail.objects.values(
            'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
                Count('bill_id')).filter(payment__created_by__id__iexact=cashier,payment__date_created__range=[date_from, date_to],payment__action=transaction_type)
        else:
            payment = PaymentDetail.objects.values(
            'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
                Count('bill_id')).filter(payment__created_by__id__iexact=cashier,payment__date_created__range=[date_from, date_to])

    elif is_valid_query_param(date_from):
        if not date_to:
            messages.error(request, 'Please enter "Transaction date-to"')
            return redirect('single_user_reports')
        payment = PaymentDetail.objects.values(
        'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(payment__date_created__range=[date_from, date_to])
            
    elif is_valid_query_param(date_to):
        payment = PaymentDetail.objects.values(
        'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(payment__date_created__lte=date_to)
     
    sum_total = 0.00
    for p in payment:
        total = float(p['payment__amount_paid'])
        sum_total += total
    
    paginator = Paginator(payment, 100) # Show 100 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    
    context = {
        "payments":page_obj, "cash_officers":cash_officers, "sum_total":sum_total,
        "date_from":get_date_from, "date_to":get_date_to
        }
    return render(request, 'reports/all_users_transaction.html', context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','cashier'])
def clinical_reports_home_view(request):
    return render(request, 'reports/home.html', {})


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','cashier'])
def reports_by_service_view(request):    
    lab_services = Bill.objects.filter(lab_request__isnull=False).filter(date_created__gte=datetime.date.today())
    med_services = Bill.objects.filter(medical_service__isnull=False).filter(date_created__gte=datetime.date.today())
    pharm_services = Bill.objects.filter(dispensary__isnull=False).filter(date_created__gte=datetime.date.today())
    rad_services = Bill.objects.filter(radiology_service__isnull=False).filter(date_created__gte=datetime.date.today())
    
    lab_count = lab_services.count()
    med_service_count = med_services.count()
    pharm_count = pharm_services.count()
    rad_count = rad_services.count()

    get_date_from = request.GET.get('date_from')
    get_date_to = request.GET.get('date_to')
    
    date_to=None
    date_from=None
    if get_date_from and get_date_to:
        date_to = datetime.datetime.strptime(get_date_to, "%Y-%m-%d")
        date_to = date_to + datetime.timedelta(days=1)
        date_from = datetime.datetime.strptime(get_date_from, "%Y-%m-%d")

        lab_services = Bill.objects.filter(lab_request__isnull=False).filter(date_created__range=[date_from, date_to])
        med_services = Bill.objects.filter(medical_service__isnull=False).filter(date_created__range=[date_from, date_to])
        pharm_services = Bill.objects.filter(dispensary__isnull=False).filter(date_created__range=[date_from, date_to])
        rad_services = Bill.objects.filter(radiology_service__isnull=False).filter(date_created__range=[date_from, date_to])

        if not date_from or not date_to:
            lab_count = lab_services.count()
            med_service_count = med_services.count()
            pharm_count = pharm_services.count()
            rad_count = rad_services.count()
        else:
            lab_count = Bill.objects.filter(lab_request__isnull=False).filter(date_created__range=[date_from, date_to]).count()
            med_service_count = Bill.objects.filter(medical_service__isnull=False).filter(date_created__range=[date_from, date_to]).count()
            pharm_count = Bill.objects.filter(dispensary__isnull=False).filter(date_created__range=[date_from, date_to]).count()
            rad_count = Bill.objects.filter(radiology_service__isnull=False).filter(date_created__range=[date_from, date_to]).count()
    
    context = {
                "lab_count":lab_count,"lab_services":lab_services,
                "med_service_count":med_service_count,"med_services":med_services,
                "rad_count":rad_count,"rad_services":rad_services,
                "pharm_count":pharm_count,"pharm_services":pharm_services,
                "date_from":get_date_from,"date_to":get_date_to               
            }
    return render(request, 'reports/reports_by_service.html', context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','cashier'])
def clinical_reports_view(request):
    lab_bills = Bill.objects.filter(lab_request__isnull=False)
    pharm_bills = Bill.objects.filter(dispensary__isnull=False)
    rad_bills = Bill.objects.filter(radiology_service__isnull=False)
   
    lab_requests = LabRequest.objects.filter(date_created__gte=datetime.date.today())
    lab_results = LabRequest.objects.filter(date_created__gte=datetime.date.today())
    bills = Bill.objects.filter(date_created__gte=datetime.date.today())
    # bills = Bill.objects.all
    cash_officers = User.objects.filter(group__name__iexact='cashier')

    service_contains = request.GET.get('service_contains')
    pid_exact = request.GET.get('pid_exact')
    service_category = request.GET.get('service_category')
    get_date_from = request.GET.get('date_from')
    get_date_to = request.GET.get('date_to')
    service_category = (service_category)

    date_to=None
    date_from=None
    if get_date_from and get_date_to:
        date_to = datetime.datetime.strptime(get_date_to, "%Y-%m-%d")
        date_to = date_to + datetime.timedelta(days=1)
        date_from = datetime.datetime.strptime(get_date_from, "%Y-%m-%d")

    if is_valid_query_param(pid_exact):
        bills = Bill.objects.filter(Q(patient__id__iexact=pid_exact))
    
    elif service_category=='lab':
        if not date_from or not date_to:
            messages.error(request, 'Please enter "Date-Range for your query"!')
            return redirect('clinical_reports')
        bills = lab_bills.filter(date_created__range=[date_from, date_to])
    elif service_category=='rad':
        if not date_from or not date_to:
            messages.error(request, 'Please enter "Date-Range for your query"!')
            return redirect('clinical_reports')
        bills = rad_bills.filter(date_created__range=[date_from, date_to])
    elif service_category=='pharm':
        if not date_from or not date_to:
            messages.error(request, 'Please enter "Date-Range for your query"!')
            return redirect('clinical_reports')
        bills = pharm_bills.filter(date_created__range=[date_from, date_to])
    elif service_contains and date_from and date_to:
        bills = Bill.objects.filter(
            Q(date_created__gte=date_from, date_created__lte=date_to,
            radiology_service__radiology_service__radiology_service__icontains=service_contains) |
            Q(date_created__gte=date_from, date_created__lte=date_to,
            lab_request__test__title__icontains=service_contains))
    elif date_from and date_to:
        bills = Bill.objects.filter(date_created__gte=date_from, date_created__lte=date_to)
    
    elif is_valid_query_param(service_contains):
        bills = Bill.objects.filter(
                Q(radiology_service__radiology_service__radiology_service__icontains=service_contains) | 
                Q(lab_request__test__title__icontains=service_contains)
            )

    paginator = Paginator(bills, 100) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    context = {
                "page_obj":page_obj,
                "lab_requests":lab_requests, 
                "lab_results":lab_results, 
                "cash_officers":cash_officers,
                "date_from":get_date_from, "date_to":get_date_to 
            }
    return render(request, 'reports/clinical_reports.html', context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','cashier'])
def receipt_detail_view(request, payment_id):
    payment_detail = PaymentDetail.objects.filter(payment_id=payment_id)

    return render(request, 'reports/receipt_details.html', {"payment_detail":payment_detail})


# DIAGNOSIS
def diagnosis_report_view(request):
    diagnosis = MakeDiagnosis.objects.values('diagnosis__id','diagnosis__title').annotate(
            Count('diagnosis')).filter(date_created__gte=datetime.date.today())
    
    get_date_from = request.GET.get('date_from')
    get_date_to = request.GET.get('date_to')
    search_variable = request.GET.get('diagnosis_contains')

    date_to=None
    date_from=None
    if get_date_from and get_date_to:
        date_to = datetime.datetime.strptime(get_date_to, "%Y-%m-%d")
        date_to = date_to + datetime.timedelta(days=1)
        date_from = datetime.datetime.strptime(get_date_from, "%Y-%m-%d")
    elif date_from and date_to:
        diagnosis = MakeDiagnosis.objects.values('diagnosis__id','diagnosis__title').annotate(
            Count('diagnosis')).filter(date_created__range=[date_from, date_to])

    if search_variable:
        diagnosis = MakeDiagnosis.objects.values('diagnosis__id','diagnosis__title').annotate(
            Count('diagnosis')).filter(diagnosis__title__icontains=search_variable,date_created__range=[date_from, date_to])

    paginator = Paginator(diagnosis, 25) # Show 25 contacts per page.
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

    date_to=None
    date_from=None
    if get_date_from and get_date_to:
        date_to = datetime.datetime.strptime(get_date_to, "%Y-%m-%d")
        date_to = date_to + datetime.timedelta(days=1)
        date_from = datetime.datetime.strptime(get_date_from, "%Y-%m-%d")

    if select_ward:
        if not date_from or not date_to:
            messages.error(request, 'Please enter "Transaction dates"')
            return redirect('diagnosis_detail_report',diagnosis_id=diagnosis_id)
        else:
            diagnosis = MakeDiagnosis.objects.filter(diagnosis_id=diagnosis_id,
            encounter__current_ward__id=select_ward,date_created__range=[date_from, date_to])
    elif select_clinic:
        if not date_from or not date_to:
            messages.error(request, 'Please enter "Transaction dates"')
            return redirect('diagnosis_detail_report',diagnosis_id=diagnosis_id)
        else:
            diagnosis = MakeDiagnosis.objects.filter(
                    diagnosis_id=diagnosis_id,encounter__current_clinic__id=select_clinic, 
                    date_created__range=[date_from, date_to])

    paginator = Paginator(diagnosis, 25) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, "clinics":clinics, "wards":wards, "users":users}
    return render(request, 'reports/diagnosis_details.html', context)