# Generated by Django 4.2.4 on 2024-01-30 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('labs', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lab_unit',
            field=models.ForeignKey(blank=True, help_text='For MedLab staff only', null=True, on_delete=django.db.models.deletion.CASCADE, to='labs.labunit'),
        ),
    ]
