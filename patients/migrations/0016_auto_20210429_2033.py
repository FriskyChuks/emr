# Generated by Django 3.1.2 on 2021-04-29 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0015_delete_patientimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='foto',
            field=models.ImageField(blank=True, default='male.jpg', null=True, upload_to='image/'),
        ),
    ]
