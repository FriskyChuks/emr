# Generated by Django 3.1.6 on 2021-10-16 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_clinic_female_only'),
    ]

    operations = [
        migrations.AddField(
            model_name='ward',
            name='female_only',
            field=models.BooleanField(default=False),
        ),
    ]