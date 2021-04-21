from django.http import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Bill, Payment


@login_required(login_url="auth_login")
def pending_bills_view(request, pid):
    # bills = Bill.objects.filter(patient=pid, status="pending") | Bill.objects.filter(patient=pid, status="billed") | Bill.objects.filter(patient=pid, status="paid")
    bills = Bill.objects.filter(patient=pid, status="billed") | Bill.objects.filter(patient=pid, status="pending")
    services_bill = Bill.objects.filter(patient=pid, medical_service__isnull=False)
    radiology_bill = Bill.objects.filter(patient=pid, radiology_service__isnull=False)
    pharmacy_bill = Bill.objects.filter(patient=pid, prescription__isnull=False)

    medical_service_total_bill = 0
    radiology_total_bill = 0
    pharmacy_total_bill = 0

    # Medical Service Bill
    for obj in services_bill:
        qty = obj.medical_service.unit 
        service_subtotal = obj.medical_service.medical_service.price * qty
        medical_service_total_bill += service_subtotal
    
    # Radiology Bill
    for obj in radiology_bill: 
        qty = obj.radiology_service.unit 
        radiology_subtotal = obj.radiology_service.radiology_service.price * qty
        radiology_total_bill += radiology_subtotal 
    
    # Pharmacy Bill
    # for obj in pharmacy_bill: 
    #     qty = (obj.qty_per_take * obj.times_daily * obj.no_of_days)
    #     pharmacy_subtotal = obj.item.price * qty
    #     pharmacy_total_bill += pharmacy_subtotal
    
    med_total = medical_service_total_bill
    rad_total = radiology_total_bill
    # pharm_total = pharmacy_total_bill
    total_bill = med_total + rad_total# + pharm_total

    template = "bills/bills.html"
    context = {
                "bills":bills,
                "services_bill":services_bill,
                "radiology_bill":radiology_bill,
                "pharmacy_bill":pharmacy_bill,
                'med_total':med_total,
                'rad_total':rad_total,
                'total_bill':total_bill
              }
    return render(request, template, context)


# @login_required(login_url="auth_login")
# def bill_payment_view(request):
    