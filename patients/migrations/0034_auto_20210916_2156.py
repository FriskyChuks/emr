# Generated by Django 3.1.6 on 2021-09-16 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0033_patient_l_g_a'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='users/'),
        ),
    ]
