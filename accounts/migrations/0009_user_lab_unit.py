# Generated by Django 3.1.2 on 2021-07-06 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0012_auto_20210514_1046'),
        ('accounts', '0008_user_clinic'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lab_unit',
            field=models.ForeignKey(blank=True, help_text='For Med. Lab. Staff only', null=True, on_delete=django.db.models.deletion.CASCADE, to='labs.labunit'),
        ),
    ]
