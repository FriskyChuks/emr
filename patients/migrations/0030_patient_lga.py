# Generated by Django 3.1.2 on 2021-07-30 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0029_remove_patient_l_g_a'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='lga',
            field=models.CharField(default='keffi', max_length=100),
        ),
    ]
