# Generated by Django 4.2.4 on 2024-02-01 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0006_relationship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='next_of_kin_relationship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.relationship'),
        ),
    ]
