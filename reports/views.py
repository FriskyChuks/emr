from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers


from bills.models import Bill, Payment, PaymentDetail


def dashboard_with_pivot(request):
    return render(request, 'reports/dashboard_with_pivot.html', {})


def pivot_data(request, user_id=8):
    # dataset = Bill.objects.all()
    dataset = Payment.objects.filter(created_by=user_id, action='receipt')
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)


def payment_reports_view(request, user_id):
    payments = Payment.objects.filter(created_by=user_id, action='deposit')

    context = {"payments":payments}
    return render(request, 'reports/payments.html', context)
