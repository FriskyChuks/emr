# Generated by Django 3.1.6 on 2022-01-14 06:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0002_patientencounter_pay_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diagnosis', '0004_auto_20210924_1401'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MakeDiagosis',
            new_name='MakeDiagnosis',
        ),
    ]