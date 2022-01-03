import datetime
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib import messages

from accounts.models import User
from labs.models import LabRequest
from bills.models import Bill, Payment, PaymentDetail


def single_user_reports_view(request, user_id):
    payment = PaymentDetail.objects.values(
        'payment','payment__action','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(created_by=user_id, date_created__gte=datetime.date.today())

    cash_officers = User.objects.filter(group__name__iexact='cashier')

    service_contains = request.GET.get('service_contains')
    pid_exact = request.GET.get('pid_exact')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    cashier = request.GET.get('cashier')
    
    if is_valid_query_param(pid_exact):
        payment = PaymentDetail.objects.values(
        'payment','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(bill__patient__id__iexact=pid_exact)

    elif is_valid_query_param(service_contains):
        payment = PaymentDetail.objects.values(
        'payment','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(created_by=user_id).filter(
            bill__radiology_service__radiology_service__radiology_service__icontains=service_contains)
        
    elif is_valid_query_param(min_amount):
        payment = PaymentDetail.objects.values(
        'payment','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(created_by=user_id).filter(payment__amount_paid__gte=min_amount)
        
    elif is_valid_query_param(max_amount):
        payment = PaymentDetail.objects.values(
        'payment','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(created_by=user_id).filter(payment__amount_paid__lte=max_amount)
        
    elif is_valid_query_param(cashier):
        payment = PaymentDetail.objects.values(
        'payment','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(created_by=user_id).filter(payment__created_by__id__iexact=cashier)
         
    if is_valid_query_param(date_from):
        if not date_to:
            messages.error(request, 'Please enter "Transaction date-to"')
            return redirect('single_user_reports', user_id=request.user.id)
        payment = PaymentDetail.objects.values(
        'payment','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(created_by=user_id).filter(payment__date_created__range=[date_from, date_to])
            
    elif is_valid_query_param(date_to):
        payment = PaymentDetail.objects.values(
        'payment','payment__date_created','payment__amount_paid','bill__patient', 'created_by__first_name', 'created_by__last_name').annotate(
            Count('bill_id')).filter(payment__date_created__lte=date_to)
           
    # sum_total = 0.00
    # for p in payment:
    #     total = float(p.payment.amount_paid)
    #     sum_total += total
    
    paginator = Paginator(payment, 25) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {"payment":page_obj, "cash_officers":cash_officers}
    return render(request, 'reports/single_user_transaction.html', context)


def is_valid_query_param(param):
    return param != '' and param != None


def all_user_reports_view(request):
    payments = PaymentDetail.objects.filter(date_created__gte=datetime.date.today())
    cash_officers = User.objects.filter(group__name__iexact='cashier')

    service_contains = request.GET.get('service_contains')
    pid_exact = request.GET.get('pid_exact')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    cashier = request.GET.get('cashier')
    
    if is_valid_query_param(pid_exact):
        payments = PaymentDetail.objects.filter(Q(bill__patient__id__iexact=pid_exact))

    elif is_valid_query_param(service_contains):
        payments = PaymentDetail.objects.filter(
                Q(bill__radiology_service__radiology_service__radiology_service__icontains=service_contains) |
                Q(bill__lab_request__test__title__icontains=service_contains)
            )
    
    elif is_valid_query_param(min_amount):
        payments = PaymentDetail.objects.filter(Q(payment__amount_paid__gte=min_amount))
    
    elif is_valid_query_param(max_amount):
        payments = PaymentDetail.objects.filter(Q(payment__amount_paid__lte=max_amount))
    
    elif is_valid_query_param(cashier):
        payments = PaymentDetail.objects.filter(Q(payment__created_by__id__iexact=cashier))
    
    if is_valid_query_param(date_from):
        payments = PaymentDetail.objects.filter(Q(payment__date_created__gte=date_from))
    
    elif is_valid_query_param(date_to):
        payments = PaymentDetail.objects.filter(Q(payment__date_created__lte=date_to))
    
    sum_total = 0.00
    for p in payments:
        total = float(p.payment.amount_paid)
        sum_total += total

    paginator = Paginator(payments, 50) # Show 50 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {"payments":page_obj, "cash_officers":cash_officers, "sum_total":sum_total}
    return render(request, 'reports/all_users_transaction.html', context)


def clinical_reports_view(request):
    lab_requests = LabRequest.objects.filter(date_created__gte=datetime.date.today())
    lab_results = LabRequest.objects.filter(date_created__gte=datetime.date.today())
    bills = Bill.objects.filter(date_created__gte=datetime.date.today())
    # bills = Bill.objects.all
    cash_officers = User.objects.filter(group__name__iexact='cashier')

    service_contains = request.GET.get('service_contains')
    pid_exact = request.GET.get('pid_exact')
    service_category = request.GET.get('service_category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    # cashier = request.GET.get('cashier')
    service_category = (service_category)

    if is_valid_query_param(pid_exact):
        bills = Bill.objects.filter(Q(patient__id__iexact=pid_exact))
    
    elif service_category=='lab':
        bills = Bill.objects.filter(lab_request__isnull=False, radiology_service__isnull=True)
    elif service_category=='rad':
        bills = Bill.objects.filter(lab_request__isnull=True, radiology_service__isnull=False)
    
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

    paginator = Paginator(bills, 25) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    context = {
                "bills":page_obj,
                "lab_requests":lab_requests, 
                "lab_results":lab_results, 
                "cash_officers":cash_officers, 
            }
    return render(request, 'reports/clinical_reports.html', context)


def receipt_detail_view(request, payment_id):
    payment_detail = PaymentDetail.objects.filter(payment_id=payment_id)

    return render(request, 'reports/receipt_details.html', {"payment_detail":payment_detail})

