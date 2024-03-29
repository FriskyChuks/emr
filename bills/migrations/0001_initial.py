# Generated by Django 4.0.6 on 2022-12-20 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('radiology', '0001_initial'),
        ('medical_services', '0005_auto_20210730_0917'),
        ('pharmacy', '0001_initial'),
        ('patients', '0035_auto_20211226_1411'),
        ('visits', '0002_patientencounter_pay_status'),
        ('labs', '0013_remove_labrequest_patient'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('billed', 'Billed'), ('paid', 'Paid')], default='pending', max_length=10)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('dispensary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pharmacy.dispensary')),
                ('encounter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='visits.patientencounter')),
                ('lab_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='labs.labrequest')),
                ('medical_service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medical_services.patientencounterservice')),
                ('radiology_service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='radiology.radiologyrequest')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.DecimalField(decimal_places=2, default='00.00', max_digits=20)),
                ('action', models.CharField(choices=[('deposit', 'Deposit'), ('invoice', 'Invoice'), ('receipt', 'Receipt')], max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_balance', models.DecimalField(decimal_places=2, default='00.00', max_digits=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='patients.patient')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('bill', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bills.bill')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bills.payment')),
            ],
        ),
    ]
