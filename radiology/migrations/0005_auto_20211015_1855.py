# Generated by Django 3.1.6 on 2021-10-15 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('radiology', '0004_auto_20211015_1855'),
        ('bills', '0018_auto_20211015_1855'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patients', '0034_auto_20210916_2156'),
        ('visits', '0002_patientencounter_pay_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RaiseRadiologyService',
        ),
        migrations.AddField(
            model_name='radiologyrequest',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='radiologyrequest',
            name='encounter_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visits.patientencounter'),
        ),
        migrations.AddField(
            model_name='radiologyrequest',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patient'),
        ),
        migrations.AddField(
            model_name='radiologyrequest',
            name='radiology_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='radiology.radiologyservice'),
        ),
        migrations.AddField(
            model_name='radiologyreport',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='radiologyreport',
            name='radiologyrequest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='radiology.radiologyrequest'),
        ),
    ]