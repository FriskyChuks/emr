# Generated by Django 3.1.6 on 2022-01-03 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0002_patientencounter_pay_status'),
        ('bills', '0029_auto_20220103_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='encounter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='visits.patientencounter'),
        ),
    ]