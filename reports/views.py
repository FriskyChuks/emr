from django.shortcuts import render

from bills.models import Bill


def pending_consultation_fee_view(request, pid):
    med_serv_outstanding_bill = Bill.objects.filter(patient=pid, medical_service__isnull=False, status='billed')
    if len(med_serv_outstanding_bill) > 0:
        for ms_bill in med_serv_outstanding_bill:
            ms_os_bill = float(ms_bill.medical_service.medical_service.price)
    else:
        ms_os_bill = float(0.00)
    outstanding_bill = ms_os_bill
