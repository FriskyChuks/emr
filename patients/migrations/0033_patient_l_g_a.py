# Generated by Django 3.1.2 on 2021-08-02 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0032_remove_patient_l_g_a'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='l_g_a',
            field=models.CharField(default='keffi', max_length=100),
        ),
    ]
