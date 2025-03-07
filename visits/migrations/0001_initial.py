# Generated by Django 4.2.4 on 2024-01-30 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '0001_initial'),
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientEncounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('pay_status', models.BooleanField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('current_clinic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.clinic')),
                ('current_ward', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.ward')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patients.patient')),
            ],
        ),
        migrations.CreateModel(
            name='EncounterRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('clinic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.clinic')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('encounter_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visits.patientencounter')),
                ('ward', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.ward')),
            ],
        ),
        migrations.CreateModel(
            name='DischargePatient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discharge_type', models.CharField(choices=[('regular', 'Regular Discharge'), ('against medical advice', 'Against Medical Advice')], max_length=50)),
                ('reason_for_discharge', models.CharField(blank=True, max_length=50, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('encounter_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visits.patientencounter')),
            ],
        ),
    ]
