from django.http import request
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.decorators import allowed_users
from patients.models import Patient
from visits.models import PatientEncounter

from .models import Bill, Payment, PaymentDetail, Wallet


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','cashier'])
def billing_home_view(request):
    template = "bills/billing_home.html"
    context = {}
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','cashier'])
def clear_outstanding_bills_view(request, pid):
    user = request.user
    new_bill_list = []
    patient = Patient.objects.get(id=pid)
    patient_wallet = Wallet.objects.get(patient_id=pid)
    initial_balance = patient_wallet.account_balance
    med_serv_outstanding_bill = Bill.objects.filter(
                                encounter__patient__id=pid, medical_service__isnull=False, status='billed')
    pharm_outstanding_bill = Bill.objects.filter(encounter__patient__id=pid,
                                 dispensary__isnull=False, status='billed')                            
    os_total = float(0.00)
    bill_list = []
    for bill in med_serv_outstanding_bill:
        bill_list.append(bill.id)
        price = bill.medical_service.medical_service.price
        os_total = os_total + float(price)
        # print(os_total)
    
    # pharmacy bill
    pharm_os_total = float(0.00)
    pharm_bill_list = []
    for pharm_bill in pharm_outstanding_bill:
        pharm_bill_list.append(pharm_bill.id)
        pharm_price = pharm_bill.dispensary.brand.sale_price
        pharm_qty_dispensed = pharm_bill.dispensary.qty_dispensed
        pharm_os_total = pharm_os_total + (float(pharm_price * pharm_qty_dispensed))

    # Sum of all outstanding
    new_os_total = os_total + pharm_os_total
    # Combine all bill IDs into one list
    new_bill_list = bill_list + pharm_bill_list
       
    initial_balance = patient_wallet.account_balance
    if float(new_os_total) >= float(initial_balance):
        amount_paid = float(new_os_total) - float(initial_balance)
        balance_os = 0.00
    else:
        amount_paid = 0.00
        balance_os = float(initial_balance) - float(new_os_total)
    
    # Form to clear outstanding
    if request.method == 'POST':
        payment = Payment.objects.create(amount_paid=amount_paid, action='receipt', patient_id=pid, created_by=user)
        for item in new_bill_list:
            PaymentDetail.objects.create(bill_id=item, payment_id=payment.id, created_by=user)
            Bill.objects.filter(id=item).update(status="paid")
        Wallet.objects.filter(patient=pid).update(account_balance=balance_os)
        PatientEncounter.objects.filter(patient=pid).update(pay_status=True)
        messages.success(request, "Payment successful!")
        return redirect('outstanding_bills', pid=pid)
        
    template = "bills/outstanding_bills.html"
    context = {"os_total":os_total,
                "med_serv_outstanding_bill":med_serv_outstanding_bill, 
                "pharm_os_total":pharm_os_total,
                "pharm_outstanding_bill":pharm_outstanding_bill,
                "new_os_total":new_os_total,
                "patient":patient, 
                "initial_balance":initial_balance,
              }
    return render(request, template, context)


