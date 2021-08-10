from django.http import request
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.decorators import allowed_users
from patients.models import Patient

from .models import Bill, Payment, PaymentDetail, Wallet



@login_required(login_url="auth_login")
def clear_outstanding_bills_view(request, pid):
    user = request.user
    patient = Patient.objects.get(id=pid)
    patient_wallet = Wallet.objects.get(patient_id=pid)
    initial_balance = patient_wallet.account_balance
    med_serv_outstanding_bill = Bill.objects.filter(patient=pid, medical_service__isnull=False, status='billed')
    if len(med_serv_outstanding_bill) > 0:
        for ms_bill in med_serv_outstanding_bill:
            ms_os_bill = float(ms_bill.medical_service.medical_service.price)
    else:
        ms_os_bill = float(0.00)
    outstanding_bill = ms_os_bill

    patient_wallet = Wallet.objects.get(patient_id=pid) 
    initial_balance = patient_wallet.account_balance

    # Form input to clear outstanding
    if request.method == 'POST':
        os_amount = request.POST.get('amount')
        payment = Payment.objects.create(amount_paid=os_amount, action='receipt', created_by=user)
        payment_detail = PaymentDetail.objects.create(bill_id=ms_bill.id, payment_id=payment.id, created_by=user)
        bill_update = Bill.objects.filter(id=ms_bill.id).update(status="paid")
    
    template = "bills/outstanding_bills.html"
    context = {"outstanding_bill":outstanding_bill, 
                "patient":patient, 
                "initial_balance":initial_balance,
                "ms_os_bill":ms_os_bill
              }
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','cashier'])
def pending_bills_view(request, pid): 
    # bills = Bill.objects.filter(patient=pid, status="pending") | Bill.objects.filter(patient=pid, status="billed") | Bill.objects.filter(patient=pid, status="paid")
    bills = Bill.objects.filter(patient=pid, status="billed") | Bill.objects.filter(patient=pid, status="pending")
    services_bills = Bill.objects.filter(patient=pid, medical_service__isnull=False, status='pending')
    radiology_bills = Bill.objects.filter(patient=pid, radiology_service__isnull=False, status='pending')
    lab_bills = Bill.objects.filter(patient=pid, lab_request__isnull=False, status='pending')
    pharmacy_bills = Bill.objects.filter(patient=pid, prescription__isnull=False)

    # OUTSTANDING BILLS
    billed_med_serv = Bill.objects.filter(patient=pid, medical_service__isnull=False, status='billed')
    billed_rad_serv = Bill.objects.filter(patient=pid, radiology_service__isnull=False, status='billed')
    billed_lab_serv = Bill.objects.filter(patient=pid, lab_request__isnull=False, status='billed')
    
    # OUTSATANDING MEDICAL SERVICES
    outstanding_med_serv = 0.00
    outstanding_rad_serv = 0.00
    outstanding_lab_serv = 0.00

    for billed_med_serv in billed_med_serv:
        med_serv_qty = billed_med_serv.medical_service.unit
        med_serv_price = billed_med_serv.medical_service.medical_service.price
        outstanding_med_serv = float(med_serv_price * med_serv_qty)
    # OUTSATANDING RADIOLOGY BILLS
    for billed_rad_serv in billed_rad_serv:
        rad_qty = billed_rad_serv.radiology_service.unit
        rad_price = billed_rad_serv.radiology_service.radiology_service.price
        outstanding_rad_serv = float(rad_price * rad_qty)
    # OUTSATANDING LAB BILLS
    for billed_lab_serv in billed_lab_serv:
        lab_price = billed_lab_serv.lab_request.test.price
        outstanding_lab_serv += float(lab_price)

    outstanding_bills = outstanding_med_serv + outstanding_rad_serv + outstanding_lab_serv

    medical_service_total_bill = 0
    radiology_total_bill = 0
    pharmacy_total_bill = 0
    lab_total_bill = 0

    # Medical Service Bill
    for obj in services_bills:
        qty = obj.medical_service.unit 
        service_subtotal = obj.medical_service.medical_service.price * qty
        medical_service_total_bill += service_subtotal
    
    # Radiology Bill
    for obj in radiology_bills: 
        qty = obj.radiology_service.unit 
        radiology_subtotal = obj.radiology_service.radiology_service.price * qty
        radiology_total_bill += radiology_subtotal

     # LAB Bill
    for obj in lab_bills:
        lab_subtotal = obj.lab_request.test.price
        lab_total_bill += lab_subtotal 
    
    # Pharmacy Bill
    # for obj in pharmacy_bill: 
    #     qty = (obj.qty_per_take * obj.times_daily * obj.no_of_days)
    #     pharmacy_subtotal = obj.item.price * qty
    #     pharmacy_total_bill += pharmacy_subtotal
    
    med_total = medical_service_total_bill
    rad_total = radiology_total_bill
    # pharm_total = pharmacy_total_bill
    lab_total = lab_total_bill
    total_bill = float(med_total + rad_total + lab_total)# + pharm_total

    wallet = Wallet.objects.get(patient_id=pid)
    wallet_balance = wallet.account_balance

    if wallet_balance >= 0:
        pay_now = float(wallet_balance) - (float(total_bill) + float(outstanding_bills))
    else:
        pay_now = (float(total_bill) + float(outstanding_bills))

    patient = Patient.objects.get(id=pid)
    if request.method == "POST":
        if request.POST.get("bill_ID"):
            selected_bill = Payment()
            selected_bill.bill_id = request.POST.get("bill_ID")
            paid_amount = request.POST.get("paid_amount")
            if paid_amount != "":
                paid_amount = float(paid_amount)
            else:
                messages.error(request, "Pls enter payment amount!")
            pay_bill = selected_bill.bill_id
            l = len(pay_bill)
            t = type(pay_bill)

            if (l > 0 and  l <= 2): 
                payment_obj = Payment.objects.create(amount_paid=paid_amount,action='receipt',created_by=request.user)
                payment_obj.save()
                if payment_obj:
                    instance = payment_obj
                    obj = PaymentDetail.objects.create(
                            bill_id         = pay_bill,
                            payment_id      = instance.id,
                            created_by      = request.user
                        )
                    obj.save()
                    bill_obj = Bill.objects.filter(id=pay_bill).update(status="paid")
                messages.success(request, "Payment processed successfully!")
            else:
                payment_obj = Payment.objects.create(amount_paid=paid_amount,action='receipt',created_by=request.user)
                payment_obj.save()
                if payment_obj:
                    instance = payment_obj
                    # Convert the string(pay_bill) to a tuple
                    bill_list = eval(pay_bill)
                    for item in bill_list:
                        obj = PaymentDetail.objects.create(
                                bill_id         = item,
                                payment_id      = instance.id,
                                created_by      = request.user
                            )
                        obj.save()
                        bill_obj = Bill.objects.filter(id=item).update(status="paid")
                    messages.success(request, "Payment processed successfully!")

    template = "bills/bills.html"
    context = {
                "outstanding_bills":outstanding_bills,
                "bills":bills,
                "services_bills":services_bills,
                "radiology_bills":radiology_bills,
                "pharmacy_bills":pharmacy_bills,
                'lab_bills':lab_bills,
                'med_total':med_total,
                'rad_total':rad_total,
                'lab_total':lab_total,
                'total_bill':total_bill,
                "pay_now":pay_now,
                'patient':patient,
                'wallet_balance':wallet_balance
              }
    return render(request, template, context)



@login_required(login_url="auth_login")
def load_wallet_view(request, pid):
    user = request.user
    patient = Patient.objects.get(id=pid)
    patient_wallet = Wallet.objects.get(patient_id=pid)
    initial_balance = patient_wallet.account_balance

    med_serv_outstanding_bill = Bill.objects.filter(patient=pid, medical_service__isnull=False, status='billed')
    if len(med_serv_outstanding_bill) > 0:
        for ms_bill in med_serv_outstanding_bill:
            ms_os_bill = float(ms_bill.medical_service.medical_service.price)
            outstanding_bill = ms_os_bill
    else:
        ms_os_bill = float(0.00)
        outstanding_bill = ms_os_bill

    if request.method == 'POST':
        deposit_amount = request.POST.get('amount')
        initial_balance = float(initial_balance) + float(deposit_amount)
        object = Wallet.objects.filter(patient_id=pid).update(account_balance=initial_balance, created_by=request.user)
        payment = Payment.objects.create(amount_paid=deposit_amount, action='deposit', created_by=user)

    template = "bills/wallet.html"
    context = {"patient":patient, "initial_balance":initial_balance, "outstanding_bill":outstanding_bill}
    return render(request, template, context)

    
    