@login_required(login_url="auth_login")
@allowed_users(alllowed_roles=['admin','cashier'])
def pending_bills_view(request, pid): 
    bills = Bill.objects.filter(encounter__patient=pid, status="billed") | Bill.objects.filter(encounter__patient=pid, status="pending")
    services_bills = Bill.objects.filter(encounter__patient=pid, medical_service__isnull=False, status='pending')
    radiology_bills = Bill.objects.filter(encounter__patient=pid, radiology_service__isnull=False, status='pending')
    lab_bills = Bill.objects.filter(encounter__patient=pid, lab_request__isnull=False, status='pending')
    pharmacy_bills = Bill.objects.filter(encounter__patient=pid, dispensary__isnull=False)

    # OUTSTANDING BILLS
    billed_med_serv = Bill.objects.filter(encounter__patient=pid, medical_service__isnull=False, status='billed')
    billed_rad_serv = Bill.objects.filter(encounter__patient=pid, radiology_service__isnull=False, status='billed')
    billed_lab_serv = Bill.objects.filter(encounter__patient=pid, lab_request__isnull=False, status='billed')
    pharm_outstanding_bill = Bill.objects.filter(encounter__patient=pid, dispensary__isnull=False, status='billed')
    
    # OUTSATANDING SERVICES
    outstanding_med_serv = 0.00
    # outstanding_rad_serv = 0.00
    # outstanding_lab_serv = 0.00
    outstanding_pharm = 0.00

    # OUTSATANDING MEDICAL SERVICES
    for billed_med_serv in billed_med_serv:
        med_serv_qty = billed_med_serv.medical_service.unit
        med_serv_price = billed_med_serv.medical_service.medical_service.price
        outstanding_med_serv = float(med_serv_price * med_serv_qty)
    # OUTSATANDING PHARM BILLS
    for pharm_bill in pharm_outstanding_bill:
        pharm_price = pharm_bill.dispensary.brand.sale_price
        pharm_qty_dispensed = pharm_bill.dispensary.qty_dispensed
        outstanding_pharm = float(pharm_price * pharm_qty_dispensed)
    # # OUTSATANDING RADIOLOGY BILLS
    # for billed_rad_serv in billed_rad_serv:
    #     rad_qty = billed_rad_serv.radiology_service.unit
    #     rad_price = billed_rad_serv.radiology_service.radiology_service.price
    #     outstanding_rad_serv = float(rad_price * rad_qty)
    # # OUTSATANDING LAB BILLS
    # for billed_lab_serv in billed_lab_serv:
    #     lab_price = billed_lab_serv.lab_request.test.price
    #     outstanding_lab_serv += float(lab_price)

    outstanding_bills = outstanding_med_serv + outstanding_pharm

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

    pay_now = (float(total_bill) + float(outstanding_bills))

    patient = Patient.objects.get(id=pid)
    if request.method == "POST":
        if request.POST.get("bill_ID"):
            selected_bill = Payment()
            selected_bill.bill_id = request.POST.get("bill_ID")
            paid_amount = request.POST.get("pay_amount")
            if float(wallet_balance) < float(paid_amount):
                paid_amount = float(paid_amount) - float(wallet_balance)
                wallet = Wallet.objects.filter(patient_id=pid).update(account_balance=0.00)
            else:
                paid_amount = paid_amount
                wallet_balance = float(wallet_balance) - float(paid_amount)
                wallet = Wallet.objects.filter(patient_id=pid).update(account_balance=wallet_balance)
                
            pay_bill = selected_bill.bill_id
            pay_bill = str(pay_bill)
            # convert Comma separated string to a python list
            my_list = pay_bill.split(",")
           
            payment_obj = Payment.objects.create(amount_paid=paid_amount,action='receipt',patient_id=pid,created_by=request.user)
            if payment_obj:
                instance = payment_obj
                for item in my_list:
                    obj = PaymentDetail.objects.create(
                            bill_id         = item,
                            payment_id      = instance.id,
                            created_by      = request.user
                        )
                    obj.save()
                    bill_obj = Bill.objects.filter(id=item).update(status="paid")
                messages.success(request, "Payment processed successfully!")
                return redirect('pending_bills', pid=pid)
        else:
            messages.error(request, "Please check items to pay for!")

    template = "bills/bills.html"
    context = {
                "outstanding_bills":outstanding_bills,
                "bills":bills,
                "services_bills":services_bills,
                "radiology_bills":radiology_bills,
                "outstanding_pharm":outstanding_pharm,
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

    med_serv_outstanding_bill = Bill.objects.filter(encounter__patient=pid, medical_service__isnull=False, status='billed')
    pharm_outstanding_bill = Bill.objects.filter(encounter__patient=pid, dispensary__isnull=False, status='billed')

    os_total = float(0.00)
    for bill in med_serv_outstanding_bill:
        price = bill.medical_service.medical_service.price
        os_total += float(price)
    
    # pharmacy bill
    pharm_os_total = float(0.00)
    for pharm_bill in pharm_outstanding_bill:
        pharm_price = pharm_bill.dispensary.brand.sale_price
        pharm_qty_dispensed = pharm_bill.dispensary.qty_dispensed
        pharm_os_total += (float(pharm_price * pharm_qty_dispensed))

    # Sum of all outstanding
    new_os_total = os_total + pharm_os_total

    if request.method == 'POST':
        deposit_amount = request.POST.get('amount')
        if deposit_amount == '':
            messages.error(request, "Amount of deposit cannot be empty")
            return redirect('wallet', pid=pid)
        else:
            if float(deposit_amount) > float(0):
                initial_balance = float(initial_balance) + float(deposit_amount)
                Wallet.objects.filter(patient_id=pid).update(account_balance=initial_balance, created_by=request.user)
                payment_instance = Payment.objects.create(amount_paid=deposit_amount, action='deposit', patient_id=pid, created_by=user)
                bill_instance = Bill.objects.create(status='paid', created_by=user)
                PaymentDetail.objects.create(payment_id=payment_instance.id,bill_id=bill_instance.id,created_by=user)
                messages.success(request, 'Wallet loaded successfully, thanks!')
                return redirect('wallet', pid=pid)
            else:
                messages.error(request, "Please enter POSITIVE VALUES only, Thanks!")   

    template = "bills/wallet.html"
    context = {"patient":patient, "initial_balance":initial_balance, "new_os_total":new_os_total}
    return render(request, template, context)

    
    